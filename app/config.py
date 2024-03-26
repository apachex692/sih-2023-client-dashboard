# Author: Sakthi Santhosh
# Created on: 16/10/2023
from os import getenv
from uuid import uuid4

class DeploymentConfig:
    pass

class DevelopmentConfig:
    SECRET_KEY = getenv("FLASK_SECRET_KEY", str(uuid4()))
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"
    SQLALCHEMY_ECHO = True

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_SUPPRESS_SEND = False

    MAIL_USERNAME = getenv("FLASK_MAIL_USERNAME")
    MAIL_PASSWORD = getenv("FLASK_MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = getenv("FLASK_MAIL_DEFAULT_SENDER")

    TWILIO_SEND_SMS = False

class TestingConfig:
    pass
