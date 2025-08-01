from typing import Annotated
from fastapi import  Depends

from security import verify_token

AuthenticatedUserID = Annotated[int, Depends(verify_token)]