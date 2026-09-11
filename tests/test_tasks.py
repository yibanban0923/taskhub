from fastapi.testclient import TestClient


def test_task_crud(client: TestClient, auth_headers: dict[str, str]):
    created = client.post(
        "/api/v1/tasks",
        headers=auth_headers,
        json={"title": "Learn FastAPI", "priority": "high"},
    )
    assert created.status_code == 201
    task_id = created.json()["id"]

    fetched = client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert fetched.status_code == 200
    assert fetched.json()["title"] == "Learn FastAPI"

    updated = client.patch(
        f"/api/v1/tasks/{task_id}",
        headers=auth_headers,
        json={"status": "done"},
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "done"

    deleted = client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert deleted.status_code == 204
    assert client.get(
        f"/api/v1/tasks/{task_id}",
        headers=auth_headers,
    ).status_code == 404


def test_filter_and_pagination(
    client: TestClient,
    auth_headers: dict[str, str],
):
    for i in range(5):
        client.post(
            "/api/v1/tasks",
            headers=auth_headers,
            json={
                "title": f"Python task {i}",
                "priority": "high" if i % 2 == 0 else "low",
            },
        )

    response = client.get(
        "/api/v1/tasks?priority=high&keyword=Python&page=1&page_size=2",
        headers=auth_headers,
    )
    body = response.json()

    assert response.status_code == 200
    assert body["total"] == 3
    assert len(body["items"]) == 2


def test_user_cannot_access_another_users_task(client: TestClient):
    def register_and_login(username: str, email: str) -> dict[str, str]:
        client.post(
            "/api/v1/auth/register",
            json={
                "username": username,
                "email": email,
                "password": "password123",
            },
        )
        login = client.post(
            "/api/v1/auth/login",
            data={
                "username": username,
                "password": "password123",
            },
        )
        return {"Authorization": f"Bearer {login.json()['access_token']}"}

    alice = register_and_login("alice2", "alice2@example.com")
    bob = register_and_login("bob2", "bob2@example.com")

    task = client.post(
        "/api/v1/tasks",
        headers=alice,
        json={"title": "Alice secret"},
    )
    task_id = task.json()["id"]

    assert client.get(
        f"/api/v1/tasks/{task_id}",
        headers=bob,
    ).status_code == 404

    assert client.patch(
        f"/api/v1/tasks/{task_id}",
        headers=bob,
        json={"title": "hack"},
    ).status_code == 404

    assert client.delete(
        f"/api/v1/tasks/{task_id}",
        headers=bob,
    ).status_code == 404


def test_task_update_rejects_null_required_fields(
    client: TestClient,
    auth_headers: dict[str, str],
):
    created = client.post(
        "/api/v1/tasks",
        headers=auth_headers,
        json={
            "title": "Null validation test",
            "status": "todo",
            "priority": "medium",
        },
    )
    assert created.status_code == 201
    task_id = created.json()["id"]

    for field_name in ("title", "status", "priority"):
        response = client.patch(
            f"/api/v1/tasks/{task_id}",
            headers=auth_headers,
            json={field_name: None},
        )
        assert response.status_code == 422

    optional_fields = client.patch(
        f"/api/v1/tasks/{task_id}",
        headers=auth_headers,
        json={
            "description": None,
            "due_date": None,
        },
    )
    assert optional_fields.status_code == 200
