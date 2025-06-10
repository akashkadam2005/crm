from flask import Blueprint, request, jsonify
import sqlite3
from database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash 

auth_bp = Blueprint('auth_bp', __name__)
  
# LOGIN
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password required'}), 400

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM employees WHERE email = ?', (email,)).fetchone()
    conn.close()

    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    stored_password = user['password']
    
    # Case 1: Password is already hashed with Werkzeug
    if stored_password.startswith('pbkdf2:'):
        if check_password_hash(stored_password, password):
            return login_success(user)
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    
    # Case 2: Password is plaintext (TEMPORARY FIX - UNSAFE!)
    elif stored_password == password:
        return login_success(user)
    
    # Case 3: Password is invalid
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

def login_success(user):
    return jsonify({
        'message': 'Login successful',
        'user_id': user['id'],
        'email': user['email'],
        'name': user['name']   
    }), 200