class OrderRepository:
    def __init__(self, connection):
        self.connection = connection

    def create_order(self, customer_id: int, status: str = "reserved", notes: str | None = None) -> int:
        cur = self.connection.cursor()
        cur.execute(
            "insert into `order` (customer_id, status, notes) values (%s, %s, %s)",
            (customer_id, status, notes),
        )
        return cur.lastrowid

    def add_item(self, order_id: int, ticket_id: int, quantity: int = 1) -> None:
        cur = self.connection.cursor()
        cur.execute(
            "insert into order_item (order_id, ticket_id, quantity) values (%s, %s, %s)",
            (order_id, ticket_id, quantity),
        )

    def cancel_order(self, order_id: int):
        cur = self.connection.cursor()
        cur.execute("update `order` set status = 'cancelled' where id = %s", (order_id,))
