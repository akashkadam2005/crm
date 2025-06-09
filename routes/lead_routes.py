from flask import Blueprint, request, jsonify
import sqlite3
from datetime import datetime
from database import get_db_connection
lead_bp = Blueprint('lead_bp', __name__)
 

# GET all leads
@lead_bp.route('/leads', methods=['GET'])
def get_leads():
    conn = get_db_connection()
    leads = conn.execute('SELECT * FROM leads').fetchall()
    conn.close()
    return jsonify([dict(row) for row in leads])

# GET one lead
@lead_bp.route('/leads/<int:lead_id>', methods=['GET'])
def get_lead(lead_id):
    conn = get_db_connection()
    lead = conn.execute('SELECT * FROM leads WHERE lead_id = ?', (lead_id,)).fetchone()
    conn.close()
    if lead:
        return jsonify(dict(lead))
    return jsonify({'message': 'Lead not found'}), 404

# CREATE a lead
@lead_bp.route('/leads', methods=['POST'])
def create_lead():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO leads (
            lead_title, lead_customer, lead_employee,
            lead_description, lead_date, lead_time,
            lead_priority, lead_tags, lead_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('lead_title'),
        data.get('lead_customer'),
        data.get('lead_employee'),
        data.get('lead_description'),
        data.get('lead_date'),
        data.get('lead_time'),
        data.get('lead_priority'),
        data.get('lead_tags'),
        data.get('lead_status', 1)
    ))

    conn.commit()
    lead_id = cursor.lastrowid
    conn.close()
    return jsonify({'message': 'Lead created', 'lead_id': lead_id}), 201

# UPDATE a lead
@lead_bp.route('/leads/<int:lead_id>', methods=['PUT'])
def update_lead(lead_id):
    data = request.get_json()
    updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE leads SET
            lead_title = ?,
            lead_customer = ?,
            lead_employee = ?,
            lead_description = ?,
            lead_date = ?,
            lead_time = ?,
            lead_priority = ?,
            lead_tags = ?,
            lead_status = ?,
            lead_updated_at = ?
        WHERE lead_id = ?
    ''', (
        data.get('lead_title'),
        data.get('lead_customer'),
        data.get('lead_employee'),
        data.get('lead_description'),
        data.get('lead_date'),
        data.get('lead_time'),
        data.get('lead_priority'),
        data.get('lead_tags'),
        data.get('lead_status'),
        updated_at,
        lead_id
    ))

    conn.commit()
    conn.close()
    return jsonify({'message': 'Lead updated successfully'})
