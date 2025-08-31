from app import create_app
from database import db, Admin
from werkzeug.security import generate_password_hash

def init_admin():
    app = create_app()
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if admin already exists
        existing_admin = Admin.query.filter_by(username='admin').first()
        
        if not existing_admin:
            # Create default admin
            admin = Admin(
                username='admin',
                password=generate_password_hash('admin123'),
                nama='Administrator'
            )
            
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin berhasil dibuat!")
            print("Username: admin")
            print("Password: admin123")
        else:
            print("✅ Admin sudah ada di database")
            print("Username: admin")
            print("Password: admin123")
        
        # Show all admins
        admins = Admin.query.all()
        print(f"\n📊 Total admin: {len(admins)}")
        for admin in admins:
            print(f"- {admin.username} ({admin.nama})")

if __name__ == '__main__':
    init_admin()
