import logging
from typing import List

from fastapi import APIRouter, HTTPException, status

from services import users_service
from .dependencies import AuthenticatedUserID, DBHandlerInstance
from models.users_model import User


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/users", response_model=List[str], tags=["Users"])
def get_all_users(
    _user_id: AuthenticatedUserID,
    _db: DBHandlerInstance
):
    """Retrieve a list of all usernames."""
    logger.info("API: Request received for all usernames.")
    return users_service.get_all_usernames_service(_db)

@router.get("/users/{username}", response_model=User, tags=["Users"])
def get_user_by_username(
    username: str,
    _user_id: AuthenticatedUserID,
    _db: DBHandlerInstance
):
    """Retrieve a single user data by its username."""
    logger.info("API: Request received for all usernames.")
    return users_service.get_user_by_username_service(_db,username)