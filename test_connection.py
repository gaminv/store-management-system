from psycopg2 import connect

def test_connection():
    try:
        conn = connect(
            host="localhost",
            port=5432,
            database="lab11",
            user="postgres",
            password="1234"
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM users LIMIT 1;")
        print("Таблица users доступна!")
        conn.close()
    except Exception as e:
        print("Ошибка подключения или отсутствует таблица users:", e)

test_connection()