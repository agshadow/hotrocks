import os
import tempfile

import pytest
from hotrocks import create_app
from hotrocks.db import initialise_db_and_create_tables, populate_user

# from db_test_data import populate_test_data

# from flaskr import create_app
# from flaskr.db import get_db, init_db

# with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
#    _data_sql = f.read().decode("utf8")


@pytest.fixture
def app():
    # make a temp file file descriptor and path.
    db_fd, db_path = tempfile.mkstemp()

    # sest the testing True and database path in the app.
    app = create_app(
        {
            "TESTING": True,
            "DATABASE": db_path,
        }
    )
    # create database and tables
    initialise_db_and_create_tables()
    # populate tables
    populate_user
    # populate_test_data()
    print("populated user")
    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


"""class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)"""
