from flask import Flask, request, jsonify
import random, string, time

app = Flask(__name__)

# key store (temporary memory)
VALID_KEYS = {}

@app.route("/")
def home():
    return "Level Bot Server is Running ✅"

@app.route("/generate-key")
def generate_key():
    key = "LVL-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    VALID_KEYS[key] = time.time() + 86400  # 24 hours

    return jsonify({
        "key": key,
        "expires_in": "24 hours"
    })

@app.route("/verify-key")
def verify_key():
    key = request.args.get("key")

    if not key:
        return jsonify({"status": "error", "msg": "key missing"})

    if key in VALID_KEYS:
        if time.time() < VALID_KEYS[key]:
            return jsonify({"status": "valid", "msg": "key is valid"})
        else:
            return jsonify({"status": "expired", "msg": "key expired"})

    return jsonify({"status": "invalid", "msg": "key not found"})
