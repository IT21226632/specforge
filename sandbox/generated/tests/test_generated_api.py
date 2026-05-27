from fastapi.testclient import TestClient
from sandbox.generated.generated_api import app

client = TestClient(app)

def test_login_success():
    response = client.post(
        "/auth/login",
        data={"username": "user@example.com", "password": "securepassword123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_password():
    response = client.post(
        "/auth/login",
        data={"username": "user@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_login_nonexistent_user():
    response = client.post(
        "/auth/login",
        data={"username": "nonexistent@example.com", "password": "securepassword123"}
    )
    assert response.status_code == 401

def test_login_invalid_email_format():
    # OAuth2PasswordRequestForm expects username/password in form-data
    response = client.post(
        "/auth/login",
        data={"username": "not-an-email", "password": "securepassword123"}
    )
    assert response.status_code == 401

def test_login_missing_fields():
    response = client.post("/auth/login", data={})
    # OAuth2PasswordRequestForm requires username and password
    assert response.status_code == 422