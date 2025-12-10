from flask import Blueprint, jsonify, request, current_app
from app.controllers.account_controller import AccountController
from app.utils.helpers import success, error
import jwt, datetime
ctrl = AccountController()
bp = Blueprint('accounts', __name__, url_prefix='/api/accounts')

SECRET = 'supersecret_jwt_key_change_me'

@bp.route('/register', methods=['POST'])
def register():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')
    role = data.get('role','user')
    if not username or not password:
        return jsonify(error('username and password required')), 400
    acc = ctrl.get_by_username(username)
    if acc:
        return jsonify(error('username exists')), 400
    acc_id = ctrl.create(username, password, role)
    return jsonify(success({'account_id': acc_id}, 'Account created'))

@bp.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')
    acc = ctrl.get_by_username(username)
    if not acc or acc.get('password') != password:
        return jsonify(error('invalid credentials')), 401
    payload = {
        'account_id': acc.get('account_id'),
        'username': acc.get('username'),
        'role': acc.get('role'),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    }
    token = jwt.encode(payload, SECRET, algorithm='HS256')
    return jsonify(success({'token': token}, 'Login success'))
