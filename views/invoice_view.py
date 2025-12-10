from flask import Blueprint, jsonify, request
from app.controllers.invoice_controller import InvoiceController
from app.utils.helpers import success, error

bp = Blueprint('invoices', __name__, url_prefix='/api/invoices')
ctrl = InvoiceController()

@bp.route('', methods=['POST'])
def create_invoice():
    data = request.json or {}
    invoice = data.get('invoice')
    details = data.get('details', [])
    if not invoice or not details:
        return jsonify(error('invoice and details required')), 400
    inv_id = ctrl.create_invoice(invoice, details)
    return jsonify(success({'invoice_id': inv_id}, 'Invoice created'))

@bp.route('', methods=['GET'])
def get_invoices():
    return jsonify(success(ctrl.get_all()))
