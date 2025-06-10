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

@lead_bp.route('/leads/status/<int:lead_status>', methods=['GET'])
def get_lead_status(lead_status):
    conn = get_db_connection()
    lead = conn.execute('SELECT * FROM leads WHERE lead_status = ?', (lead_status,)).fetchall()
    conn.close()
    if lead:
        return jsonify([dict(row) for row in lead])
    return jsonify([])


@lead_bp.route('/leads/summary', methods=['GET'])
def lead_summary():
    start_date = request.args.get('start')
    end_date = request.args.get('end')

    conn = get_db_connection()
    cursor = conn.cursor()

    # --- Count Query ---
    base_count_query = "SELECT lead_status, COUNT(*) as count FROM leads"
    base_total_query = "SELECT COUNT(*) FROM leads"
    base_list_query = "SELECT * FROM leads"
    params = []

    # Apply date filter if present
    if start_date and end_date:
        filter_clause = " WHERE DATE(lead_created_date) BETWEEN ? AND ?"
        params.extend([start_date, end_date])
        count_query = base_count_query + filter_clause + " GROUP BY lead_status"
        total_query = base_total_query + filter_clause
        list_query = base_list_query + filter_clause + " ORDER BY lead_created_date DESC"
    else:
        count_query = base_count_query + " GROUP BY lead_status"
        total_query = base_total_query
        list_query = base_list_query + " ORDER BY lead_created_date DESC"

    # --- Execute queries ---
    total_count = cursor.execute(total_query, params).fetchone()[0]
    status_counts = cursor.execute(count_query, params).fetchall()
    leads = cursor.execute(list_query, params).fetchall()
    conn.close()

    # --- Build Response ---
    result = {
        'total': total_count,
        'pending': 0,
        'ongoing': 0,
        'cancelled': 0,
        'completed': 0,
        'leads': [dict(row) for row in leads]
    }

    for row in status_counts:
        status = row['lead_status']
        count = row['count']
        if status == 1:
            result['pending'] = count
        elif status == 2:
            result['ongoing'] = count
        elif status == 3:
            result['cancelled'] = count
        elif status == 4:
            result['completed'] = count

    return jsonify(result)


# CREATE a lead
@lead_bp.route('/leads', methods=['POST'])
def create_lead():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Convert list to comma-separated string
    lead_tags = data.get('lead_tags')
    if isinstance(lead_tags, list):
        lead_tags = ','.join(lead_tags)

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
        lead_tags,
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
