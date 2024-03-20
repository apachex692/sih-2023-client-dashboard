# Author: Sakthi Santhosh
# Created on: 16/10/2023
from flask import Blueprint, render_template

main_bp_handle = Blueprint("main", __name__)

@main_bp_handle.route('/')
def index_handle():
    return render_template("/main/index.html")

@main_bp_handle.route("/about")
def about_handle():
    return render_template("/main/about.html")

@main_bp_handle.route("/test/socket")
def testsocket_handle():
    return render_template("/main/testsocket.html")
