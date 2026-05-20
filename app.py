import os
from flask import Flask, request

from handlers import procesar
from meta_sender import enviar_meta

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
# MENSAJES ENTRANTES (META CLOUD API)
# ─────────────────────────────

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    print("WEBHOOK DATA:", data)

    try:
        entry = data["entry"][0]["changes"][0]["value"]

        if "messages" in entry:
            msg = entry["messages"][0]

            numero = msg["from"]
            texto = msg["text"]["body"]

            numero_formateado = f"whatsapp:+{numero}"

            # 🔥 ADAPTADOR REAL (sin Twilio)
            class RespAdapter:
                def body(self, text):
                    enviar_meta(numero_formateado, text)

            resp = RespAdapter()

            procesar(numero_formateado, texto, resp)

    except Exception as e:
        print("ERROR WEBHOOK:", e)

    return "OK", 200

# ─────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
