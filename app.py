from flask import Flask, jsonify, request
import os
import random
import string

app = Flask(__name__)

@app.route("/")
def home():
    return "Server is running 🔥", 200

@app.route("/generate-key")
def generate_key():
    owner = request.args.get("owner")
    if not owner:
        return jsonify({"error": "owner required"}), 400

    key = "KEY-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=16))
    return jsonify({
        "owner": owner,
        "key": key
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
