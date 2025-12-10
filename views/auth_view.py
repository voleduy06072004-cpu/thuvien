from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.config.db_config import get_db_connection

bp = Blueprint("auth", __name__)

# ==== Đăng ký ====
@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        full_name = request.form["full_name"]
        email = request.form["email"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # kiểm tra username tồn tại
        cursor.execute("SELECT * FROM accounts WHERE username=%s", (username,))
        existing = cursor.fetchone()

        if existing:
            flash("Tên đăng nhập đã tồn tại!", "danger")
            cursor.close()
            conn.close()
            return render_template("register.html")

        hashed_pw = generate_password_hash(password)
        cursor.execute("INSERT INTO accounts (username, password, role) VALUES (%s, %s, %s)",
                       (username, hashed_pw, 'user'))
        conn.commit()

        # Tạo user info
        cursor.execute("SELECT account_id FROM accounts WHERE username=%s", (username,))
        acc = cursor.fetchone()
        cursor.execute("INSERT INTO users (account_id, full_name, email) VALUES (%s, %s, %s)",
                       (acc["account_id"], full_name, email))
        conn.commit()

        cursor.close()
        conn.close()

        flash("Đăng ký thành công! Hãy đăng nhập.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

# ==== Đăng nhập ====
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM accounts WHERE username=%s", (username,))
        account = cursor.fetchone()

        if account and check_password_hash(account["password"], password):
            session["user_id"] = account["account_id"]
            session["role"] = account["role"]
            session["username"] = account["username"]

            cursor.close()
            conn.close()

            flash("Đăng nhập thành công!", "success")
            return redirect(url_for("index"))  # Chuyển hướng đến trang chủ
        else:
            flash("Sai tên đăng nhập hoặc mật khẩu!", "danger")
            cursor.close()
            conn.close()
            return render_template("login.html")

    return render_template("login.html")

# ==== Đăng xuất ====
@bp.route("/logout")
def logout():
    session.clear()
    flash("Đã đăng xuất!", "info")
    return redirect(url_for("auth.login"))