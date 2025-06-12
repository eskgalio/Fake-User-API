import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    # 1. Create API key
    headers = {"Content-Type": "application/json"}
    data = {"name": "test-app", "tier": "free"}
    response = requests.post(f"{BASE_URL}/api-keys", headers=headers, json=data)
    print("\n1. Create API Key:")
    print(json.dumps(response.json(), indent=2))
    
    if response.status_code == 200:
        api_key = response.json().get("api_key")
        headers["X-API-Key"] = api_key
        
        # 2. Get a single user
        response = requests.get(f"{BASE_URL}/user", headers=headers)
        print("\n2. Get Single User:")
        print(json.dumps(response.json(), indent=2))
        
        # 3. Get multiple users
        response = requests.get(f"{BASE_URL}/users/2", headers=headers)
        print("\n3. Get Multiple Users:")
        print(json.dumps(response.json(), indent=2))
        
        # 4. Export users
        data = {"format": "json", "count": 2}
        response = requests.post(f"{BASE_URL}/export", headers=headers, json=data)
        print("\n4. Export Users:")
        print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_api() 