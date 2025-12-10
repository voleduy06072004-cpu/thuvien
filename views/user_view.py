from flask import Blueprint, render_template, request, redirect, url_for
from app.presenters.user_presenter import UserPresenter

bp = Blueprint('user_web', __name__, url_prefix='/users')
presenter = UserPresenter()

@bp.route('/', methods=['GET'])
def list_users():
    users = presenter.get_all_users()
    return render_template("users.html", users=users)

# Hiển thị form sửa user
@bp.route('/edit/<int:user_id>', methods=['GET'])
def edit_user(user_id):
    user = presenter.get_user(user_id)
    if not user:
        return redirect(url_for("user_web.list_users"))
    return render_template("edit_user.html", user=user)

# ADD USER FORM
@bp.route('/add', methods=['POST'])
def add_user():
    presenter.create_user(request.form)
    return redirect(url_for("user_web.list_users"))

# UPDATE USER FORM
@bp.route('/update/<int:user_id>', methods=['POST'])
def update_user(user_id):
    presenter.update_user(user_id, request.form)
    return redirect(url_for("user_web.list_users"))

# DELETE
@bp.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    presenter.delete_user(user_id)
    return redirect(url_for("user_web.list_users"))