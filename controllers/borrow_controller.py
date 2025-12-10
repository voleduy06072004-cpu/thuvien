from app.models.borrow_model import BorrowModel

class BorrowController:
    def borrow(self, data):
        return BorrowModel.borrow(data)

    def get_all(self):
        return BorrowModel.get_all()
