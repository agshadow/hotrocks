from flask import Blueprint, render_template

bp = Blueprint("order", __name__)


@bp.route("/")
def index():
    return render_template("order/index.html")
