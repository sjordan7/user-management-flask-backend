def test_signup(client):
    response = client.post("/api/signup", json={
        "username": "testuser",
        "email": "test@email.com",
        "password": "123456"
    })

    assert response.status_code == 201


def test_login(client):
    # First create user
    client.post("/api/signup", json={
        "username": "testuser",
        "email": "test@email.com",
        "password": "123456"
    })

    # Then login
    response = client.post("/api/login", json={
        "email": "test@email.com",
        "password": "123456"
    })

    data = response.get_json()

    assert response.status_code == 200
    assert "access_token" in data


def test_invalid_login(client):
    response = client.post("/api/login", json={
        "email": "wrong@email.com",
        "password": "wrong"
    })

    assert response.status_code == 404


def test_protected_route(client):
    # Signup + login
    client.post("/api/signup", json={
        "username": "test",
        "email": "test@email.com",
        "password": "123456"
    })

    login = client.post("/api/login", json={
        "email": "test@email.com",
        "password": "123456"
    })

    token = login.get_json()["access_token"]

    # Call protected route
    response = client.get(
        "/api/users",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
