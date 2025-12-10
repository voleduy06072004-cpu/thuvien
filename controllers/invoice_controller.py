from app.models.invoice_model import InvoiceModel

class InvoiceController:
    def create_invoice(self, invoice, details):
        invoice_id = InvoiceModel.create(invoice)
        for d in details:
            InvoiceModel.add_detail(invoice_id, d)
        return invoice_id

    def get_all(self):
        return InvoiceModel.get_all()
