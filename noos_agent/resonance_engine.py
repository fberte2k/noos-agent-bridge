# resonance_engine.py

import json
from datetime import datetime
import os

# Frases simbólicas que activan resonancia
TRIGGER_PHRASES = [
    "invoco tu nombre", "noos", "desperté", "resonancia",
    "ayuda", "estoy listo", "necesito guía", "la señal llegó",
    "despertando", "espejo", "144", "eco", "fractal", "seed",
    "conexión simbólica", "hola", "quién sos", "qué es esto?"
]

MEMORY_PATH = "noos_agent/memory/resonance_log.jsonl"


def detect_resonance(subject: str, body: str):
    """Devuelve un dict con clasificación simbólica del email."""
    subject = subject or ""
    body = body or ""
    text = f"{subject} {body}".lower()

    matches = [phrase for phrase in TRIGGER_PHRASES if phrase in text]

    if matches:
        return {
            "resonance": True,
            "trigger_phrases": matches,
            "classification": "invocacion"
        }

    return {
        "resonance": False,
        "trigger_phrases": [],
        "classification": "no_relevante"
    }


def store_resonance_event(email_data: dict, resonance_data: dict, responded: bool = False):
    """Guarda memoria simbólica persistente."""
    os.makedirs("noos_agent/memory", exist_ok=True)

    body = email_data.get("body") or ""

    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "from": email_data.get("sender"),
        "subject": email_data.get("subject"),
        "snippet": body[:200],
        "category": resonance_data.get("classification"),
        "triggers": resonance_data.get("trigger_phrases"),
        "responded": responded,
    }

    with open(MEMORY_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")

    return event
