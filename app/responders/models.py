# Author: Sakthi Santhosh
# Created on: 16/10/2023
from flask import current_app
from itsdangerous import URLSafeTimedSerializer as Serializer

from app import db_handle

class Responder(db_handle.Model):
    id = db_handle.Column(
        db_handle.Integer,
        primary_key=True
    )
    first_name = db_handle.Column(
        db_handle.String(32),
        nullable=False,
        unique=False
    )
    last_name = db_handle.Column(
        db_handle.String(32),
        nullable=True,
        unique=False
    )
    _email_id = db_handle.Column(
        db_handle.String(256),
        nullable=False,
        unique=True
    )
    phone = db_handle.Column(
        db_handle.String(10),
        nullable=False,
        unique=True
    )
    area = db_handle.Column(
        db_handle.String(32),
        nullable=False,
        unique=False
    )
    preferred_language = db_handle.Column(
        db_handle.String(10),
        default="English",
        nullable=False,
        unique=False
    )
    is_working = db_handle.Column(
        db_handle.Boolean,
        default=False,
        nullable=False,
        unique=False
    )
    email_verified = db_handle.Column(
        db_handle.Boolean,
        default=False,
        nullable=False,
        unique=False
    )
    phone_verified = db_handle.Column(
        db_handle.Boolean,
        default=False,
        nullable=False,
        unique=False
    )

    @property
    def full_name(self):
        return self.first_name + (' ' + self.last_name if self.last_name else '')

    @property
    def email_id(self):
        return self._email_id

    @email_id.setter
    def email_id(self, email_id):
        self._email_id = email_id.lower()

    def generate_token(self, identity):
        serializer = Serializer(current_app.config["SECRET_KEY"])

        return serializer.dumps({
            "user_id": self.id,
            "identity": identity
        })

    @staticmethod
    def verify_token(token, expiration_s=300):
        serializer = Serializer(current_app.config["SECRET_KEY"])

        try:
            payload = serializer.loads(token, max_age=expiration_s)
        except Exception:
            return None
        else:
            return payload

    def __repr__(self):
        return f"<{self.full_name} ({self.email_id})>"
