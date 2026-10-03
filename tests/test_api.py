import uuid


def create_user(client):
    random_email = uuid.uuid4()
    response = client.post(
        "/users/register",
        json={"name": "Bobby", "email": str(random_email), "password": "526710239"}
    )
    return response, response.json()["id"], response.json()["email"], "526710239" 

def test_create_user(client):
    response, user_id, email, password = create_user(client)
    assert response.status_code == 201
    assert "id" in response.json() and response.json()["email"] == email

def test_create_note(client):
    response, user_id, email, password = create_user(client)

    response = client.post(
        "/users/login",
        json={"email": email, "password": password}
    )
    assert response.status_code == 200
    access_token = response.json()["access_token"]

    response = client.post(
        "/notes/add_note",
        headers={f"Authorization": f"Bearer {access_token}"},
        json={"text": "Сделать API"}
    )

    assert response.status_code == 201
    assert response.json()["user_id"] == user_id and response.json()["text"] == "Сделать API"

def test_note_unauthorized(client):
    response = client.post(
        "/notes/add_note",
        headers={f"Authorization": f"Bearer g9uiefgiufsdgdfbygdfbngfduib"},
        json={"text": "Сделать API"}
        )
    assert response.status_code == 401


def test_not_found(client):
    response, user_id, email, password = create_user(client)

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

def test_existing_user(client):
    response1, user_id, email, password = create_user(client)
    assert response1.status_code == 201

    response2 = client.post(
        "/users/register",
        json={"name": "Bobby", "email": email, "password": password}
    )
    assert response2.status_code == 409


def test_filter(client):

    response1, user_id, email, password = create_user(client)
    assert response1.status_code == 201

    
    response = client.post(
        "/users/login",
        json={"email": email, "password": password}
    )
    assert response.status_code == 200
    access_token = response.json()["access_token"]

    response = client.post(
        "/notes/add_note",
        headers={f"Authorization": f"Bearer {access_token}"},
        json={"text": "Сделать API1"}
    )
    assert response.status_code == 201
    assert response.json()["user_id"] == user_id and response.json()["text"] == "Сделать API1"

    response = client.post(
        "/notes/add_note",
        headers={f"Authorization": f"Bearer {access_token}"},
        json={"text": "Сделать API2"}
    )
    
    assert response.status_code == 201
    assert response.json()["user_id"] == user_id and response.json()["text"] == "Сделать API2"
    

    response = client.get(
        "/notes/",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"filter": "API"}
    )
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["text"] == "Сделать API1"
    assert response.json()[1]["text"] == "Сделать API2"

    response = client.get(
        "/notes/",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"filter": "API1"}
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["text"] == "Сделать API1"




def test_edit_note(client):
    
    response, user_id, email, password = create_user(client)
    
    assert response.status_code == 201

    response = client.post(
        "/users/login",
        json={"email": email, "password": password} 
    )
    assert response.status_code == 200
    access_token = response.json()["access_token"]

    response = client.post(
        "/notes/add_note",
        headers={f"Authorization": f"Bearer {access_token}"},
        json={"text": "Сделать API"}
    )

    note_id = response.json()["id"]

    assert response.status_code == 201
    assert response.json()["user_id"] == user_id and response.json()["text"] == "Сделать API"

    response = client.patch(
        f"/notes/{note_id}",
        headers={f"Authorization": f"Bearer {access_token}"},
        json={"text": "Сделать API +++"}
    )


    assert response.status_code == 200
    assert response.json()["text"] == "Сделать API +++"
    

    response = client.patch(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"is_done": True}
    )
    assert response.status_code == 200
    assert response.json()["is_done"] == True

def test_delete_note(client):
    response, user_id, email, password = create_user(client)

    
    response = client.post(
        "/users/login",
        json={"email": email, "password": password}
    )
    assert response.status_code == 200
    access_token = response.json()["access_token"]

    response = client.post(
        "/notes/add_note",
        headers={f"Authorization": f"Bearer {access_token}"},
        json={"text": "Сделать API"}
    )

    note_id = response.json()["id"]
    assert response.status_code == 201
    assert response.json()["user_id"] == user_id and response.json()["text"] == "Сделать API"

    response = client.delete(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 204

    response = client.get(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 404

def test_foreign_note(client):
    response1, user_id, email, password = create_user(client)
    assert response1.status_code == 201

    response2, user_id2, email2, password2 = create_user(client)
    assert response2.status_code == 201

    response = client.post(
        "/users/login",
        json={"email": email, "password": password}
    )
    assert response.status_code == 200
    access_token = response.json()["access_token"]

    response = client.post(
        "/notes/add_note",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"text":"Сделать API"}
    )

    note_id = response.json()["id"]
    assert response.status_code == 201
    assert response.json()["user_id"] == user_id and response.json()["text"] == "Сделать API"

    response = client.post(
        "/users/login",
        json={"email": email2, "password": password2}
    )
    assert response.status_code == 200
    access_token2 = response.json()["access_token"]

    response = client.get(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {access_token2}"}
    )
    assert response.status_code == 404

