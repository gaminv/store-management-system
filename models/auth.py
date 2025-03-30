from .database import get_db_connection
from utils import check_password

def authenticate_user(username: str, password: str):
    """Проверяет логин и пароль пользователя."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT username, password_hash, role FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    conn.close()

    if user and check_password(password, user[1]):
        return {"username": user[0], "role": user[2]}
    return None
