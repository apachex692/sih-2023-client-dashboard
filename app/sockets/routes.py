# Author: Sakthi Santhosh
# Created on: 20/03/2024
from flask_socketio import Namespace, emit

class RTDataStream(Namespace):
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_data_ingress(self, data):
        print("Ingress:", data)
        emit("data_egress", data, broadcast=True)
