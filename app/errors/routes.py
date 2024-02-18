# Author: Sakthi Santhosh
# Created on: 18/10/2023
from flask import render_template

def page_not_found_handle(error):
    return render_template(
        "/error.html",
        title="404 Not Found",
        message=error
    ), 404

def forbidden_handle(error):
    return render_template(
        "/error.html",
        title="403 Forbidden",
        message=error
    ), 403

def internal_server_error_handle(error):
    return render_template(
        "/error.html",
        title="500 Internal Server Error",
        message=error
    ), 500
