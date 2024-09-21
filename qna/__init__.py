from flask import Blueprint

qna_bp = Blueprint('qna', __name__)

from . import routes
