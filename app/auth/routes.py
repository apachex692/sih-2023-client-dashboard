# Author: Sakthi Santhosh
# Created on: 16/10/2023
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for
)
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from app import db_handle
from app.auth.forms import (
    ForgotPasswordForm,
    LoginForm,
    ResetPasswordForm
)
from app.auth.models import User
from app.constants import (
    EMAIL_ID_NONEXIST_MESSAGE,
    EXTERNAL_URL_ROOT,
    FORGOTPW_MAIL_SENT_MESSAGE,
    INVALID_TOKEN_MESSAGE,
    PASSWORD_MISMATCH_MESSAGE,
    RESETPW_SUCCESS_MESSAGE,
    USER_LOGGEDIN_MESSAGE
)
from app.utils import send_email

auth_bp_handle = Blueprint("auth", __name__)

@auth_bp_handle.route("/login", methods=["GET", "POST"])
def login_handle():
    if current_user.is_authenticated:
        return redirect(url_for("main.index_handle"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(_email_id=form.email_id.data).first()

        if not user:
            form.email_id.errors.append(EMAIL_ID_NONEXIST_MESSAGE)
        elif not user.check_password(form.password.data):
            form.password.errors.append(PASSWORD_MISMATCH_MESSAGE)
        else:
            redirect_to = request.args.get("next")

            login_user(
                user=user,
                remember=form.remember_me.data
            )
            flash(USER_LOGGEDIN_MESSAGE%(user.full_name), "success")
            return redirect(redirect_to) if redirect_to else redirect(url_for("main.index_handle"))
    return render_template("/auth/login.html", form=form)

@auth_bp_handle.route("/forgotpw", methods=["GET", "POST"])
def forgotpw_handle():
    if current_user.is_authenticated:
        return redirect(url_for("main.index_handle"))

    form = ForgotPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(_email_id=form.email_id.data).first()

        with current_app.test_request_context(EXTERNAL_URL_ROOT):
            url = url_for("auth.resetpw_handle", jwt=user.generate_token(), _external=True)

        send_email(
            subject="Sussy Bakas - Reset Password",
            message=open(
                "./app/templates/auth/email_resetpw.html", 'r',
                encoding="utf-8").read()%(
                    user.full_name,
                    url
                ),
            recipients=[user.email_id]
        )
        flash(FORGOTPW_MAIL_SENT_MESSAGE%(form.email_id.data), "success")
        return redirect(url_for("auth.login_handle"))
    return render_template("/auth/forgotpw.html", form=form)

@auth_bp_handle.route("/resetpw/<string:jwt>", methods=["GET", "POST"])
def resetpw_handle(jwt):
    if current_user.is_authenticated:
        return redirect(url_for("main.index_handle"))

    user_id = User.verify_token(token=jwt)

    if user_id is None:
        flash(INVALID_TOKEN_MESSAGE, "danger")
        return redirect(url_for("auth.login_handle"))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user = User.query.get(user_id)
        user.password = form.password.data

        db_handle.session.add(user)
        db_handle.session.commit()
        flash(RESETPW_SUCCESS_MESSAGE%(user.full_name), "success")
        return redirect(url_for("auth.login_handle"))
    return render_template("/auth/resetpw.html", form=form)

@auth_bp_handle.route("/logout")
def logout_handle():
    logout_user()
    return redirect(url_for("auth.login_handle"))
