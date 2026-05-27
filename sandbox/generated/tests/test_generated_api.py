from fastapi.testclient import TestClient
from sandbox.generated.generated_api import app

client = TestClient(app)

def test_login_success():
    response = client.post(
        "/login",
        data={"username": "user@example.com", "password": "password123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_failure_wrong_password():
    response = client.post(
        "/login",
        data={"username": "user@example.com", "password": "wrongpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_get_me_success():
    # Obtain token first
    login_res = client.post(
        "/login",
        data={"username": "user@example.com", "password": "password123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = login_res.json()["access_token"]
    
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "user@example.com"

def test_get_me_unauthorized():
    response = client.get("/users/me")
    assert response.status_code == 401

def test_get_me_invalid_token():
    response = client.get(
        "/users/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401