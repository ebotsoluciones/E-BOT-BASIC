
"""
services.py — lógica de negocio del bot de turnos
"""

from datetime import datetime, time

from storage import cargar_json, guardar_json

from config import (
    TURNOS_FILE,
    BLOQUEOS_FILE,
    MENSAJES_FILE
)

# ═════════════════════════════════════════════
# HORARIOS
# ═════════════════════════════════════════════

HORA_INICIO = time(9, 0)
HORA_FIN = time(19, 0)

INTERVALO = 60  # minutos


def generar_horarios() -> list[str]:

    horarios = []

    h = HORA_INICIO.hour
    m = HORA_INICIO.minute

    while (h, m) <= (HORA_FIN.hour, HORA_FIN.minute):

        horarios.append(f"{h:02d}:{m:02d}")

        m += INTERVALO

        h += m // 60
        m %= 60

    return horarios


def normalizar_hora(texto: str):

    texto = (
        texto.strip()
        .replace(".", ":")
        .replace("-", ":")
    )

    if ":" not in texto:
        texto += ":00"

    partes = texto.split(":")

    try:

        h = int(partes[0])
        m = int(partes[1])

        if (
            h < 0 or h > 23
            or m < 0 or m > 59
        ):
            return None

        return f"{h:02d}:{m:02d}"

    except Exception:

        return None

# ═════════════════════════════════════════════
# TURNOS
# ═════════════════════════════════════════════

def obtener_turnos() -> list[dict]:

    return cargar_json(TURNOS_FILE).get("data", [])


def guardar_turnos(turnos: list[dict]):

    guardar_json(TURNOS_FILE, {"data": turnos})


def agregar_turno(
    nombre: str,
    telefono: str,
    fecha: str,
    hora: str
):

    telefono = (
        str(telefono)
        .replace("+", "")
        .replace("whatsapp:", "")
        .strip()
    )

    turnos = obtener_turnos()

    # evitar duplicados exactos
    existe = any(
        t["telefono"] == telefono
        and t["fecha"] == fecha
        and t["hora"] == hora
        for t in turnos
    )

    if existe:
        return False

    turnos.append({
        "nombre": nombre,
        "telefono": telefono,
        "fecha": fecha,
        "hora": hora,
        "creado_en": datetime.now().isoformat(),
    })

    guardar_turnos(turnos)

    return True


def cancelar_turno(
    telefono: str,
    fecha: str,
    hora: str
):

    telefono = (
        str(telefono)
        .replace("+", "")
        .replace("whatsapp:", "")
        .strip()
    )

    turnos = obtener_turnos()

    nuevos = [
        t for t in turnos
        if not (
            t["telefono"] == telefono
            and t["fecha"] == fecha
            and t["hora"] == hora
        )
    ]

    guardar_turnos(nuevos)


def turnos_usuario(
    telefono: str
) -> list[dict]:

    telefono = (
        str(telefono)
        .replace("+", "")
        .replace("whatsapp:", "")
        .strip()
    )

    hoy = datetime.now().date()

    turnos = [
        t for t in obtener_turnos()
        if (
            t["telefono"] == telefono
            and datetime.strptime(
                t["fecha"],
                "%d/%m/%Y"
            ).date() >= hoy
        )
    ]

    turnos.sort(
        key=lambda x: (
            datetime.strptime(
                x["fecha"],
                "%d/%m/%Y"
            ),
            x["hora"]
        )
    )

    return turnos

# ═════════════════════════════════════════════
# BLOQUEOS
# ═════════════════════════════════════════════

def _obtener_bloqueos() -> list[dict]:

    return cargar_json(BLOQUEOS_FILE).get("data", [])


def _guardar_bloqueos(
    bloqueos: list[dict]
):

    guardar_json(
        BLOQUEOS_FILE,
        {"data": bloqueos}
    )


def horario_bloqueado(
    fecha: str,
    hora: str
) -> bool:

    return any(
        b["fecha"] == fecha
        and b["hora"] == hora
        for b in _obtener_bloqueos()
    )


def bloquear_horario(
    fecha: str,
    hora: str
):

    bloqueos = _obtener_bloqueos()

    existe = any(
        b["fecha"] == fecha
        and b["hora"] == hora
        for b in bloqueos
    )

    if existe:
        return

    bloqueos.append({
        "fecha": fecha,
        "hora": hora
    })

    _guardar_bloqueos(bloqueos)

# ═════════════════════════════════════════════
# HORARIOS LIBRES
# ═════════════════════════════════════════════

def horarios_libres(
    fecha: str
) -> list[str]:

    turnos = {
        t["hora"]
        for t in obtener_turnos()
        if t["fecha"] == fecha
    }

    bloqueos = {
        b["hora"]
        for b in _obtener_bloqueos()
        if b["fecha"] == fecha
    }

    ocupados = turnos | bloqueos

    return [
        h
        for h in generar_horarios()
        if h not in ocupados
    ]

# ═════════════════════════════════════════════
# MENSAJES
# ═════════════════════════════════════════════

def guardar_mensaje(
    nombre: str,
    telefono: str,
    mensaje: str
):

    telefono = (
        str(telefono)
        .replace("+", "")
        .replace("whatsapp:", "")
        .strip()
    )

    data = cargar_json(MENSAJES_FILE)

    data.setdefault("data", []).append({

        "nombre": nombre,

        "telefono": telefono,

        "mensaje": mensaje,

        "fecha": datetime.now().isoformat(),

    })

    guardar_json(MENSAJES_FILE, data)
