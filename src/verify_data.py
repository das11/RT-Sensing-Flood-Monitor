
import os
import sys
import logging
from influxdb_client import InfluxDBClient

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Load Env (Simulated as we are running in docker where env is injected)
INFLUX_URL = os.getenv("INFLUX_URL")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")

def verify():
    print(f"--- InfluxDB Data Verification ---")
    print(f"Connecting to: {INFLUX_URL}")
    print(f"Org: {INFLUX_ORG}")
    print(f"Bucket: {INFLUX_BUCKET}")
    
    if not INFLUX_TOKEN:
        print("❌ Error: INFLUX_TOKEN is missing")
        return

    # Fix type hint issue by ensuring string
    client = InfluxDBClient(url=str(INFLUX_URL), token=str(INFLUX_TOKEN), org=str(INFLUX_ORG))
    query_api = client.query_api()

    print("\n🔎 Collecting Sensor Statistics (This may take a moment)...")

    # Helper to execute a query and extract simple {sensor_id: val} mapping
    def get_stats(agg_fn, extract_fn):
        q = f"""
        from(bucket: "{INFLUX_BUCKET}")
          |> range(start: 1970-01-01T00:00:00Z, stop: 2200-01-01T00:00:00Z)
          |> filter(fn: (r) => r["_measurement"] == "sensor_reading")
          |> filter(fn: (r) => r["_field"] == "dist_cm")
          |> group(columns: ["sensor_id"])
          |> {agg_fn}()
        """
        results = {}
        try:
            tables = query_api.query(q)
            for table in tables:
                for record in table.records:
                    sid = record.values.get("sensor_id")
                    results[sid] = extract_fn(record)
        except Exception as e:
            print(f"⚠️ Error in {agg_fn}: {e}")
        return results

    # 1. Fetch all metrics
    counts = get_stats("count", lambda r: r.get_value())
    min_vals = get_stats("min", lambda r: r.get_value())
    max_vals = get_stats("max", lambda r: r.get_value())
    first_times = get_stats("first", lambda r: r.get_time().strftime('%Y-%m-%d %H:%M:%S'))
    last_times = get_stats("last", lambda r: r.get_time().strftime('%Y-%m-%d %H:%M:%S'))

    # 2. Display Table
    sensors = set(counts.keys()) | set(min_vals.keys())
    
    if not sensors:
        print("⚠️ No data found in bucket.")
        return

    print(f"\n{'SENSOR_ID':<20} | {'COUNT':<8} | {'MIN':<6} | {'MAX':<6} | {'FIRST SEEN (UTC)':<20} | {'LAST SEEN (UTC)':<20}")
    print("-" * 100)
    
    for s in sorted(sensors):
        c = counts.get(s, 0)
        mn = min_vals.get(s, "N/A")
        mx = max_vals.get(s, "N/A")
        ft = first_times.get(s, "N/A")
        lt = last_times.get(s, "N/A")
        print(f"✅ {s:<20} | {c:<8} | {mn:<6} | {mx:<6} | {ft:<20} | {lt:<20}")

    print("\n\n🔎 Recent Raw Data (Last 5 records per sensor):")
    # Query to get last 5 records with their fields
    # Pivot matches fields by time, then we sort and limit.
    q_recent = f"""
    from(bucket: "{INFLUX_BUCKET}")
      |> range(start: 1970-01-01T00:00:00Z, stop: 2200-01-01T00:00:00Z)
      |> filter(fn: (r) => r["_measurement"] == "sensor_reading")
      |> filter(fn: (r) => r["_field"] == "dist_cm" or r["_field"] == "fb_key")
      |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
      |> group(columns: ["sensor_id"])
      |> sort(columns: ["_time"], desc: true)
      |> limit(n: 5)
    """
    try:
        tables = query_api.query(q_recent)
        for table in tables:
            for record in table.records:
                sid = record.values.get("sensor_id")
                val = record.values.get("dist_cm", "N/A")
                key = record.values.get("fb_key", "N/A")
                t = record.get_time().strftime('%Y-%m-%d %H:%M:%S')
                print(f"   [{sid}] {t} -> {val} cm (Key: {key})")
    except Exception as e:
        print(f"⚠️ Error fetching recent data: {e}")

    client.close()
    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    verify()
