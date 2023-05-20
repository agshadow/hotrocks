from flask import Blueprint, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from hotrocks.auth import login_required
from hotrocks.extensions import mail

bp = Blueprint("order", __name__)


@bp.route("/")
# @login_required
def index():
    return render_template("order/index.html")


@bp.route("/input_new_job", methods=["GET", "POST"])
@login_required
def input_new_job():
    # get current job from post method.
    currentJob = {}
    if request.method == "POST":
        for i in request.form:
            # print (i, " : ", request.form[i])
            currentJob[i] = request.form[i]
            # get the key

        # TODO  *****Implement saveCurrentJob(currentJob)

        # TODO flash message Saved
        return redirect(url_for("index"))
    else:
        # headingsList = loadHeadings()
        # TODO headings list
        headingsList = ("heading1", "heading2")
        return render_template("order/input_new_job.html", headings=headingsList)


@bp.route("/get_saved_jobs")
@login_required
def get_saved_jobs():
    # loadedJobData = []
    # loadedJobData = loadJobData()
    # print(loadedJobData)
    # for i in loadedJobData:
    #    print(i["CREW:"])
    #    print(i["CREW MANAGER/PE"])

    # print("calling db---------------")
    # get_all_job_orders()

    # print(loadedJobData)
    loadedJobData = {"CREW:": "Jeff", "CREW MANAGER/PE": "Julian"}
    return render_template("order/get_saved_jobs.html", jobData=loadedJobData)


@bp.route("/review_and_submit", methods=["GET", "POST"])
@login_required
def review_and_submit():
    if request.method == "POST":
        print(request.form["KEY:"])
        # todo save the message again
        print("SAVED")

        # TODO  Save the record
        # TODO  send email
        crew = request.form.get("CREW:")
        date = request.form.get("DATE:")
        job = request.form.get("JOB NAME:")
        print(f"{crew} - {date} - {job}")
        emailaddr = request.form.get("emailaddr")
        msg = Message(
            f"{crew} - {date} - {job}",
            sender="AFAApp2023@gmail.com",
            recipients=[emailaddr],
        )
        # format the message

        # headingsList = loadHeadings()
        messageBody = "<table>"
        # for heading in headingsList:
        #    messageBody += (
        #        f"<tr><td>{heading}</td><td> {request.form.get(heading)}\n</td></tr>"
        #    )

        messageBody += "</table>"
        print(messageBody)

        msg.html = messageBody
        mail.send(msg)

        return render_template("order/email_send_result.html", result="Success")

    else:
        # url is: /ques/?idd=ABC
        key = request.args.get("key", default="", type=int)
        # TODO create method to get entry from JSON from the key
        job = 1

        # print("job:", job)
        # headingsList = loadHeadings()
        headingsList = ("heading1", "heading2")
        return render_template(
            "order/review_and_submit.html", jobData=job, headings=headingsList
        )
