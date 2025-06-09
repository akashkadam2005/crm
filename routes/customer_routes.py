from flask import Blueprint, request, jsonify
from database import get_db_connection

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/customers', methods=['GET'])
def get_customers():
    conn = get_db_connection()
    customers = conn.execute('SELECT * FROM customers').fetchall()
    conn.close()
    return jsonify([dict(row) for row in customers])

@customer_bp.route('/customer/<int:id>', methods=['GET'])
def get_customer(id):
    conn = get_db_connection()
    customer = conn.execute('SELECT * FROM customers WHERE id = ?', (id,)).fetchone()
    conn.close()
    if customer:
        return jsonify(dict(customer))
    return jsonify({'error': 'Customer not found'}), 404

@customer_bp.route('/customer', methods=['POST'])
def add_customer():
    data = request.json
    conn = get_db_connection()
    conn.execute('INSERT INTO customers (name, email, phone, address) VALUES (?, ?, ?, ?)',
                 (data['name'], data['email'], data['phone'], data['address']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Customer added successfully'}), 201
