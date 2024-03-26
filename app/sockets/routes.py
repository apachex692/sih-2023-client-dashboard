# Author: Sakthi Santhosh
# Created on: 20/03/2024
from random import choice as rchoice

from flask import current_app, url_for
from flask_socketio import Namespace, emit

from app import db_handle
from app.constants import EXTERNAL_URL_ROOT, RESPONDER_MAINTENANCE_SMS
from app.lights.models import Light
from app.responders.models import Responder
from app.utils import send_email, send_sms

class RTDataStream(Namespace):
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_data_ingress(self, data):
        print(data)
        action_delegator(data)
        emit("data_egress", data, broadcast=True)

def action_delegator(ingress_data: str) -> None: # <id>:<etype>,<id>:<etype>
    if not ingress_data:
        return

    components = ingress_data.split(',')

    for component in components:
        id, err_type = list(map(int, component.split(':')))
        light = Light.query.get(id)

        if not light or light.status_code == err_type:
            print('1')
            return

        light.status_code = err_type

        db_handle.session.commit()
        if err_type < 2:
            print('2')
            return

        non_working_responders = Responder.query.filter_by(
            area=light.area, is_working=False
        ).all()

        if not non_working_responders:
            print('3')
            return

        non_working_responder = rchoice(non_working_responders)

        maps_link = f"https://www.google.com/maps/place/{light.latitude},{light.longitude}"

        with current_app.test_request_context(EXTERNAL_URL_ROOT):
            ack_url = url_for(
                "responders.maintenance_confirm_handle",
                light=light.id,
                responder=non_working_responder.id,
                _external=True
            )
            comptd_url = url_for(
                "responders.maintenance_comptd_handle",
                light=light.id,
                responder=non_working_responder.id,
                _external=True
            )

        print(component, ack_url)
        send_email(
            subject="Sussy Bakas - Maintenance Required",
            message=open(
                "./app/templates/responders/email_maintenance.html", 'r',
                encoding="utf-8"
            ).read()%(maps_link, ack_url, comptd_url),
            recipients=[non_working_responder.email_id]
        )
        send_sms(
            message=RESPONDER_MAINTENANCE_SMS%(maps_link, ack_url, comptd_url),
            recipient=non_working_responder.phone
        )
        db_handle.session.commit()
