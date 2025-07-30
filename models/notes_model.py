from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class NoteUpdate(BaseModel):
    """Model for updating an existing note. All fields are optional."""
    note_title: Optional[str] = Field(None, min_length=1, max_length=255)
    note_description: Optional[str] = None
    note_tags: Optional[str] = None


class NoteCreate(BaseModel):
    """Model for creating a new note."""
    note_title: str = Field(..., min_length=1, max_length=255)
    note_description: Optional[str] = None
    note_tags: Optional[str] = None


class Note(BaseModel):
    note_id: int
    note_title: str
    note_description: Optional[str] = None
    note_tags: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True