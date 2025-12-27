from src.db.connection import create_connection
from src.repositories.event_repository import EventRepository
from src.repositories.ticket_repository import TicketRepository


def run_menu() -> None:
    try:
        conn = create_connection()
    except Exception as e:
        print("CHYBA: nepodařilo se připojit k databázi.")
        print("Detail:", e)
        return

    event_repo = EventRepository(conn)
    ticket_repo = TicketRepository(conn)

    while True:
        print("\n=== ticket system ===")
        print("1) vypsat aktivni akce")
        print("2) detail akce (volne vstupenky)")
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
                print("CHYBA: nepodařilo se načíst akce.")
                print("Detail:", e)

        elif choice == "2":
            try:
                event_id = int(input("Zadej ID akce: ").strip())
                tickets = ticket_repo.list_available_by_event(event_id)

                if not tickets:
                    print("Pro tuto akci nejsou zadne volne vstupenky.")
                    continue

                print("\nTICKET_ID | SEKTOR | RADA | MISTO | CENA")
                print("-" * 70)
                for t in tickets:
                    print(
                        f"{t['ticket_id']} | {t['sector']} | {t['seat_row']} | {t['seat_no']} | {t['price']}"
                    )
            except ValueError:
                print("Zadej platne cislo.")
            except Exception as e:
                print("CHYBA: nepodařilo se načíst vstupenky.")
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
