# Author: Sakthi Santhosh
# Created on: 16/10/2023
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

from app.config import (
    DeploymentConfig,
    DevelopmentConfig,
    TestingConfig
)
from app.constants import (
    LOGIN_VIEW_HANDLER,
    LOGIN_MESSAGE,
    LOGIN_MESSAGE_CATEGORY,
    SERIAL_PORT
)

db_handle = SQLAlchemy()
lm_handle = LoginManager()
mail_handle = Mail()
socketio_handle = SocketIO()


lm_handle.login_view = LOGIN_VIEW_HANDLER
lm_handle.login_message = LOGIN_MESSAGE
lm_handle.login_message_category = LOGIN_MESSAGE_CATEGORY

def create_app(config: str=None):
    assert isinstance(config, str)

    if config == "development":
        config = DevelopmentConfig
    elif config == "testing":
        config = TestingConfig
    elif config == "deployment":
        config = DeploymentConfig

    app_handle = Flask(__name__)

    app_handle.config.from_object(obj=config)
    db_handle.init_app(app_handle)
    lm_handle.init_app(app_handle)
    mail_handle.init_app(app_handle)
    socketio_handle.init_app(app_handle)

    from app.auth.routes import auth_bp_handle
    from app.lights.routes import lights_bp_handle
    from app.main.routes import main_bp_handle
    from app.responders.routes import responders_bp_handle
    from app.tickets.routes import tickets_bp_handle

    app_handle.register_blueprint(auth_bp_handle, url_prefix="/auth")
    app_handle.register_blueprint(lights_bp_handle, url_prefix="/lights")
    app_handle.register_blueprint(main_bp_handle)
    app_handle.register_blueprint(responders_bp_handle, url_prefix="/responders")
    app_handle.register_blueprint(tickets_bp_handle, url_prefix="/tickets")

    from app.sockets.routes import RTDataStream
    #from app.utils import SerialToSocketDaemon

    socketio_handle.on_namespace(RTDataStream("/rtdatastream"))
    #SerialToSocketDaemon(SERIAL_PORT).start()

    import app.errors.routes as error_handler

    app_handle.register_error_handler(404, error_handler.page_not_found_handle)
    app_handle.register_error_handler(403, error_handler.forbidden_handle)
    app_handle.register_error_handler(500, error_handler.internal_server_error_handle)

    from app.auth.models import User

    return app_handle
