from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'khoa_bi_mat_cua_ban'  # Cần thiết để sử dụng flash message và session

# --- PHẦN 1: CẤU HÌNH DATABASE (SQLite) ---
DB_NAME = "library.db"

def init_db():
    """Hàm này sẽ tạo bảng User nếu chưa tồn tại"""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()

# Gọi hàm tạo DB ngay khi chạy app
if not os.path.exists(DB_NAME):
    init_db()

# --- PHẦN 2: CÁC ROUTE (Đường dẫn) ---

@app.route('/')
def home():
    """Trang chủ là trang đăng nhập"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    """Xử lý logic Đăng ký"""
    fullname = request.form['fullname']
    email = request.form['email']
    password = request.form['password'] # Lưu ý: Thực tế nên mã hóa password (dùng bcrypt)

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (fullname, email, password) VALUES (?, ?, ?)", 
                           (fullname, email, password))
            conn.commit()
            flash('Đăng ký thành công! Hãy đăng nhập.', 'success')
    except sqlite3.IntegrityError:
        flash('Email này đã tồn tại!', 'error')
    except Exception as e:
        flash(f'Lỗi xảy ra: {e}', 'error')

    return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    """Xử lý logic Đăng nhập"""
    email = request.form['email']
    password = request.form['password']

    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row # Để lấy dữ liệu dạng từ điển
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user['id']
            session['fullname'] = user['fullname']
            return redirect(url_for('dashboard'))
        else:
            flash('Sai email hoặc mật khẩu!', 'error')
            return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    """Trang quản lý sau khi đăng nhập thành công"""
    if 'user_id' not in session:
        return redirect(url_for('home'))
    
    return f"<h1>Chào mừng {session['fullname']} đến với Hệ thống Quản lý Thư viện!</h1> <a href='/logout'>Đăng xuất</a>"

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('fullname', None)
    flash('Đã đăng xuất.', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)