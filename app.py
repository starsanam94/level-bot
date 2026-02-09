from flask import Flask, request, jsonify
import os
import time

app = Flask(__name__)

# ====== OWNER SETTINGS ======
OWNER_TOKEN = os.getenv("OWNER_TOKEN", "change-this-owner-token")
APP_NAME = "Level Bot Backend"

# ====== DUMMY DATABASE (in-memory) ======
# real project me isko DB (SQLite/Mongo) me shift kar sakte ho
KEYS_DB = {
    "ABC123": {
        "active": True,
        "created": int(time.time()),
        "note": "test key"
    },
    "VIP999": {
        "active": True,
        "created": int(time.time()),
        "note": "vip key"
    }
}

# ====== HOME ======
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "app": APP_NAME
    })

# ====== KEY VERIFY (APP USE KAREGA) ======
@app.route("/verify", methods=["POST"])
def verify_key():
    data = request.json
    if not data or "key" not in data:
        return jsonify({"status": "error", "msg": "key missing"}), 400

    key = data["key"]

    if key in KEYS_DB and KEYS_DB[key]["active"]:
        return jsonify({
            "status": "success",
            "msg": "key valid",
            "key": key
        })
    else:
        return jsonify({
            "status": "failed",
            "msg": "invalid or disabled key"
        }), 403

# ====== ADMIN: CREATE KEY ======
@app.route("/admin/create_key", methods=["POST"])
def create_key():
    token = request.headers.get("Owner-Token")
    if token != OWNER_TOKEN:
        return jsonify({"error": "unauthorized"}), 401

    data = request.json
    new_key = data.get("key")

    if not new_key:
        return jsonify({"error": "key required"}), 400

    KEYS_DB[new_key] = {
        "active": True,
        "created": int(time.time()),
        "note": data.get("note", "")
    }

    return jsonify({"status": "created", "key": new_key})

# ====== ADMIN: DISABLE KEY ======
@app.route("/admin/disable_key", methods=["POST"])
def disable_key():
    token = request.headers.get("Owner-Token")
    if token != OWNER_TOKEN:
        return jsonify({"error": "unauthorized"}), 401

    data = request.json
    key = data.get("key")

    if key in KEYS_DB:
        KEYS_DB[key]["active"] = False
        return jsonify({"status": "disabled", "key": key})
    else:
        return jsonify({"error": "key not found"}), 404

# ====== ADMIN: LIST KEYS ======
@app.route("/admin/keys", methods=["GET"])
def list_keys():
    token = request.headers.get("Owner-Token")
    if token != OWNER_TOKEN:
        return jsonify({"error": "unauthorized"}), 401

    return jsonify(KEYS_DB)

# ====== RUN ======
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
    
