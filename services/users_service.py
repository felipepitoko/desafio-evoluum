import logging
from typing import List, Optional, Dict, Any

import db_handler

logger = logging.getLogger(__name__)


def get_all_usernames_service() -> List[str]:
    """Service to retrieve all usernames."""
    return db_handler.get_all_usernames()


def get_user_by_username_service(username: str) -> Optional[Dict[str, Any]]:
    """
    Service to retrieve a single user by username.
    Returns user data as a dict or None if not found.
    """
    return db_handler.get_user_by_username(username)


def login_or_create_user_service(username: str) -> Optional[Dict[str, Any]]:
    """
    Service to get a user if they exist, or create them if they don't.

    Args:
        username (str): The user's username.

    Returns:
        A dictionary containing the user object, or None if an error occurred.
    """
    existing_user = db_handler.get_user_by_username(username)
    if existing_user:
        logger.info(f"Service: Found existing user '{username}'.")
        return existing_user

    logger.info(f"Service: User '{username}' not found. Proceeding to create.")
    return db_handler.create_user(username)