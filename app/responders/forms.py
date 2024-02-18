# Author: Sakthi Santhosh
# Created on: 16/10/2023
from flask_wtf import FlaskForm
from wtforms import EmailField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError

from app.auth.models import User
from app.constants import (
    AREA_FORM_CHOICES,
    EMAIL_ID_EXIST_MESSAGE,
    INVALID_PHONE_FORMAT,
    PREFERRED_LANGUAGE_FORM_CHOICES
)
from app.responders.models import Responder

class CreateResponderForm(FlaskForm):
    first_name = StringField(
        label="First Name",
        validators=[DataRequired(), Length(max=32)]
    )
    last_name = StringField(
        label="Last Name",
        validators=[Length(max=32)]
    )
    email_id = EmailField(
        label="Email ID",
        validators=[DataRequired(), Length(max=256)]
    )
    phone = StringField(
        label="Phone #",
        validators=[
            DataRequired(),
            Length(min=10, max=10),
            Regexp(regex="^[0-9]+$", message=INVALID_PHONE_FORMAT)
        ]
    )
    area = SelectField(
        label="Work Area",
        choices=AREA_FORM_CHOICES,
        validators=[DataRequired()]
    )
    preferred_language = SelectField(
        label="Preferred Language",
        choices=PREFERRED_LANGUAGE_FORM_CHOICES,
        validators=[DataRequired()]
    )
    submit = SubmitField(
        label="Create Responder"
    )

    def validate_email_id(self, email_id):
        if (
            User.query.filter_by(_email_id=email_id.data).first()
            or Responder.query.filter_by(_email_id=email_id.data).first()
        ):
            raise ValidationError(EMAIL_ID_EXIST_MESSAGE)
