from typing import List, Dict


class ReportRepository:
    def __init__(self, connection):
        self.connection = connection

    def event_sales(self) -> List[Dict]:
        cur = self.connection.cursor(dictionary=True)
        cur.execute(
            """
            select
                event_id,
                event_name,
                city,
                start_at,
                tickets_total,
                tickets_sold,
                tickets_available,
                revenue
            from v_event_sales
            order by start_at;
            """
        )
        return cur.fetchall()
