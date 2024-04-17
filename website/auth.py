from operator import or_
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
import hashlib


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_or_username = request.form.get('email_or_username')  # Thêm input field cho username hoặc email
        password = request.form.get('password')

        # Kiểm tra xem người dùng nhập vào là email hay username
        user = User.query.filter(or_(User.email == email_or_username, User.user_name == email_or_username)).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email or username does not exist.', category='error')

    return render_template("login.html", user=current_user)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        user_name = request.form.get('userName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Kiểm tra các điều kiện và thông báo lỗi nếu có
        error = None
        if len(email) < 4:
            error = 'Email must be greater than 3 characters.'
        elif len(user_name) < 2:
<<<<<<< HEAD
            error = 'Username must be greater than 1 character.'
=======
            flash('User\'s name must be greater than 1 character.', category='error')
>>>>>>> 4b9c041851f17a034b1576d1961c3ec890aa0f9d
        elif password1 != password2:
            error = 'Passwords do not match.'
        elif len(password1) < 7:
            error = 'Password must be at least 7 characters.'

        if error is not None:
            flash(error, category='error')
            # Trả về form đăng ký với dữ liệu đã nhập
            return render_template("sign_up.html", user=current_user, email=email, user_name=user_name,
                                   security_question=security_question)
        else:
<<<<<<< HEAD
            # Tiếp tục quá trình đăng ký nếu không có lỗi
            hashed_password = sha256(password1.encode()).hexdigest()
            new_user = User(email=email, user_name=user_name, password=hashed_password,
                            security_question=security_question, security_answer=security_answer)
=======
            new_user = User(email=email, user_name=user_name, password=hashlib.sha256(password1.encode()).hexdigest())
>>>>>>> 4b9c041851f17a034b1576d1961c3ec890aa0f9d
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

<<<<<<< HEAD
    return render_template("sign_up.html", user=current_user)



@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    user = None  # Đặt giá trị mặc định cho user
    if request.method == 'POST':
        email = request.form.get('email')
        # Kiểm tra xem email có tồn tại trong cơ sở dữ liệu hay không
        user = User.query.filter_by(email=email).first()
        if user:
            # Chuyển hướng đến trang nhập câu hỏi bí mật
            return redirect(url_for('auth.secret_question', email=email))
        else:
            flash('Email does not exist.', category='error')
    return render_template("forgot_password.html", user=user)


@auth.route('/secret-question', methods=['GET', 'POST'])
def secret_question():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        return redirect(url_for('auth.login'))

    # Xử lý các câu hỏi bí mật ở đây
    if request.method == 'POST':
        security_answer = request.form.get('securityAnswer')
        # Kiểm tra câu trả lời có đúng không
        if user.security_answer == security_answer:
            # Nếu đúng, chuyển hướng đến trang đổi mật khẩu mới
            return redirect(url_for('auth.reset_password', email=email))
        else:
            # Nếu sai, hiển thị thông báo lỗi
            flash('Incorrect answer!', category='error')

    return render_template("secret_question.html", email=email)


@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            if password1 == password2:
                # Mã hóa mật khẩu mới
                hashed_password = hashlib.sha256(password1.encode()).hexdigest()
                # Cập nhật mật khẩu mới vào cơ sở dữ liệu
                user.password = hashed_password
                User.query.filter_by(email=email).update({"password": hashed_password})

                db.session.commit()
                flash('Password changed successfully!', category='success')
                # Chuyển hướng đến trang đăng nhập
                return redirect(url_for('auth.login'))
            else:
                flash('Passwords don\'t match.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("reset_password.html")
=======
    return render_template("sign_up.html", user=current_user)
>>>>>>> 4b9c041851f17a034b1576d1961c3ec890aa0f9d
