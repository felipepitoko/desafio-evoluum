from fastapi.testclient import TestClient
from database.db_handler import DBHandler
from config import SECRET_TOKEN

def test_login_and_create_new_user(client: TestClient, db_handler_test_instance: DBHandler):
    """
    Test that a new user can log in, which creates a user record in the DB
    and returns a valid token.
    """
    username = "newuser"
    response = client.post("/login", json={"username": username})

    # 1. Check the API response
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    # The first user created in the test DB should have id=1
    assert data["token"] == f"{SECRET_TOKEN} id=1"

    # 2. Verify the user was actually created in the database
    user_in_db = db_handler_test_instance.get_user_by_username(username)
    assert user_in_db is not None
    assert user_in_db["username"] == username
    assert user_in_db["user_id"] == 1

def test_login_existing_user(client: TestClient, db_handler_test_instance: DBHandler):
    """
    Test that an existing user can log in and receive the correct token.
    """
    username = "existinguser"
    # Pre-populate the database with a user
    created_user = db_handler_test_instance.create_user(username)
    assert created_user is not None
    user_id = created_user["user_id"]

    # Now, perform the login via the API
    response = client.post("/login", json={"username": username})

    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["token"] == f"{SECRET_TOKEN} id={user_id}"

def test_login_empty_username(client: TestClient):
    """
    Test that sending an empty or whitespace-only username results in a 400 Bad Request error.
    """
    response = client.post("/login", json={"username": "   "})

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Username cannot be empty"