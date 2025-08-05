import logging
from typing import List

from fastapi import APIRouter, Depends

from services import users_service
from .dependencies import AuthenticatedUserID, DBHandlerInstance

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/users/", response_model=List[str], tags=["Users"])
def get_all_users_api(
    _user_id: AuthenticatedUserID,
    _db: DBHandlerInstance
):
    """Retrieve a list of all usernames."""
    logger.info("API: Request received for all usernames.")
    return users_service.get_all_usernames_service(_db)