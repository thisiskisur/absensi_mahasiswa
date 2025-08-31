from app import create_app
from database import db, Admin
from werkzeug.security import generate_password_hash

def fix_admin_password():
    app = create_app()
    
    with app.app_context():
        print("🔧 Fixing admin password...")
        
        # Find admin user
        admin = Admin.query.filter_by(username='admin').first()
        
        if admin:
            # Update password with new hash
            admin.password = generate_password_hash('admin123', method='pbkdf2:sha256')
            db.session.commit()
            print("✅ Admin password updated successfully!")
            print("Username: admin")
            print("Password: admin123")
        else:
            print("❌ Admin user not found!")

if __name__ == '__main__':
    fix_admin_password()
