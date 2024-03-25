# Author: Sakthi Santhosh
# Created on: 16/10/2023
from os import getenv
from threading import Thread

from flask import current_app
from flask_mail import Message
import serial
from socketio import Client as SocketClient
from twilio.rest import Client as TwilioClient

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
        twilio_handle = TwilioClient(
            getenv("FLASK_TWILIO_SID"),
            getenv("FLASK_TWILIO_KEY")
        )

        twilio_handle.messages.create(
            body=message,
            from_=getenv("FLASK_TWILIO_PHONE"),
            to="+91" + recipient
        )

class SerialToSocketDaemon(Thread):
    def __init__(
        self,
        serial_port: str,
        socket_host: str = "127.0.0.1",
        socket_port: int = 5000,
        serial_baud_rate: int = 115200
    ):
        super().__init__()

        self.serial_port = serial_port
        self.socket_host = socket_host
        self.socket_port = socket_port
        self.serial_baud_rate = serial_baud_rate

        self.serial_connection = None
        self.socket_connection = None

        self.setDaemon(True)

    def run(self):
        print("Info: SerialToSocketDaemon service started in the background.")

        try:
            self.serial_connection = serial.Serial(
                self.serial_port,
                self.serial_baud_rate,
                timeout=1
            )
            self.socket_connection = SocketClient()

            self.socket_connection.connect(
                f"http://{self.socket_host}:{self.socket_port}",
                namespaces=["/rtdatastream"]
            )
            print("Info: Serial port at \"%s\" opened successfully."%(
                self.serial_port
            ))
            while True:
                data = self.serial_connection.readline().strip()

                if data:
                    print("Serial:", data)
                    self.socket_connection.emit(
                        event="data_ingress",
                        data=str(data),
                        namespace="/rtdatastream"
                    )
        except Exception as exc:
            print(f"Error: {exc}")
        finally:
            if self.serial_connection and self.serial_connection.is_open:
                self.serial_connection.close()
            if self.socket_connection:
                self.socket_connection.close()

            print("Info: All interfaces have been closed.")
