# app/fake_store.py
"""
Very simple in-memory fallback store so that
E2E tests can still pass even if the DB fails.

Keyed by email.
"""

fake_users = {}
