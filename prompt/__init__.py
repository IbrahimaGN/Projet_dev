from flask import Blueprint

prompt_bp = Blueprint('prompt', __name__)

from . import routes



