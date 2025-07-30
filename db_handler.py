import logging
import psycopg2
from db_config import get_db_connection
from typing import Optional

logger = logging.getLogger(__name__)

def get_all_usernames():
    """
    Retrieves a list of all usernames from the database.

    Returns:
        list: A list of username strings, or an empty list if none are found or an error occurs.
    """
    conn = get_db_connection()
    if not conn:
        return []

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT username FROM users ORDER BY username;")
            # The result of fetchall is a list of tuples, e.g., [('user1',), ('user2',)]
            # We convert it to a simple list of strings.
            usernames = [row[0] for row in cur.fetchall()]
            logger.info(f"Successfully retrieved {len(usernames)} usernames.")
            return usernames
    except psycopg2.Error as e:
        logger.error("Failed to retrieve usernames.", exc_info=True)
        return []
    finally:
        if conn:
            conn.close()

def get_user_by_username(username: str):
    """
    Retrieves a single user's data by their username, excluding the password.

    Args:
        username (str): The username to search for.

    Returns:
        dict: A dictionary containing user data (user_id, username, created_at) or None if not found.
    """
    conn = get_db_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cur:
            # Note: We explicitly exclude user_pwd for security.
            cur.execute(
                "SELECT user_id, username, created_at FROM users WHERE username = %s;",
                (username,)
            )
            user_data = cur.fetchone()
            if user_data:
                logger.info(f"Successfully found user: {username}")
                # Convert tuple to a more usable dictionary
                return {"user_id": user_data[0], "username": user_data[1], "created_at": user_data[2]}
            else:
                logger.warning(f"User not found: {username}")
                return None
    except psycopg2.Error as e:
        logger.error(f"Failed to retrieve user {username}.", exc_info=True)
        return None
    finally:
        if conn:
            conn.close()

def get_user_by_id(user_id: int):
    """
    Retrieves a single user's data by their ID, excluding the password.

    Args:
        user_id (int): The user ID to search for.

    Returns:
        dict: A dictionary containing user data or None if not found.
    """
    conn = get_db_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cur:
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
    finally:
        if conn:
            conn.close()

def create_user(username: str):
    """
    Creates a new user in the database with a placeholder password.

    Args:
        username (str): The username for the new user.

    Returns:
        dict: A dictionary containing the new user's data, or None if creation failed.
    """
    conn = get_db_connection()
    if not conn:
        return None

    # A placeholder since the password field cannot be null.
    placeholder_password = "not_set"

    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, user_pwd) VALUES (%s, %s);",
                (username, placeholder_password)
            )
        conn.commit()
        logger.info(f"Successfully created user: {username}")
        # After creating, fetch the user data to return it in a consistent format
        return get_user_by_username(username)
    except psycopg2.errors.UniqueViolation:
        logger.warning(f"Attempted to create user '{username}', but they already exist (race condition).")
        conn.rollback()
        return get_user_by_username(username)
    except psycopg2.Error:
        logger.error(f"Failed to create user {username}.", exc_info=True)
        conn.rollback()
        return None
    finally:
        if conn:
            conn.close()

def create_note(user_id: int, title: str, description: Optional[str], tags: Optional[str]):
    """
    Inserts a new note into the database for a given user.

    Args:
        user_id (int): The ID of the user creating the note.
        title (str): The title of the note.
        description (Optional[str]): The body of the note.
        tags (Optional[str]): Comma-separated tags.

    Returns:
        dict: A dictionary representing the newly created note, or None on failure.
    """
    conn = get_db_connection()
    if not conn:
        return None

    sql = """
        INSERT INTO notes (user_id, note_title, note_description, note_tags)
        VALUES (%s, %s, %s, %s)
        RETURNING note_id, note_title, note_description, note_tags, created_at;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (user_id, title, description, tags))
            new_note_data = cur.fetchone()
            conn.commit()
            columns = [desc[0] for desc in cur.description]
            logger.info(f"Successfully created note for user_id {user_id}")
            return dict(zip(columns, new_note_data))
    except psycopg2.Error:
        logger.error(f"Failed to create note for user_id {user_id}.", exc_info=True)
        conn.rollback()
        return None
    finally:
        if conn:
            conn.close()

def get_notes_by_user_id(user_id: int):
    """
    Retrieves all notes for a specific user ID.

    Args:
        user_id (int): The ID of the user whose notes are to be retrieved.

    Returns:
        list: A list of dictionaries, where each dictionary represents a note.
    """
    conn = get_db_connection()
    if not conn:
        return []

    sql = "SELECT note_id, note_title, note_description, note_tags, created_at FROM notes WHERE user_id = %s ORDER BY created_at DESC;"

    try:
        with conn.cursor() as cur:
            cur.execute(sql, (user_id,))
            notes_data = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            notes = [dict(zip(columns, row)) for row in notes_data]
            logger.info(f"Found {len(notes)} notes for user_id {user_id}.")
            return notes
    except psycopg2.Error:
        logger.error(f"Failed to retrieve notes for user_id {user_id}.", exc_info=True)
        return []
    finally:
        if conn:
            conn.close()

def get_note_by_id(note_id: int):
    """
    Retrieves a single note by its ID.

    Args:
        note_id (int): The ID of the note to retrieve.

    Returns:
        dict: A dictionary containing the note data, including the owner's user_id.
    """
    conn = get_db_connection()
    if not conn:
        return None

    sql = "SELECT note_id, user_id, note_title, note_description, note_tags, created_at FROM notes WHERE note_id = %s;"
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (note_id,))
            note_data = cur.fetchone()
            if not note_data:
                return None
            columns = [desc[0] for desc in cur.description]
            return dict(zip(columns, note_data))
    except psycopg2.Error:
        logger.error(f"Failed to retrieve note with id {note_id}.", exc_info=True)
        return None
    finally:
        if conn:
            conn.close()

def update_note(note_id: int, update_data: dict):
    """
    Updates a note in the database with the provided data.

    Args:
        note_id (int): The ID of the note to update.
        update_data (dict): A dictionary with the fields to update.

    Returns:
        dict: A dictionary representing the updated note, or None on failure.
    """
    if not update_data:
        logger.warning(f"Update called for note {note_id} with no data.")
        return get_note_by_id(note_id)

    conn = get_db_connection()
    if not conn:
        return None

    set_clauses = [f"{key} = %s" for key in update_data.keys()]
    values = list(update_data.values())
    values.append(note_id)

    sql = f"UPDATE notes SET {', '.join(set_clauses)} WHERE note_id = %s RETURNING note_id, user_id, note_title, note_description, note_tags, created_at;"

    try:
        with conn.cursor() as cur:
            cur.execute(sql, tuple(values))
            updated_note_data = cur.fetchone()
            conn.commit()
            columns = [desc[0] for desc in cur.description]
            return dict(zip(columns, updated_note_data))
    except psycopg2.Error:
        logger.error(f"Failed to update note {note_id}.", exc_info=True)
        conn.rollback()
        return None
    finally:
        if conn:
            conn.close()

def delete_note(note_id: int) -> bool:
    """
    Deletes a note from the database by its ID.

    Args:
        note_id (int): The ID of the note to delete.

    Returns:
        bool: True if the note was deleted successfully, False otherwise.
    """
    conn = get_db_connection()
    if not conn:
        return False

    sql = "DELETE FROM notes WHERE note_id = %s;"
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (note_id,))
            # Check if a row was actually deleted
            deleted_rows = cur.rowcount
            conn.commit()
            if deleted_rows > 0:
                logger.info(f"Successfully deleted note with id {note_id}")
                return True
            else:
                logger.warning(f"Attempted to delete note with id {note_id}, but it was not found.")
                return False
    except psycopg2.Error:
        logger.error(f"Failed to delete note {note_id}.", exc_info=True)
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    # Example usage for testing the functions
    logging.basicConfig(level=logging.INFO)
    print("All usernames:", get_all_usernames())
    print("User 'admin':", get_user_by_username('admin'))