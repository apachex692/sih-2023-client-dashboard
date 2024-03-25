# Author: Sakthi Santhosh
# Created on: 16/10/2023
from flask import Blueprint, render_template
from flask_login import login_required
import folium
from sqlalchemy import func

from app.constants import LIGHT_STATUS_CODE, MAP_LIGHT_MARKER_POPUP_TEMPLATE
from app.lights.models import Light
from app.responders.models import Responder

main_bp_handle = Blueprint("main", __name__)

@main_bp_handle.route('/')
@login_required
def index_handle():
    map_obj = folium.Map([13.099334672659834, 80.15614658500027], zoom_start=100)

    for light in Light.query.all():
        folium.Marker(
            [light.latitude, light.longitude],
            popup=folium.Popup(MAP_LIGHT_MARKER_POPUP_TEMPLATE%(
                light.id,
                light.latitude,
                light.longitude,
                LIGHT_STATUS_CODE[light.status_code]["disp"]
            ), max_width=400),
            icon=folium.Icon(
                **LIGHT_STATUS_CODE[light.status_code],
                prefix="fa" # font-awesome
            )
        ).add_to(map_obj)

    map_obj.get_root().width = "100%"
    map_obj.get_root().height = "500px"
    iframe = map_obj.get_root()._repr_html_()

    light_stats = {
        "active": Light.query.with_entities(
            func.count()).filter(Light.status_code == 0
        ).scalar(),
        "under_maintenance": Light.query.with_entities(
            func.count()).filter(Light.status_code == 1
        ).scalar(),
        "inactive": Light.query.with_entities(
            func.count()).filter(Light.status_code == 3
        ).scalar(),
    }
    responder_stats = {
        "total": Responder.query.count()
    }

    return render_template(
        "/main/index.html",
        map_iframe=iframe,
        light_stats=light_stats,
        responder_stats=responder_stats
    )

@main_bp_handle.route("/about")
def about_handle():
    return render_template("/main/about.html")

@main_bp_handle.route("/test/socket")
def testsocket_handle():
    return render_template("/main/testsocket.html")
