from flask import Blueprint, render_template

from sqlmodel import Session, select
from hotrocks.db import engine

from hotrocks.auth import login_required
from hotrocks.models import ShiftSummary, ShiftSummaryLog


bp = Blueprint("shiftsummary", __name__)


@bp.route("/shiftsummary/", methods=("GET", "POST"))
@login_required
def shiftsummary_index():
    return render_template("shiftsummary/index.html")


@bp.route("/new_shiftsummary/", methods=("GET", "POST"))
@login_required
def new_shiftsummary():
    return render_template("shiftsummary/index.html")


@bp.route("/shiftsummary/list/", methods=("GET", "POST"))
@login_required
def shiftsummary_list():
    # select all from database
    with Session(engine) as sqlsession:
        statement = select(ShiftSummary)
        results = sqlsession.exec(statement).all()
    shiftsummaries = []
    for result in results:
        print("result:", result.dict())
        shiftsummaries.append(result.dict())

    print("shift summary data: ", shiftsummaries)
    # return to template
    return render_template("shiftsummary/list.html", items=shiftsummaries)
