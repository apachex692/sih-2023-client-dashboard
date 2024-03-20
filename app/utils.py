# Author: Sakthi Santhosh
# Created on: 16/10/2023
from os import getenv
from flask import current_app
from flask_mail import Message
from twilio.rest import Client

from app import mail_handle

def send_email(subject: str, message: str, recipients: list[str]):
    message_handle = Message(
        subject=subject,
        html=message,
        recipients=recipients
    )

    mail_handle.send(message_handle)

def send_sms(message: str, recipient: str):
    if current_app.config.get("TWILIO_SEND_SMS", False):
        twilio_handle = Client(
            getenv("FLASK_TWILIO_SID"),
            getenv("FLASK_TWILIO_KEY")
        )

        twilio_handle.messages.create(
            body=message,
            from_=getenv("FLASK_TWILIO_PHONE"),
            to="+91" + recipient
        )
