import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ...main import app
from api.db.database import Base, get_db
from api.utils.settings import settings

test_db_name = 'test_db'
test_db_pw = 'root'

# Create a test database engine
SQLALCHEMY_DATABASE_URL = f"{settings.DB_TYPE}://postgres:{test_db_pw}@localhost:5432/{test_db_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create the test database and tables
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="module")
def db():
    db = TestingSessionLocal()
    yield db
    db.close()

@pytest.mark.asyncio
async def test_password_reset_email(client, db):
    # Create a test user
    test_user = User(email="testuser@example.com", hashed_password="fakehashedpassword")
    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    response = await client.post("/api/v1/password-reset-email", json={"email": "testuser@example.com"})
    assert response.status_code == 200
    assert response.json() == {"message": "Password reset email sent successfully."}

    response = await client.post("/api/v1/password-reset-email", json={"email": "nonexistent@example.com"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Email not found"}

    # Clean up test user
    db.delete(test_user)
    db.commit()
