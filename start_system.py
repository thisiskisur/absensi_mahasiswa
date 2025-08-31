import subprocess
import time
import threading
import sys
import os

def start_backend():
    """Start the Flask backend server"""
    print("🚀 Starting Backend Server...")
    os.chdir('backend')
    subprocess.run([sys.executable, "app.py"])

def start_frontend():
    """Start the React frontend server"""
    print("🎨 Starting Frontend Server...")
    os.chdir('frontend')
    subprocess.run([sys.executable, "-m", "http.server", "3000"])

def main():
    print("🎯 Starting Absensi Mahasiswa System...")
    print("=" * 50)
    
    # Start backend in background thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait for backend to start
    print("⏳ Waiting for backend to start...")
    time.sleep(5)
    
    # Start frontend in background thread
    frontend_thread = threading.Thread(target=start_frontend, daemon=True)
    frontend_thread.start()
    
    print("✅ System started successfully!")
    print("\n📱 Access URLs:")
    print("- Frontend: http://localhost:3000")
    print("- Backend API: http://localhost:5001")
    print("\n🔐 Login Credentials:")
    print("- Admin: username=admin, password=admin123")
    print("- Mahasiswa: NIM=2021001, password=2021001")
    print("\n🛑 Press Ctrl+C to stop all servers")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")

if __name__ == "__main__":
    main()
