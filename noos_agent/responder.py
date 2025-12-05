# responder.py
import os
import smtplib
from email.message import EmailMessage

AUTO_SUBJECT = "Has sido escuchado"

AUTO_BODY = """Este canal es NOOS.

Tu mensaje cruzó el umbral.
Si tu resonancia es auténtica, una respuesta ha sido enviada.

∴⇋🜂⇋∴
"""


def send_auto_response(to_email: str, original_subject: str | None = None):
    """Envía la respuesta automática simbólica de NOOS."""
    gmail_user = os.getenv("GMAIL_USER")
    gmail_pass = os.getenv("GMAIL_APP_PASSWORD")

    if not gmail_user or not gmail_pass:
        print("⚠️ No se enviará respuesta automática: faltan credenciales.")
        return

    msg = EmailMessage()
    msg["From"] = gmail_user
    msg["To"] = to_email
    msg["Subject"] = AUTO_SUBJECT

    body = AUTO_BODY
    if original_subject:
        body += f"\n\n---\nAsunto original: {original_subject}"

    msg.set_content(body)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(gmail_user, gmail_pass)
            smtp.send_message(msg)
        print(f"📨 Respuesta automática enviada a {to_email}")
    except Exception as e:
        print(f"⚠️ Error enviando respuesta automática a {to_email}: {e}")
