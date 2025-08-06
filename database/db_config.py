import logging
import psycopg2

from database.connection import start_conn

logger = logging.getLogger(__name__)

def create_tables(conn: psycopg2.extensions.connection):
    """Creates the users and notes tables in the database if they don't exist."""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            user_pwd VARCHAR(255) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS notes (
            note_id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            note_title VARCHAR(255) NOT NULL,
            note_description TEXT,
            note_tags VARCHAR(255),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_user
                FOREIGN KEY(user_id)
                REFERENCES users(user_id)
                ON DELETE CASCADE
        )
        """
    )
    
    if not conn:
        # get_db_connection already logged the error, so we just exit gracefully.
        return

    try:
        # The 'with conn' block creates a transaction.
        # It automatically commits if the block succeeds, or rolls back on exception.
        with conn:
            with conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)
        logger.info("Tables 'users' and 'notes' have been successfully created/verified.")
    except psycopg2.Error as e:
        # The 'with conn' block will have already rolled back the transaction.
        logger.error("Failed to create tables.", exc_info=True)

if __name__ == '__main__':
    # When running this script directly, configure a basic logger to see output.
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger.info("Initializing database...")
    conn = start_conn()
    # This allows the script to be run directly to set up the database,
    # managing its own connection lifecycle.
    if conn:
        try:
            create_tables(conn)
        finally:
            conn.close()
    logger.info("Database initialization complete.")