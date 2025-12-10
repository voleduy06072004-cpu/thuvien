from app.config.db_config import get_db_connection

class UserModel:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    @staticmethod
    def add(data):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """INSERT INTO users (account_id, full_name, age, email, phone, gender, address)
                 VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql, (
            data.get('account_id'), data.get('full_name'), data.get('age'), data.get('email'),
            data.get('phone'), data.get('gender'), data.get('address')
        ))
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return last_id

    @staticmethod
    def update(user_id, data):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """UPDATE users SET full_name=%s, age=%s, email=%s, phone=%s, gender=%s, address=%s WHERE user_id=%s"""
        cursor.execute(sql, (data.get('full_name'), data.get('age'), data.get('email'), data.get('phone'), data.get('gender'), data.get('address'), user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    @staticmethod
    def delete(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
