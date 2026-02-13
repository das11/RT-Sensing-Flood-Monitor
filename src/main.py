
import os
import time
import datetime
import re
import json
import logging
from typing import Dict, Any, Optional

import firebase_admin
from firebase_admin import credentials, db
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load Environment Variables
load_dotenv()

# Configuration
FIREBASE_DB_URL = os.getenv("FIREBASE_DB_URL")
SERVICE_ACCOUNT_KEY = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "serviceAccountKey.json")

INFLUX_URL = os.getenv("INFLUX_URL")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")

def clean_sensor_data(key: str, data: Dict[str, Any]) -> Optional[Point]:
    """
    Normalizes sensor data and converts it to an InfluxDB Point.
    
    Expected Key format: floodmonitor1/some_push_id
    Expected Data format:
    {
        "dist_cm": "R0845", 
        "bat_volt": 12.5, 
        "solar_volt": 14.2,
        "timestamp": 1700000000 or "1700000000"
    }
    """
    try:
        # 1. Extract Sensor ID from the path/structure
        # Adjust logic based on actual Firebase structure. 
        # Assuming the listener is at root, 'path' might be "/floodmonitor1/-Oa3..."
        sensor_id = key.split('/')[1] if '/' in key else "unknown_sensor"

        # 2. Normalize Distance/Level
        # Priority: dist_cm -> distance_cm -> ultrasound -> level -> distance
        raw_dist = (data.get("dist_cm") or 
                   data.get("distance_cm") or 
                   data.get("ultrasound") or 
                   data.get("level") or 
                   data.get("distance"))
        
        dist_cm = 0
        if raw_dist is not None:
            # Handle String (e.g., "R0231", "MR0152", "512")
            if isinstance(raw_dist, str):
                # Use regex to find the first sequence of digits
                match = re.search(r'\d+', raw_dist)
                if match:
                    try:
                        dist_cm = int(match.group())
                    except ValueError:
                        logger.warning(f"Failed to parse digits: {raw_dist} in {key}")
                else:
                    if raw_dist.strip():
                        logger.warning(f"No digits found in: {raw_dist} in {key}")
            
            # Handle Number
            elif isinstance(raw_dist, (int, float)):
                 dist_cm = int(raw_dist)

        # 3. Voltage Handling (Aliases)
        bat = data.get("bat_volt") or data.get("battery_voltage") or data.get("battery") or data.get("voltage") or 0.0
        sol = data.get("solar_volt") or data.get("solar_voltage") or data.get("solar") or 0.0

        # 4. Timestamp Handling
        raw_ts = data.get("timestamp", time.time())
        try:
            ts = float(raw_ts)
            
            # Heuristic: If timestamp is > 100 billion (year 5138), assume milliseconds
            if ts > 1e11:
                ts = ts / 1000.0
                
            dt_obj = datetime.datetime.fromtimestamp(ts, datetime.timezone.utc)
        except (ValueError, TypeError, OSError):
             dt_obj = datetime.datetime.now(datetime.timezone.utc)

        # 5. Create Influx Point
        point = Point("sensor_reading") \
            .tag("sensor_id", sensor_id) \
            .field("dist_cm", dist_cm) \
            .field("bat_volt", float(bat)) \
            .field("solar_volt", float(sol)) \
            .field("fb_key", str(key.split('/')[-1])) \
            .time(dt_obj)
        
        return point

    except Exception as e:
        logger.error(f"Error processing data for key {key}: {e}")
        return None

def main():
    # 1. Initialize InfluxDB Client
    if not INFLUX_TOKEN:
        logger.error("INFLUX_TOKEN is missing.")
        return

    if not INFLUX_BUCKET:
        logger.error("INFLUX_BUCKET is missing.")
        return

    bucket = INFLUX_BUCKET
    org = INFLUX_ORG

    if not org:
        logger.error("INFLUX_ORG is missing.")
        return

    influx_client = InfluxDBClient(
        url=INFLUX_URL,
        token=INFLUX_TOKEN,
        org=org
    )
    write_api = influx_client.write_api(write_options=WriteOptions(batch_size=1, flush_interval=100))
    logger.info("Connected to InfluxDB.")

    # 2. Initialize Firebase
    if not os.path.exists(SERVICE_ACCOUNT_KEY):
        logger.error(f"Service Account Key not found at {SERVICE_ACCOUNT_KEY}")
        # For dev purposes, continuing might fail, but let's warn.
        return

    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
    firebase_admin.initialize_app(cred, {
        'databaseURL': FIREBASE_DB_URL
    })
    logger.info(f"Connected to Firebase at {FIREBASE_DB_URL}")

    # 3. Define Listener
    def listener(event):
        """
        Callback for Firebase events.
        """
        try:
            if event.data is None:
                return

            logger.info(f"Received event: {event.event_type} at {event.path}")
            
            # We only care about new data (put)
            if event.event_type == 'put':
                # CASE 1: Root Update (Initial Load or Massive Push)
                if event.path == "/":
                    if isinstance(event.data, dict):
                        points = []
                        logger.info(f"Processing ROOT update with {len(event.data)} sensors.")
                        for sensor_key, sensor_data in event.data.items():
                            if isinstance(sensor_data, dict):
                                 for push_id, record in sensor_data.items():
                                     if isinstance(record, dict):
                                         pt = clean_sensor_data(f"/{sensor_key}/{push_id}", record)
                                         if pt: points.append(pt)
                        
                        if points:
                            write_api.write(bucket=bucket, record=points)
                            logger.info(f"Backfilled {len(points)} records from ROOT update.")
                
                # CASE 2: Specific Record Update (e.g., /floodmonitor1/-Oa3...)
                else:
                    # event.path matches something like "/floodmonitor1/-Oa3810239120"
                    # We need to ensure we are at the RECORD level, not the sensor level
                    parts = event.path.strip('/').split('/')
                    
                    # If parts = ['floodmonitor1'], then event.data is a dict of records
                    if len(parts) == 1:
                        sensor_id = parts[0]
                        if isinstance(event.data, dict):
                            points = []
                            for push_id, record in event.data.items():
                                if isinstance(record, dict):
                                    pt = clean_sensor_data(f"/{sensor_id}/{push_id}", record)
                                    if pt: points.append(pt)
                            if points:
                                write_api.write(bucket=bucket, record=points)
                                logger.info(f"Wrote {len(points)} records for sensor {sensor_id}")

                    # If parts = ['floodmonitor1', '-Key123'], then event.data is the record
                    elif len(parts) == 2:
                        pt = clean_sensor_data(event.path, event.data)
                        if pt:
                            write_api.write(bucket=bucket, record=pt)
                            logger.info(f"Wrote 1 record: {event.path}")
                            
        except Exception as e:
            logger.error(f"Listener Error: {e}")

    # 4. Start Polling Loop
    SENSORS = ["floodmonitor1", "floodmonitor2", "LoRaWAN"]
    STATE_FILE = "src/bridge_state.json"
    cursors = {} # {sensor_id: last_seen_key}

    # Helper to load/save state
    def load_state_from_file():
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load state file: {e}")
        return {}

    def save_state(cursors_data):
        try:
            with open(STATE_FILE, 'w') as f:
                json.dump(cursors_data, f)
        except Exception as e:
            logger.error(f"Failed to save state file: {e}")

    def fetch_last_key_from_influx(sensor_id):
        """
        Queries InfluxDB to find the last 'fb_key' written for this sensor.
        """
        query_api = influx_client.query_api()
        q = f"""
        from(bucket: "{bucket}")
          |> range(start: -30d)
          |> filter(fn: (r) => r["_measurement"] == "sensor_reading")
          |> filter(fn: (r) => r["sensor_id"] == "{sensor_id}")
          |> filter(fn: (r) => r["_field"] == "fb_key")
          |> last()
        """
        try:
            result = query_api.query(q)
            if result:
                for table in result:
                    for record in table.records:
                        return record.get_value()
        except Exception as e:
            logger.warning(f"[{sensor_id}] Could not fetch last key from InfluxDB: {e}")
        return None

    # Initialize cursors
    saved_state = load_state_from_file()
    logger.info("Initializing cursors...")
    
    for sensor in SENSORS:
        # Priority 1: Local State File
        if sensor in saved_state:
            cursors[sensor] = saved_state[sensor]
            logger.info(f"[{sensor}] Resuming from LOCAL FILE cursor: {cursors[sensor]}")
        
        else:
            # Priority 2: InfluxDB (Recovery)
            influx_key = fetch_last_key_from_influx(sensor)
            if influx_key:
                cursors[sensor] = influx_key
                logger.info(f"[{sensor}] Resuming from INFLUXDB cursor: {cursors[sensor]}")
            
            # Priority 3: Fresh Start (Latest)
            else:
                try:
                    snapshot = db.reference(f"/{sensor}").order_by_key().limit_to_last(1).get()
                    if snapshot and isinstance(snapshot, dict):
                        last_key = list(snapshot.keys())[-1]
                        cursors[sensor] = last_key
                        logger.info(f"[{sensor}] No history found. Starting FRESH at: {last_key}")
                    else:
                        cursors[sensor] = None 
                        logger.info(f"[{sensor}] No data found on Firebase. Starting fresh.")
                except Exception as e:
                    logger.error(f"Failed to fetch initial cursor for {sensor}: {e}")
                    cursors[sensor] = None

    # Initial save
    save_state(cursors)
    logger.info("Starting Polling Loop...")

    try:
        while True:
            for sensor in SENSORS:
                try:
                    ref = db.reference(f"/{sensor}")
                    query = ref.order_by_key()
                    
                    last_key = cursors.get(sensor)
                    if last_key:
                        # Fetch records starting AFTER the last known key
                        # Firebase only has start_at, so we fetch starting at last_key
                        # and filter it out locally.
                        query = query.start_at(last_key).limit_to_first(100)
                    else:
                        # If no history, just get current/new
                        query = query.limit_to_last(100)

                    snapshot = query.get()

                    if snapshot and isinstance(snapshot, dict):
                        # If snapshot returns the exact same single key as last_key, nothing new
                        if len(snapshot) == 1 and last_key in snapshot:
                            continue
                            
                        # Process records
                        points = []
                        new_last_key = last_key
                        
                        # Sort keys to ensure order (get() might return OrderedDict or dict)
                        sorted_keys = sorted(snapshot.keys())
                        
                        for key in sorted_keys:
                            if key == last_key:
                                continue # Skip the cursor itself
                            
                            record = snapshot[key]
                            if isinstance(record, dict):
                                pt = clean_sensor_data(f"/{sensor}/{key}", record)
                                if pt: points.append(pt)
                            
                            new_last_key = key # Advance cursor
                        
                        if points:
                            write_api.write(bucket=bucket, record=points)
                            logger.info(f"[{sensor}] Processed {len(points)} new records.")
                            cursors[sensor] = new_last_key
                            save_state(cursors)
                            
                except Exception as e:
                    logger.error(f"Error polling {sensor}: {e}")
            
            # Sleep to prevent high CPU usage
            time.sleep(1.0)

    except KeyboardInterrupt:
        logger.info("Stopping bridge service...")
        influx_client.close()

if __name__ == "__main__":
    main()
