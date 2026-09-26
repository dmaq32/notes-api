from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)


def create_user():
    random_email = uuid.uuid4()
    response = client.post(
        "/users/register",
        json={"name": "Bobby", "email": str(random_email), "password": "526710239"}
    )
    return response, response.json()["id"], response.json()["email"], "526710239" 

def test_create_user():
    response, user_id, email, password = create_user()
    assert response.status_code == 201
    assert "id" in response.json() and response.json()["email"] == email

def test_create_note():
    response, user_id, email, password = create_user()

    response = client.post(
        "/users/login",
        json={"email": email, "password": password}
    )
    access_token = response.json()["access_token"]

    response = client.post(
        "/notes/add_note",
        headers={f"Authorization": f"Bearer {access_token}"},
        json={"text": "Сделать API"}
    )

    assert response.status_code == 201
    assert response.json()["user_id"] == user_id and response.json()["text"] == "Сделать API"

def test_note_unauthorized():
    response = client.post(
        "/notes/add_note",
        headers={f"Authorization": f"Bearer g9uiefgiufsdgdfbygdfbngfduib"},
        json={"text": "Сделать API"}
        )
    assert response.status_code == 401


def test_not_found():
    response, user_id, email, password = create_user()

    response = client.post(
            "/users/login",
            json={"email": email, "password": password}
        )
    access_token = response.json()["access_token"]

    response = client.get(
        "/notes/999999",
        headers={"Authorization": f"Bearer {access_token}"},
        )
    assert response.status_code == 404