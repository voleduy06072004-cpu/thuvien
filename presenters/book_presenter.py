from app.models.book_model import Book, TextBook, ReferenceBook
from typing import List, Optional, Dict
from datetime import datetime

class BookPresenter:
    """
    Presenter - Chịu trách nhiệm format và transform dữ liệu cho View
    Tuân thủ SRP: chỉ lo presentation logic, không có business logic
    """
    
    # ========== List Presentations ==========
    
    @staticmethod
    def present_books_list(books_data: List[Book], message: Optional[str] = None, 
                          error: Optional[str] = None, search_query: Optional[str] = None) -> dict:
        """Chuẩn bị dữ liệu cho template danh sách sách"""
        transformed_books = [BookPresenter._transform_book_for_list(book) for book in books_data]
        
        return {
            'books': transformed_books,
            'message': message,
            'error': error,
            'search_query': search_query or '',
            'books_count': len(transformed_books)
        }
    
    @staticmethod
    def present_books_by_type(books_data: List[Book], book_type: str) -> dict:
        """Chuẩn bị dữ liệu cho danh sách sách theo loại"""
        transformed_books = [BookPresenter._transform_book_for_list(book) for book in books_data]
        total_amount = sum(book.calculate_total_amount() for book in books_data)
        
        return {
            'books': transformed_books,
            'book_type': book_type,
            'books_count': len(transformed_books),
            'total_amount': total_amount,
            'formatted_total_amount': f"{total_amount:,.0f} VND"
        }
    
    @staticmethod
    def present_books_by_publisher(books_data: List[Book], publisher: str, 
                                   book_type: Optional[str] = None) -> dict:
        """Chuẩn bị dữ liệu cho danh sách sách theo nhà xuất bản"""
        transformed_books = [BookPresenter._transform_book_for_list(book) for book in books_data]
        
        return {
            'books': transformed_books,
            'publisher': publisher,
            'book_type': book_type,
            'books_count': len(transformed_books)
        }
    
    # ========== Form Presentations ==========
    
    @staticmethod
    def present_create_form(book_type: Optional[str] = None, 
                           message: Optional[str] = None, 
                           error: Optional[str] = None) -> dict:
        """Chuẩn bị dữ liệu cho form tạo sách mới"""
        return {
            'book': None,
            'book_type': book_type,
            'book_types': ['Sách giáo khoa', 'Sách tham khảo'],
            'condition_statuses': ['mới', 'cũ'],
            'default_date': datetime.now().strftime('%Y-%m-%d'),
            'message': message,
            'error': error,
            'is_edit': False
        }
    
    @staticmethod
    def present_edit_form(book_data: Book, message: Optional[str] = None, 
                         error: Optional[str] = None) -> dict:
        """Chuẩn bị dữ liệu cho form chỉnh sửa"""
        transformed_book = BookPresenter._transform_book_for_form(book_data)
        
        return {
            'book': transformed_book,
            'book_type': book_data.get_book_type(),
            'book_types': ['Sách giáo khoa', 'Sách tham khảo'],
            'condition_statuses': ['mới', 'cũ'],
            'message': message,
            'error': error,
            'is_edit': True
        }
    
    # ========== Statistics Presentation ==========
    
    @staticmethod
    def present_statistics(stats_data: Dict) -> dict:
        """Chuẩn bị dữ liệu thống kê cho view"""
        return {
            'total_books': stats_data['total_books'],
            'total_textbooks': stats_data['total_textbooks'],
            'total_reference_books': stats_data['total_reference_books'],
            'total_amount_textbooks': stats_data['total_amount_textbooks'],
            'total_amount_reference_books': stats_data['total_amount_reference_books'],
            'average_price_reference_books': stats_data['average_price_reference_books'],
            'total_amount_all': stats_data['total_amount_all'],
            # Formatted versions
            'formatted_total_amount_textbooks': f"{stats_data['total_amount_textbooks']:,.0f} VND",
            'formatted_total_amount_reference': f"{stats_data['total_amount_reference_books']:,.0f} VND",
            'formatted_average_price': f"{stats_data['average_price_reference_books']:,.0f} VND",
            'formatted_total_amount_all': f"{stats_data['total_amount_all']:,.0f} VND"
        }
    
    # ========== Helper Methods ==========
    
    @staticmethod
    def _transform_book_for_list(book: Book) -> dict:
        """Transform đối tượng Book cho hiển thị trong danh sách"""
        if not book:
            return {}
        
        base_data = {
            'book_id': book.book_id,
            'book_code': book.book_code,
            'book_name': book.book_name,
            'book_type': book.get_book_type(),
            'price': book.price,
            'quantity': book.quantity,
            'publisher': book.publisher,
            'import_date': book.import_date.strftime('%Y-%m-%d') if book.import_date else '',
            'description': book.description,
            'formatted_price': f"{book.price:,.0f} VND",
            'formatted_import_date': BookPresenter._format_date(book.import_date),
            'total_amount': book.calculate_total_amount(),
            'formatted_total_amount': f"{book.calculate_total_amount():,.0f} VND"
        }
        
        # Thêm field đặc thù theo loại sách
        if isinstance(book, TextBook):
            base_data['condition_status'] = book.condition_status
        elif isinstance(book, ReferenceBook):
            base_data['tax'] = book.tax
            base_data['formatted_tax'] = f"{book.tax:,.0f} VND"
        
        return base_data
    
    @staticmethod
    def _transform_book_for_form(book: Book) -> dict:
        """Transform đối tượng Book cho hiển thị trong form"""
        if not book:
            return {}
        
        base_data = {
            'book_id': book.book_id,
            'book_code': book.book_code,
            'book_name': book.book_name,
            'price': book.price,
            'quantity': book.quantity,
            'publisher': book.publisher,
            'import_date': book.import_date.strftime('%Y-%m-%d') if book.import_date else '',
            'description': book.description
        }
        
        # Thêm field đặc thù
        if isinstance(book, TextBook):
            base_data['condition_status'] = book.condition_status
        elif isinstance(book, ReferenceBook):
            base_data['tax'] = book.tax
        
        return base_data
    
    @staticmethod
    def _format_date(date_obj: Optional[datetime]) -> str:
        """Định dạng ngày tháng cho hiển thị"""
        if not date_obj:
            return ""
        try:
            return date_obj.strftime('%d/%m/%Y')
        except:
            return str(date_obj)
    
    @staticmethod
    def _format_currency(amount: float) -> str:
        """Định dạng tiền tệ"""
        return f"{amount:,.0f} VND"