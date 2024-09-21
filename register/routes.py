# register/routes.py

from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from qna import db  # Use the shared db instance from qna
from .models import User

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists, please choose a different one.')
            return redirect(url_for('register.register'))
        else:
            new_user = User(
                username=request.form['username'],
                password=generate_password_hash(request.form.get('password'))
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful, please log in.')
            return redirect(url_for('register.login'))
    return render_template('register.html')

@register_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form.get('password')

        query_user = User.query.filter_by(username=username).first()

        if query_user and check_password_hash(query_user.password, password):
            session['logged_in'] = True
            return redirect(url_for('qna.index'))  # Redirect to Q&A page after login
        else:
            flash('Username or password is incorrect.')
            return redirect(url_for('register.login'))

@register_bp.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('register.login'))
