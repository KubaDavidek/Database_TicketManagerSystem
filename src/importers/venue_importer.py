import csv
from pathlib import Path


class VenueImporter:
    def __init__(self, connection):
        self.connection = connection

    def import_csv(self, csv_path: str) -> tuple[int, int]:
        """
        Vrátí (imported_ok, imported_fail)
        """
        path = Path(csv_path)
        ok = 0
        fail = 0

        with path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    name = (row.get("name") or "").strip()
                    city = (row.get("city") or "").strip()
                    address = (row.get("address") or "").strip() or None

                    if not name or not city:
                        raise ValueError("name/city nesmí být prázdné")

                    cur = self.connection.cursor()
                    cur.execute(
                        "insert into venue (name, city, address) values (%s, %s, %s)",
                        (name, city, address),
                    )
                    ok += 1
                except Exception:
                    fail += 1

        self.connection.commit()
        return ok, fail
