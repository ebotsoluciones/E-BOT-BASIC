
# E-BOT BASIC 🦙

Bot de turnos para WhatsApp utilizando Meta WhatsApp Cloud API.

Sin base de datos:
todos los datos se guardan en archivos JSON locales.

Ideal para:
- profesionales independientes,
- consultorios,
- pequeños negocios,
- MVP SaaS de bajo costo.

---

# Stack

- Python
- Flask
- Meta WhatsApp Cloud API
- JSON persistente en disco
- Gunicorn
- Railway / VPS

---

# Arquitectura

```txt
ebot-basic/
├── app.py
├── config.py
├── handlers.py
├── services.py
├── storage.py
├── meta_sender.py
├── requirements.txt
├── Procfile
├── .env.example
└── data/
    ├── estados_usuarios.json
    ├── turnos.json
    ├── bloqueos.json
    └── mensajes.json
````

---

# Características

✅ Turnos automáticos
✅ Panel administrador
✅ Bloqueo de horarios
✅ Persistencia JSON
✅ Sin base de datos
✅ Deploy rápido
✅ Compatible Railway
✅ Arquitectura modular
✅ WhatsApp real vía Meta Cloud API

---

# Instalación local

```bash
git clone <repo>

cd ebot-basic

python -m venv venv
```

## Linux / Mac

```bash
source venv/bin/activate
```

## Windows

```bash
venv\Scripts\activate
```

## Instalar dependencias

```bash
pip install -r requirements.txt
```

## Variables ENV

```bash
cp .env.example .env
```

Editar `.env` con:

* token Meta,
* número WhatsApp,
* admins,
* configuración general.

## Ejecutar local

```bash
python app.py
```

---

# Variables de entorno

```env
MODO_TEST=true

ADMINS=5493515337035

META_ACCESS_TOKEN=TU_TOKEN

META_PHONE_NUMBER_ID=1100001633202652

META_VERIFY_TOKEN=e_bot_basic_verify

DATA_DIR=data
```

---

# Deploy Railway

## 1. Crear proyecto

Subir el repositorio a GitHub y conectar Railway.

## 2. Variables ENV

Agregar todas las variables del `.env.example`.

## 3. Procfile

```txt
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 4
```

## 4. Deploy

Railway detecta automáticamente:

* Python,
* requirements,
* gunicorn.

---

# Webhook Meta

## URL

```txt
https://TU_DOMINIO/webhook
```

## Verify Token

```txt
e_bot_basic_verify
```

---

# Configuración Meta Developers

En Meta for Developers:

1. Crear app Business
2. Agregar WhatsApp
3. Configurar Webhook
4. Suscribirse a:

   * messages
   * message_deliveries
   * message_reads

---

# Panel Admin

## Modo test

```env
MODO_TEST=true
```

Cualquier usuario puede escribir:

```txt
adm
```

## Producción

```env
MODO_TEST=false
```

Solo los números en `ADMINS` acceden al panel.

---

# Opciones Admin

```txt
1 Turnos hoy
2 Próximos turnos
3 Mensajes
4 Nuevo turno
5 Cancelar turno
6 Bloquear agenda
7 Salir
```

---

# Configuración horarios

En `services.py`

```python
HORA_INICIO = time(9, 0)

HORA_FIN = time(19, 0)

INTERVALO = 60
```

---

# Persistencia

Todos los datos se guardan automáticamente en:

```txt
data/
```

Archivos:

| Archivo               | Función              |
| --------------------- | -------------------- |
| estados_usuarios.json | estados conversación |
| turnos.json           | turnos               |
| bloqueos.json         | horarios bloqueados  |
| mensajes.json         | mensajes pacientes   |

---

# Producción recomendada

Railway funciona perfecto para MVP.

Para escalado:

* VPS
* PostgreSQL
* Redis
* workers
* colas
* backups automáticos

---

# Roadmap futuro

* Multi profesional
* Calendario web
* Recordatorios automáticos
* Confirmación de asistencia
* Integración Google Calendar
* Panel web
* Multi sucursal
* E-BOT SUITE
* E-BOT ENTERPRISE

---

# Modelo comercial sugerido

## Instalación

USD 50 → 300

## Mensualidad

USD 20 → 50

## Versiones superiores

* CUSTOM
* SUITE
* ENTERPRISE

---

# Licencia

Uso privado / comercial bajo autorización del desarrollador.
