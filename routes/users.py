import logging
from typing import List, Dict, Any

from fastapi import APIRouter, HTTPException, status, Depends, Response

from services import users_service
from models.users_model import LoginResponse, UserLoginRequest
from security import verify_token

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/users/", response_model=List[str], tags=["Users"], dependencies=[Depends(verify_token)])
def get_all_users_api():
    """Retrieve a list of all usernames."""
    logger.info("API: Request received for all usernames.")
    return users_service.get_all_usernames_service()


@router.post("/users/login", response_model=LoginResponse, tags=["Users"])
def login_or_create_user_api(login_request: UserLoginRequest):
    """
    Logs a user in by their username.

    If the user exists, it returns their ID and a token.
    If the user does not exist, it creates them first and then returns the ID and token.
    """
    logger.info(f"API: Login/Create request for user: {login_request.username}")
    user = users_service.login_or_create_user_service(login_request.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not process user login or creation."
        )

    token_string = f"super_secret_token id={user['user_id']}"
    return {
        "token": token_string
    }