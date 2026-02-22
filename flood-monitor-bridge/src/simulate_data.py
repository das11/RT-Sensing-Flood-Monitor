import os
import time
import json
import random
import math
import argparse
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()
FIREBASE_DB_URL = os.getenv("FIREBASE_DB_URL")
SERVICE_ACCOUNT_KEY = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "serviceAccountKey.json")
KEYS_FILE = "src/generated_keys.json"

def setup_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
        firebase_admin.initialize_app(cred, {'databaseURL': FIREBASE_DB_URL})

def save_key(sensor_id, key):
    try:
        with open(KEYS_FILE, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    if sensor_id not in data:
        data[sensor_id] = []
    
    data[sensor_id].append(key)
    
    with open(KEYS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def generate_data(sensor_id, count, delay, interval, start_past=False, static_value=None):
    print(f"🚀 Starting simulation for {sensor_id}...")
    print(f"📡 Generating {count} records.")
    print(f"   - Virtual Interval: {interval}s (Data timestamp spacing)")
    print(f"   - Execution Delay:  {delay}s (Wait time between pushes)")
    
    # Determine start time
    if start_past:
        # Start "count * interval" seconds ago
        current_virtual_time = time.time() - (count * interval)
        print(f"   - Starting timestamp: {current_virtual_time} (Backfilling history)")
    else:
        current_virtual_time = time.time()
        print(f"   - Starting timestamp: {current_virtual_time} (Live simulation)")

    ref = db.reference(f"/{sensor_id}")
    
    # Batch update for speed if delay is small
    batch_data = {}
    batch_keys = []
    
    for i in range(count):
        if static_value is not None:
            dist_raw = static_value
        else:
            # Simulate a sine wave for water level (0 to 250cm)
            ft = current_virtual_time
            dist_raw = int(150 + 100 * math.sin(ft / 1000))
            dist_raw += random.randint(-2, 2)
            dist_raw = max(0, dist_raw)

        # Basic values for solar/battery
        bat = round(random.uniform(12.5, 14.5), 2)
        sol = round(random.uniform(18.0, 22.0), 2)

        # === 1. LoRaWAN Format ===
        if "lora" in sensor_id.lower():
            # Schema: distance_cm (int), timestamp (ms int)
            payload = {
                "distance_cm": dist_raw, 
                "packet_number": i,
                "timestamp": int(current_virtual_time * 1000), # Milliseconds
                "device_id": "lora-indoor-sim",
                "simulated": True
            }

        # === 2. FloodMonitor Format (Default) ===
        else:
            # Schema: ultrasound (string "R..."), bat_volt (string), timestamp (string sec)
            payload = {
                "ultrasound": f"R{dist_raw:04d}",
                "bat_volt": f"{bat}",
                "solar_volt": f"{sol}",
                "timestamp": f"{int(current_virtual_time)}",
                "simulated": True
            }

        # Decide whether to push immediately or batch
        if delay >= 0.2:
            # Slow mode: individual pushes
            new_ref = ref.push(payload)
            save_key(sensor_id, new_ref.key)
            print(f"[{i+1}/{count}] Ts: {payload['timestamp']} | Value: {dist_raw} | Key: {new_ref.key}")
            time.sleep(delay)
        else:
            # Fast mode: append to batch
            # Generate a local push id (approximate) or let Firebase handle if we use push()
            # Actually, `ref.push()` generates a key locally without network call if we don't pass data immediately
            new_ref = ref.push() 
            batch_data[new_ref.key] = payload
            batch_keys.append(new_ref.key)
            
            # Update virtual time for next iteration
            current_virtual_time += interval

    # Execute Batch if any
    if batch_data:
        print(f"⚡ Fast Mode: Sending {len(batch_data)} records in one batch update...")
        ref.update(batch_data)
        
        # Save keys
        for key in batch_keys:
            save_key(sensor_id, key)
            
        print("✅ Batch update complete.")
    else:
        print("✅ Simulation complete.")

def cleanup_data():
    print("🧹 Cleaning up simulated data...")
    try:
        with open(KEYS_FILE, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("⚠️ No keys file found. Nothing to clean.")
        return

    for sensor_id, keys in data.items():
        print(f"Cleaning {len(keys)} records for {sensor_id}...")
        ref = db.reference(f"/{sensor_id}")
        
        for key in keys:
            try:
                ref.child(key).delete()
                print(f"Deleted {key}", end='\r')
            except Exception as e:
                print(f"Failed to delete {key}: {e}")
        print() # Newline

    # Clear file
    os.remove(KEYS_FILE)
    print("✨ Cleanup complete. All traced keys removed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate Flood Monitor Data")
    parser.add_argument("--mode", choices=["run", "clean"], required=True, help="Mode: run or clean")
    parser.add_argument("--sensor", default="floodmonitor1", help="Sensor ID to direct data to")
    parser.add_argument("--count", type=int, default=10, help="Number of records to push")
    parser.add_argument("--delay", type=float, default=0.5, help="Execution delay (seconds) between pushes (Speed of script)")
    parser.add_argument("--interval", type=int, default=120, help="Virtual time interval (seconds) between data points (Timestamp spacing)")
    parser.add_argument("--past", action="store_true", help="If set, generates data ending at 'now' (Backfill mode). If not set, starts at 'now' (Future/Live mode).")
    parser.add_argument("--static-value", type=int, default=None, help="Optional static value to use instead of generating a sine wave")

    args = parser.parse_args()
    setup_firebase()

    if args.mode == "run":
        generate_data(args.sensor, args.count, args.delay, args.interval, args.past, args.static_value)
    elif args.mode == "clean":
        cleanup_data()
