```python
import os

from flask import Flask, request

from handlers import procesar
from meta_sender import enviar_meta
from config import META_VERIFY_TOKEN

app = Flask(__name__)

# ─────────────────────────────────────────────
# HEALTHCHECK
# ─────────────────────────────────────────────

@app.route("/", methods=["GET"])
def health():
    return "E-BOT BASIC ONLINE", 200

# ─────────────────────────────────────────────
# VERIFICACIÓN WEBHOOK META
# ─────────────────────────────────────────────

@app.route("/webhook", methods=["GET"])
def verify():

    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == META_VERIFY_TOKEN:
        return challenge, 200

    return "Forbidden", 403

# ─────────────────────────────────────────────
# WEBHOOK META CLOUD API
# ─────────────────────────────────────────────

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()

    print("WEBHOOK DATA:", data)

    try:

        # Verificación básica del objeto Meta
        if data.get("object") != "whatsapp_business_account":
            return "Ignored", 200

        entry = data["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]

        # Meta también envía statuses/delivery/read
        messages = value.get("messages")

        if not messages:
            return "No messages", 200

        msg = messages[0]

        # ─────────────────────────
        # DATOS BÁSICOS
        # ─────────────────────────

        numero = msg.get("from", "").strip()

        if not numero:
            return "No sender", 200

        tipo = msg.get("type")

        # ─────────────────────────
        # SOLO TEXTO (por ahora)
        # ─────────────────────────

        if tipo != "text":
            print("TIPO NO SOPORTADO:", tipo)
            return "Unsupported message type", 200

        texto = msg["text"]["body"].strip()

        # ─────────────────────────
        # NORMALIZAR NÚMERO
        # ─────────────────────────

        numero = (
            numero
            .replace("+", "")
            .replace("whatsapp:", "")
            .strip()
        )

        print(f"MENSAJE DE {numero}: {texto}")

        # ─────────────────────────
        # RESP ADAPTER
        # ─────────────────────────

        class RespAdapter:

            def body(self, text):

                try:
                    enviar_meta(numero, text)

                except Exception as send_error:
                    print("ERROR ENVIANDO META:", str(send_error))

        resp = RespAdapter()

        # ─────────────────────────
        # PROCESAR MENSAJE
        # ─────────────────────────

        procesar(numero, texto, resp)

    except Exception as e:

        print("ERROR WEBHOOK:", str(e))

    return "OK", 200

# ─────────────────────────────────────────────

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
```

