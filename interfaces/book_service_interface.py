from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Dict
from app.models.book_model import Book

class BookServiceInterface(ABC):
    """Interface cho Book Service - Business Logic"""
    
    # CRUD Operations
    @abstractmethod
    def get_all_books(self) -> List[Book]:
        """Lấy tất cả sách"""
        pass
    
    @abstractmethod
    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """Lấy sách theo ID"""
        pass
    
    @abstractmethod
    def search_books(self, query: str) -> List[Book]:
        """Tìm kiếm sách"""
        pass
    
    @abstractmethod
    def create_book(self, book_data: dict) -> Tuple[bool, str, Optional[int]]:
        """Tạo sách mới"""
        pass
    
    @abstractmethod
    def update_book(self, book_id: int, book_data: dict) -> Tuple[bool, str]:
        """Cập nhật sách"""
        pass
    
    @abstractmethod
    def delete_book(self, book_id: int) -> Tuple[bool, str]:
        """Xóa sách"""
        pass
    
    # Business Logic Methods
    @abstractmethod
    def get_books_by_type(self, book_type: str) -> List[Book]:
        """Lấy sách theo loại"""
        pass
    
    @abstractmethod
    def get_books_by_publisher(self, publisher: str, book_type: Optional[str] = None) -> List[Book]:
        """Xuất ra các sách theo nhà xuất bản (có thể lọc theo loại)"""
        pass
    
    @abstractmethod
    def calculate_total_amount_by_type(self, book_type: str) -> float:
        """Tính tổng thành tiền cho từng loại sách"""
        pass
    
    @abstractmethod
    def calculate_average_price_reference_books(self) -> float:
        """Tính trung bình cộng đơn giá của các sách tham khảo"""
        pass
    
    @abstractmethod
    def get_statistics(self) -> Dict:
        """Lấy thống kê tổng quan"""
        pass
    
    @abstractmethod
    def validate_book_data(self, book_data: dict) -> Tuple[bool, str]:
        """Validate dữ liệu sách"""
        pass