from hotrocks import create_app


def test_1plus1():
    assert 1 == 1


def test_config():
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


'''def test_hello(client):
    response = client.get("/hello")
    assert response.data == b"Hello, World!"'''
