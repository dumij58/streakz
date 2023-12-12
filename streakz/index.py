from flask import (
    Blueprint, render_template
)
from datetime import date


bp = Blueprint('index', __name__, url_prefix='/')


@bp.route('/')
def index():
    d = date.today().day
    days = [f"{day:0>2d}" for day in range(d, d-7, -1)]
    return render_template("index/index.html", days=days)