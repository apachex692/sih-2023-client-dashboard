# Author: Sakthi Santhosh
# Created on: 16/10/2023
SERIAL_PORT = "/dev/ttyUSB0"

LOGIN_VIEW_HANDLER = "auth.login_handle"
LOGIN_MESSAGE_CATEGORY = "warning"

EXTERNAL_URL_ROOT = "http://192.168.0.210:5000"

AREA_FORM_CHOICES = [
    "Avadi",
    "Ambattur",
    "Annanur",
    "Anna Nagar",
    "T. Nagar",
    "Mount Road"
]
PREFERRED_LANGUAGE_FORM_CHOICES = [
    "Tamil",
    "English",
    "Hindi",
    "Malayalam",
    "Telugu",
]
LIGHT_AUTOMATION_TYPE_FORM_CHOICES = [
    (0, None),
    (1, "Daylight-based"),
    (2, "Time-based")
]
LIGHT_STATUS_CODE = {
    0: {"color": "green", "icon": "thumbs-up"},
    1: {"color": "beige", "icon": "spinner"},
    2: {"color": "red", "icon": "down-long"}
}

MAP_LIGHT_MARKER_POPUP_TEMPLATE = """\
<b>ID:</b> %d
<br>
<b>Location:</b> (%f, %f)
<br>
<b>Status:</b> %d
<br>
"""

LOGIN_MESSAGE = "You must first log-in to access this page."

INVALID_PHONE_FORMAT = """\
The provided phone number is invalid. Phone number must contain only numbers.\
"""

EMAIL_ID_NONEXIST_MESSAGE = """\
The email ID does not exist. Please recheck your email ID or contact the administrator.\
"""
EMAIL_ID_EXIST_MESSAGE = "A responder with the email ID already exist."

PASSWORD_MISMATCH_MESSAGE = """\
It seems you've entered an incorrect password. Please double-check your password and try again.\
"""

USER_LOGGEDIN_MESSAGE = """\
Success, you've logged-in. Welcome aboard, %s! 🚀
"""

FORGOTPW_MAIL_SENT_MESSAGE = """\
An email with instructions to reset your password has been sent to email ID %s.
"""

INVALID_TOKEN_MESSAGE = """\
This link is either invalid or has expired. Regenerate a new token by following the necessary procedure.
"""

RESETPW_SUCCESS_MESSAGE = """\
Good job %s, your password has been reset successfully. You can now use the new password to log-in to the website.
"""

RESPONDER_CREATION_SUCCESS_MESSAGE = """\
A new responder has been added successfully. An email and SMS has been sent with links to verify them respectively. The link will be valid for one day.
"""

RESPONDER_DELETION_SUCCESS_MESSAGE = """\
The responder %s was deleted successfully.
"""

RESPONDER_PHONE_VERIFICATION_SMS = """Dear Lineman,
    You have been added to the database by our admins. We're sending this SMS to you to verify your details. Kindly check the details given below and if they're correct, click the link to confirm it. This link will be valid for only one day.

Verify Details Link: %s

Regards,
Team Sussy Bakas
"""

LIGHT_REGISTERED_SUCCESS_MESSAGE = """\
A new light has been successfully registered to the database.
"""

LIGHT_DEREGISTERED_SUCCESS_MESSAGE = """\
The light has been successfully deregistered from the database.
"""

LIGHT_UPDATED_SUCCESS_MESSAGE = """\
The automation type of the light is changed successfully.
"""
