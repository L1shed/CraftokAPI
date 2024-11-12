import re

import requests
from bs4 import BeautifulSoup
import sqlite3
import os

from converter import convert_to_minutes

if os.path.exists("stats.db"):
    os.remove("stats.db")

conn = sqlite3.connect("stats.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS player_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT,
        kills INTEGER,
        stat_type TEXT,
        period TEXT
    )
''')
conn.commit()

base_url = 'https://craftok.fr/leaderboard/bedwars'

stat_types = ["lits-casses", "victoires", "temps-de-jeu", "final-kills", "morts", "kills"]
periods = ["jour", "mois", "a-vie"]


def fetch_and_store_data(stat_type, period):
    url = f"{base_url}/{stat_type}/{period}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data for {stat_type} ({period}): {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Scrape podium players (top 3 players)
    players_data = []
    podium_ranks = soup.select('.podium .rank')
    for rank in podium_ranks:
        player_name = rank.select_one('.name').text.strip()
        value = rank.select_one('.face2 .value').text.strip()

        if stat_type == 'temps-de-jeu':
            value = convert_to_minutes(value)

        players_data.append((player_name, value, stat_type, period))

    # Reestablish correct order
    players_data[0], players_data[1] = players_data[1], players_data[0]

    # Scrape other players
    rank_rows = soup.select('.mt-5 .d-flex')
    for row in rank_rows[1:]:
        player_name = row.select_one('div.px-5').text.strip()
        value = row.select_one('div[style*="width:20%"]').text.strip().split()[0]

        if stat_type == 'temps-de-jeu':
            value = convert_to_minutes(value)

        players_data.append((player_name, value, stat_type, period))


        print(stat_type, period, player_name, value)

    insert_query = """
    INSERT INTO player_stats (player_name, kills, stat_type, period)
    VALUES (?, ?, ?, ?)
    """
    print(players_data)
    cursor.executemany(insert_query, players_data)
    conn.commit()


for stat_type in stat_types:
    for period in periods:
        fetch_and_store_data(stat_type, period)

cursor.close()
conn.close()
