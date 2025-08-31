import requests

def test_server():
    print("Testing server connectivity...")
    
    # Test root endpoint
    try:
        response = requests.get("http://127.0.0.1:3001/", timeout=5)
        print(f"Root endpoint status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
    except Exception as e:
        print(f"Root endpoint error: {e}")
    
    # Test health endpoint
    try:
        response = requests.get("http://127.0.0.1:3001/health", timeout=5)
        print(f"Health endpoint status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Health endpoint error: {e}")
    
    # Test login endpoint
    try:
        data = {"username": "admin", "password": "admin123", "user_type": "admin"}
        response = requests.post("http://127.0.0.1:3001/api/login", json=data, timeout=5)
        print(f"Login endpoint status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Login endpoint error: {e}")

if __name__ == "__main__":
    test_server()
