from utils import hash_password
from models.database import get_db_connection


def create_users():
    conn = get_db_connection()
    cur = conn.cursor()

    users = [
        ("admin", hash_password("123a").decode('utf-8'), "admin"),
        ("user", hash_password("123u").decode('utf-8'), "user"),
    ]

    for username, password_hash, role in users:
        # Проверяем, существует ли пользователь
        cur.execute("SELECT username FROM users WHERE username = %s", (username,))
        if cur.fetchone():
            print(f"Пользователь {username} уже существует, пропуск...")
            continue
        # Если пользователя нет, добавляем его
        cur.execute("INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                    (username, password_hash, role))

    conn.commit()
    conn.close()
    print("Пользователи успешно добавлены или обновлены!")


if __name__ == "__main__":
    create_users()
