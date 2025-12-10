import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "123456"),
    "database": os.getenv("DB_NAME", "libraryx"),
    "port": int(os.getenv("DB_PORT", 3306))
}

# Simple connection function
def get_db_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn
