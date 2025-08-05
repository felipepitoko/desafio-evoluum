from typing import Annotated
from fastapi import  Depends

from security import verify_token
from database.connection import get_db_handler
from database.db_handler import DBHandler

AuthenticatedUserID = Annotated[int, Depends(verify_token)]
DBHandlerInstance = Annotated[DBHandler, Depends(get_db_handler)]

