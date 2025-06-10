from flask import Flask
from flask_cors import CORS
from routes.customer_routes import customer_bp
from routes.employee_routes import employee_bp  # if you have employee APIs
from routes.lead_routes import lead_bp  # if you have employee APIs
from routes.login_routes import auth_bp  # if you have employee APIs
from routes.dahboard_routes import dashboard_bp   # if you have employee APIs
from database import create_tables  # ensure tables are created if needed

app = Flask(__name__)
CORS(app)

# Create database tables if not already created
create_tables()
@app.route('/')
def index():
    return {
        "message": "Welcome to the API!",
        "status": "running",
        "version": "1.0.0",
        "author": "Sanket Jadhav"
    }

# Register blueprints
app.register_blueprint(customer_bp, url_prefix='/api')
app.register_blueprint(employee_bp, url_prefix='/api')  # optional if you have employees
app.register_blueprint(lead_bp, url_prefix='/api')  # optional if you have employees
app.register_blueprint(auth_bp, url_prefix='/api')  # optional if you have employees
app.register_blueprint(dashboard_bp, url_prefix='/api')  # optional if you have employees

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
