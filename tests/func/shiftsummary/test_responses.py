def test_shiftsummary_index(client, app):
    response = client.get("/shiftsummary/")
    assert response.status_code == 302
    assert b"Redirecting" in response.data


def test_new_shift_summary(client, app):
    response = client.get("/new_shiftsummary/")
    assert response.status_code == 404
    assert b"404" in response.data


def test_input_new_job(client, app):
    response = client.get("/input_new_job")
    assert response.status_code == 302
    assert b"Input New Job" in response.data
