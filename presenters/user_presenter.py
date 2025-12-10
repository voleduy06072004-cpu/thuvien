from app.controllers.user_controller import UserController

class UserPresenter:
    def __init__(self):
        self.ctrl = UserController()

    def get_all_users(self):
        rows = self.ctrl.get_all()
        return rows

    def get_user(self, user_id):
        return self.ctrl.get(user_id)

    def create_user(self, form):
        data = {
            'account_id': form.get('account_id'),
            'full_name': form.get('full_name'),
            'age': form.get('age'),
            'email': form.get('email'),
            'phone': form.get('phone'),
            'gender': form.get('gender'),
            'address': form.get('address'),
        }
        return self.ctrl.create(data)

    def update_user(self, user_id, form):
        data = {
            'full_name': form.get('full_name'),
            'age': form.get('age'),
            'email': form.get('email'),
            'phone': form.get('phone'),
            'gender': form.get('gender'),
            'address': form.get('address'),
        }
        return self.ctrl.update(user_id, data)

    def delete_user(self, user_id):
        return self.ctrl.delete(user_id)