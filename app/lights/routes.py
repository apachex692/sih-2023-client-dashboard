# Author: Sakthi Santhosh
# Created on: 16/10/2023
from flask import (
    abort,
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for
)
from flask_login import login_required

from app import db_handle
from app.constants import (
    LIGHT_DEREGISTERED_SUCCESS_MESSAGE,
    LIGHT_REGISTERED_SUCCESS_MESSAGE,
    LIGHT_UPDATED_SUCCESS_MESSAGE
)
from app.lights.forms import RegisterStreetLightForm
from app.lights.models import Light

lights_bp_handle = Blueprint("lights", __name__)

@lights_bp_handle.route('/')
@login_required
def index_handle():
    lights = Light.query.paginate(
        page=request.args.get("page", 1, type=int),
        per_page=request.args.get("per_page", 10, type=int),
        max_per_page=100
    )

    return render_template("/lights/index.html", lights=lights)

@lights_bp_handle.route("/create", methods=["GET", "POST"])
@login_required
def register_handle():
    form = RegisterStreetLightForm()

    if form.validate_on_submit():
        light = Light()

        form.populate_obj(obj=light)
        db_handle.session.add(light)
        db_handle.session.commit()

        flash(LIGHT_REGISTERED_SUCCESS_MESSAGE, "success")
        return redirect(url_for("lights.index_handle"))
    return render_template("/lights/register.html", form=form)

@lights_bp_handle.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_handle(id):
    light = Light.query.get(id)

    if light is None:
        abort(404)

    form = RegisterStreetLightForm(obj=light if request.method == "GET" else None)

    if request.method == "POST":
        light.automation_type = request.form.get("automation_type", None)

        db_handle.session.add(light)
        db_handle.session.commit()
        flash(LIGHT_UPDATED_SUCCESS_MESSAGE, "success")
        return redirect(url_for("lights.index_handle"))
    return render_template("/lights/update.html", form=form)

# FIXME: CSRF
@lights_bp_handle.route("/deregister/<int:id>")
@login_required
def deregister_handle(id):
    light = Light.query.get(id)

    if light is None:
        abort(404)

    db_handle.session.delete(light)
    db_handle.session.commit()
    flash(LIGHT_DEREGISTERED_SUCCESS_MESSAGE, "success")
    return redirect(url_for("lights.index_handle"))
