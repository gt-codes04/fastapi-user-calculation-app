# tests/integration/test_calculations_integration.py

from fastapi.testclient import TestClient

from app.main import app
from app.auth import get_current_user

client = TestClient(app)


class DummyUser:
    """
    Minimal user object for dependency override.
    Only needs an `id` attribute because calculations are
    associated with a user_id / owner_id.
    """
    def __init__(self, user_id: int):
        self.id = user_id


def override_get_current_user():
    # We don't care if this user actually exists in the DB for this test.
    # In SQLite, foreign key constraints are typically not enforced unless enabled.
    return DummyUser(user_id=1)


def test_calculation_crud():
    """
    Full BREAD integration test for /calculations using a dependency override
    for authentication and verifying the new 'pow' operation.
    """
    # Override auth for this test so routes think we're logged in
    app.dependency_overrides[get_current_user] = override_get_current_user

    try:
        # --------------------
        # ADD (Create)
        # --------------------
        create_payload = {"a": 10, "b": 5, "type": "add"}
        resp = client.post("/calculations/", json=create_payload)
        assert resp.status_code in (200, 201)

        created = resp.json()
        calc_id = created["id"]
        assert created["a"] == 10
        assert created["b"] == 5
        assert created["type"] == "add"
        assert created["result"] == 15

        # --------------------
        # BROWSE (List)
        # --------------------
        resp = client.get("/calculations/")
        assert resp.status_code == 200
        items = resp.json()
        assert any(c["id"] == calc_id for c in items)

        # --------------------
        # READ (Get by ID)
        # --------------------
        resp = client.get(f"/calculations/{calc_id}")
        assert resp.status_code == 200
        got = resp.json()
        assert got["id"] == calc_id
        assert got["result"] == 15

        # --------------------
        # EDIT (Update with pow)
        # change operation to pow and b to 2 → 10^2 = 100
        # --------------------
        update_payload = {"type": "pow", "b": 2}
        resp = client.patch(f"/calculations/{calc_id}", json=update_payload)
        assert resp.status_code == 200
        updated = resp.json()
        assert updated["type"] == "pow"
        assert updated["b"] == 2
        assert updated["result"] == 10 ** 2  # 100

        # --------------------
        # DELETE
        # --------------------
        resp = client.delete(f"/calculations/{calc_id}")
        assert resp.status_code == 200
        assert resp.json().get("detail") in ("Deleted", "Calculation deleted")

        # Verify it is really gone
        resp = client.get(f"/calculations/{calc_id}")
        assert resp.status_code == 404

    finally:
        # Clean up override so it doesn't affect other tests
        app.dependency_overrides.pop(get_current_user, None)
