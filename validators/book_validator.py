from typing import Tuple

class BookValidator:
    
    
    @staticmethod
    def validate_common_fields(book_data: dict) -> Tuple[bool, str]:
        """Validate các trường chung cho tất cả loại sách"""
        required_fields = ['book_code', 'book_name', 'price', 'quantity', 'publisher']
        
        # Kiểm tra trường bắt buộc
        for field in required_fields:
            if not book_data.get(field):
                return False, f"Thiếu trường bắt buộc: {field}"
        
        # Validate số
        try:
            price = float(book_data.get('price', 0))
            quantity = int(book_data.get('quantity', 0))
            
            if price < 0:
                return False, "Đơn giá không thể âm"
            if quantity < 0:
                return False, "Số lượng không thể âm"
                
        except (ValueError, TypeError):
            return False, "Đơn giá và số lượng phải là số hợp lệ"
        
        return True, "Dữ liệu hợp lệ"
    
    @staticmethod
    def validate_textbook(book_data: dict) -> Tuple[bool, str]:
        """Validate dữ liệu cho Sách giáo khoa"""
        # Validate common fields
        is_valid, message = BookValidator.validate_common_fields(book_data)
        if not is_valid:
            return False, message
        
        # Validate condition_status
        condition = book_data.get('condition_status', '').lower()
        if condition not in ['mới', 'cũ']:
            return False, "Tình trạng sách phải là 'mới' hoặc 'cũ'"
        
        return True, "Dữ liệu hợp lệ"
    
    @staticmethod
    def validate_reference_book(book_data: dict) -> Tuple[bool, str]:
        """Validate dữ liệu cho Sách tham khảo"""
        # Validate common fields
        is_valid, message = BookValidator.validate_common_fields(book_data)
        if not is_valid:
            return False, message
        
        # Validate tax
        try:
            tax = float(book_data.get('tax', 0))
            if tax < 0:
                return False, "Thuế không thể âm"
        except (ValueError, TypeError):
            return False, "Thuế phải là số hợp lệ"
        
        return True, "Dữ liệu hợp lệ"
    
    @staticmethod
    def validate_book_type(book_type: str) -> Tuple[bool, str]:
        """Validate loại sách"""
        valid_types = ['Sách giáo khoa', 'Sách tham khảo']
        if book_type not in valid_types:
            return False, f"Loại sách không hợp lệ. Phải là: {', '.join(valid_types)}"
        return True, "Loại sách hợp lệ"