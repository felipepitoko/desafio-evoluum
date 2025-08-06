import logging
from typing import List

from fastapi import APIRouter, HTTPException, status

from services import notes_service
from .dependencies import AuthenticatedUserID
from .dependencies import DBHandlerInstance
from models.notes_model import Note, NoteCreate, NoteUpdate

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/notes", response_model=List[Note], tags=["Notes"])
def get_my_notes_api(
    user_id: AuthenticatedUserID,
    _db: DBHandlerInstance
    ):
    """
    Retrieve all notes for the authenticated user.
    Returns 404 if no notes are found.
    """
    logger.info(f"API: Request received for notes of user_id: {user_id}")
    notes = notes_service.get_notes_by_user_id_service(_db, user_id)

    if not notes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No notes found for this user."
        )
    return notes

@router.post("/notes", response_model=Note, status_code=status.HTTP_201_CREATED, tags=["Notes"])
def create_new_note_api(
    note_data: NoteCreate,
    user_id: AuthenticatedUserID,
    _db: DBHandlerInstance
):
    """
    Creates a new note for the authenticated user.

    If the user ID from the token does not exist in the database,
    it returns a 401 Unauthorized error.
    """
    logger.info(f"API: Request to create note for user_id: {user_id}")

    new_note = notes_service.create_note_for_user_service(_db, user_id, note_data.model_dump())

    if not new_note:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create note."
        )
    return new_note

@router.put("/notes/{note_id}", response_model=Note, tags=["Notes"])
def update_note_api(
    note_id: int,
    note_data: NoteUpdate,
    user_id: AuthenticatedUserID,
    _db: DBHandlerInstance
):
    """
    Updates an existing note for the authenticated user.

    - Returns 401 if the user token is invalid.
    - Returns 400 if the note is not found or the user does not own it.
    """
    logger.info(f"API: Request to update note {note_id} for user_id: {user_id}")

    update_data = note_data.model_dump(exclude_unset=True)

    result = notes_service.update_note_service(
        _db, user_id=user_id, note_id=note_id, note_data=update_data
    )

    if result == "user_not_found":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user token."
        )
    if result == "note_not_found":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Note with id {note_id} not found."
        )
    if not isinstance(result, dict):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not update note due to a server error."
        )

    return result

@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Notes"])
def delete_note_api(
    note_id: int,
    user_id: AuthenticatedUserID,
    _db: DBHandlerInstance
):
    """
    Deletes a note for the authenticated user.

    - Returns 401 if the user token is invalid.
    - Returns 404 if the note is not found or the user does not own it.
    - Returns 204 on successful deletion.
    """
    logger.info(f"API: Request to delete note {note_id} for user_id: {user_id}")

    result = notes_service.delete_note_service(_db, user_id=user_id, note_id=note_id)

    if result == "user_not_found":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user token."
        )
    if result == "note_not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found or access denied."
        )
    if result != "success":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not delete note due to a server error."
        )
        
    return None