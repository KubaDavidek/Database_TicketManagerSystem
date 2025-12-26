from typing import List, Dict


class EventRepository:
    def __init__(self, connection):
        self.connection = connection

    def list_active(self) -> List[Dict]:
        cur = self.connection.cursor(dictionary=True)
        cur.execute(
            """
            select id, name, start_at
            from event
            where is_active = 1
            order by start_at;
            """
        )
        return cur.fetchall()
