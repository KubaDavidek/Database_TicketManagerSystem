from src.repositories.customer_repository import CustomerRepository
from src.repositories.order_repository import OrderRepository
from src.repositories.ticket_repository import TicketRepository


class OrderService:
    def __init__(self, connection):
        self.connection = connection
        self.customers = CustomerRepository(connection)
        self.orders = OrderRepository(connection)
        self.tickets = TicketRepository(connection)

    def buy_single_ticket(
        self,
        full_name: str,
        email: str,
        phone: str | None,
        event_id: int,
        ticket_id: int,
        notes: str | None = None,
    ) -> int:
        # kontrola že ticket patří k eventu a je volný
        if not self.tickets.is_available_for_event(ticket_id, event_id):
            raise Exception("Ticket neexistuje, nepatří k této akci nebo už je prodaný.")

        try:
            self.connection.start_transaction()

            # zákazník
            customer = self.customers.find_by_email(email)
            if customer:
                customer_id = customer["id"]
            else:
                customer_id = self.customers.create(full_name, email, phone)

            # objednávka
            order_id = self.orders.create_order(customer_id, status="reserved", notes=notes)

            # položka objednávky
            self.orders.add_item(order_id, ticket_id, quantity=1)

            # označit ticket jako prodaný
            changed = self.tickets.mark_sold(ticket_id)
            if changed != 1:
                raise Exception("Ticket už byl mezitím prodaný.")

            self.connection.commit()
            return order_id

        except Exception:
            self.connection.rollback()
            raise

    def cancel_order(self, order_id: int):
        try:
            self.connection.start_transaction()

            self.tickets.unmark_sold_by_order(order_id)
            self.orders.cancel_order(order_id)

            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise
