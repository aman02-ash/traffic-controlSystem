import requests
import json
import time

BACKEND_URL = "http://localhost:8080/traffic/update"

while True:
    try:
        with open("output/traffic_data.json", "r") as f:
            data = json.load(f)

        payload = {
            "lanes": data   # 🔥 THIS LINE IS IMPORTANT
        }

        response = requests.post(BACKEND_URL, json=payload)

        print("Status:", response.status_code)

    except Exception as e:
        print("Error:", e)

    time.sleep(5)