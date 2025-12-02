# tests/e2e/test_auth_e2e.py
import time
import httpx

BASE_URL = "http://localhost:8000"


def unique_email(prefix: str) -> str:
    return f"{prefix}_{int(time.time() * 1000)}@example.com"


def test_register_success(page):
    email = unique_email("play_reg")
    page.goto(f"{BASE_URL}/register-page")

    page.fill("#username", "playuser")
    page.fill("#email", email)
    page.fill("#password", "LongPassword123")

    page.click("text=Register")

    page.wait_for_timeout(1000)
    assert "Registration successful" in page.text_content("#success")


def test_register_short_password_client_error(page):
    page.goto(f"{BASE_URL}/register-page")

    page.fill("#username", "shortpass")
    page.fill("#email", unique_email("short"))
    page.fill("#password", "123")  # too short

    page.click("text=Register")

    page.wait_for_timeout(500)
    assert "Password must be at least 8 characters" in page.text_content("#error")


def _ensure_user_exists(email: str, password: str):
    # Call backend API directly to register user if not already there
    with httpx.Client(base_url=BASE_URL) as client:
        resp = client.post(
            "/users/register",
            json={
                "username": "loginuser",
                "email": email,
                "password": password,
            },
        )
        # 201 created or 400 email already registered are both fine
        if resp.status_code not in (201, 400):
            raise RuntimeError(f"Unexpected status creating user: {resp.status_code}")


def test_login_success(page):
    email = unique_email("play_login")
    password = "ValidPassword123"
    _ensure_user_exists(email, password)

    page.goto(f"{BASE_URL}/login-page")

    page.fill("#email", email)
    page.fill("#password", password)
    page.click("text=Login")

    page.wait_for_timeout(1000)

    success_text = page.text_content("#success")
    assert "Login successful" in success_text

    # Token stored in localStorage
    token = page.evaluate("() => window.localStorage.getItem('access_token')")
    assert token is not None
    assert len(token) > 10


def test_login_wrong_password(page):
    email = unique_email("play_wrong")
    correct_password = "CorrectPassword123"
    wrong_password = "WrongPassword123"

    _ensure_user_exists(email, correct_password)

    page.goto(f"{BASE_URL}/login-page")

    page.fill("#email", email)
    page.fill("#password", wrong_password)
    page.click("text=Login")

    page.wait_for_timeout(1000)
    assert "Invalid credentials" in page.text_content("#error")
