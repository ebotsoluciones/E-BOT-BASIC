
"""
config.py — configuración de E-BOT BASIC 🚀
Compatible con Meta WhatsApp Cloud API
"""

import os

# ─────────────────────────────────────────────────────
# MODO TEST
# true  → cualquier usuario puede acceder como admin
# false → sólo números incluidos en ADMINS
# ─────────────────────────────────────────────────────

MODO_TEST = os.getenv("MODO_TEST", "true").lower() == "true"

# ─────────────────────────────────────────────────────
# ADMINS
# Formato:
# 5493515337035
# sin + ni whatsapp:
# ─────────────────────────────────────────────────────

_admins_raw = os.getenv("ADMINS", "5493515337035")

ADMINS = [
    a.strip().replace("+", "").replace("whatsapp:", "")
    for a in _admins_raw.split(",")
    if a.strip()
]

# ─────────────────────────────────────────────────────
# STORAGE
# ─────────────────────────────────────────────────────

DATA_DIR = os.getenv("DATA_DIR", "data")

TURNOS_FILE = "turnos.json"
BLOQUEOS_FILE = "bloqueos.json"
MENSAJES_FILE = "mensajes.json"

# ─────────────────────────────────────────────────────
# META CLOUD API
# ─────────────────────────────────────────────────────

META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "")



META_PHONE_NUMBER_ID = os.getenv(
    "META_PHONE_NUMBER_ID",
    "1100001633202652"
)

META_API_VERSION = "v25.0"

META_API_URL = (
    f"https://graph.facebook.com/"
    f"{META_API_VERSION}/"
    f"{META_PHONE_NUMBER_ID}/messages"
)

# ─────────────────────────────────────────────────────
# WEBHOOK VERIFY TOKEN
# ─────────────────────────────────────────────────────

META_VERIFY_TOKEN = os.getenv(
    "META_VERIFY_TOKEN",
    "e_bot_basic_verify"
)
