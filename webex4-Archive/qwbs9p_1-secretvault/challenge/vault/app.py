import base64
import os
import secrets
import sys
from datetime import datetime
from functools import wraps
import requests

from cryptography.fernet import Fernet
from flask import (
    Flask,
    flash,
    g,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import hashlib

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    vault_entries = db.relationship('VaultEntry', backref='user', lazy=True, cascade='all, delete-orphan')


class VaultEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    label = db.Column(db.String(120), nullable=False)
    login = db.Column(db.String(120), nullable=False)
    password_encrypted = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

def hash_password(password: str, salt: bytes) -> str:
    data = salt + password.encode('utf-8')
    for _ in range(50):
        data = hashlib.sha256(data).digest()
    return base64.b64encode(data).decode('utf-8')

def verify_password(password: str, salt_b64: str, digest: str) -> bool:
    salt = base64.b64decode(salt_b64.encode('utf-8'))
    return hash_password(password, salt) == digest

def generate_salt() -> bytes:
    return secrets.token_bytes(16)

def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secrets.token_hex(32)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///vault.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SIGN_SERVER'] = os.getenv('SIGN_SERVER', 'http://127.0.0.1:4444/sign')
    fernet_key = os.getenv('FERNET_KEY')
    if not fernet_key:
        raise RuntimeError('Missing FERNET_KEY environment variable. Generate one with `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`.')
    app.config['FERNET_KEY'] = fernet_key
    db.init_app(app)

    fernet = Fernet(app.config['FERNET_KEY'])
    with app.app_context():
        db.create_all()

        if not User.query.first():
            salt = secrets.token_bytes(16)
            password = secrets.token_bytes(32).hex()
            password_hash = hash_password(password, salt)
            user = User(
                id=0,
                username='admin',
                password_hash=password_hash,
                salt=base64.b64encode(salt).decode('utf-8'),
            )
            db.session.add(user)
            db.session.commit()

            flag = open('/flag').read().strip()
            flagEntry = VaultEntry(
                user_id=user.id,
                label='flag',
                login='flag',
                password_encrypted=fernet.encrypt(flag.encode('utf-8')).decode('utf-8'),
                notes='This is the flag entry.',
            )
            db.session.add(flagEntry)
            db.session.commit()

    def login_required(view_func):
        @wraps(view_func)
        def wrapped(*args, **kwargs):
            uid = request.headers.get('X-User', '0')
            print(uid)
            if uid == 'anonymous':
                flash('Please sign in first.', 'warning')
                return redirect(url_for('login'))
            try:
                uid_int = int(uid)
            except (TypeError, ValueError):
                flash('Invalid session. Please sign in again.', 'warning')
                return redirect(url_for('login'))
            user = User.query.filter_by(id=uid_int).first()
            if not user:
                flash('User not found. Please sign in again.', 'warning')
                return redirect(url_for('login'))

            g.current_user = user
            return view_func(*args, **kwargs)

        return wrapped

    @app.route('/')
    def index():
        uid = request.headers.get('X-User', '0')
        if not uid or uid == 'anonymous':
            return redirect(url_for('login'))
        
        return redirect(url_for('dashboard'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            if not username or not password:
                flash('Username and password are required.', 'danger')
                return render_template('register.html')
            if password != confirm_password:
                flash('Passwords do not match.', 'danger')
                return render_template('register.html')
            salt = generate_salt()
            password_hash = hash_password(password, salt)
            user = User(
                username=username,
                password_hash=password_hash,
                salt=base64.b64encode(salt).decode('utf-8'),
            )
            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                flash('Username already exists. Please choose another.', 'warning')
                return render_template('register.html')
            flash('Registration successful. Please sign in.', 'success')
            return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
            user = User.query.filter_by(username=username).first()
            if not user or not verify_password(password, user.salt, user.password_hash):
                flash('Invalid username or password.', 'danger')
                return render_template('login.html')
            r = requests.get(app.config['SIGN_SERVER'], params={'uid': user.id}, timeout=5)
            if r.status_code != 200:
                flash('Unable to reach the authentication server. Please try again later.', 'danger')
                return render_template('login.html')
            
            token = r.text.strip()
            response = make_response(redirect(url_for('dashboard')))
            response.set_cookie(
                'token',
                token,
                httponly=True,
                secure=app.config.get('SESSION_COOKIE_SECURE', False),
                samesite='Lax',
                max_age=12 * 3600,
            )
            return response
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        response = make_response(redirect(url_for('login')))
        response.delete_cookie('token')
        flash('Signed out.', 'info')
        return response

    @app.route('/dashboard')
    @login_required
    def dashboard():
        user = g.current_user
        entries = [
            {
                'id': entry.id,
                'label': entry.label,
                'login': entry.login,
                'password': fernet.decrypt(entry.password_encrypted.encode('utf-8')).decode('utf-8'),
                'notes': entry.notes,
                'created_at': entry.created_at,
            }
            for entry in user.vault_entries
        ]
        return render_template('dashboard.html', username=user.username, entries=entries)

    @app.route('/passwords/new', methods=['POST'])
    @login_required
    def create_password():
        user = g.current_user
        label = request.form.get('label', '').strip()
        login_value = request.form.get('login', '').strip()
        password_plain = request.form.get('password', '').strip()
        notes = request.form.get('notes', '').strip() or None
        if not label or not login_value or not password_plain:
            flash('Service name, login, and password are required.', 'danger')
            return redirect(url_for('dashboard'))
        encrypted_password = fernet.encrypt(password_plain.encode('utf-8')).decode('utf-8')
        entry = VaultEntry(
            user_id=user.id,
            label=label,
            login=login_value,
            password_encrypted=encrypted_password,
            notes=notes,
        )
        db.session.add(entry)
        db.session.commit()
        flash('Password entry saved.', 'success')
        return redirect(url_for('dashboard'))

    @app.route('/passwords/<int:entry_id>', methods=['DELETE'])
    @login_required
    def delete_password(entry_id: int):
        user = g.current_user
        entry = VaultEntry.query.filter_by(id=entry_id, user_id=user.id).first()
        if not entry:
            return jsonify({'success': False, 'message': 'Entry not found'}), 404
        db.session.delete(entry)
        db.session.commit()
        return jsonify({'success': True})

    return app


if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run(host='127.0.0.1', port=5000, debug=False)
