import pytest
from flask import g, session


def test_register(client, app):
    assert client.get("/auth/register").status_code == 200
    response = client.post("/auth/register", data={"username": "a", "password": "a"})
    assert response.headers["Location"] == "/auth/login"


def test_login(client, app):
    assert client.get("/auth/login").status_code == 200
    response = client.post(
        "/auth/login", data={"username": "Admin", "password": "Julian1"}
    )
    assert response.headers["Location"] == "/"


"""def test_login2(client, auth):
    assert client.get("/auth/login").status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get("/")
        assert session["user_id"] == 1
        assert g.user["username"] == "test"
"""


"""@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("", "", b"Username is required."),
        ("Admin", "", b"Password is required."),
        ("Admin", "Julian1", b"already registered"),
    ),
)
def test_register_validate_input(client, username, password, message):
    response = client.post(
        "/auth/register", data={"username": username, "password": password}
    )
    assert message in response.data
"""

"""def test_login_fail(client, app):
    response = client.post(
        "/auth/login", data={"username": "Test", "password": "Password1"}
    )
    assert response.headers["Location"] == "/auth/login"
"""
