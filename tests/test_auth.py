from fastapi.testclient import TestClient


def test_register_login_and_me(client: TestClient):
    register = client.post(
        "/api/v1/auth/register",
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "password123",
        },
    )
    assert register.status_code == 201
    assert register.json()["email"] == "bob@example.com"

    login = client.post(
        "/api/v1/auth/login",
        data={"username": "bob", "password": "password123"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    me = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me.status_code == 200
    assert me.json()["username"] == "bob"


def test_duplicate_email_returns_409(client: TestClient):
    payload = {
        "username": "user1",
        "email": "same@example.com",
        "password": "password123",
    }
    assert client.post("/api/v1/auth/register", json=payload).status_code == 201
    payload["username"] = "user2"
    assert client.post("/api/v1/auth/register", json=payload).status_code == 409


def test_wrong_password_returns_401(client: TestClient):
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "charlie",
            "email": "charlie@example.com",
            "password": "password123",
        },
    )
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "charlie", "password": "wrong-password"},
    )
    assert response.status_code == 401


def test_me_requires_token(client: TestClient):
    assert client.get("/api/v1/users/me").status_code == 401
