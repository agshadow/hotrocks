from flask import Blueprint, render_template


from hotrocks.auth import login_required


bp = Blueprint("shiftsummary", __name__)


@bp.route("/shiftsummary/", methods=("GET", "POST"))
@login_required
def shiftsummary_index():
    return render_template("shiftsummary/index.html")


@bp.route("/new_shiftsummary/", methods=("GET", "POST"))
@login_required
def new_shiftsummary():
    return render_template("shiftsummary/index.html")
