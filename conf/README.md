# Ticket Management System

Konzolová aplikace v Pythonu pro správu a prodej vstupenek s databází MySQL.

## Instalace
1. Nainstaluj Python 3.11+
2. Nainstaluj závislosti: pip install mysql-connector-python
3. Vytvoř databázi a spusť db/schema.sql
4. Zkopíruj conf/config.example.json → conf/config.json a doplň přístup
5. Spusť: python -m src.main

## Funkce
- výpis akcí
- výpis dostupných vstupenek
- nákup vstupenky (transakčně)
- zrušení objednávky
- reporty
- import dat

## Struktura projektu
src/ – zdrojový kód  
doc/ – dokumentace  
test/ – test scénáře  
db/ – databázové skripty  
