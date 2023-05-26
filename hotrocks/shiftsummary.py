from flask import Blueprint, render_template, request, redirect, flash, url_for

from sqlmodel import Session, select, col
from hotrocks.db import engine, save_log_record, add_log

from hotrocks.auth import login_required
from hotrocks.models import ShiftSummary, ShiftSummaryLog
from datetime import datetime

bp = Blueprint("shiftsummary", __name__)


@bp.route("/shiftsummary/", methods=("GET", "POST"))
@login_required
def shiftsummary_index():
    return render_template("shiftsummary/index.html")


@bp.route("/new_shiftsummary/", methods=("GET", "POST"))
@login_required
def new_shiftsummary():
    return render_template("shiftsummary/index.html")


@bp.route("/shiftsummary/review_item", methods=("GET", "POST"))
@login_required
def review_item():
    if request.method == "POST":
        pass
    else:
        # url is: review_and_submit?key=7
        key = request.args.get("key", default="", type=int)
        error = None

        if not key:
            error = "No record specified"
            print("error no record")

        if error is not None:
            flash(error)
            print("redirecting)")
            return redirect(url_for("shiftsummary.shiftsummary_index"))

        # get data from database for id = key
        with Session(engine) as sqlsession:
            statement = select(ShiftSummary).where(col(ShiftSummary.id) == key)
            results = sqlsession.exec(statement).first()
            results_dict = results.dict()
            statement = select(ShiftSummaryLog).where(
                col(ShiftSummaryLog.shiftsummaryid) == key
            )
            results = sqlsession.exec(statement).all()
            logs = []
            for result in results:
                print("shift summary log:", result.dict())
                logs.append(result.dict())
        return render_template(
            "shiftsummary/review_item.html", item=results_dict, shiftsummarylogs=logs
        )


@bp.route("/shiftsummary/editlog", methods=("GET", "POST"))
@login_required
def editlog():
    if request.method == "POST":
        shiftsummarylog = ShiftSummaryLog(**request.form.to_dict(flat=True))

        shiftsummarylog = save_log_record(shiftsummarylog)
        print("shift summary log: ", shiftsummarylog, shiftsummarylog.shiftsummaryid)
        flash("Saved record")
        return redirect(
            url_for("shiftsummary.review_item", key=shiftsummarylog.shiftsummaryid)
        )
    else:
        # url is: review_and_submit?key=7
        key = request.args.get("key", default="", type=int)
        error = None

        if not key:
            error = "No record specified"
            print("error no record")

        if error is not None:
            flash(error)
            print("redirecting)")
            return redirect(url_for("shiftsummary.shiftsummary_index"))

        # get data from database for id = key
        with Session(engine) as sqlsession:
            statement = select(ShiftSummaryLog).where(col(ShiftSummaryLog.id) == key)
            results = sqlsession.exec(statement).first()
            results_dict = results.dict()

        print("log results:", results_dict)
        return render_template("shiftsummary/editlog.html", log=results_dict)


@bp.route("/shiftsummary/addlog", methods=("GET", "POST"))
@login_required
def addlog():
    if request.method == "POST":
        print("--------------------------------")
        print("inside addlog")
        print("--------------------------------")
        shiftsummarylog = ShiftSummaryLog(**request.form.to_dict(flat=True))

        print(
            "shift summary log: \n ------------------ ",
            shiftsummarylog,
            shiftsummarylog.shiftsummaryid,
        )
        shiftsummarylog = add_log(shiftsummarylog)
        print(
            "shift summary log: \n ------------------ ",
            shiftsummarylog,
            shiftsummarylog.shiftsummaryid,
        )
        flash("Saved record")
        return redirect(
            url_for("shiftsummary.review_item", key=shiftsummarylog.shiftsummaryid)
        )
    else:
        # url is: review_and_submit?key=7
        key = request.args.get("key", default="", type=int)
        error = None

        if not key:
            error = "No record specified"
            print("error no record")

        if error is not None:
            flash(error)
            print("redirecting)")
            return redirect(url_for("shiftsummary.shiftsummary_index"))

        # we should validate the key.
        date = datetime.now()
        print("date:", date, " key: ", key)
        return render_template(
            "shiftsummary/addlog.html", shiftsummaryid=key, date=date
        )


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
