from app.config.db_config import get_db_connection

class BorrowModel:
    @staticmethod
    def borrow(data):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO borrow_books (user_id, book_id, quantity, borrow_date, return_date, fee)
                          VALUES (%s,%s,%s,%s,%s,%s)""", (
            data.get('user_id'), data.get('book_id'), data.get('quantity'), data.get('borrow_date'), data.get('return_date'), data.get('fee')
        ))
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return last_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM borrow_books")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
