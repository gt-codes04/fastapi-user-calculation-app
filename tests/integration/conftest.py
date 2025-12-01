import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base, get_db, DATABASE_URL
from app.main import app

# Prefer TEST_DATABASE_URL (used in GitHub Actions)
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", DATABASE_URL)

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False} if TEST_DATABASE_URL.startswith("sqlite") else {},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables for testing
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    return TestClient(app)
