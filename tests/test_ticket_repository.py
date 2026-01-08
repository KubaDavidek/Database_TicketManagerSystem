from unittest.mock import Mock
from src.repositories.report_repository import ReportRepository


def test_event_sales_uses_view_v_event_sales():
    conn = Mock()
    cur = Mock()
    cur.fetchall.return_value = [{"event_id": 1}]
    conn.cursor.return_value = cur

    repo = ReportRepository(conn)
    rows = repo.event_sales()

    assert rows == [{"event_id": 1}]
    cur.execute.assert_called_once()
    sql = cur.execute.call_args[0][0].lower()
    assert "from v_event_sales" in sql


def test_customer_orders_uses_view_v_customer_orders():
    conn = Mock()
    cur = Mock()
    cur.fetchall.return_value = [{"customer_id": 1}]
    conn.cursor.return_value = cur

    repo = ReportRepository(conn)
    rows = repo.customer_orders()

    assert rows == [{"customer_id": 1}]
    cur.execute.assert_called_once()
    sql = cur.execute.call_args[0][0].lower()
    assert "from v_customer_orders" in sql
