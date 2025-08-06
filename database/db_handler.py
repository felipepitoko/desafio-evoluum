import logging
import psycopg2
from typing import Optional, List, Dict, Any
from psycopg2.extensions import connection as Connection

logger = logging.getLogger(__name__)

class DBHandler:
    def __init__(self, db_session: Connection):
        """
        Initializes the handler with an active database connection.

        Args:
            db_session (Connection): An active psycopg2 connection object.
        """
        self.conn = db_session
        
    
    def get_all_usernames(self):
        """
        Retrieves a list of all usernames from the database.

        Returns:
            list: A list of username strings, or an empty list if none are found or an error occurs.
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT username FROM users ORDER BY username;")
                usernames = [row[0] for row in cur.fetchall()]
                logger.info(f"Successfully retrieved {len(usernames)} usernames.")
                return usernames
        except psycopg2.Error as e:
            logger.error("Failed to retrieve usernames.", exc_info=True)
            return []
            
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT user_id, username, created_at FROM users WHERE username = %s;",
                    (username,)
                )
                user_data = cur.fetchone()
                if user_data:
                    return {"user_id": user_data[0], "username": user_data[1], "created_at": user_data[2]}
                return None
        except psycopg2.Error:
            logger.error(f"Failed to retrieve user {username}.", exc_info=True)
            return None

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT user_id, username, created_at FROM users WHERE user_id = %s;",
                    (user_id,)
                )
                user_data = cur.fetchone()
                if user_data:
                    return {"user_id": user_data[0], "username": user_data[1], "created_at": user_data[2]}
                return None
        except psycopg2.Error:
            logger.error(f"Failed to retrieve user with id {user_id}.", exc_info=True)
            return None

    def create_user(self, username: str) -> Optional[Dict[str, Any]]:
        placeholder_password = "not_set"
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (username, user_pwd) VALUES (%s, %s) RETURNING user_id, username, created_at;",
                    (username, placeholder_password)
                )
                user_data = cur.fetchone()
                self.conn.commit()
                logger.info(f"Successfully created user: {username}")
                return {"user_id": user_data[0], "username": user_data[1], "created_at": user_data[2]}
        except psycopg2.errors.UniqueViolation:
            logger.warning(f"Attempted to create user '{username}', but they already exist.")
            self.conn.rollback()
            return self.get_user_by_username(username)
        except psycopg2.Error:
            logger.error(f"Failed to create user {username}.", exc_info=True)
            self.conn.rollback()
            return None

    def create_note(self, user_id: int, title: str, description: Optional[str], tags: Optional[str]) -> Optional[Dict[str, Any]]:
        sql = """
            INSERT INTO notes (user_id, note_title, note_description, note_tags)
            VALUES (%s, %s, %s, %s)
            RETURNING note_id, note_title, note_description, note_tags, created_at;
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, (user_id, title, description, tags))
                new_note_data = cur.fetchone()
                self.conn.commit()
                columns = [desc[0] for desc in cur.description]
                logger.info(f"Successfully created note for user_id {user_id}")
                return dict(zip(columns, new_note_data))
        except psycopg2.Error:
            logger.error(f"Failed to create note for user_id {user_id}.", exc_info=True)
            self.conn.rollback()
            return None

    def get_notes_by_user_id(self, user_id: int) -> List[Dict[str, Any]]:
        sql = "SELECT note_id, note_title, note_description, note_tags, created_at FROM notes WHERE user_id = %s ORDER BY created_at DESC;"
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, (user_id,))
                notes_data = cur.fetchall()
                columns = [desc[0] for desc in cur.description]
                return [dict(zip(columns, row)) for row in notes_data]
        except psycopg2.Error:
            logger.error(f"Failed to retrieve notes for user_id {user_id}.", exc_info=True)
            return []

    def get_note_by_id(self, note_id: int) -> Optional[Dict[str, Any]]:
        sql = "SELECT note_id, user_id, note_title, note_description, note_tags, created_at FROM notes WHERE note_id = %s;"
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, (note_id,))
                note_data = cur.fetchone()
                if not note_data:
                    return None
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, note_data))
        except psycopg2.Error:
            logger.error(f"Failed to retrieve note with id {note_id}.", exc_info=True)
            return None

    def update_note(self, note_id: int, update_data: dict) -> Optional[Dict[str, Any]]:
        set_clauses = [f"{key} = %s" for key in update_data.keys()]
        values = list(update_data.values()) + [note_id]
        sql = f"UPDATE notes SET {', '.join(set_clauses)} WHERE note_id = %s RETURNING note_id, user_id, note_title, note_description, note_tags, created_at;"
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, tuple(values))
                updated_note_data = cur.fetchone()
                self.conn.commit()
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, updated_note_data))
        except psycopg2.Error:
            logger.error(f"Failed to update note {note_id}.", exc_info=True)
            self.conn.rollback()
            return None

    def delete_note(self, note_id: int) -> bool:
        sql = "DELETE FROM notes WHERE note_id = %s;"
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, (note_id,))
                deleted_rows = cur.rowcount
                self.conn.commit()
                return deleted_rows > 0
        except psycopg2.Error:
            logger.error(f"Failed to delete note {note_id}.", exc_info=True)
            self.conn.rollback()
            return False