# tests/integration/test_reports_integration.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_reports_summary_requires_auth():
    """
    Basic integration test to confirm the /reports/summary route exists
    and is protected by authentication.
    """
    resp = client.get("/reports/summary")
    # Depending on your auth implementation, this may be 401 or 403.
    assert resp.status_code in (401, 403)

