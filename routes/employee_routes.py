from flask import Blueprint, request, jsonify
from database import get_db_connection
import bcrypt

employee_bp = Blueprint('employee', __name__)

# 📥 Get All Employees
@employee_bp.route('/employees', methods=['GET'])
def get_employees():
    conn = get_db_connection()
    employees = conn.execute('SELECT * FROM employees').fetchall()
    conn.close()
    return jsonify([dict(row) for row in employees])

# 📥 Get Single Employee by ID
@employee_bp.route('/employee/<int:id>', methods=['GET'])
def get_employee(id):
    conn = get_db_connection()
    employee = conn.execute('SELECT * FROM employees WHERE id = ?', (id,)).fetchone()
    conn.close()
    if employee:
        return jsonify(dict(employee))
    return jsonify({'error': 'Employee not found'}), 404

# ➕ Add New Employee with Password Hashing
@employee_bp.route('/employee', methods=['POST'])
def add_employee():
    data = request.json

    # Validate required fields
    required_fields = ['name', 'email', 'date_of_joining', 'password']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'{field} is required'}), 400

    # Hash the password
    plain_password = data['password']
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Insert into database
    conn = get_db_connection()
    try:
        conn.execute('''
            INSERT INTO employees 
            (name, email, phone, address, department, designation,
             date_of_joining, salary, password, status, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['email'],
            data.get('phone'),
            data.get('address'),
            data.get('department'),
            data.get('designation'),
            data['date_of_joining'],
            data.get('salary', 0.0),
            hashed_password,
            data.get('status', 2),
            data.get('updated_at', None)
        ))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Failed to add employee: {str(e)}'}), 500
    finally:
        conn.close()

    return jsonify({'message': '✅ Employee added successfully'}), 201


@employee_bp.route('/employee/<int:employee_id>', methods=['PATCH'])
def update_employee(employee_id):
    data = request.json

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # List of fields that can be updated
    updatable_fields = [
        'name', 'email', 'phone', 'address',
        'department', 'designation', 'date_of_joining',
        'salary', 'password', 'status', 'updated_at'
    ]

    # Build the query dynamically
    fields = []
    values = []

    for field in updatable_fields:
        if field in data and data[field] is not None:
            if field == 'password':
                # Hash the new password before updating
                hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                fields.append('password = ?')
                values.append(hashed_password)
            else:
                fields.append(f'{field} = ?')
                values.append(data[field])

    if not fields:
        return jsonify({'error': 'No valid fields to update'}), 400

    values.append(employee_id)

    query = f'''
        UPDATE employees
        SET {', '.join(fields)}
        WHERE id = ?
    '''

    conn = get_db_connection()
    try:
        conn.execute(query, values)
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Failed to update employee: {str(e)}'}), 500
    finally:
        conn.close()

    return jsonify({'message': '✅ Employee updated successfully'}), 200
