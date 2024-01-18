from flask import Blueprint, render_template, request, redirect, flash, url_for

from sqlmodel import Session, select, col
from hotrocks.db import (
    engine,
    save_log_record,
    add_log,
    add_new_shiftsummary,
    get_shift_summary_by_key,
)

from hotrocks.auth import login_required
from hotrocks.models import ShiftSummary, ShiftSummaryLog
from datetime import datetime, date
from flask_mail import Message
import dateutil.parser

from hotrocks.extensions import mail

bp = Blueprint("shiftsummary", __name__)


@bp.route("/shiftsummary/", methods=("GET", "POST"))
@login_required
def shiftsummary_index():
    return render_template("shiftsummary/index.html")


@bp.route("/shiftsummary/new", methods=("GET", "POST"))
@login_required
def new():
    if request.method == "POST":
        shiftsummary = ShiftSummary(**request.form.to_dict(flat=True))
        print(shiftsummary)

        shiftsummary.date = dateutil.parser.parse(
            request.form.get("date"), dayfirst=True
        )
        print(f"{shiftsummary.date=}")
        add_new_shiftsummary(shiftsummary)
        return redirect(url_for("shiftsummary.shiftsummary_list"))
    else:
        return render_template(
            "shiftsummary/new.html",
            todaysDate=f"{date.strftime(date.today(), '%d/%m/%Y')}",
        )


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
            return redirect(url_for("shiftsummary.shiftsummary_list"))

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

            print("_____ SORTING")
            print(logs)
            logs = sorted(logs, key=lambda d: d["date"], reverse=False)
            print(logs)
        return render_template(
            "shiftsummary/review_item.html",
            item=results_dict,
            shiftsummarylogs=logs,
            default_email_address="AFAAPP2023@gmail.com",
        )


@bp.route("/shiftsummary/editlog", methods=("GET", "POST"))
@login_required
def editlog():
    if request.method == "POST":
        shiftsummarylog = ShiftSummaryLog.load_form(request.form.to_dict(flat=True))
        print("EDIT LOG: ssl: ", shiftsummarylog)
        # shiftsummarylog = add_log(shiftsummarylog)

        """shiftsummarylog = ShiftSummaryLog(**request.form.to_dict(flat=True))

        # if date is not entered in isoformat, it will need to be parsed
        shiftsummarylog.date = dateutil.parser.parse(request.form.get("date"), dayfirst=True)"""

        shiftsummarylog = save_log_record(shiftsummarylog)
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
        # read in shiftsummarylog from form
        # shiftsummarylog = ShiftSummaryLog(**request.form.to_dict(flat=True))
        # if date is not entered in isoformat, it will need to be parsed
        # shiftsummarylog.date = dateutil.parser.parse(request.form.get("date"), dayfirst=True)
        # save shift summary log
        shiftsummarylog = ShiftSummaryLog.load_form(request.form.to_dict(flat=True))
        print("ADD LOG: ssl: ", shiftsummarylog)
        shiftsummarylog = add_log(shiftsummarylog)

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
    return render_template(
        "shiftsummary/list.html",
        items=shiftsummaries,
    )


@bp.route("/shiftsummary/email_summary", methods=["GET", "POST"])
@login_required
def email_summary():
    if request.method == "POST":
        """
        # if nightshift then add Nightshif to title.
        if savedJob.shift.lower() == "night" or savedJob.shift.lower() == "nightshift":
            msg.subject = (
                f"{savedJob.crew} - Nightshift -  {savedJob.date} - {savedJob.job_name}"
            )
        # format the message

        messageBody = "<table>"
        db_headings = get_job_mapping()
        for heading in job_title_list:
            if db_headings[heading] == "id":
                pass
            elif db_headings[heading] == "date":
                messageBody += f"<tr><td>DATE:</td><td> {savedJob.dict()[db_headings[heading]]}\n</td></tr>"
            else:
                messageBody += f"<tr><td>{heading}</td><td> {savedJob.dict()[db_headings[heading]]}\n</td></tr>"

        messageBody += "</table>"
        print(messageBody)

        msg.html = messageBody
        mail.send(msg)"""

        print("INSIDE email_summary")
        key = request.form.get("key", default="", type=int)

        emailaddr = request.form.get("emailaddr")
        print(f"{key=}")
        print(f"{emailaddr=}")
        shiftsummarytuple = get_shift_summary_by_key(key)
        print(f"{shiftsummarytuple=}")
        shiftsummary, shiftsummarylog = shiftsummarytuple

        # load shift summary log
        # set up email address
        emailaddr = request.form.get("emailaddr")
        msg = Message(
            "Shift Summary : ",
            # {shiftsummary.date} - {shiftsummary.location} - {shiftsummary.shift}",
            # sender=os.environ.get("emailUsername"),
            sender="AFAAPP2023@gmail.com",
            recipients=[emailaddr],
        )

        messageBody = f"<table><tr><td>Date:</td<td>{shiftsummary['date']}</td></tr>"
        messageBody += f"<tr><td>Job:</td<td>{shiftsummary['location']}</td></tr>"
        messageBody += f"<tr><td>Shift:</td<td>{shiftsummary['shift']}</td></tr>"
        messageBody += f"<tr><td>Forecast:</td<td>{shiftsummary['forecast']}</td></tr>"
        messageBody += f"<tr><td>Location:</td<td>{shiftsummary['scope']}</td></tr>"
        messageBody += f"</table>"
        messageBody += f"<table>"
        for i in shiftsummarylog:
            messageBody += f"<tr><td>{datetime.strftime(i['date'], '%d/%m/%Y %H:%M')}</td><td>{i['data']}</td></tr>"
        messageBody += f"</table>"

        msg.html = messageBody
        mail.send(msg)

        return render_template("shiftsummary/email_send_result.html", result="Success")

    else:
        # url is: review_and_submit?key=7
        """key = request.args.get("key", default="", type=int)
        error = None

        if not key:
            error = "No record specified"
            print("error no record")

        if error is not None:
            flash(error)
            print("redirecting)")
            return redirect(url_for("order.index"))

        # get data from database for id = key
        with Session(engine) as sqlsession:
            statement = select(Job).where(col(Job.id) == key)
            results = sqlsession.exec(statement).first()
            results_dict = results.dict()
        return render_template(
            "order/review_and_submit.html",
            jobData=results_dict,
            headings=job_title_list,
            db_headings=get_job_mapping(),
            default_email_address="AFAAPP2023@gmail.com",
        )"""
        return render_template("shiftsummary/index.html")
