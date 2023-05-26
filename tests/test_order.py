import pytest


def test_index(client):
    response = client.get("/")
    print(response.status_code)
    assert b"Log In" in response.data
    assert b"Register" in response.data
    assert response.status_code == 200


def test_get_saved_jobs(client, app):
    # print("inside testing")
    assert client.get("/get_saved_jobs").status_code == 302
