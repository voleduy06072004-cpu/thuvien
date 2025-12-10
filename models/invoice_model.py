from app.config.db_config import get_db_connection

class InvoiceModel:
    @staticmethod
    def create(invoice):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO invoices (user_id, invoice_code, total_amount) VALUES (%s,%s,%s)",
                       (invoice.get('user_id'), invoice.get('invoice_code'), invoice.get('total_amount')))
        conn.commit()
        invoice_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return invoice_id

    @staticmethod
    def add_detail(invoice_id, detail):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO invoice_details (invoice_id, book_id, quantity, unit_price) VALUES (%s,%s,%s,%s)",
                       (invoice_id, detail.get('book_id'), detail.get('quantity'), detail.get('unit_price')))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM invoices")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
