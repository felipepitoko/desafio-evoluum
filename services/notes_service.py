import logging
from typing import List, Optional, Dict, Any

import db_handler

logger = logging.getLogger(__name__)


def create_note_for_user_service(user_id: int, note_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Service to create a new note for a user.

    It first validates that the user exists.
    - If the user does not exist, it returns None.
    - If the user exists, it creates the note and returns it.
    """
    # 1. Validate that the user from the token exists in the database.
    if not db_handler.get_user_by_id(user_id):
        logger.warning(f"Service: Attempt to create note for non-existent user_id: {user_id}")
        return None

    # 2. Create the note.
    return db_handler.create_note(
        user_id=user_id,
        title=note_data["note_title"],
        description=note_data.get("note_description"),
        tags=note_data.get("note_tags")
    )

def update_note_service(user_id: int, note_id: int, note_data: Dict[str, Any]) -> Optional[Any]:
    """
    Service to update an existing note.

    It validates user existence, note existence, and ownership.

    Returns:
        - A dictionary of the updated note on success.
        - A string "user_not_found" if the user is invalid.
        - A string "note_not_found" if the note is not found or doesn't belong to the user.
        - None on other database errors.
    """
    # 1. Validate that the user from the token exists in the database.
    if not db_handler.get_user_by_id(user_id):
        logger.warning(f"Service: Attempt to update note for non-existent user_id: {user_id}")
        return "user_not_found"

    # 2. Validate that the note exists and the user owns it.
    note = db_handler.get_note_by_id(note_id)
    if not note or note.get("user_id") != user_id:
        logger.warning(f"Service: Update access denied for note {note_id} by user {user_id}.")
        # Combine "not found" and "permission denied" to prevent leaking information.
        return "note_not_found"

    # 3. If there's no new data, return the existing note without hitting the DB.
    if not note_data:
        logger.info(f"Service: Update request for note {note_id} had no new data.")
        return note

    # 4. Perform the update.
    return db_handler.update_note(note_id, note_data)

def delete_note_service(user_id: int, note_id: int) -> str:
    """
    Service to delete an existing note.

    It validates user existence, note existence, and ownership.

    Returns:
        - "success" on successful deletion.
        - "user_not_found" if the user is invalid.
        - "note_not_found" if the note is not found or doesn't belong to the user.
        - "error" on other database errors.
    """
    # 1. Validate that the user from the token exists in the database.
    if not db_handler.get_user_by_id(user_id):
        logger.warning(f"Service: Attempt to delete note for non-existent user_id: {user_id}")
        return "user_not_found"

    # 2. Validate that the note exists and the user owns it.
    note = db_handler.get_note_by_id(note_id)
    if not note or note.get("user_id") != user_id:
        logger.warning(f"Service: Delete access denied for note {note_id} by user {user_id}.")
        return "note_not_found"

    # 3. Perform the deletion.
    return "success" if db_handler.delete_note(note_id) else "error"

def get_notes_by_user_id_service(user_id: int) -> List[Dict[str, Any]]:
    """Service to retrieve all notes for a given user ID."""
    return db_handler.get_notes_by_user_id(user_id)