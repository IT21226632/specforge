from fastapi.testclient import TestClient
from sandbox.generated.generated_api import app

client = TestClient(app)

def test_login_success():
    payload = {"email": "user@example.com", "password": "securepassword123"}
    response = client.post("/auth/login", json=payload)
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_password():
    payload = {"email": "user@example.com", "password": "wrongpassword"}
    response = client.post("/auth/login", json=payload)
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_login_nonexistent_user():
    payload = {"email": "notfound@example.com", "password": "password123"}
    response = client.post("/auth/login", json=payload)
    
    assert response.status_code == 401

def test_login_invalid_email_format():
    payload = {"email": "invalid-email", "password": "password123"}
    response = client.post("/auth/login", json=payload)
    
    assert response.status_code == 422  # Pydantic validation error

def test_login_missing_fields():
    response = client.post("/auth/login", json={"email": "user@example.com"})
    
    assert response.status_code == 422