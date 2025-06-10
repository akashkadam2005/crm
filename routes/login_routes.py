from flask import Blueprint, request, jsonify
from database import get_db_connection 
import bcrypt

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

    stored_password = user['password'].encode('utf-8')  # Convert to bytes for bcrypt
    
    try:
        # Verify the password
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return jsonify({
                'status': user['status'],
                'message': 'Login successful',
                'users': dict(user)
            }), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    except ValueError:
        return jsonify({'message': 'Invalid password hash format'}), 500