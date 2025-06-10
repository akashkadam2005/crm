from flask import Blueprint, request, jsonify
import sqlite3
from database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

dashboard_bp = Blueprint('dashboard_bp', __name__)


@dashboard_bp.route('/dashboard/summary', methods=['GET'])
def dashboard_summary():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Count totals
    lead_count = cursor.execute('SELECT COUNT(*) FROM leads').fetchone()[0]
    employee_count = cursor.execute('SELECT COUNT(*) FROM employees').fetchone()[0]
    customer_count = cursor.execute('SELECT COUNT(*) FROM customers').fetchone()[0]

    # Count leads by status
    status_data = cursor.execute('''
        SELECT lead_status, COUNT(*) as count
        FROM leads
        GROUP BY lead_status
    ''').fetchall()

    conn.close()

    # Map status codes to readable labels
    status_map = {
        1: "Pending",
        2: "On Going",
        3: "Cancelled",
        4: "Completed"
    }

    status_counts = [
        {
            "status": status_map.get(row["lead_status"], "Unknown"),
            "count": row["count"]
        }
        for row in status_data
    ]

    return jsonify({
        "total_leads": lead_count,
        "total_employees": employee_count,
        "total_customers": customer_count,
        "lead_status_counts": status_counts
    })