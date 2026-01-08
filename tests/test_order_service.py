import pytest
from unittest.mock import Mock

from src.services.order_service import OrderService


def make_service():
    conn = Mock()
    service = OrderService(conn)


    service.customers = Mock()
    service.orders = Mock()
    service.tickets = Mock()

    return service, conn


def test_buy_single_ticket_success_existing_customer():
    service, conn = make_service()

    service.tickets.is_available_for_event.return_value = True
    service.customers.find_by_email.return_value = {"id": 10}
    service.orders.create_order.return_value = 77
    service.tickets.mark_sold.return_value = 1

    order_id = service.buy_single_ticket(
        full_name="Jan Novak",
        email="jan@novak.cz",
        phone="777111222",
        event_id=1,
        ticket_id=5,
    )

    assert order_id == 77
    conn.start_transaction.assert_called_once()
    conn.commit.assert_called_once()
    conn.rollback.assert_not_called()

    service.customers.create.assert_not_called()
    service.orders.add_item.assert_called_once_with(77, 5, quantity=1)
    service.tickets.mark_sold.assert_called_once_with(5)


def test_buy_single_ticket_success_new_customer_created():
    service, conn = make_service()

    service.tickets.is_available_for_event.return_value = True
    service.customers.find_by_email.return_value = None
    service.customers.create.return_value = 55
    service.orders.create_order.return_value = 99
    service.tickets.mark_sold.return_value = 1

    order_id = service.buy_single_ticket(
        full_name="Petra Svobodova",
        email="petra@svobodova.cz",
        phone=None,
        event_id=2,
        ticket_id=8,
    )

    assert order_id == 99
    service.customers.create.assert_called_once_with("Petra Svobodova", "petra@svobodova.cz", None)
    conn.commit.assert_called_once()


def test_buy_single_ticket_ticket_not_available_raises_and_no_transaction():
    service, conn = make_service()

    service.tickets.is_available_for_event.return_value = False

    with pytest.raises(Exception) as e:
        service.buy_single_ticket(
            full_name="X",
            email="x@x.cz",
            phone=None,
            event_id=1,
            ticket_id=123,
        )

    assert "Ticket neexistuje" in str(e.value)

    conn.start_transaction.assert_not_called()
    conn.commit.assert_not_called()
    conn.rollback.assert_not_called()


def test_buy_single_ticket_mark_sold_failed_rolls_back():
    service, conn = make_service()

    service.tickets.is_available_for_event.return_value = True
    service.customers.find_by_email.return_value = {"id": 1}
    service.orders.create_order.return_value = 2
    service.tickets.mark_sold.return_value = 0  # už prodaný

    with pytest.raises(Exception):
        service.buy_single_ticket(
            full_name="Jan Novak",
            email="jan@novak.cz",
            phone=None,
            event_id=1,
            ticket_id=5,
        )

    conn.start_transaction.assert_called_once()
    conn.rollback.assert_called_once()
    conn.commit.assert_not_called()


def test_buy_single_ticket_add_item_raises_rolls_back():
    service, conn = make_service()

    service.tickets.is_available_for_event.return_value = True
    service.customers.find_by_email.return_value = {"id": 1}
    service.orders.create_order.return_value = 2
    service.orders.add_item.side_effect = Exception("DB error on insert")
    service.tickets.mark_sold.return_value = 1

    with pytest.raises(Exception):
        service.buy_single_ticket(
            full_name="Jan Novak",
            email="jan@novak.cz",
            phone=None,
            event_id=1,
            ticket_id=5,
        )

    conn.start_transaction.assert_called_once()
    conn.rollback.assert_called_once()
    conn.commit.assert_not_called()


def test_cancel_order_success_commits():
    service, conn = make_service()

    service.cancel_order(123)

    conn.start_transaction.assert_called_once()
    service.tickets.unmark_sold_by_order.assert_called_once_with(123)
    service.orders.cancel_order.assert_called_once_with(123)
    conn.commit.assert_called_once()
    conn.rollback.assert_not_called()


def test_cancel_order_error_rolls_back():
    service, conn = make_service()
    service.orders.cancel_order.side_effect = Exception("DB fail")

    with pytest.raises(Exception):
        service.cancel_order(123)

    conn.start_transaction.assert_called_once()
    conn.rollback.assert_called_once()
    conn.commit.assert_not_called()
