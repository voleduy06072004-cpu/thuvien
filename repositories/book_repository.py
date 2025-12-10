from app.config.db_config import get_db_connection
from app.interfaces.book_repository_interface import BookRepositoryInterface
from app.models.book_model import Book, TextBook, ReferenceBook
from typing import List, Optional

class BookRepository(BookRepositoryInterface):
    """
    Concrete implementation của Book Repository
    Chịu trách nhiệm: Truy xuất và lưu trữ dữ liệu vào database
    Tuân thủ SRP: chỉ lo database operations
    """
    
    def _execute_query(self, query: str, params: tuple = None, fetch_one: bool = False, fetch_all: bool = False):
        """Helper method để quản lý connection tốt hơn"""
        conn = None
        try:
            conn = get_db_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, params or ())
                
                if fetch_one:
                    return cursor.fetchone()
                elif fetch_all:
                    return cursor.fetchall()
                else:
                    conn.commit()
                    return cursor.lastrowid if cursor.lastrowid else True
        finally:
            if conn:
                conn.close()
    
    def _row_to_book(self, row: dict) -> Optional[Book]:
        """Convert database row thành Book object (Factory pattern)"""
        if not row:
            return None
        
        book_type = row.get('book_type')
        if book_type == 'Sách giáo khoa':
            return TextBook.from_dict(row)
        elif book_type == 'Sách tham khảo':
            return ReferenceBook.from_dict(row)
        return None
    
    def find_all(self) -> List[Book]:
        """Lấy tất cả sách"""
        rows = self._execute_query("SELECT * FROM books ORDER BY book_id DESC", fetch_all=True)
        return [self._row_to_book(row) for row in rows if self._row_to_book(row)]
    
    def find_by_id(self, book_id: int) -> Optional[Book]:
        """Tìm sách theo ID"""
        row = self._execute_query(
            "SELECT * FROM books WHERE book_id = %s", 
            (book_id,), 
            fetch_one=True
        )
        return self._row_to_book(row)
    
    def find_by_code(self, book_code: str) -> Optional[Book]:
        """Tìm sách theo mã"""
        row = self._execute_query(
            "SELECT * FROM books WHERE book_code = %s", 
            (book_code,), 
            fetch_one=True
        )
        return self._row_to_book(row)
    
    def search_by_name(self, name: str) -> List[Book]:
        """Tìm kiếm sách theo tên"""
        rows = self._execute_query(
            "SELECT * FROM books WHERE book_name LIKE %s ORDER BY book_name", 
            (f'%{name}%',), 
            fetch_all=True
        )
        return [self._row_to_book(row) for row in rows if self._row_to_book(row)]
    
    def find_by_type(self, book_type: str) -> List[Book]:
        """Lấy sách theo loại"""
        rows = self._execute_query(
            "SELECT * FROM books WHERE book_type = %s ORDER BY book_name", 
            (book_type,), 
            fetch_all=True
        )
        return [self._row_to_book(row) for row in rows if self._row_to_book(row)]
    
    def find_by_publisher(self, publisher: str, book_type: Optional[str] = None) -> List[Book]:
        """Lấy sách theo nhà xuất bản, có thể lọc theo loại"""
        if book_type:
            query = "SELECT * FROM books WHERE publisher = %s AND book_type = %s ORDER BY book_name"
            params = (publisher, book_type)
        else:
            query = "SELECT * FROM books WHERE publisher = %s ORDER BY book_name"
            params = (publisher,)
        
        rows = self._execute_query(query, params, fetch_all=True)
        return [self._row_to_book(row) for row in rows if self._row_to_book(row)]
    
    def create(self, book: Book) -> int:
        """Tạo sách mới"""
        if isinstance(book, TextBook):
            sql = """INSERT INTO books 
                     (book_code, book_name, book_type, import_date, price, quantity, 
                      publisher, condition_status, image, description)
                     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            params = (
                book.book_code, book.book_name, book.get_book_type(), book.import_date,
                book.price, book.quantity, book.publisher, book.condition_status,
                book.image, book.description
            )
        elif isinstance(book, ReferenceBook):
            sql = """INSERT INTO books 
                     (book_code, book_name, book_type, import_date, price, quantity, 
                      publisher, tax, image, description)
                     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            params = (
                book.book_code, book.book_name, book.get_book_type(), book.import_date,
                book.price, book.quantity, book.publisher, book.tax,
                book.image, book.description
            )
        else:
            raise ValueError("Invalid book type")
        
        return self._execute_query(sql, params)
    
    def update(self, book_id: int, book: Book) -> bool:
        """Cập nhật sách"""
        if isinstance(book, TextBook):
            sql = """UPDATE books SET 
                     book_name=%s, import_date=%s, price=%s, quantity=%s, 
                     publisher=%s, condition_status=%s, description=%s
                     WHERE book_id=%s"""
            params = (
                book.book_name, book.import_date, book.price, book.quantity,
                book.publisher, book.condition_status, book.description, book_id
            )
        elif isinstance(book, ReferenceBook):
            sql = """UPDATE books SET 
                     book_name=%s, import_date=%s, price=%s, quantity=%s, 
                     publisher=%s, tax=%s, description=%s
                     WHERE book_id=%s"""
            params = (
                book.book_name, book.import_date, book.price, book.quantity,
                book.publisher, book.tax, book.description, book_id
            )
        else:
            raise ValueError("Invalid book type")
        
        self._execute_query(sql, params)
        return True
    
    def delete(self, book_id: int) -> bool:
        """Xóa sách"""
        self._execute_query("DELETE FROM books WHERE book_id = %s", (book_id,))
        return True