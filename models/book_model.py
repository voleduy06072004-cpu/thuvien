from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from abc import ABC, abstractmethod

@dataclass
class Book(ABC):
    """Base Model - Đại diện cho sách (Abstract)"""
    book_id: Optional[int] = None
    book_code: str = ""
    book_name: str = ""
    import_date: Optional[datetime] = None
    price: float = 0.0
    quantity: int = 0
    publisher: str = ""
    image: str = ""
    description: str = ""
    
    @abstractmethod
    def calculate_total_amount(self) -> float:
        """Tính thành tiền - mỗi loại sách có cách tính khác nhau"""
        pass
    
    @abstractmethod
    def get_book_type(self) -> str:
        """Trả về loại sách"""
        pass
    
    def to_dict(self) -> dict:
        """Chuyển đổi đối tượng Book thành dictionary"""
        return {
            'book_id': self.book_id,
            'book_code': self.book_code,
            'book_name': self.book_name,
            'book_type': self.get_book_type(),
            'import_date': self.import_date.isoformat() if self.import_date else None,
            'price': self.price,
            'quantity': self.quantity,
            'publisher': self.publisher,
            'image': self.image,
            'description': self.description,
            'total_amount': self.calculate_total_amount()
        }


@dataclass
class TextBook(Book):
    """Sách giáo khoa - có tình trạng (mới/cũ)"""
    condition_status: str = "mới"  # mới hoặc cũ
    
    def calculate_total_amount(self) -> float:
        """
        Tính thành tiền cho sách giáo khoa:
        - Nếu mới: số lượng * đơn giá
        - Nếu cũ: số lượng * đơn giá * 50%
        """
        base_amount = self.quantity * self.price
        if self.condition_status.lower() == "cũ":
            return base_amount * 0.5
        return base_amount
    
    def get_book_type(self) -> str:
        return "Sách giáo khoa"
    
    def to_dict(self) -> dict:
        data = super().to_dict()
        data['condition_status'] = self.condition_status
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TextBook':
        """Tạo đối tượng TextBook từ dictionary"""
        import_date = data.get('import_date')
        if import_date and isinstance(import_date, str):
            try:
                import_date = datetime.fromisoformat(import_date.replace('Z', '+00:00'))
            except ValueError:
                import_date = None
        
        return cls(
            book_id=data.get('book_id'),
            book_code=data.get('book_code', ''),
            book_name=data.get('book_name', ''),
            import_date=import_date,
            price=float(data.get('price', 0)),
            quantity=int(data.get('quantity', 0)),
            publisher=data.get('publisher', ''),
            image=data.get('image', ''),
            description=data.get('description', ''),
            condition_status=data.get('condition_status', 'mới')
        )


@dataclass
class ReferenceBook(Book):
    """Sách tham khảo - có thuế"""
    tax: float = 0.0
    
    def calculate_total_amount(self) -> float:
        """
        Tính thành tiền cho sách tham khảo:
        Thành tiền = số lượng * đơn giá + thuế
        """
        return (self.quantity * self.price) + self.tax
    
    def get_book_type(self) -> str:
        return "Sách tham khảo"
    
    def to_dict(self) -> dict:
        data = super().to_dict()
        data['tax'] = self.tax
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ReferenceBook':
        """Tạo đối tượng ReferenceBook từ dictionary"""
        import_date = data.get('import_date')
        if import_date and isinstance(import_date, str):
            try:
                import_date = datetime.fromisoformat(import_date.replace('Z', '+00:00'))
            except ValueError:
                import_date = None
        
        return cls(
            book_id=data.get('book_id'),
            book_code=data.get('book_code', ''),
            book_name=data.get('book_name', ''),
            import_date=import_date,
            price=float(data.get('price', 0)),
            quantity=int(data.get('quantity', 0)),
            publisher=data.get('publisher', ''),
            image=data.get('image', ''),
            description=data.get('description', ''),
            tax=float(data.get('tax', 0))
        )