from flask import Flask
from waitress import serve
import os


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev", DATABASE=os.path.join(app.instance_path, "hotrocks.sqlite")
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

    # from . import db
    # db.init_db()
    # db.init_app(app)

    from . import auth

    app.register_blueprint(auth.bp)

    from . import order

    app.register_blueprint(order.bp)
    app.add_url_rule("/", endpoint="index")

    return app


if __name__ == "__main__":
    app = create_app()
    serve(app, listen="*:80")
