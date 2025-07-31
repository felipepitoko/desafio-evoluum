import logging
from typing import List

from fastapi import APIRouter, Depends

from services import users_service
from security import verify_token

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/users/", response_model=List[str], tags=["Users"], dependencies=[Depends(verify_token)])
def get_all_users_api():
    """Retrieve a list of all usernames."""
    logger.info("API: Request received for all usernames.")
    return users_service.get_all_usernames_service()