import pytest


def test_index(client):
    response = client.get("/")
    assert b"Log In" in response.data
    assert b"Register" in response.data
