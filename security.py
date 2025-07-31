from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from config import SECRET_TOKEN

# This defines that we expect the token in a header named "Authorization".
# auto_error=False allows us to provide our own custom error message.
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

async def verify_token(token: str = Security(api_key_header)) -> int:
    """
    Dependency to verify the authorization token.
    Raises HTTPException if the token is missing or invalid.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing",
        )

    # The expected format is "super_secret_token id=123"
    parts = token.split(" ")
    if len(parts) != 2 or parts[0] != SECRET_TOKEN or not parts[1].startswith("id="):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authorization token format",
        )

    try:
        # Extract and convert the user ID to an integer
        user_id_str = parts[1].split("=")[1]
        user_id = int(user_id_str)
        return user_id
    except (IndexError, ValueError):
        # This catches errors like "id=" with no number or "id=abc"
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authorization token",
        )