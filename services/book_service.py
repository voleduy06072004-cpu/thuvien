from app.interfaces.book_service_interface import BookServiceInterface
from app.interfaces.book_repository_interface import BookRepositoryInterface
from app.models.book_model import Book, TextBook, ReferenceBook
from app.validators.book_validator import BookValidator
from typing import List, Optional, Tuple, Dict

class BookService(BookServiceInterface):
    """
    Concrete implementation của Book Service
    Chịu trách nhiệm: Business logic, orchestration, validation
    Tuân thủ SRP: không trực tiếp làm việc với database
    """
    
    def __init__(self, book_repository: BookRepositoryInterface):
        self.book_repository = book_repository
        self.validator = BookValidator()
    
    # ========== CRUD Operations ==========
    
    def get_all_books(self) -> List[Book]:
        """Lấy tất cả sách"""
        return self.book_repository.find_all()
    
    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """Lấy sách theo ID"""
        return self.book_repository.find_by_id(book_id)
    
    def search_books(self, query: str) -> List[Book]:
        """Tìm kiếm sách theo tên"""
        return self.book_repository.search_by_name(query)
    
    def create_book(self, book_data: dict) -> Tuple[bool, str, Optional[int]]:
        """Tạo sách mới"""
        # Lấy loại sách
        book_type = book_data.get('book_type')
        
        # Validate loại sách
        is_valid, message = self.validator.validate_book_type(book_type)
        if not is_valid:
            return False, message, None
        
        # Validate theo loại sách
        if book_type == 'Sách giáo khoa':
            is_valid, message = self.validator.validate_textbook(book_data)
        else:  # Sách tham khảo
            is_valid, message = self.validator.validate_reference_book(book_data)
        
        if not is_valid:
            return False, message, None
        
        # Business rule: Kiểm tra mã sách trùng
        if self.book_repository.find_by_code(book_data['book_code']):
            return False, "Mã sách đã tồn tại", None
        
        # Tạo đối tượng Book tương ứng
        try:
            if book_type == 'Sách giáo khoa':
                book = TextBook.from_dict(book_data)
            else:
                book = ReferenceBook.from_dict(book_data)
            
            book_id = self.book_repository.create(book)
            return True, "Thêm sách thành công", book_id
        except Exception as e:
            return False, f"Lỗi khi thêm sách: {str(e)}", None
    
    def update_book(self, book_id: int, book_data: dict) -> Tuple[bool, str]:
        """Cập nhật sách"""
        # Kiểm tra sách tồn tại
        existing_book = self.book_repository.find_by_id(book_id)
        if not existing_book:
            return False, "Không tìm thấy sách"
        
        # Validate theo loại sách
        book_type = existing_book.get_book_type()
        if book_type == 'Sách giáo khoa':
            is_valid, message = self.validator.validate_textbook(book_data)
            book = TextBook.from_dict(book_data)
        else:
            is_valid, message = self.validator.validate_reference_book(book_data)
            book = ReferenceBook.from_dict(book_data)
        
        if not is_valid:
            return False, message
        
        try:
            book.book_id = book_id
            self.book_repository.update(book_id, book)
            return True, "Cập nhật sách thành công"
        except Exception as e:
            return False, f"Lỗi khi cập nhật sách: {str(e)}"
    
    def delete_book(self, book_id: int) -> Tuple[bool, str]:
        """Xóa sách"""
        # Kiểm tra sách tồn tại
        existing_book = self.book_repository.find_by_id(book_id)
        if not existing_book:
            return False, "Không tìm thấy sách"
        
        try:
            self.book_repository.delete(book_id)
            return True, "Xóa sách thành công"
        except Exception as e:
            return False, f"Lỗi khi xóa sách: {str(e)}"
    
    # ========== Business Logic Methods (Theo yêu cầu đề bài) ==========
    
    def get_books_by_type(self, book_type: str) -> List[Book]:
        """Lấy sách theo loại"""
        return self.book_repository.find_by_type(book_type)
    
    def get_books_by_publisher(self, publisher: str, book_type: Optional[str] = None) -> List[Book]:
        """
        Xuất ra các sách theo nhà xuất bản
        Nếu book_type = 'Sách giáo khoa' thì xuất sách giáo khoa của NXB đó
        """
        return self.book_repository.find_by_publisher(publisher, book_type)
    
    def calculate_total_amount_by_type(self, book_type: str) -> float:
        """
        Tính tổng thành tiền cho từng loại sách
        - Sách giáo khoa: tính theo condition_status
        - Sách tham khảo: tính có thuế
        """
        books = self.book_repository.find_by_type(book_type)
        total = sum(book.calculate_total_amount() for book in books)
        return total
    
    def calculate_average_price_reference_books(self) -> float:
        """Tính trung bình cộng đơn giá của các sách tham khảo"""
        reference_books = self.book_repository.find_by_type('Sách tham khảo')
        
        if not reference_books:
            return 0.0
        
        total_price = sum(book.price for book in reference_books)
        return total_price / len(reference_books)
    
    def get_statistics(self) -> Dict:
        """
        Lấy thống kê tổng quan
        Trả về dictionary chứa các thông tin thống kê
        """
        all_books = self.get_all_books()
        textbooks = [b for b in all_books if b.get_book_type() == 'Sách giáo khoa']
        reference_books = [b for b in all_books if b.get_book_type() == 'Sách tham khảo']
        
        return {
            'total_books': len(all_books),
            'total_textbooks': len(textbooks),
            'total_reference_books': len(reference_books),
            'total_amount_textbooks': self.calculate_total_amount_by_type('Sách giáo khoa'),
            'total_amount_reference_books': self.calculate_total_amount_by_type('Sách tham khảo'),
            'average_price_reference_books': self.calculate_average_price_reference_books(),
            'total_amount_all': sum(book.calculate_total_amount() for book in all_books)
        }
    
    def validate_book_data(self, book_data: dict) -> Tuple[bool, str]:
        """Validate dữ liệu sách (wrapper method)"""
        book_type = book_data.get('book_type')
        
        if book_type == 'Sách giáo khoa':
            return self.validator.validate_textbook(book_data)
        elif book_type == 'Sách tham khảo':
            return self.validator.validate_reference_book(book_data)
        else:
            return False, "Loại sách không hợp lệ"