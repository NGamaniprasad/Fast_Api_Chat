


# import smtplib
# from email.message import EmailMessage

# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 587

# # CHANGE THESE
# # EMAIL = "grownbyaigp@gmail.com"
# # PASSWORD = "agblkeblhtorwrnv"

# import os

# EMAIL = os.getenv("EMAIL")
# PASSWORD = os.getenv("EMAIL_PASSWORD")


# async def send_email(sender, receivers, subject, message, file):
#     msg = EmailMessage()
#    # msg["From"] = sender
#     msg["From"] = EMAIL
#     msg["Reply-To"] = sender

#     msg["To"] = ", ".join(receivers)
#     msg["Subject"] = subject
#     msg.set_content(message)

#     if file:
#         data = await file.read()
#         msg.add_attachment(
#             data,
#             maintype="application",
#             subtype="octet-stream",
#             filename=file.filename,
#         )

#     with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#         server.starttls()
#         server.login(EMAIL, PASSWORD)
#         server.send_message(msg)
# """
# DS/
# │
# ├── main.py
# ├── email_utils.py
# ├── requirements.txt
# ├── render.yaml          (only if deploying)
# │
# ├── templates/
# │   ├── home.html        (login / try it out page)
# │   ├── chat.html        (send mail page)
# │   ├── response.html    (success / failed message)
# │   └── data.html        (wrong password page)
# │
# └── dot/                 (Python virtual environment)
#     ├── Scripts/
#     ├── Lib/
#     └── pyvenv.cfg
# """


import smtplib
from email.message import EmailMessage
import os

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL = os.getenv("EMAIL")  # your Gmail address
PASSWORD = os.getenv("EMAIL_PASSWORD")  # Gmail App Password

def send_email(sender, receivers, subject, message, file):
    msg = EmailMessage()
    msg["From"] = EMAIL
    msg["Reply-To"] = sender
    msg["To"] = ", ".join(receivers)
    msg["Subject"] = subject
    msg.set_content(message)

    if file:
        data = file.file.read()
        msg.add_attachment(
            data,
            maintype="application",
            subtype="octet-stream",
            filename=file.filename,
        )

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)

