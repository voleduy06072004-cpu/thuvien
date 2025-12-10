from app.models.account_model import AccountModel

class AccountController:
    def create(self, username, password, role='user'):
        return AccountModel.create_account(username, password, role)

    def get_by_username(self, username):
        return AccountModel.get_by_username(username)
