# Author: Sakthi Santhosh
# Created on: 16/10/2023
from datetime import datetime

from app import db_handle

class Light(db_handle.Model):
    id = db_handle.Column(
        db_handle.Integer,
        primary_key=True
    )
    area = db_handle.Column(
        db_handle.String(32),
        nullable=False,
        unique=False
    )
    status_code = db_handle.Column(
        db_handle.Integer,
        default=0,
        nullable=False,
        unique=False
    )
    automation_type = db_handle.Column(
        db_handle.Integer,
        nullable=True,
        unique=False
    )
    latitude = db_handle.Column(
        db_handle.Float,
        unique=False,
        nullable=False
    )
    longitude = db_handle.Column(
        db_handle.Float,
        unique=False,
        nullable=False
    )
    last_maintenance = db_handle.Column(
        db_handle.DateTime,
        default=datetime.now,
        nullable=False,
        unique=False
    )

    def __repr__(self):
        return f"<{self.id} ({self.status_code})>"
