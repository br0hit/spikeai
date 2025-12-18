import requests

url = "http://localhost:8080/query"
payload = {
    # Tier 2 example from the problem statement [cite: 129]
    "query": "Which URLs do not use HTTPS and have title tags longer than 60 characters?"
}

try:
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("✅ Response:", response.json())
    else:
        print(f"❌ Error {response.status_code}:", response.text)
except Exception as e:
    print("❌ Request failed:", e)