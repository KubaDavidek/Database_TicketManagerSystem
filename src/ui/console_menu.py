from src.db.connection import create_connection
from src.repositories.event_repository import EventRepository
from src.repositories.ticket_repository import TicketRepository
from src.repositories.report_repository import ReportRepository
from src.services.order_service import OrderService


def run_menu() -> None:
    try:
        conn = create_connection()
    except Exception as e:
        print("CHYBA: nepodařilo se připojit k databázi.")
        print("Detail:", e)
        return

    event_repo = EventRepository(conn)
    ticket_repo = TicketRepository(conn)
    order_service = OrderService(conn)
    report_repo = ReportRepository(conn)

    while True:
        print("\n=== ticket system ===")
        print("1) vypsat aktivni akce")
        print("2) detail akce (volne vstupenky)")
        print("3) koupit vstupenku (vytvorit objednavku)")
        print("4) report: prodeje podle akce")
        print("5) report: zakaznici a objednavky")
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

        elif choice == "3":
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

                ticket_id = int(input("\nZadej TICKET_ID, ktery chces koupit: ").strip())

                full_name = input("Jmeno a prijmeni: ").strip()
                email = input("Email: ").strip()
                phone = input("Telefon (muze byt prazdne): ").strip() or None

                if len(full_name) < 3:
                    print("CHYBA: jmeno je moc kratke.")
                    continue
                if "@" not in email or "." not in email:
                    print("CHYBA: email nevypada validne.")
                    continue

                order_id = order_service.buy_single_ticket(
                    full_name=full_name,
                    email=email,
                    phone=phone,
                    ticket_id=ticket_id,
                )
                print(f"Objednavka vytvorena. ID objednavky: {order_id}")

            except ValueError:
                print("CHYBA: zadej platne cislo.")
            except Exception as e:
                print("CHYBA: objednavku se nepodarilo vytvorit.")
                print("Detail:", e)

        elif choice == "4":
            try:
                rows = report_repo.event_sales()
                if not rows:
                    print("zadna data pro report.")
                    continue

                print("\nEVENT | MESTO | START | SOLD/TOTAL | REVENUE")
                print("-" * 90)
                for r in rows:
                    sold_total = f"{r['tickets_sold']}/{r['tickets_total']}"
                    print(
                        f"{r['event_name']} | {r['city']} | {r['start_at']} | {sold_total} | {r['revenue']}"
                    )
            except Exception as e:
                print("CHYBA: report se nepodarilo nacist.")
                print("Detail:", e)

        elif choice == "5":
            try:
                rows = report_repo.customer_orders()
                if not rows:
                    print("zadna data pro report.")
                    continue

                print("\nZAKAZNIK | EMAIL | OBJEDNAVKY | NAPOSLEDY")
                print("-" * 90)
                for r in rows:
                    print(
                        f"{r['full_name']} | {r['email']} | {r['orders_count']} | {r['last_order_at']}"
                    )
            except Exception as e:
                print("CHYBA: report se nepodarilo nacist.")
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
