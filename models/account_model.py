from app.config.db_config import get_db_connection

class AccountModel:
    @staticmethod
    def create_account(username, password, role='user'):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO accounts (username, password, role) VALUES (%s,%s,%s)", (username, password, role))
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return last_id

    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM accounts WHERE username = %s", (username,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row
