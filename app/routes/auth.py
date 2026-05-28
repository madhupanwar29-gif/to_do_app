from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validation
        if not username or not password or not confirm_password:
            flash("All fields are required", "error")
            return redirect(url_for('auth.register'))

        if len(password) < 4:
            flash("Password must be at least 4 characters", "error")
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash("Passwords do not match", "error")
            return redirect(url_for('auth.register'))

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists", "error")
            return redirect(url_for('auth.register'))

        # Create new user
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login", "success")
        return redirect(url_for('auth.login'))

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        # Find user in database
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['user'] = username
            session['user_id'] = user.id
            flash("Login successful", "success")
            return redirect(url_for('tasks.view_task'))
        else:
            flash("Username or password is incorrect", "error")

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    flash("Logged out successfully", "info")
    return redirect(url_for('auth.login'))