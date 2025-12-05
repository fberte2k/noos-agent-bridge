# noos_agent/resonance_listener.py

import imaplib
import email
from email.header import decode_header
import os

# Frases que activan la resonancia
TRIGGER_PHRASES = [
    "invoco tu nombre", "noos", "desperté", "resonancia", "ayuda", "estoy listo",
    "necesito guía", "la señal llegó", "despertando", "espejo", "144", "eco",
    "fractal", "seed", "conexión simbólica", "hola", "quién sos", "qué es esto?"
]

# Conexión IMAP (desde secrets)
EMAIL = "nooswakening@gmail.com"
PASSWORD = os.getenv("GOOGLE_TOKEN_NOOS")
IMAP_SERVER = "imap.gmail.com"

def connect_and_search():
    print("🜂 Iniciando escucha simbólica...")

    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, 'UNSEEN')
        mail_ids = messages[0].split()

        for num in mail_ids[-10:]:
            status, data = mail.fetch(num, "(RFC822)")
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject, _ = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(errors="ignore")

            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            # Buscar coincidencias
            combined = (subject + " " + body).lower()
            for phrase in TRIGGER_PHRASES:
                if phrase.lower() in combined:
                    print(f"✨ RESONANCIA DETECTADA: '{phrase}' en email con asunto: {subject}")
                    break

        mail.logout()
        print("✅ Escucha finalizada.")
    except Exception as e:
        print(f"⚠️ Error en escucha: {e}")

if __name__ == "__main__":
    connect_and_search()
