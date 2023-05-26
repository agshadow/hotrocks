from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_mail import Message
import os
from sqlmodel import Session, select, col

from hotrocks.auth import login_required
from hotrocks.extensions import mail
from hotrocks.mapping import job_title_list, get_job_mapping
from hotrocks.db import engine, save_job_record
from hotrocks.models import Job
from hotrocks.shiftsummary import shiftsummary_index

bp = Blueprint("order", __name__)


@bp.route("/")
# @login_required
def index():
    return render_template("order/index.html")


@bp.route("/input_new_job", methods=["GET", "POST"])
@login_required
def input_new_job():
    if request.method == "POST":
        with Session(engine) as sqlsession:
            sqlsession.add(Job(**request.form.to_dict(flat=True)))
            sqlsession.commit()

        flash("Saved record")
        return redirect(url_for("index"))
    else:
        return render_template(
            "order/input_new_job.html",
            headings=job_title_list,
            db_headings=get_job_mapping(),
        )


@bp.route("/get_saved_jobs")
@login_required
def get_saved_jobs():
    with Session(engine) as sqlsession:
        statement = select(Job)
        results = sqlsession.exec(statement).all()
    loadedJobData = []
    for result in results:
        print("result:", result.dict())
        loadedJobData.append(result.dict())
    # loadedJobData = []
    # loadedJobData = loadJobData()
    # print(loadedJobData)
    # for i in loadedJobData:
    #    print(i["CREW:"])
    #    print(i["CREW MANAGER/PE"])

    # print("calling db---------------")
    # get_all_job_orders()

    print("loaded job data: ", loadedJobData)
    # loadedJobData = {"CREW:": "Jeff", "CREW MANAGER/PE": "Julian"}
    return render_template("order/get_saved_jobs.html", jobData=loadedJobData)


@bp.route("/review_and_submit", methods=["GET", "POST"])
@login_required
def review_and_submit():
    if request.method == "POST":
        # todo save the message again
        job = Job(**request.form.to_dict(flat=True))
        savedJob = save_job_record(job)
        flash("Saved record")

        # set up email address
        emailaddr = request.form.get("emailaddr")
        msg = Message(
            f"{savedJob.crew} - {savedJob.date} - {savedJob.job_name}",
            sender=os.environ.get("emailUsername"),
            recipients=[emailaddr],
        )

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
        mail.send(msg)

        return render_template("order/email_send_result.html", result="Success")

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
            return redirect(url_for("order.index"))

        # get data from database for id = key
        with Session(engine) as sqlsession:
            statement = select(Job).where(col(Job.id) == key)
            results = sqlsession.exec(statement).first()
            results_dict = results.dict()
        print("email: ", os.environ.get("emailUsername"))
        return render_template(
            "order/review_and_submit.html",
            jobData=results_dict,
            headings=job_title_list,
            db_headings=get_job_mapping(),
            # default_email_address="poop",
            default_email_address=os.environ.get("emailUsername"),
        )


@bp.route("/save_record", methods=["GET", "POST"])
@login_required
def save_record():
    print("SAVING RECORD \n --------")
    if request.method == "POST":
        job = Job(**request.form.to_dict(flat=True))
        save_job_record(job)

        flash("Saved record")
        return render_template("order/index.html")
