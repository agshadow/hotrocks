import functools
from flask import (
    Blueprint,
    render_template,
    request,
    url_for,
    redirect,
    flash,
    session,
    g,
)
from .models import User
from sqlmodel import Session, select, col
from .db import engine
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                user = User(
                    username=username, password=generate_password_hash(password)
                )
                with Session(engine) as sqlsession:
                    sqlsession.add(user)
                    sqlsession.commit()
            except Exception:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None
        results = None
        with Session(engine) as sqlsession:
            statement = select(User).where(col(User.username) == username)
            results = sqlsession.exec(statement).first()

        try:
            if results is None:
                error = "Incorrect username."
                print(error)
            elif not check_password_hash(results.password, password):
                error = "Incorrect password."
                print(error)
        except Exception:
            pass

        if error is None:
            session.clear()
            session["user_id"] = results.id
            print("my id:", results.id)
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        with Session(engine) as sqlsession:
            statement = select(User).where(col(User.id) == user_id)
            results = sqlsession.exec(statement).first()
            print(results.id)
            g.user = results.id


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
