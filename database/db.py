import pymysql
import os
from dotenv import load_dotenv

load_dotenv()
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 14054)),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_NAME"),
    "charset": 'utf8mb4',
    "cursorclass": pymysql.cursors.DictCursor,
    "connect_timeout": 10
}

def get_connection():
    try:
        return pymysql.connect(**DB_CONFIG)
    except Exception as e:
        print(f"[!] DB 연결 실패: {e}")
        return None

def save_to_db(data_list):
    if not data_list:
        return

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO victims (data_key, company_name, leaked_date, company_url, industry, country)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.executemany(sql, data_list)
        conn.commit()
    except Exception as e:
        print(f"[!] MySQL 저장 에러: {e}")
    finally:
        conn.close()