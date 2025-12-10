from app.models.user_model import UserModel

class UserController:
    def get_all(self):
        return UserModel.get_all()

    def get(self, user_id):
        return UserModel.get_by_id(user_id)

    def create(self, data):
        return UserModel.add(data)

    def update(self, user_id, data):
        return UserModel.update(user_id, data)

    def delete(self, user_id):
        return UserModel.delete(user_id)
