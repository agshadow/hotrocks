from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from flask_mail import Message
import os
from sqlmodel import Session, select, col
import pprint

from hotrocks.auth import login_required
from hotrocks.extensions import mail
from hotrocks.mapping import job_title_list, get_job_mapping
from hotrocks.db import engine, save_job_record
from hotrocks.models import Job
from datetime import date

bp = Blueprint("order", __name__)


@bp.route("/")
# @login_required
def index():
    return render_template(
        "order/index.html",
    )


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
        print("---------------------------")
        print("result (all jobs):", result.dict())
        loadedJobData.append(result.dict())
    # loadedJobData = []
    # loadedJobData = loadJobData()
    # print(loadedJobData)
    # for i in loadedJobData:
    #    print(i["CREW:"])
    #    print(i["CREW MANAGER/PE"])

    # print("calling db---------------")
    # get_all_job_orders()

    print("sorted loaded job data: ")
    print("=================================================")
    loadedJobData = sorted(loadedJobData, key=lambda x: x["id"])
    pprint.pprint(loadedJobData)
    # loadedJobData = {"CREW:": "Jeff", "CREW MANAGER/PE": "Julian"}
    return render_template("order/get_saved_jobs.html", jobData=loadedJobData)


@bp.route("/duplicate_job")
@login_required
def duplicate_job():
    # url is: review_and_submit?key=7
    print("inside duplicate job")
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
    print("results dict duplicate: ", results_dict)
    # finish code to duplicate the item
    # #results_dict.pop("id")
    # print("results dict duplicate popped: ", results_dict)
    # job = Job(**results_dict)
    # newjob = save_job_record(job)
    # results_dict = newjob.dict()

    return render_template(
        "order/review_and_submit.html",
        jobData=results_dict,
        headings=job_title_list,
        db_headings=get_job_mapping(),
        default_email_address="AFAAPP2023@gmail.com",
    )


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
            f"{savedJob.crew} - {date.strftime(savedJob.date, '%a %d %b')} - {savedJob.job_name}",
            # sender=os.environ.get("emailUsername"),
            sender="AFAAPP2023@gmail.com",
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
                messageBody += f"<tr><td>DATE:</td><td> {date.strftime(savedJob.dict()[db_headings[heading]], '%a %d %b %Y ')}\n</td></tr>"
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
        return render_template(
            "order/review_and_submit.html",
            jobData=results_dict,
            headings=job_title_list,
            db_headings=get_job_mapping(),
            default_email_address="AFAAPP2023@gmail.com",
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
