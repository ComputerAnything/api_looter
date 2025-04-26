from flask import Blueprint, render_template
from .models import APIModel

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    apis = APIModel.query.all()
    return render_template('index.html', apis=apis)
