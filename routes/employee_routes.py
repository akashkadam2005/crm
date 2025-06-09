from flask import Blueprint, request, jsonify
from database import get_db_connection

employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/employees', methods=['GET'])
def get_employees():
    conn = get_db_connection()
    employees = conn.execute('SELECT * FROM employees').fetchall()
    conn.close()
    return jsonify([dict(row) for row in employees])

@employee_bp.route('/employee/<int:id>', methods=['GET'])
def get_employee(id):
    conn = get_db_connection()
    employee = conn.execute('SELECT * FROM employees WHERE id = ?', (id,)).fetchone()
    conn.close()
    if employee:
        return jsonify(dict(employee))
    return jsonify({'error': 'Employee not found'}), 404

@employee_bp.route('/employee', methods=['POST'])
def add_employee():
    data = request.json
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO employees 
        (name, email, phone, address, department, designation, employee_code, date_of_joining, salary, status, notes, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['name'], data['email'], data.get('phone'),
        data.get('address'), data.get('department'),
        data.get('designation'), data['employee_code'],
        data['date_of_joining'], data.get('salary', 0.0),
        data.get('status', 'Active'), data.get('notes'), data.get('updated_at')
    ))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Employee added successfully'}), 201
