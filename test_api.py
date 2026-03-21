import requests
import json

BASE_URL = "http://localhost:8000"

# Register
print("1. Registering user...")
reg_response = requests.post(f"{BASE_URL}/register", json={
    "username": "testuser",
    "email": "test@example.com",
    "password": "pass123"
})
print(f"Status: {reg_response.status_code}")
print(json.dumps(reg_response.json(), indent=2))

# Login
print("\n2. Logging in...")
login_response = requests.post(f"{BASE_URL}/login", json={
    "username": "testuser",
    "password": "pass123"
})
print(f"Status: {login_response.status_code}")
login_data = login_response.json()
print(json.dumps(login_data, indent=2))
token = login_data["access_token"]

# Protected endpoint
print("\n3. Accessing protected endpoint...")
protected_response = requests.get(
    f"{BASE_URL}/protected",
    headers={"Authorization": f"Bearer {token}"}
)
print(f"Status: {protected_response.status_code}")
print(json.dumps(protected_response.json(), indent=2))
