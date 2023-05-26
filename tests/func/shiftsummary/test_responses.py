def test_shiftsummary_index(client, app):
    response = client.get("/shiftsummary/")
    assert response.status_code == 302
    assert b"SHIFT SUMMARY" in response.data


def test_new_shift_summary(client, app):
    response = client.get("/new_shiftsummary/")
    assert response.status_code == 302
    assert b"SHIFT SUMMARY" in response.data
