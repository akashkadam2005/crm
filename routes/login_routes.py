from flask import Blueprint, request, jsonify
import sqlite3
from database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth_bp', __name__)
 
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password required'}), 400

    hashed_password = generate_password_hash(password)

    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO employees (email, password) VALUES (?, ?)', (email, hashed_password))
        conn.commit()
        conn.close()
        return jsonify({'message': 'User registered successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Email already exists'}), 409

# LOGIN
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM employees WHERE email = ?', (email,)).fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        return jsonify({'message': 'Login successful', 'user_id': user['id'], 'email': user['email']}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
