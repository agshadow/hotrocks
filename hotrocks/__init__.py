from flask import Flask
import os
from sqlmodel import Session, select
from dotenv import load_dotenv
from hotrocks.db import engine, create_tables, populate_user
from flask_mail import Mail, Message
from hotrocks.models import User
from hotrocks.extensions import mail


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev", DATABASE=os.path.join(app.instance_path, "flaskr.sqlite")
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        load_dotenv()

    # create the database
    create_tables()

    # check if data exists in database, and populate it
    result = None
    with Session(engine) as session:
        stmt = select(User)
        result = session.exec(stmt).first()

    if result is None:
        print("populating")
        populate_user()
    else:
        print("data already loded")

    # need .env file with the username and password
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USERNAME"] = os.environ.get("emailUsername")
    app.config["MAIL_PASSWORD"] = os.environ.get("emailPassword")
    app.config["MAIL_USE_SSL"] = True
    app.config["MAIL_USE_TLS"] = False

    mail.init_app(app)

    # a simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    from . import auth

    app.register_blueprint(auth.bp)

    from . import order

    app.register_blueprint(order.bp)
    app.add_url_rule("/", endpoint="index")

    return app


def create_db_tables():
    create_tables()
