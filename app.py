from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('stats.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/bedwars/player/<username>', methods=['GET'])
def get_player_stats(username):
    conn = get_db_connection()
    cursor = conn.execute("SELECT * FROM player_stats WHERE player_name = ?", (username,))
    stats = cursor.fetchall()
    conn.close()

    if not stats:
        return jsonify({"message": f"Aucune statistique trouvée pour le joueur '{username}'."}), 404

    # Formatage des résultats
    player_stats = [
        {
            "player_name": row["player_name"],
            "kills": row["kills"],
            "stat_type": row["stat_type"],
            "period": row["period"]
        } for row in stats
    ]

    return jsonify(player_stats)

@app.route('/bedwars/top', methods=['GET'])
def get_top_players():
    stat_type = request.args.get('stat_type')
    period = request.args.get('period')
    n = request.args.get('limit', default=100, type=int)

    # Validation des paramètres
    if not stat_type or not period:
        return jsonify({"error": "Les paramètres 'stat_type' et 'period' sont requis."}), 400
    if not (1 <= n <= 100):
        return jsonify({"error": "Le paramètre 'n' doit être entre 1 et 100."}), 400

    conn = get_db_connection()
    cursor = conn.execute("""
        SELECT player_name, kills FROM player_stats 
        WHERE stat_type = ? AND period = ? 
        ORDER BY kills DESC 
        LIMIT ?
    """, (stat_type, period, n))
    top_players = cursor.fetchall()
    conn.close()

    # Formatage des résultats
    top_players_list = [
        {"player_name": row["player_name"], "kills": row["kills"]}
        for row in top_players
    ]

    return jsonify(top_players_list)

if __name__ == '__main__':
    app.run(debug=True)
