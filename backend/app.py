from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from database import db
import os
from dotenv import load_dotenv

# Import routes
from routes.auth import auth_bp
from routes.mahasiswa import mahasiswa_bp
from routes.absensi import absensi_bp

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key-here')
    
    # Database configuration for XAMPP MySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 
        'mysql+pymysql://root:@localhost/absensi_mahasiswa'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000'], supports_credentials=True, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    JWTManager(app)
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(mahasiswa_bp, url_prefix='/api')
    app.register_blueprint(absensi_bp, url_prefix='/api')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Endpoint tidak ditemukan'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'message': 'Method tidak diizinkan'
        }), 405
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'success': True,
            'message': 'Server is running',
            'status': 'healthy'
        }), 200
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        return jsonify({
            'success': True,
            'message': 'Sistem Absensi Mahasiswa API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/login, /api/register, /api/profile',
                'mahasiswa': '/api/mahasiswa',
                'absensi': '/api/absensi'
            }
        }), 200
    
    return app

def init_database():
    """Initialize database tables"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    app = create_app()
    
    # Initialize database on first run
    try:
        init_database()
    except Exception as e:
        print(f"Database initialization error: {e}")
        print("Please make sure MySQL is running and database 'absensi_mahasiswa' exists")
    
    # Run the app
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True
    )
