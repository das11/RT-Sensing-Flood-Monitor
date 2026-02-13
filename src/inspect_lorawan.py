
import os
import sys
import json
import logging
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load Env
load_dotenv()
FIREBASE_DB_URL = os.getenv("FIREBASE_DB_URL")
SERVICE_ACCOUNT_KEY = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "serviceAccountKey.json")

def inspect():
    if not os.path.exists(SERVICE_ACCOUNT_KEY):
        logger.error(f"Service Account Key not found at {SERVICE_ACCOUNT_KEY}")
        return

    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
    firebase_admin.initialize_app(cred, {
        'databaseURL': FIREBASE_DB_URL
    })
    
    logger.info("Fetching /LoRaWAN data...")
    ref = db.reference("/LoRaWAN")
    data = ref.get()
    
    print("\n--- RAW DATA DUMP (First 1000 chars) ---")
    json_str = json.dumps(data, indent=2)
    print(json_str[:2000])
    print("\n--- TYPE INFO ---")
    print(f"Type: {type(data)}")
    if isinstance(data, dict):
        print(f"Keys: {list(data.keys())[:10]}")
        first_val = list(data.values())[0]
        print(f"First Value Type: {type(first_val)}")
    
if __name__ == "__main__":
    inspect()
