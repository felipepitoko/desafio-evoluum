from fastapi.testclient import TestClient
from typing import Dict, Any
from database.db_handler import DBHandler

def test_create_note_success(client: TestClient, authenticated_user: Dict[str, Any]):
    """Test successful note creation with valid data and token."""
    note_data = {"note_title": "My First Note", "note_description": "This is a test description."}
    response = client.post("/notes", json=note_data, headers=authenticated_user["auth_headers"])

    assert response.status_code == 201
    data = response.json()
    assert data["note_title"] == note_data["note_title"]
    assert data["note_description"] == note_data["note_description"]
    assert "note_id" in data

def test_create_note_unauthorized(client: TestClient):
    """Test note creation fails without an authorization header."""
    note_data = {"note_title": "This will fail"}
    response = client.post("/notes", json=note_data) # No headers
    assert response.status_code == 401

def test_create_note_missing_title(client: TestClient, authenticated_user: Dict[str, Any]):
    """Test that Pydantic validation catches missing required fields."""
    note_data = {"note_description": "Missing the title"}
    response = client.post("/notes", json=note_data, headers=authenticated_user["auth_headers"])
    assert response.status_code == 422 # Unprocessable Entity

def test_get_notes_for_user(client: TestClient, db_handler_test_instance: DBHandler, authenticated_user: Dict[str, Any]):
    """Test retrieving all notes for the authenticated user."""
    user_id = authenticated_user["user_id"]
    auth_headers = authenticated_user["auth_headers"]

    # Create notes directly in the DB to test retrieval
    db_handler_test_instance.create_note(user_id, "Note 1", "Desc 1", None)
    db_handler_test_instance.create_note(user_id, "Note 2", "Desc 2", None)

    response = client.get("/notes", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["note_title"] == "Note 2" # Should be ordered by creation date descending

def test_get_notes_no_notes_found(client: TestClient, authenticated_user: Dict[str, Any]):
    """Test that a 404 is returned when a user has no notes."""
    response = client.get("/notes", headers=authenticated_user["auth_headers"])
    assert response.status_code == 404
    assert response.json()["detail"] == "No notes found for this user."

def test_update_note_success(client: TestClient, db_handler_test_instance: DBHandler, authenticated_user: Dict[str, Any]):
    """Test successfully updating a note's title and tags."""
    user_id = authenticated_user["user_id"]
    auth_headers = authenticated_user["auth_headers"]

    original_note = db_handler_test_instance.create_note(user_id, "Original Title", "Original Desc", "tag1")
    note_id = original_note["note_id"]

    update_data = {"note_title": "Updated Title", "note_tags": "tag2,tag3"}
    response = client.put(f"/notes/{note_id}", json=update_data, headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["note_title"] == "Updated Title"
    assert data["note_description"] == "Original Desc" # Description was not updated
    assert data["note_tags"] == "tag2,tag3"

def test_update_note_not_owner(client: TestClient, db_handler_test_instance: DBHandler, authenticated_user: Dict[str, Any]):
    """Test that a user cannot update a note they do not own."""
    # Create another user and a note for them
    other_user = db_handler_test_instance.create_user("otheruser")
    other_note = db_handler_test_instance.create_note(other_user["user_id"], "Other's Note", "...", None)
    note_id_to_steal = other_note["note_id"]

    # Try to update it as the primary authenticated_user
    update_data = {"note_title": "My new title"}
    response = client.put(f"/notes/{note_id_to_steal}", json=update_data, headers=authenticated_user["auth_headers"])

    # The API should return an error indicating the resource is not found for this user
    assert response.status_code == 400
    assert "not found" in response.json()["detail"]

def test_delete_note_success(client: TestClient, db_handler_test_instance: DBHandler, authenticated_user: Dict[str, Any]):
    """Test successful deletion of a note."""
    user_id = authenticated_user["user_id"]
    auth_headers = authenticated_user["auth_headers"]

    note_to_delete = db_handler_test_instance.create_note(user_id, "To Be Deleted", "...", None)
    note_id = note_to_delete["note_id"]

    response = client.delete(f"/notes/{note_id}", headers=auth_headers)

    assert response.status_code == 204

    # Verify it's gone from the DB
    deleted_note = db_handler_test_instance.get_note_by_id(note_id)
    assert deleted_note is None

def test_delete_note_not_owner(client: TestClient, db_handler_test_instance: DBHandler, authenticated_user: Dict[str, Any]):
    """Test that a user cannot delete a note they do not own."""
    other_user = db_handler_test_instance.create_user("otheruser")
    other_note = db_handler_test_instance.create_note(other_user["user_id"], "Other's Note", "...", None)
    note_id_to_steal = other_note["note_id"]

    response = client.delete(f"/notes/{note_id_to_steal}", headers=authenticated_user["auth_headers"])

    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_delete_note_not_found(client: TestClient, authenticated_user: Dict[str, Any]):
    """Test deleting a note that does not exist."""
    response = client.delete("/notes/99999", headers=authenticated_user["auth_headers"])
    assert response.status_code == 404
