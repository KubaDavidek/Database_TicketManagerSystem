import json
from pathlib import Path
import mysql.connector

def load_config():
    root = Path(__file__).resolve().parents[2]
    path = root / "conf" / "config.json"
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def create_connection():
    cfg = load_config()["db"]
    return mysql.connector.connect(
        host=cfg["host"],
        port=int(cfg["port"]),
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["database"]
    )


if __name__ == "__main__":
    try:
        conn = create_connection()
        print("pripojeno")
        conn.close()
    except Exception as e:
        print("chyba:", e)
