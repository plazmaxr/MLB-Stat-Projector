from flask import Flask, request, jsonify
from flask_cors import CORS
import mlb
import io
import contextlib

app = Flask(__name__)
CORS(app, origins="*")

@app.route("/", methods=["GET"])
def index():
    return "MLB backend running"

def capture_print(func, *args, **kwargs):
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            result = func(*args, **kwargs)
    except Exception as e:
        return {"returned": None, "printed": f"ERROR: {e}"}
    output = buf.getvalue()
    if result is not None:
        return {"returned": result, "printed": output}
    return {"returned": None, "printed": output}

@app.route("/api/player-id", methods=["POST"])
def api_player_id():
    data = request.json or {}
    name = data.get("name", "")
    if not name:
        return jsonify({"error": "no name provided"}), 400

    player_id = mlb.get_player_id_by_name(name)
    if player_id is None:
        return jsonify({"error": "player not found / ambiguous"}), 404
    return jsonify({"player_id": player_id})

@app.route("/api/player-stats", methods=["POST"])
def api_player_stats():
    data = request.json or {}
    player_id = data.get("player_id")
    if not player_id:
        return jsonify({"error": "no player_id provided"}), 400

    stats = mlb.get_player_stats(player_id)
    if not stats:
        return jsonify({"error": "no stats found"}), 404
    return jsonify({"stats": stats})

@app.route("/api/pitcher-stats", methods=["POST"])
def api_pitcher_stats():
    data = request.json or {}
    player_id = data.get("player_id")
    if not player_id:
        return jsonify({"error": "no player_id provided"}), 400

    stats = mlb.get_pitcher_stats(player_id)
    if not stats:
        return jsonify({"error": "no stats found"}), 404
    return jsonify({"stats": stats})

@app.route("/api/project-player", methods=["POST"])
def api_project_player():
    data = request.json or {}
    player_name = data.get("player_name", "")
    stats = data.get("stats")

    if not stats:
        pid = mlb.get_player_id_by_name(player_name)
        if not pid:
            return jsonify({"error": "player id not found"}), 404
        stats = mlb.get_player_stats(pid)
        if not stats:
            return jsonify({"error": "player stats not found"}), 404

    captured = capture_print(mlb.project_player_stats_with_ai, player_name, stats)
    if captured.get("returned"):
        return jsonify({"projection": captured["returned"], "printed": captured["printed"]})
    return jsonify({"projection": captured["printed"]})

@app.route("/api/project-pitcher", methods=["POST"])
def api_project_pitcher():
    data = request.json or {}
    pitcher_name = data.get("pitcher_name", "")
    stats = data.get("stats")

    if not stats:
        pid = mlb.get_player_id_by_name(pitcher_name)
        if not pid:
            return jsonify({"error": "pitcher id not found"}), 404
        stats = mlb.get_pitcher_stats(pid)
        if not stats:
            return jsonify({"error": "pitcher stats not found"}), 404

    captured = capture_print(mlb.project_pitcher_stats_with_ai, pitcher_name, stats)
    if captured.get("returned"):
        return jsonify({"projection": captured["returned"], "printed": captured["printed"]})
    return jsonify({"projection": captured["printed"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
