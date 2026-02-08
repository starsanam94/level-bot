from flask import Flask, jsonify, request
import uuid
import time

app = Flask(__name__)

# in-memory key store (simple)
KEY_DB = {}

KEY_VALIDITY_SECONDS = 24 * 60 * 60  # 24 hours

@app.route("/")
def home():
    return "Level Bot Server is Running ✅"

@app.route("/generate-key", methods=["GET"])
def generate_key():
    key = str(uuid.uuid4())
    expiry = int(time.time()) + KEY_VALIDITY_SECONDS
    KEY_DB[key] = expiry
    return jsonify({
        "key": key,
        "expires_in_hours": 24
    })

@app.route("/verify-key", methods=["GET"])
def verify_key():
    key = request.args.get("key")
    if not key:
        return jsonify({"status": "error", "msg": "key required"}), 400

    expiry = KEY_DB.get(key)
    if not expiry:
        return jsonify({"status": "invalid", "msg": "key not found"}), 401

    if time.time() > expiry:
        return jsonify({"status": "expired", "msg": "key expired"}), 401

    return jsonify({"status": "valid", "msg": "key is valid"})
