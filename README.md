# CraftokAPI

Unofficial Bedwars-focused API for Craftok stats.

## Installation

Make sure you have a recent version of Python installed.

Run the scraper
```bash
scrap.bat
```

Run the API locally
```bash
flask run
```

## Examples

### Get player stats
```js
GET /bedwars/player/<username>
```

### Get player stats
```js
GET /bedwars/top
params: {
    stat_type: "lits-casses" | "victoires" | "temps-de-jeu" | "final-kills" | "morts" | "kills"
    period: "jour" | "mois" | "a-vie"
    limit: default=100 // amount of players to return
}
```

All requests return a JSON object.

## Why SQLite

Originally, I just wanted to use sqlite to easily store and manipulate data then put it on a clean MySQL database and keep the sqlite file as backup.

## State of development

Actually, this is only a proof of concept, the API is functional but not minded to be publicly available.

It's just a fun project and I don't have any intention to continue it.