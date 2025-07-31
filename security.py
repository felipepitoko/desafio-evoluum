from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from config import SECRET_TOKEN

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

async def verify_token(token: str = Security(api_key_header)) -> int:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing",
        )

    parts = token.split(" ")
    if len(parts) != 2 or parts[0] != SECRET_TOKEN or not parts[1].startswith("id="):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authorization token format",
        )

    try:
        user_id_str = parts[1].split("=")[1]
        user_id = int(user_id_str)
        return user_id
    except (IndexError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authorization token",
        )