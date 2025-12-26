from src.db.connection import create_connection
from src.repositories.event_repository import EventRepository


def run_menu() -> None:
    try:
        conn = create_connection()
    except Exception as e:
        print("CHYBA: nepodařilo se připojit k databázi.")
        print("Detail:", e)
        return

    event_repo = EventRepository(conn)

    while True:
        print("\n=== ticket system ===")
        print("1) vypsat aktivni akce")
        print("0) konec")

        choice = input("> ").strip()

        if choice == "1":
            try:
                events = event_repo.list_active()
                if not events:
                    print("Zadne aktivni akce.")
                    continue

                print("\nID | NAZEV | START")
                print("-" * 60)
                for e in events:
                    print(f"{e['id']} | {e['name']} | {e['start_at']}")
            except Exception as e:
                print("CHYBA: nepodařilo se načíst akce z databáze.")
                print("Detail:", e)

        elif choice == "0":
            try:
                conn.close()
            except Exception:
                pass
            print("konec.")
            break
        else:
            print("neplatna volba.")
