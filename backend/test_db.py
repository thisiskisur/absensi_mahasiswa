from app import create_app
from database import db, Admin, Mahasiswa
from sqlalchemy import text
import requests

def test_database():
    print("🗄️ Testing database connection...")
    
    app = create_app()
    with app.app_context():
        try:
            # Test database connection
            result = db.session.execute(text("SELECT 1")).fetchone()
            print("✅ Database connection successful!")
            
            # Test admin query
            admin = Admin.query.filter_by(username='admin').first()
            if admin:
                print(f"✅ Admin found: {admin.username} ({admin.nama})")
            else:
                print("❌ Admin not found")
            
            # Test mahasiswa query
            mahasiswa_count = Mahasiswa.query.count()
            print(f"✅ Mahasiswa count: {mahasiswa_count}")
            
            return True
        except Exception as e:
            print(f"❌ Database error: {e}")
            return False

def test_api_with_server():
    print("\n🌐 Testing API with server...")
    
    # Start server in background
    import subprocess
    import time
    import threading
    
    def start_server():
        subprocess.run(["python", "app.py"])
    
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(5)
    
    # Test API
    try:
        response = requests.get("http://127.0.0.1:5001/", timeout=5)
        print(f"✅ Server responding: {response.status_code}")
        
        # Test login
        data = {"username": "admin", "password": "admin123", "user_type": "admin"}
        response = requests.post("http://127.0.0.1:5001/api/login", json=data, timeout=5)
        print(f"✅ Login test: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("🎉 Login successful! System is working!")
                return True
        
        print(f"❌ Login failed: {response.text}")
        return False
        
    except Exception as e:
        print(f"❌ API test error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing System Components...")
    print("=" * 50)
    
    # Test database
    db_ok = test_database()
    
    if db_ok:
        print("\n✅ Database is working!")
        print("\n🔧 Now testing API...")
        api_ok = test_api_with_server()
        
        if api_ok:
            print("\n🎉 All systems are working!")
            print("You can now use the frontend to login.")
        else:
            print("\n❌ API test failed. Check server logs.")
    else:
        print("\n❌ Database test failed. Check MySQL connection.")
