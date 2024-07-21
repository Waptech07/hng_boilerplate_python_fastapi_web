import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from unittest.mock import Mock, patch
from api.v1.routes.auth import auth
from api.v1.models.user import User
from api.db.database import get_db

app = FastAPI()
app.include_router(auth)

# Mock database dependency
def override_get_db():
    db = Mock()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="module")
def mock_db():
    return Mock()

@pytest.mark.anyio
async def test_password_reset_email(client, mock_db):
    # Mock user in the database
    test_user = User(email="gihxdma356@couldmail.com", password="fakehashedpassword")
    mock_db.query.return_value.filter.return_value.first.return_value = test_user

    # Override get_db dependency with mock_db
    app.dependency_overrides[get_db] = lambda: mock_db

    # Determine the correct import path for create_access_token
    with patch('api.v1.routes.auth.create_access_token', return_value="fake_token") as mock_create_token:
        # Mock the send_password_reset_email function
        with patch('api.v1.services.email.send_password_reset_email', return_value=None) as mock_send_email:
            # Test valid user
            response = await client.post("/api/v1/auth/password-reset-email", json={"email": "gihxdma356@couldmail.com"})      

            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
            print(f"create_access_token called: {mock_create_token.called}")
            print(f"send_password_reset_email called: {mock_send_email.called}")

            assert response.status_code == 200
            response_json = response.json()
            assert response_json["message"] == "Password reset email sent successfully."
            assert "data" in response_json
            assert "reset_link" in response_json["data"]
            assert response_json["data"]["reset_link"].startswith("https://example.com/reset-password?token=fake_token")

            # Test non-existent user
            mock_db.query.return_value.filter.return_value.first.return_value = None
            response = await client.post("/api/v1/auth/password-reset-email", json={"email": "nonexistent@example.com"})

            print(f"Response status code (non-existent user): {response.status_code}")
            print(f"Response content (non-existent user): {response.text}")

            assert response.status_code == 404
            assert response.json() == {"detail": "Email not found"}

            # Test missing email in request
            response = await client.post("/api/v1/auth/password-reset-email", json={})

            print(f"Response status code (missing email): {response.status_code}")
            print(f"Response content (missing email): {response.text}")

            assert response.status_code == 422  # Unprocessable Entity for missing required fields
            assert "detail" in response.json()  # Check if there is an error detail
