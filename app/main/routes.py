# Author: Sakthi Santhosh
# Created on: 16/10/2023
from flask import Blueprint, render_template
import folium

from app.constants import LIGHT_STATUS_CODE, MAP_LIGHT_MARKER_POPUP_TEMPLATE
from app.lights.models import Light

main_bp_handle = Blueprint("main", __name__)

@main_bp_handle.route('/')
def index_handle():
    map_obj = folium.Map([13.099334672659834, 80.15614658500027], zoom_start=100)

    for light in Light.query.all():
        folium.Marker(
            [light.latitude, light.longitude],
            popup=MAP_LIGHT_MARKER_POPUP_TEMPLATE%(
                light.id,
                light.latitude,
                light.longitude,
                light.status_code
            ),
            icon=folium.Icon(
                **LIGHT_STATUS_CODE[light.status_code],
                prefix="fa" # font-awesome
            )
        ).add_to(map_obj)

    map_obj.get_root().width = "100%"
    map_obj.get_root().height = "500px"
    iframe = map_obj.get_root()._repr_html_()

    return render_template("/main/index.html", map_iframe=iframe)

@main_bp_handle.route("/about")
def about_handle():
    return render_template("/main/about.html")

@main_bp_handle.route("/test/socket")
def testsocket_handle():
    return render_template("/main/testsocket.html")
