from datetime import datetime
from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: int
    username: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserLoginRequest(BaseModel):
    """Model for the simplified login request, only needs a username."""
    username: str = Field(..., example="johndoe")


class LoginResponse(BaseModel):
    """Model for the successful login response."""
    token: str