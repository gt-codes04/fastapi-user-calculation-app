def test_register_user(client):
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPass123"
    }

    resp = client.post("/users/register", json=payload)
    assert resp.status_code in (200, 201)

    data = resp.json()
    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]
    assert "id" in data


def test_login_success(client):
    # Register first
    reg_payload = {
        "username": "loginuser",
        "email": "login@example.com",
        "password": "LoginPass123"
    }
    client.post("/users/register", json=reg_payload)

    # Login
    login_payload = {
        "username": "loginuser",
        "email": "login@example.com",
        "password": "LoginPass123"
    }
    resp = client.post("/users/login", json=login_payload)
    assert resp.status_code == 200

    data = resp.json()
    assert data["message"] == "Login successful"
    assert "user_id" in data


def test_login_failure(client):
    payload = {
        "username": "nouser",
        "email": "no@example.com",
        "password": "WrongPass"
    }

    resp = client.post("/users/login", json=payload)
    assert resp.status_code == 401
