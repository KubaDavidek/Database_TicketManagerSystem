from typing import List, Dict
from typing import Optional, Dict

class TicketRepository:
    def __init__(self, connection):
        self.connection = connection

    def list_available_by_event(self, event_id: int) -> List[Dict]:
        cur = self.connection.cursor(dictionary=True)
        cur.execute(
            """
            select
                t.id as ticket_id,
                s.sector,
                s.seat_row,
                s.seat_no,
                t.price
            from ticket t
            join seat s on s.id = t.seat_id
            where t.event_id = %s and t.is_sold = 0
            order by s.sector, s.seat_row, s.seat_no;
            """,
            (event_id,),
        )
        return cur.fetchall()

    def mark_sold(self, ticket_id: int) -> int:

        cur = self.connection.cursor()
        cur.execute(
            "update ticket set is_sold = 1 where id = %s and is_sold = 0",
            (ticket_id,),
        )
        return cur.rowcount

    def unmark_sold_by_order(self, order_id: int):
        cur = self.connection.cursor()
        cur.execute(
            """
            update ticket t
            join order_item oi on oi.ticket_id = t.id
            set t.is_sold = 0
            where oi.order_id = %s
            """,
            (order_id,),
        )

    def find_by_id(self, ticket_id: int) -> Optional[Dict]:
        cur = self.connection.cursor(dictionary=True)
        cur.execute(
            "select id, event_id, seat_id, price, is_sold from ticket where id = %s",
            (ticket_id,),
        )
        return cur.fetchone()

    def is_available_for_event(self, ticket_id: int, event_id: int) -> bool:
        cur = self.connection.cursor()
        cur.execute(
            "select 1 from ticket where id = %s and event_id = %s and is_sold = 0",
            (ticket_id, event_id),
        )
        return cur.fetchone() is not None

