from app import create_app
from database import db, Admin, Mahasiswa
from werkzeug.security import generate_password_hash
import os

def setup_database():
    app = create_app()
    
    with app.app_context():
        print("🗄️ Setting up database...")
        
        # Create tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Create admin user
        admin = Admin.query.filter_by(username='admin').first()
        if not admin:
            admin = Admin(
                username='admin',
                password=generate_password_hash('admin123'),
                nama='Administrator'
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created successfully!")
        else:
            print("✅ Admin user already exists!")
        
        # Create sample mahasiswa
        sample_mahasiswa = [
            {'nim': '2021001', 'nama': 'Ahmad Fauzi', 'jurusan': 'Teknik Informatika'},
            {'nim': '2021002', 'nama': 'Siti Nurhaliza', 'jurusan': 'Sistem Informasi'},
            {'nim': '2021003', 'nama': 'Budi Santoso', 'jurusan': 'Teknik Komputer'},
        ]
        
        for data in sample_mahasiswa:
            existing = Mahasiswa.query.filter_by(nim=data['nim']).first()
            if not existing:
                mahasiswa = Mahasiswa(
                    nim=data['nim'],
                    nama=data['nama'],
                    jurusan=data['jurusan'],
                    foto_wajah=''  # Will be updated when photo is uploaded
                )
                db.session.add(mahasiswa)
                print(f"✅ Created mahasiswa: {data['nama']} ({data['nim']})")
        
        db.session.commit()
        
        # Show summary
        admin_count = Admin.query.count()
        mahasiswa_count = Mahasiswa.query.count()
        
        print(f"\n📊 Database Summary:")
        print(f"- Admin users: {admin_count}")
        print(f"- Mahasiswa: {mahasiswa_count}")
        
        print(f"\n🔐 Login Credentials:")
        print(f"- Admin: username=admin, password=admin123")
        print(f"- Mahasiswa: NIM=2021001, password=2021001")
        
        print(f"\n✅ Database setup completed successfully!")

if __name__ == '__main__':
    setup_database()
