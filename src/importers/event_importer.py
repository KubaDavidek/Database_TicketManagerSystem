import json
from pathlib import Path


class EventImporter:
    def __init__(self, connection):
        self.connection = connection

    def import_json(self, json_path: str) -> tuple[int, int]:
        """
        Vrátí (imported_ok, imported_fail)
        """
        path = Path(json_path)
        ok = 0
        fail = 0

        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError("JSON musí být seznam objektů")

        for item in data:
            try:
                venue_id = int(item["venue_id"])
                name = str(item["name"]).strip()
                start_at = str(item["start_at"]).strip()
                base_price = float(item["base_price"])
                is_active = int(item.get("is_active", 1))

                if not name:
                    raise ValueError("name nesmí být prázdné")

                cur = self.connection.cursor()
                cur.execute(
                    """
                    insert into event (venue_id, name, start_at, base_price, is_active)
                    values (%s, %s, %s, %s, %s)
                    """,
                    (venue_id, name, start_at, base_price, is_active),
                )
                ok += 1
            except Exception:
                fail += 1

        self.connection.commit()
        return ok, fail
