from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from app.controllers.book_controller import BookController
from app.presenters.book_presenter import BookPresenter
from app.utils.helpers import success, error

# Blueprint cho Web UI
book_web_bp = Blueprint('book_web', __name__)
# Blueprint cho API
book_api_bp = Blueprint('book_api', __name__)

# Khởi tạo controller và presenter
ctrl = BookController()
presenter = BookPresenter()

# ===== WEB UI ROUTES =====

@book_web_bp.route('', methods=['GET'])
def books_page():
    """Trang danh sách tất cả sách"""
    try:
        search_query = request.args.get('q', '')
        
        if search_query:
            books_data = ctrl.search_books(search_query)
        else:
            books_data = ctrl.get_all_books()
            
        template_data = presenter.present_books_list(books_data, search_query=search_query)
        return render_template('books.html', **template_data)
        
    except Exception as e:
        template_data = presenter.present_books_list([], error=f"Lỗi: {str(e)}")
        return render_template('books.html', **template_data)

@book_web_bp.route('/type/<book_type>', methods=['GET'])
def books_by_type_page(book_type):
    """In danh sách sách theo loại (Giáo khoa / Tham khảo)"""
    try:
        books_data = ctrl.get_books_by_type(book_type)
        template_data = presenter.present_books_by_type(books_data, book_type)
        return render_template('books_by_type.html', **template_data)
    except Exception as e:
        flash(f"Lỗi: {str(e)}", 'error')
        return redirect(url_for('book_web.books_page'))

@book_web_bp.route('/publisher/<publisher>', methods=['GET'])
def books_by_publisher_page(publisher):
    """Xuất ra các sách của nhà xuất bản"""
    try:
        book_type = request.args.get('type')  # Optional filter
        books_data = ctrl.get_books_by_publisher(publisher, book_type)
        template_data = presenter.present_books_by_publisher(books_data, publisher, book_type)
        return render_template('books_by_publisher.html', **template_data)
    except Exception as e:
        flash(f"Lỗi: {str(e)}", 'error')
        return redirect(url_for('book_web.books_page'))

@book_web_bp.route('/statistics', methods=['GET'])
def statistics_page():
    """Trang thống kê"""
    try:
        stats_data = ctrl.get_statistics()
        template_data = presenter.present_statistics(stats_data)
        return render_template('statistics.html', **template_data)
    except Exception as e:
        flash(f"Lỗi: {str(e)}", 'error')
        return redirect(url_for('book_web.books_page'))

@book_web_bp.route('/create', methods=['GET'])
def create_book_form():
    """Hiển thị form tạo sách mới"""
    book_type = request.args.get('type', 'Sách giáo khoa')
    template_data = presenter.present_create_form(book_type)
    return render_template('book_form.html', **template_data)

@book_web_bp.route('/create', methods=['POST'])
def create_book():
    """Xử lý tạo sách mới"""
    try:
        data = request.form.to_dict()
        success_result, message, book_id = ctrl.create_book(data)
        
        if success_result:
            flash(f"{message} - Mã sách: {book_id}", 'success')
            return redirect(url_for('book_web.books_page'))
        else:
            flash(message, 'error')
            # Redirect về trang tạo sách với dữ liệu đã nhập
            return redirect(url_for('book_web.create_book_form'))
            
    except Exception as e:
        flash(f"Lỗi: {str(e)}", 'error')
        return redirect(url_for('book_web.books_page'))

@book_web_bp.route('/<int:book_id>/edit', methods=['GET'])
def edit_book_page(book_id):
    """Hiển thị form chỉnh sửa sách"""
    try:
        book_data = ctrl.get_book_by_id(book_id)
        if not book_data:
            flash("Không tìm thấy sách", 'error')
            return redirect(url_for('book_web.books_page'))
            
        template_data = presenter.present_edit_form(book_data)
        return render_template('book_form.html', **template_data)
        
    except Exception as e:
        flash(f"Lỗi: {str(e)}", 'error')
        return redirect(url_for('book_web.books_page'))

@book_web_bp.route('/<int:book_id>/update', methods=['POST'])
def update_book(book_id):
    """Xử lý cập nhật sách"""
    try:
        data = request.form.to_dict()
        success_result, message = ctrl.update_book(book_id, data)
        
        if success_result:
            flash(message, 'success')
        else:
            flash(message, 'error')
            
        return redirect(url_for('book_web.books_page'))
            
    except Exception as e:
        flash(f"Lỗi: {str(e)}", 'error')
        return redirect(url_for('book_web.books_page'))

@book_web_bp.route('/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """Xử lý xóa sách"""
    try:
        success_result, message = ctrl.delete_book(book_id)
        
        if success_result:
            flash(message, 'success')
        else:
            flash(message, 'error')
            
        return redirect(url_for('book_web.books_page'))
            
    except Exception as e:
        flash(f"Lỗi: {str(e)}", 'error')
        return redirect(url_for('book_web.books_page'))

# ===== API ROUTES =====

@book_api_bp.route('', methods=['GET'])
def get_books_api():
    """API: Lấy danh sách sách (có thể tìm kiếm)"""
    try:
        q = request.args.get('q')
        book_type = request.args.get('type')
        
        if q:
            books = ctrl.search_books(q)
        elif book_type:
            books = ctrl.get_books_by_type(book_type)
        else:
            books = ctrl.get_all_books()
        
        books_data = [book.to_dict() for book in books]
        return jsonify(success(books_data))
    except Exception as e:
        return jsonify(error(f"Lỗi: {str(e)}")), 500

@book_api_bp.route('/<int:book_id>', methods=['GET'])
def get_book_api(book_id):
    """API: Lấy thông tin chi tiết sách"""
    try:
        book = ctrl.get_book_by_id(book_id)
        if book:
            return jsonify(success(book.to_dict()))
        return jsonify(error('Không tìm thấy sách')), 404
    except Exception as e:
        return jsonify(error(f"Lỗi: {str(e)}")), 500

@book_api_bp.route('', methods=['POST'])
def add_book_api():
    """API: Thêm sách mới"""
    try:
        data = request.json or {}
        
        # Kiểm tra trường bắt buộc
        required = ['book_code', 'book_name', 'book_type', 'price', 'quantity', 'publisher']
        missing = [f for f in required if not data.get(f)]
        if missing:
            return jsonify(error(f"Thiếu trường: {', '.join(missing)}")), 400

        success_result, message, book_id = ctrl.create_book(data)
        
        if success_result:
            return jsonify(success({'book_id': book_id}, message)), 201
        else:
            return jsonify(error(message)), 400
        
    except Exception as e:
        return jsonify(error(f"Lỗi: {str(e)}")), 500

@book_api_bp.route('/<int:book_id>', methods=['PUT'])
def update_book_api(book_id):
    """API: Cập nhật sách"""
    try:
        data = request.json or {}
        success_result, message = ctrl.update_book(book_id, data)
        
        if success_result:
            return jsonify(success(message=message))
        else:
            return jsonify(error(message)), 400
    except Exception as e:
        return jsonify(error(f"Lỗi: {str(e)}")), 500

@book_api_bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book_api(book_id):
    """API: Xóa sách"""
    try:
        success_result, message = ctrl.delete_book(book_id)
        
        if success_result:
            return jsonify(success(message=message))
        else:
            return jsonify(error(message)), 400
    except Exception as e:
        return jsonify(error(f"Lỗi: {str(e)}")), 500

# ===== API ROUTES - Business Logic =====

@book_api_bp.route('/statistics', methods=['GET'])
def get_statistics_api():
    """API: Lấy thống kê"""
    try:
        stats = ctrl.get_statistics()
        return jsonify(success(stats))
    except Exception as e:
        return jsonify(error(f"Lỗi: {str(e)}")), 500

@book_api_bp.route('/publisher/<publisher>', methods=['GET'])
def get_books_by_publisher_api(publisher):
    """API: Lấy sách theo nhà xuất bản"""
    try:
        book_type = request.args.get('type')
        books = ctrl.get_books_by_publisher(publisher, book_type)
        books_data = [book.to_dict() for book in books]
        return jsonify(success(books_data))
    except Exception as e:
        return jsonify(error(f"Lỗi: {str(e)}")), 500