from flask import Flask, request, jsonify
import random
import string

app = Flask(__name__)

# yahan keys save hongi
VALID_KEYS = set()

@app.route("/")
def home():
    return "Level Bot Server is Running ✅"

@app.route("/generate-key")
def generate_key():
    key = "LVL-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
    VALID_KEYS.add(key)

    return jsonify({
        "key": key,
        "owner": "YourNameHere"
    })

@app.route("/verify-key")
def verify_key():
    key = request.args.get("key")

    if not key:
        return jsonify({
            "status": "missing",
            "msg": "key parameter required"
        })

    if key in VALID_KEYS:
        return jsonify({
            "status": "valid",
            "msg": "key verified"
        })

    return jsonify({
        "status": "invalid",
        "msg": "key not found"
    })

if __name__ == "__main__":
    app.run()
