from typing import Optional, Dict


class CustomerRepository:
    def __init__(self, connection):
        self.connection = connection

    def find_by_email(self, email: str) -> Optional[Dict]:
        cur = self.connection.cursor(dictionary=True)
        cur.execute(
            "select id, full_name, email, phone from customer where email = %s",
            (email,),
        )
        return cur.fetchone()

    def create(self, full_name: str, email: str, phone: str | None) -> int:
        cur = self.connection.cursor()
        cur.execute(
            "insert into customer (full_name, email, phone) values (%s, %s, %s)",
            (full_name, email, phone),
        )
        return cur.lastrowid
