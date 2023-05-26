from flask import Flask
import os
from sqlmodel import Session, select
from dotenv import load_dotenv
from hotrocks.db import engine, create_tables, populate_user
from hotrocks.models import User
from hotrocks.extensions import mail


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # set the secret key and the path /instance/hotrocks.sqlite in the app
    app.config.from_mapping(
        SECRET_KEY="devaa", DATABASE=os.path.join(app.instance_path, "hotrocks.sqlite")
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        # not sure if this is working.
        print("trying to load from pyfile")
        print("app root path: ", app.root_path)
        filename = os.path.join(app.root_path, "config.py")
        print("file name", filename)
        with open(filename, mode="rb") as config_file:
            print(config_file.read())
        app.config.from_pyfile("config.py", silent=True)
    else:
        # when its testing, update the DATABASE attribute to the app.
        print("loading from test config: ", test_config)
        app.config.update(test_config)

    print("secret key \n ---------: ", app.secret_key)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initalise the database create the database
    print("DATABASE: ", app.config["DATABASE"])
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
    from . import shiftsummary

    app.register_blueprint(order.bp)
    app.register_blueprint(shiftsummary.bp)
    app.add_url_rule("/", endpoint="index")

    return app


def create_db_tables():
    create_tables()
