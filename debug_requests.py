import requests
import json

API_URL = "http://localhost:8000"
payload = {"description": "NETFLIX.COM", "amount": 10.0}

print(f"Sending payload: {payload}")
try:
    response = requests.post(f"{API_URL}/predict", json=payload)
    print(f"Response status: {response.status_code}")
    print(f"Response content: {response.text}")
except Exception as e:
    print(f"Error: {e}")
