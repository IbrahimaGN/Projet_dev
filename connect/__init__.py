from flask import Blueprint

connect_bp = Blueprint('connect', __name__)

from . import routes