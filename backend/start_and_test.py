import subprocess
import time
import requests
import threading
import sys

def start_server():
    """Start the Flask server"""
    try:
        print("🚀 Starting Flask server...")
        subprocess.run([sys.executable, "run_server.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def test_api():
    """Test the API endpoints"""
    time.sleep(3)  # Wait for server to start
    
    print("\n🧪 Testing API endpoints...")
    
    # Test root endpoint
    try:
        response = requests.get("http://127.0.0.1:3001/", timeout=5)
        print(f"✅ Root endpoint: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test health endpoint
    try:
        response = requests.get("http://127.0.0.1:3001/health", timeout=5)
        print(f"✅ Health endpoint: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
    
    # Test login endpoint
    try:
        data = {"username": "admin", "password": "admin123", "user_type": "admin"}
        response = requests.post("http://127.0.0.1:3001/api/login", json=data, timeout=5)
        print(f"✅ Login endpoint: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("🎉 Login berhasil! API siap digunakan.")
            else:
                print(f"❌ Login gagal: {result.get('message')}")
        else:
            print(f"❌ Login error: {response.text}")
    except Exception as e:
        print(f"❌ Login endpoint error: {e}")

if __name__ == "__main__":
    # Start server in background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Test API
    test_api()
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping...")
