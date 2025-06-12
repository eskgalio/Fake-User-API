import requests
import json

def print_response(response):
    """Pretty print the response"""
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    print()

# Base URL
BASE_URL = "http://localhost:8000"

# 1. Create API key
print("1. Creating API key:")
response = requests.post(
    f"{BASE_URL}/api-keys",
    json={"name": "manual-test", "tier": "free"}
)
print_response(response)

# Save the API key
api_key = response.json()["api_key"]
headers = {
    "Content-Type": "application/json",
    "X-API-Key": api_key
}

# 2. Get a single user
print("2. Getting a single user:")
response = requests.get(
    f"{BASE_URL}/user",
    headers=headers
)
print_response(response)

# 3. Get multiple users
print("3. Getting multiple users:")
response = requests.get(
    f"{BASE_URL}/users/2",
    headers=headers
)
print_response(response)

# 4. Get users from a specific country
print("4. Getting users from France:")
response = requests.get(
    f"{BASE_URL}/users/2",
    headers=headers,
    params={"country": "fr_FR"}
)
print_response(response)

# 5. Export users
print("5. Exporting users in different formats:")
formats = ["json", "csv", "xml"]
for format in formats:
    print(f"\nExporting in {format.upper()} format:")
    response = requests.post(
        f"{BASE_URL}/export",
        headers=headers,
        json={
            "format": format,
            "count": 2,
            "include_fields": ["name", "email", "country"]
        }
    )
    print_response(response) 