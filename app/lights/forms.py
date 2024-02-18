# Author: Sakthi Santhosh
# Created on: 16/10/2023
from flask_wtf import FlaskForm
from wtforms.fields import FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

from app.constants import AREA_FORM_CHOICES, LIGHT_AUTOMATION_TYPE_FORM_CHOICES

class RegisterStreetLightForm(FlaskForm):
    area = SelectField(
        label="Area",
        choices=AREA_FORM_CHOICES,
        validators=[DataRequired()]
    )
    automation_type = SelectField(
        label="Automation Type",
        choices=LIGHT_AUTOMATION_TYPE_FORM_CHOICES,
        validators=[DataRequired()]
    )
    longitude = FloatField(
        label="Longitude",
        validators=[DataRequired(), NumberRange(min=-180, max=180)]
    )
    latitude = FloatField(
        label="Latitude",
        validators=[DataRequired(), NumberRange(min=-90, max=90)]
    )
    submit = SubmitField(
        label="Register Street Light"
    )
