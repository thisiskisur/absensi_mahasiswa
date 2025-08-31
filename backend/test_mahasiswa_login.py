import requests
import json

def test_mahasiswa_login():
    print("🧪 Testing Mahasiswa Login...")
    
    # Test mahasiswa login
    data = {
        "username": "2021001",
        "password": "2021001",
        "user_type": "mahasiswa"
    }
    
    try:
        response = requests.post("http://127.0.0.1:5001/api/login", json=data, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Mahasiswa login berhasil!")
                print(f"User: {result.get('user', {}).get('nama')}")
                print(f"Type: {result.get('user', {}).get('type')}")
                return True
            else:
                print("❌ Mahasiswa login gagal!")
                print(f"Message: {result.get('message', 'N/A')}")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    return False

if __name__ == "__main__":
    test_mahasiswa_login()
