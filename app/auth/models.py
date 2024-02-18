# Author: Sakthi Santhosh
# Created on: 16/10/2023
from flask import current_app
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer

from app import db_handle, lm_handle

@lm_handle.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db_handle.Model, UserMixin):
    id = db_handle.Column(
        db_handle.Integer(),
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
    _password = db_handle.Column(
        db_handle.String(60),
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

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, plain_password):
        self._password = generate_password_hash(plain_password)

    def check_password(self, plain_password):
        return check_password_hash(self._password, plain_password)

    def generate_token(self):
        serializer = Serializer(current_app.config["SECRET_KEY"])

        return serializer.dumps({"user_id": self.id})

    @staticmethod
    def verify_token(token, expiration_s=300):
        serializer = Serializer(current_app.config["SECRET_KEY"])

        try:
            user_id = serializer.loads(token, max_age=expiration_s)["user_id"]
        except Exception:
            return None
        else:
            return user_id

    def __repr__(self):
        return f"<{self.full_name} ({self.email_id})>"
