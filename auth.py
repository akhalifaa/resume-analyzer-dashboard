from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json, os

auth = Blueprint('auth', __name__)
USERS_FILE = 'users.json'

# Simple User class
class User(UserMixin):
    def __init__(self, id):
        self.id = id

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_user(email, password_hash):
    users = load_users()
    users[email] = password_hash
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = load_users()

        if email in users and check_password_hash(users[email], password):
            login_user(User(email))
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials")
    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = load_users()

        if email in users:
            flash("User already exists")
        else:
            save_user(email, generate_password_hash(password, method='pbkdf2:sha256'))
            flash("User created, please log in")
            return redirect(url_for('auth.login'))
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
