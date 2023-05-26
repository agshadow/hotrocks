import pytest
from flask import g, session


def test_register(client, app):
    assert client.get("/auth/register").status_code == 200
    response = client.post("/auth/register", data={"username": "a", "password": "a"})
    assert response.headers["Location"] == "/auth/login"


def test_login(client, app):
    assert client.get("/auth/login").status_code == 200
    response = client.post(
        "/auth/login", data={"username": "Test", "password": "Password"}
    )
    assert response.headers["Location"] == "/"


def test_login_fail(client, app):
    response = client.post(
        "/auth/login", data={"username": "Test", "password": "Password1"}
    )
    assert response.headers["Location"] == "/auth/login"
