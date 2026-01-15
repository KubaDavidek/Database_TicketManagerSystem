# Database Ticket Manager System

Konzolová aplikace v Pythonu pro správu a prodej vstupenek na kulturní a sportovní akce. Aplikace pracuje s relační databází MySQL a umožňuje import dat, nákup vstupenek a generování souhrnných reportů.

## Požadavky

- Python 3.11 nebo novější
- MySQL Server (např. MySQL Community Server)
- Git (nebo stažení ZIP z GitHubu)
- Přístup k internetu (pro instalaci knihoven)

## Stažení projektu

Projekt stáhneš pomocí Git:

git clone https://github.com/KubaDavidek/Database_TicketManagerSystem.git  
cd Database_TicketManagerSystem

Nebo si stáhni ZIP z GitHubu a rozbal ho.

## Nastavení databáze

1. Otevři MySQL klienta (např. MySQL Workbench, phpMyAdmin nebo příkazovou řádku).
2. Vytvoř si novou databázi (např. ticket_db).
3. Otevři soubor db/schema.sql z tohoto projektu.
4. Zkopíruj celý jeho obsah a spusť ho nad vytvořenou databází.

Tím se vytvoří všechny tabulky, vazby a databázové pohledy.

## Nastavení konfigurace

1. Ve složce conf zkopíruj soubor config.example.json na config.json.
2. Otevři conf/config.json a vyplň své přihlašovací údaje k databázi:

{
  "db": {
    "host": "HOSTNAME",
    "port": 3306,
    "user": "USERNAME",
    "password": "PASSWORD",
    "database": "NAZEVDATABAZE"
  }
}

Soubor ulož.

## Instalace závislostí

V rootu projektu spusť:

pip install -r requirements.txt

## Spuštění aplikace

### Windows

Dvojklikem spusť soubor start.bat nebo v terminálu:

python main.py

### Linux / macOS

python3 main.py

## Struktura projektu

Database_TicketManagerSystem/  
├── db/             SQL skripty databáze  
├── conf/           konfigurace připojení  
├── src/            zdrojový kód aplikace  
├── test/           testovací scénáře  
├── doc/            dokumentace projektu  
├── requirements.txt  
├── start.bat  
└── README.md  

## Funkce aplikace

- Import míst konání a akcí (CSV / JSON)
- Výpis akcí a dostupných vstupenek
- Nákup vstupenky s využitím databázové transakce
- Report prodejů podle akcí
- Report zákazníků a jejich objednávek

## Další dokumentace

Podrobnější popis architektury, databázového modelu a návrhu aplikace je dostupný ve složce doc/.

## Autor

Autor projektu: Kuba Davídek  
Projekt vznikl jako školní práce v rámci výuky databázových systémů.
