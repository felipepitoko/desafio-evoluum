from fastapi import APIRouter, HTTPException, status
from models.users_model import UserLoginRequest, LoginResponse
from services import users_service
from config import SECRET_TOKEN

from .dependencies import DBHandlerInstance

router = APIRouter()

@router.post("/login", response_model=LoginResponse, tags=["Authentication"])
async def login_for_access_token(
    form_data: UserLoginRequest,
    _db: DBHandlerInstance
    ):
    """
    Logs in a user by username.
    If the user doesn't exist, it will be created.
    Returns a token to be used for subsequent requests.
    """
    username = form_data.username.strip()
    if not username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username cannot be empty",
        )

    # Use the service layer to handle the logic of finding or creating a user.
    # This is a better practice than calling the db_handler directly from the router.
    user = users_service.login_or_create_user_service(_db, username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not process user login or creation.",
        )

    user_id = user.get("user_id")
    if not user_id:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User exists but could not retrieve ID.",
        )

    # The full token is constructed securely on the server.
    access_token_str = f"{SECRET_TOKEN} id={user_id}"
    return {"token": access_token_str }