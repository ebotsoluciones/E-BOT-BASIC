```python id="v6msqf"
import requests

from config import (
    META_ACCESS_TOKEN,
    META_API_URL
)

# ─────────────────────────────────────────────
# ENVIAR MENSAJE META CLOUD API
# ─────────────────────────────────────────────

def enviar_meta(numero, texto):

    # ─────────────────────────
    # NORMALIZAR NÚMERO
    # ─────────────────────────

    numero = (
        str(numero)
        .replace("whatsapp:+", "")
        .replace("whatsapp:", "")
        .replace("+", "")
        .strip()
    )

    # ─────────────────────────
    # PAYLOAD META
    # ─────────────────────────

    payload = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {
            "body": texto
        }
    }

    # ─────────────────────────
    # HEADERS
    # ─────────────────────────

    headers = {
        "Authorization": f"Bearer {META_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    # ─────────────────────────
    # REQUEST
    # ─────────────────────────

    try:

        response = requests.post(
            META_API_URL,
            json=payload,
            headers=headers,
            timeout=10
        )

        print(
            "META RESPONSE:",
            response.status_code,
            response.text
        )

        # ─────────────────────
        # VALIDACIÓN
        # ─────────────────────

        if response.status_code >= 400:

            print("ERROR META API")

            return False

        return True

    except requests.exceptions.RequestException as e:

        print("ERROR REQUEST META:", str(e))

        return False
```
