# register/__init__.py

from flask import Blueprint
from .routes import *

register_bp = Blueprint('register', __name__, template_folder='templates')

# In the qna/__init__.py file, this blueprint is registered with the URL prefix `/auth`
