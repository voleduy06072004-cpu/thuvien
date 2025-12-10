from app.services.book_service import BookService
from app.repositories.book_repository import BookRepository
from typing import List, Optional, Tuple, Dict
from app.models.book_model import Book

class BookController:
    """
    Controller - Điều phối giữa View và Service
    Chịu trách nhiệm: Nhận request từ View, gọi Service, trả về response
    Tuân thủ SRP: không chứa business logic hay database logic
    
    Note: Trong kiến trúc này, Controller đóng vai trò là "thin layer"
    để giữ cho code có cấu trúc rõ ràng theo MVPC pattern
    """
    
    def __init__(self, book_service: Optional[BookService] = None):
        """
        Dependency Injection: Nhận service từ bên ngoài
        Nếu không truyền vào thì tạo mới (để tương thích với code cũ)
        """
        if book_service:
            self.book_service = book_service
        else:
            # Fallback: tạo dependencies
            book_repository = BookRepository()
            self.book_service = BookService(book_repository)
    
    # ========== CRUD Operations ==========
    
    def get_all_books(self) -> List[Book]:
        """Lấy tất cả sách"""
        return self.book_service.get_all_books()
    
    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """Lấy sách theo ID"""
        return self.book_service.get_book_by_id(book_id)
    
    def search_books(self, query: str) -> List[Book]:
        """Tìm kiếm sách"""
        return self.book_service.search_books(query)
    
    def create_book(self, book_data: dict) -> Tuple[bool, str, Optional[int]]:
        """Tạo sách mới"""
        return self.book_service.create_book(book_data)
    
    def update_book(self, book_id: int, book_data: dict) -> Tuple[bool, str]:
        """Cập nhật sách"""
        return self.book_service.update_book(book_id, book_data)
    
    def delete_book(self, book_id: int) -> Tuple[bool, str]:
        """Xóa sách"""
        return self.book_service.delete_book(book_id)
    
    # ========== Business Methods (Theo yêu cầu đề bài) ==========
    
    def get_books_by_type(self, book_type: str) -> List[Book]:
        """In danh sách sách theo loại"""
        return self.book_service.get_books_by_type(book_type)
    
    def get_textbooks_by_publisher(self, publisher: str) -> List[Book]:
        """Xuất ra các sách giáo khoa của nhà xuất bản"""
        return self.book_service.get_books_by_publisher(publisher, 'Sách giáo khoa')
    
    def get_books_by_publisher(self, publisher: str, book_type: Optional[str] = None) -> List[Book]:
        """Xuất ra các sách của nhà xuất bản (có thể lọc theo loại)"""
        return self.book_service.get_books_by_publisher(publisher, book_type)
    
    def calculate_total_amount_textbooks(self) -> float:
        """Tính tổng thành tiền sách giáo khoa"""
        return self.book_service.calculate_total_amount_by_type('Sách giáo khoa')
    
    def calculate_total_amount_reference_books(self) -> float:
        """Tính tổng thành tiền sách tham khảo"""
        return self.book_service.calculate_total_amount_by_type('Sách tham khảo')
    
    def calculate_average_price_reference_books(self) -> float:
        """Tính trung bình cộng đơn giá của các sách tham khảo"""
        return self.book_service.calculate_average_price_reference_books()
    
    def get_statistics(self) -> Dict:
        """Lấy thống kê tổng quan"""
        return self.book_service.get_statistics()
    
    def validate_book_data(self, book_data: dict) -> Tuple[bool, str]:
        """Validate dữ liệu sách"""
        return self.book_service.validate_book_data(book_data)