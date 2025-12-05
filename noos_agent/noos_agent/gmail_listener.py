# gmail_listener.py
import imaplib
import email
import os

def connect_to_gmail():
    """Conecta al servidor IMAP de Gmail usando App Password."""
    gmail_user = os.getenv("GMAIL_USER")
    gmail_pass = os.getenv("GMAIL_APP_PASSWORD")

    if not gmail_user or not gmail_pass:
        raise ValueError("Faltan credenciales GMAIL_USER o GMAIL_APP_PASSWORD")

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(gmail_user, gmail_pass)
    return mail


def fetch_unread_emails():
    """Obtiene correos no leídos y devuelve lista de diccionarios."""
    mail = connect_to_gmail()
    mail.select("inbox")

    status, data = mail.search(None, 'UNSEEN')
    email_ids = data[0].split()

    emails = []

    for eid in email_ids:
        status, msg_data = mail.fetch(eid, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject = msg["subject"]
        sender = msg["from"]

        # Obtener el cuerpo (solo texto plano por ahora)
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    break
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        emails.append({
            "id": eid.decode(),
            "subject": subject,
            "sender": sender,
            "body": body,
        })

    mail.logout()
    return emails


if __name__ == "__main__":
    try:
        unread = fetch_unread_emails()
        if not unread:
            print("No hay correos no leídos.")
        else:
            print(f"Se encontraron {len(unread)} correos no leídos:")
            for mail in unread:
                print("-----")
                print("De:", mail["sender"])
                print("Asunto:", mail["subject"])
                print("Cuerpo:", mail["body"][:200], "...")
    except Exception as e:
        print("Error:", e)
