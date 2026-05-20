import requests
from config import META_ACCESS_TOKEN, META_API_URL

def enviar_meta(numero, texto):
    payload = {
        "messaging_product": "whatsapp",
        "to": numero.replace("whatsapp:+", ""),
        "type": "text",
        "text": {"body": texto}
    }

    headers = {
        "Authorization": f"Bearer {META_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    r = requests.post(META_API_URL, json=payload, headers=headers)

    print("META RESPONSE:", r.status_code, r.text)
