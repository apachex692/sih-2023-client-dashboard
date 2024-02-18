# Author: Sakthi Santhosh
# Created on: 16/10/2023
from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError

from app.auth.models import User
from app.constants import PASSWORD_MISMATCH_MESSAGE, EMAIL_ID_NONEXIST_MESSAGE

class LoginForm(FlaskForm):
    email_id = EmailField(
        label="Email ID",
        validators=[DataRequired(), Length(max=256)]
    )
    password = PasswordField(
        label="Password",
        validators=[DataRequired(), Length(min=8, max=72)]
    )
    remember_me = BooleanField(
        label="Remember Me"
    )
    submit = SubmitField(
        label="Log-in"
    )

class ForgotPasswordForm(FlaskForm):
    email_id = EmailField(
        label="Email ID",
        validators=[DataRequired(), Length(max=256)]
    )
    submit = SubmitField(
        label="Send Password Reset Email"
    )

    def validate_email_id(self, email_id):
        if User.query.filter_by(_email_id=email_id.data).first() is None:
            raise ValidationError(EMAIL_ID_NONEXIST_MESSAGE)

class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        label="Password",
        validators=[DataRequired(), Length(min=8, max=72)]
    )
    confirm_password = PasswordField(
        label="Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message=PASSWORD_MISMATCH_MESSAGE),
            Length(min=8, max=72)
        ]
    )
    submit = SubmitField(
        label="Reset Password"
    )
