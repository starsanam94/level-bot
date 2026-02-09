from flask import Flask, jsonify, request
import os
import random
import string

app = Flask(__name__)

KEY_DB = {}  # owner -> key

@app.route("/")
def home():
    return "Server is running 🔥", 200

def generate_random_key():
    return "KEY-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=16))

@app.route("/generate-key")
def generate_key():
    owner = request.args.get("owner")
    if not owner:
        return jsonify({"error": "owner required"}), 400

    if owner in KEY_DB:
        key = KEY_DB[owner]
    else:
        key = generate_random_key()
        KEY_DB[owner] = key

    return jsonify({
        "owner": owner,
        "key": key
    }), 200

@app.route("/verify-key")
def verify_key():
    owner = request.args.get("owner")
    key = request.args.get("key")

    if not owner or not key:
        return jsonify({"status": "error", "msg": "owner & key required"}), 400

    if KEY_DB.get(owner) == key:
        return jsonify({"status": "valid"}), 200
    else:
        return jsonify({"status": "invalid"}), 403

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
