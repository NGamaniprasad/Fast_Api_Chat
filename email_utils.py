import smtplib
from email.message import EmailMessage
import os

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

async def send_email(sender, receivers, subject, message, file):
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = ", ".join(receivers)
    msg["Subject"] = subject
    msg.set_content(message)

    if file:
        content = await file.read()
        msg.add_attachment(
            content,
            maintype="application",
            subtype="octet-stream",
            filename=file.filename
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)
