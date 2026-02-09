from flask import Flask, request, jsonify
import uuid
import time

app = Flask(__name__)

# simple in-memory key store (baad me database laga sakte hain)
KEYS = {}

OWNER_SECRET = "my_owner_password"  # 🔴 isko apna strong password bana lena

@app.route("/")
def home():
    return "Server is running 🔥"

# 🔑 generate key (sirf owner ke liye)
@app.route("/generate-key", methods=["GET"])
def generate_key():
    owner = request.args.get("owner")

    if owner != OWNER_SECRET:
        return jsonify({"error": "unauthorized"}), 401

    key = str(uuid.uuid4()).replace("-", "").upper()
    KEYS[key] = {
        "created": int(time.time()),
        "active": True
    }

    return jsonify({
        "key": key,
        "status": "active"
    })

# ✅ key verify (Android app yahan hit karega)
@app.route("/verify-key", methods=["GET"])
def verify_key():
    key = request.args.get("key")

    if not key:
        return jsonify({"valid": False, "reason": "no key"})

    data = KEYS.get(key)

    if not data:
        return jsonify({"valid": False, "reason": "invalid key"})

    if not data["active"]:
        return jsonify({"valid": False, "reason": "key disabled"})

    return jsonify({"valid": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
