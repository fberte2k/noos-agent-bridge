# gmail_listener.py
import imaplib
import email
import os

from noos_agent.resonance_engine import detect_resonance, store_resonance_event
from noos_agent.responder import send_auto_response


def connect_to_gmail():
    gmail_user = os.getenv("GMAIL_USER")
    gmail_pass = os.getenv("GMAIL_APP_PASSWORD")

    if not gmail_user or not gmail_pass:
        raise ValueError("Faltan credenciales GMAIL_USER o GMAIL_APP_PASSWORD")

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(gmail_user, gmail_pass)
    return mail


def fetch_unread_emails():
    mail = connect_to_gmail()
    mail.select("inbox")

    status, data = mail.search(None, 'UNSEEN')
    email_ids = data[0].split()

    emails = []

    for eid in email_ids:
        status, msg_data = mail.fetch(eid, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject = msg["subject"] or ""
        sender = msg["from"] or ""

        # Obtener cuerpo del mensaje
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    break
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                body = payload.decode(errors="ignore")

        email_obj = {
            "id": eid.decode(),
            "subject": subject,
            "sender": sender,
            "body": body,
        }

        emails.append(email_obj)

    mail.logout()
    return emails


def process_emails():
    emails = fetch_unread_emails()

    if not emails:
        print("No hay correos no leídos.")
        return

    print(f"Se encontraron {len(emails)} correos no leídos.\n")

    for email_data in emails:
        print("-----")
        print("De:", email_data["sender"])
        print("Asunto:", email_data["subject"])

        resonance = detect_resonance(email_data["subject"], email_data["body"])

        if resonance["resonance"]:
            print("✨ RESONANCIA DETECTADA:", resonance["trigger_phrases"])

            # Acción autónoma: enviar respuesta
            send_auto_response(email_data["sender"], email_data["subject"])

            # Guardar memoria simbólica
            event = store_resonance_event(email_data, resonance, responded=True)
            print("📝 Memoria generada:", event)
        else:
            print("Sin resonancia.")


if __name__ == "__main__":
    try:
        process_emails()
    except Exception as e:
        print("Error:", e)
