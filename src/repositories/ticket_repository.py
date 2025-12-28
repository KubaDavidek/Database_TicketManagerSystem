from typing import List, Dict


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
