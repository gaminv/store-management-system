import psycopg2
import json
import os
def get_db_connection():
    """
    Устанавливает соединение с базой данных PostgreSQL.
    """
    with open('db_config.json', 'r', encoding='utf-8') as config_file:
        db_params = json.load(config_file)

    conn = psycopg2.connect(
        host=db_params['host'],
        port=db_params['port'],
        database=db_params['database'],
        user=db_params['user'],
        password=db_params['password']
    )
    return conn
