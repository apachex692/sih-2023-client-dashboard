# Author: Sakthi Santhosh
# Created on: 16/10/2023
from flask import Blueprint, render_template

tickets_bp_handle = Blueprint("tickets", __name__)

@tickets_bp_handle.route('/')
def index_handle():
    return render_template("/tickets/index.html")
