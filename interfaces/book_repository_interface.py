from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Dict
from app.models.book_model import Book

class BookRepositoryInterface(ABC):
    """Interface cho Book Repository - Truy xuất dữ liệu"""
    
    @abstractmethod
    def find_all(self) -> List[Book]:
        """Lấy tất cả sách"""
        pass
    
    @abstractmethod
    def find_by_id(self, book_id: int) -> Optional[Book]:
        """Tìm sách theo ID"""
        pass
    
    @abstractmethod
    def find_by_code(self, book_code: str) -> Optional[Book]:
        """Tìm sách theo mã"""
        pass
    
    @abstractmethod
    def search_by_name(self, name: str) -> List[Book]:
        """Tìm kiếm sách theo tên"""
        pass
    
    @abstractmethod
    def find_by_type(self, book_type: str) -> List[Book]:
        """Lấy sách theo loại (Giáo khoa/Tham khảo)"""
        pass
    
    @abstractmethod
    def find_by_publisher(self, publisher: str, book_type: Optional[str] = None) -> List[Book]:
        """Lấy sách theo nhà xuất bản, có thể lọc theo loại"""
        pass
    
    @abstractmethod
    def create(self, book: Book) -> int:
        """Tạo sách mới"""
        pass
    
    @abstractmethod
    def update(self, book_id: int, book: Book) -> bool:
        """Cập nhật sách"""
        pass
    
    @abstractmethod
    def delete(self, book_id: int) -> bool:
        """Xóa sách"""
        pass
