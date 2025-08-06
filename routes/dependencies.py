import logging

from typing import Annotated
from fastapi import  Depends, HTTPException, status

from security import verify_token
from database.connection import start_conn
from database.db_handler import DBHandler

logger = logging.getLogger(__name__)

def get_db_handler():
    conn = start_conn()
    if not conn:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Não foi possível conectar ao banco de dados."
        ) 
    
    try:
        yield DBHandler(conn)
    finally:
        if conn:
            logging.info("Closing database connection.")
            conn.close()

AuthenticatedUserID = Annotated[int, Depends(verify_token)]
DBHandlerInstance = Annotated[DBHandler, Depends(get_db_handler)]

