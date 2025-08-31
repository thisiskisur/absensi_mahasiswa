#!/usr/bin/env python3
"""
Sistem Absensi Mahasiswa - Runner Script
Menjalankan backend dan frontend secara bersamaan
"""

import subprocess
import time
import threading
import sys
import os
import requests
from pathlib import Path

def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get("http://127.0.0.1:5001/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def check_frontend():
    """Check if frontend is running"""
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_backend():
    """Start the Flask backend server"""
    print("🚀 Starting Backend Server...")
    os.chdir('backend')
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")

def start_frontend():
    """Start the React frontend server"""
    print("🎨 Starting Frontend Server...")
    os.chdir('frontend')
    try:
        subprocess.run(["npm", "start"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")

def test_system():
    """Test the system functionality"""
    print("\n🧪 Testing System...")
    time.sleep(10)  # Wait for servers to start
    
    # Test backend
    if check_backend():
        print("✅ Backend is running")
        
        # Test admin login
        try:
            response = requests.post("http://127.0.0.1:5001/api/login", 
                                   json={"username": "admin", "password": "admin123", "user_type": "admin"})
            if response.status_code == 200:
                print("✅ Admin login works")
            else:
                print("❌ Admin login failed")
        except Exception as e:
            print(f"❌ Admin login error: {e}")
        
        # Test mahasiswa login
        try:
            response = requests.post("http://127.0.0.1:5001/api/login", 
                                   json={"username": "2021001", "password": "2021001", "user_type": "mahasiswa"})
            if response.status_code == 200:
                print("✅ Mahasiswa login works")
            else:
                print("❌ Mahasiswa login failed")
        except Exception as e:
            print(f"❌ Mahasiswa login error: {e}")
    else:
        print("❌ Backend is not running")
    
    # Test frontend
    if check_frontend():
        print("✅ Frontend is running")
    else:
        print("❌ Frontend is not running")

def main():
    print("🎯 Sistem Absensi Mahasiswa")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("backend").exists() or not Path("frontend").exists():
        print("❌ Error: Please run this script from the project root directory")
        print("   Make sure 'backend' and 'frontend' folders exist")
        return
    
    # Start backend in background thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait a bit for backend to start
    time.sleep(3)
    
    # Start frontend in background thread
    frontend_thread = threading.Thread(target=start_frontend, daemon=True)
    frontend_thread.start()
    
    # Test system after a delay
    test_thread = threading.Thread(target=test_system, daemon=True)
    test_thread.start()
    
    print("\n✅ System started successfully!")
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
        print("✅ System stopped")

if __name__ == "__main__":
    main()
