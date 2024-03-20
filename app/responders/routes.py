# Author: Sakthi Santhosh
# Created on: 16/10/2023
from flask import (
    abort,
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for
)
from flask_login import current_user, login_required

from app import db_handle
from app.auth.models import User
from app.constants import (
    EXTERNAL_URL_ROOT,
    INVALID_TOKEN_MESSAGE,
    RESPONDER_CREATION_SUCCESS_MESSAGE,
    RESPONDER_DELETION_SUCCESS_MESSAGE,
    RESPONDER_PHONE_VERIFICATION_SMS
)
from app.responders.forms import CreateResponderForm
from app.responders.models import Responder
from app.utils import send_email, send_sms

responders_bp_handle = Blueprint("responders", __name__)

# FIXME: CSRF
@responders_bp_handle.route('/')
@login_required
def index_handle():
    filter_by = request.args.get("filter_by", '')
    query = request.args.get("query", '')

    if filter_by == '' or query == '' or current_user.is_authenticated is False:
        query_object = Responder.query
    else:
        if filter_by == "first_name":
            query_object = Responder.query.filter(
                Responder.first_name.like(f"%{query}%")
            )
        elif filter_by == "last_name":
            query_object = Responder.query.filter(
                Responder.last_name.like(f"%{query}%")
            )
        elif filter_by == "email_id":
            query_object = Responder.query.filter(
                Responder._email_id.like(f"%{query}%")
            )
        elif filter_by == "phone":
            query_object = Responder.query.filter(
                Responder.phone.like(f"%{query}%")
            )
        elif filter_by == "area":
            query_object = Responder.query.filter_by(
                area=query
            )
        elif filter_by == "preferred_language":
            query_object = Responder.query.filter_by(
                preferred_language=query
            )
        elif filter_by == "is_working":
            query_object = Responder.query.filter_by(
                is_working=(query == '1')
            )
        else:
            abort(404)

    responders = query_object.paginate(
        page=request.args.get("page", 1, type=int),
        per_page=request.args.get("per_page", 10, type=int),
        max_per_page=100
    )
    return render_template("/responders/index.html", responders=responders)

@responders_bp_handle.route("/api")
@login_required
def api_get_query_set():
    query_set = request.args.get("query_set")

    if query_set == "area":
        data = Responder.query.with_entities(Responder.area).distinct()
    elif query_set == "preferred_language":
        data = Responder.query.with_entities(Responder.preferred_language).distinct()
    else:
        abort(404)

    return jsonify({
        "data": [datum[0] for datum in data]
    }), 200

@responders_bp_handle.route("/create", methods=["GET", "POST"])
@login_required
def create_handle():
    form = CreateResponderForm()

    if form.validate_on_submit():
        responder = Responder()

        form.populate_obj(obj=responder)

        responder.phone_verified = not current_app.config.get("TWILIO_SEND_SMS", False)

        db_handle.session.add(responder)
        db_handle.session.commit()

        with current_app.test_request_context(EXTERNAL_URL_ROOT):
            email_url = url_for(
                "responders.verifydetails_handle",
                jwt=responder.generate_token(identity="email_id"),
                _external=True
            )
            sms_url = url_for(
                "responders.verifydetails_handle",
                jwt=responder.generate_token(identity="phone"),
                _external=True
            )

        send_email(
            subject="Sussy Bakas - Verify Details",
            message=open(
                "./app/templates/responders/email_verify.html", 'r',
                encoding="utf-8").read()%(
                    form.first_name.data + ' ' + form.last_name.data,
                    form.area.data,
                    form.preferred_language.data,
                    email_url
                ),
            recipients=[form.email_id.data]
        )
        send_sms(
            message=RESPONDER_PHONE_VERIFICATION_SMS%(sms_url),
            recipient=form.phone.data
        )
        flash(RESPONDER_CREATION_SUCCESS_MESSAGE, "success")
        return redirect(url_for("responders.index_handle"))
    return render_template("/responders/create.html", form=form)

@responders_bp_handle.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_handle(id):
    responder = Responder.query.get(id)

    if responder is None:
        abort(404)

    form = CreateResponderForm(obj=responder if request.method == "GET" else None)

    if request.method == "POST":
        check_user = User.query.filter_by(_email_id=form.email_id.data).first()
        check_email_responder = Responder.query.filter_by(_email_id=form.email_id.data).first()
        check_phone_responder = Responder.query.filter_by(phone=form.phone.data).first()

        if check_user is None:
            if check_email_responder is None or check_email_responder.id != id:
                responder.email_verified = False

                with current_app.test_request_context(EXTERNAL_URL_ROOT):
                    email_url = url_for(
                        "responders.verifydetails_handle",
                        jwt=responder.generate_token(identity="email_id"),
                        _external=True
                    )

                send_email(
                    subject="Sussy Bakas - Verify Details",
                    message=open(
                        "./app/templates/responders/email_verify.html", 'r',
                        encoding="utf-8").read()%(
                            form.first_name.data + ' ' + form.last_name.data,
                            form.area.data,
                            form.preferred_language.data,
                            email_url
                        ),
                    recipients=[form.email_id.data]
                )

            if check_phone_responder is None or check_phone_responder.id != id:
                responder.phone_verified = False

                with current_app.test_request_context(EXTERNAL_URL_ROOT):
                    sms_url = url_for(
                        "responders.verifydetails_handle",
                        jwt=responder.generate_token(identity="phone"),
                        _external=True
                    )
                send_sms(
                    message=RESPONDER_PHONE_VERIFICATION_SMS%(sms_url),
                    recipient=form.phone.data
                )

            form.populate_obj(obj=responder)

            db_handle.session.add(responder)
            db_handle.session.commit()
            flash(RESPONDER_CREATION_SUCCESS_MESSAGE, "success")
            return redirect(url_for(
                "responders.index_handle",
                filter_by="email_id",
                query=form.email_id.data
            ))
        else:
            pass # FIXME: flash()
    return render_template("/responders/update.html", form=form)

# FIXME: CSRF
@responders_bp_handle.route("/delete/<int:id>")
@login_required
def delete_handle(id):
    responder = Responder.query.get(id)

    if responder is None:
        abort(404)

    db_handle.session.delete(responder)
    db_handle.session.commit()
    flash(RESPONDER_DELETION_SUCCESS_MESSAGE%(responder.full_name), "success")
    return redirect(url_for("responders.index_handle"))

@responders_bp_handle.route("/verifydetails/<string:jwt>")
def verifydetails_handle(jwt):
    payload = Responder.verify_token(jwt)

    if payload is None:
        flash(INVALID_TOKEN_MESSAGE, "danger")
        return redirect(url_for("responders.index_handle"))

    responder = Responder.query.get(payload["user_id"])

    if payload["identity"] == "email_id" and not responder.email_verified:
        responder.email_verified = True
    elif payload["identity"] == "phone" and not responder.phone_verified:
        responder.phone_verified = True
    else:
        flash(INVALID_TOKEN_MESSAGE, "danger")
        return redirect("responders.index_handle")

    db_handle.session.add(responder)
    db_handle.session.commit()
    return render_template("/responders/verifydetails.html", identity=payload["identity"])
