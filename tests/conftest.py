from pathlib import Path

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env.test", override=True)

import app.models
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.main import app

if settings.MYSQL_DATABASE != "taskhub_test":
    raise RuntimeError(
        f"Tests must use taskhub_test, current database is {settings.MYSQL_DATABASE!r}"
    )


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client() -> TestClient: # type: ignore
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def auth_headers(client: TestClient) -> dict[str, str]:
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "password123",
        },
    )
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "alice", "password": "password123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
