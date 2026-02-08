from flask import Flask, request, jsonify
import random
import string

app = Flask(__name__)

@app.route("/")
def home():
    return "Level Bot Server is Running ✅"

@app.route("/generate-key")
def generate_key():
    key = "LVL-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
    return jsonify({
        "owner": "YourNameHere",
        "key": key
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
