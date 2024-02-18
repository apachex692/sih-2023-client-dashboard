# Author: Sakthi Santhosh
# Created on: 16/10/2023
from os import getenv

class DeploymentConfig:
    pass

class DevelopmentConfig:
    SECRET_KEY = "bb57ede9-6bcd-434b-b9d8-3b45ad3ff251"
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

class TestingConfig:
    pass
