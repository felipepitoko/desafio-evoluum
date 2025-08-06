import psycopg2
import logging

from config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_PORT, POSTGRES_HOST

logger = logging.getLogger(__name__)

def start_conn()-> psycopg2.extensions.connection:
    """Establishes and returns a self.connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT
        )
        return conn
    except psycopg2.OperationalError as e:
        # Log the exception with traceback for detailed debugging
        logger.error("Could not self.connect to the database. Is it running?", exc_info=True)
        return None
    

    
    