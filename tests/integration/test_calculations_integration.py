def register_user(client):
    payload = {
        "username": "calcuser",
        "email": "calc@example.com",
        "password": "CalcPass123"
    }
    resp = client.post("/users/register", json=payload)
    assert resp.status_code in (200, 201)
    return resp.json()["id"]


def test_calculation_crud(client):
    user_id = register_user(client)

    # Create
    create_payload = {"a": 10, "b": 5, "type": "add"}
    resp = client.post(f"/calculations/?owner_id={user_id}", json=create_payload)
    assert resp.status_code in (200, 201)
    created = resp.json()
    calc_id = created["id"]
    assert created["result"] == 15

    # Browse
    resp = client.get("/calculations/")
    assert resp.status_code == 200
    assert any(c["id"] == calc_id for c in resp.json())

    # Read
    resp = client.get(f"/calculations/{calc_id}")
    assert resp.status_code == 200

    # Delete
    resp = client.delete(f"/calculations/{calc_id}")
    assert resp.status_code == 200

    # Ensure deleted
    resp = client.get(f"/calculations/{calc_id}")
    assert resp.status_code == 404


def test_invalid_calculation_type(client):
    user_id = register_user(client)

    payload = {"a": 1, "b": 2, "type": "invalid"}
    resp = client.post(f"/calculations/?owner_id={user_id}", json=payload)

    assert resp.status_code >= 400
