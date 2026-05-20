import os
from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "EBOT_BASIC_VERIFY"

# ─────────────────────────────
# HEALTHCHECK
# ─────────────────────────────

@app.route("/", methods=["GET"])
def health():
    return "OK", 200

# ─────────────────────────────
# VERIFICACIÓN META
# ─────────────────────────────

@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token == VERIFY_TOKEN:
        return challenge, 200

    return "Forbidden", 403

# ─────────────────────────────
# MENSAJES ENTRANTES
# ─────────────────────────────

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    print(data)

    return "OK", 200

# ─────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
