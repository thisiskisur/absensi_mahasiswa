import requests
import json

def test_login():
    urls = [
        "http://localhost:5001/api/login",
        "http://127.0.0.1:5001/api/login",
        "http://192.168.0.104:5001/api/login"
    ]
    
    data = {
        "username": "admin",
        "password": "admin123",
        "user_type": "admin"
    }
    
    for url in urls:
        print(f"\nTesting URL: {url}")
        try:
            response = requests.post(url, json=data, timeout=5)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print("✅ Login berhasil!")
                    print(f"Token: {result.get('token', 'N/A')}")
                    return True
                else:
                    print("❌ Login gagal!")
                    print(f"Message: {result.get('message', 'N/A')}")
            else:
                print(f"❌ Error: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Tidak bisa terhubung ke server")
        except requests.exceptions.Timeout:
            print("❌ Timeout")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    return False

if __name__ == "__main__":
    print("Testing API Login...")
    test_login()
