from flask import Blueprint, jsonify, request
from app.controllers.borrow_controller import BorrowController
from app.utils.helpers import success, error

bp = Blueprint('borrow', __name__, url_prefix='/api/borrow')
ctrl = BorrowController()

@bp.route('', methods=['POST'])
def borrow_book():
    data = request.json or {}
    borrow_id = ctrl.borrow(data)
    return jsonify(success({'borrow_id': borrow_id}, 'Borrow recorded'))

@bp.route('', methods=['GET'])
def list_borrows():
    return jsonify(success(ctrl.get_all()))
