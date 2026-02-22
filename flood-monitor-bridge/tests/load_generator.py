
import time
import random
import requests
import json
import logging

# Simple script to mock Firebase Pushes if you can write to the DB.
# If read-only, this script is just a demonstration of what data looks like.

# Actually, to load test the bridge cleanly, we should mock the 'event' object in a test, 
# but here we'd want to push to actual Firebase if we had credentials.
# Since we don't have creds, this script prints what it WOULD send.

def generate_payload():
    return {
        "dist_cm": f"R{random.randint(100, 1000)}",
        "bat_volt": round(random.uniform(11.0, 13.0), 1),
        "solar_volt": round(random.uniform(0, 18.0), 1),
        "timestamp": time.time()
    }

def main():
    print("Simulating Sensor Data Generation...")
    while True:
        payload = generate_payload()
        print(f"Post to /floodmonitor1: {json.dumps(payload)}")
        time.sleep(2)

if __name__ == "__main__":
    main()
