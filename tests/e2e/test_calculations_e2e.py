# tests/e2e/test_calculations_e2e.py
import time

from playwright.sync_api import Page

BASE_URL = "http://localhost:8000"


def unique_email(prefix: str) -> str:
    return f"{prefix}_{int(time.time() * 1000)}@example.com"


def _register_via_ui(page: Page, email: str, password: str, username: str) -> None:
    page.goto(f"{BASE_URL}/register-page")
    page.fill("#username", username)
    page.fill("#email", email)
    page.fill("#password", password)
    page.click("text=Register")
    page.wait_for_timeout(800)


def _login_via_ui(page: Page, email: str, password: str) -> None:
    page.goto(f"{BASE_URL}/login-page")
    page.fill("#email", email)
    page.fill("#password", password)
    page.click("text=Login")
    page.wait_for_timeout(800)
    # Just ensure we get some success text
    success_text = page.text_content("#success") or ""
    assert "Login successful" in success_text


def test_calculation_bread_happy_path(page: Page) -> None:
    email = unique_email("calc")
    password = "CalcPassword123"
    username = "calcuser"

    # Register and login using the existing auth pages
    _register_via_ui(page, email, password, username)
    _login_via_ui(page, email, password)

    # Go to calculations page
    page.goto(f"{BASE_URL}/calculations-page")

    # If your login flow stores user_id in localStorage, the Detect button can fill this.
    # For now, we explicitly type owner id = 1 (first user in a fresh DB).
    page.fill("#owner-id", "1")

    # Create a calculation a=10, b=5, type=add
    page.fill("#a", "10")
    page.fill("#b", "5")
    page.select_option("#type", "add")
    page.click("#btn-create")
    page.wait_for_timeout(800)

    msg = page.text_content("#message") or ""
    assert "Created calculation ID" in msg

    # Browse calculations
    page.click("#btn-browse")
    page.wait_for_timeout(800)

    table_text = page.text_content("#calc-tbody") or ""
    assert "10" in table_text
    assert "5" in table_text
    assert "add" in table_text
