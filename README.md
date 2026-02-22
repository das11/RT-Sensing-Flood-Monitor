# HimDhara - Flood Monitor Bridge 🌉

The **Flood Monitor Bridge** is a robust, stateless service that synchronizes real-time sensor data from **Firebase Realtime Database** to **InfluxDB**. It acts as the core data processing engine for the HimDhara RT Sensing Dashboard, normalizing and persisting data for downstream visualization.

---

## 🏗️ Architecture & Component Logic

The system is composed of several interdependent microservices running in Docker containers.

### Component Breakdown
- **Bridge Service (Python):** The backbone. Connects to Firebase, polls for new data based on a cursor, cleans and normalizes the incoming payload (handling various string/integer formats and fixing timestamps), and writes the points to InfluxDB. It is stateless and self-healing.
- **InfluxDB (v2):** A high-performance time-series database optimized for storing massive amounts of chronological sensor readings. It acts as the single source of historical truth.
- **Grafana:** The internal analytics visualization platform, connecting directly to InfluxDB to chart historical sensor trends and provide deep-dive metric dashboards.
- **Dashboard SPA (React):** The public-facing, responsive web application (SuperHer UI) providing a curated, aesthetic view of the live sensor data to the public.
- **Nginx Gateway (Production Only):** A reverse proxy that routes traffic to the appropriate service (`/` for SPA, `/grafana` for Grafana, etc.) ensuring a single entry point and avoiding cross-origin (CORS) issues.
- **Dozzle (Production Only):** A lightweight log viewer for real-time monitoring of Docker container outputs.

### Bridge Core Features
1. **Cursor-Based Polling:** Scraps fragile WebSockets for a smart polling loop (every 1.0s). It only fetches records strictly newer than the last successfully processed key, batching up to 100 records per poll.
2. **Double-Layer State Recovery:**
   - *Tier 1 (Local Cache):* `src/bridge_state.json` provides instant resume capabilities for transient restarts.
   - *Tier 2 (InfluxDB Backup):* If the container is destroyed, it seamlessly queries InfluxDB for the last synced `fb_key` and picks up exactly where it left off.
3. **Universal Data Normalization:** Fixes messy device payloads (e.g., mapping `dist_cm` vs `level`, converting string voltages to floats, and converting milliseconds vs seconds epoch times gracefully).

---

## ⚙️ Configuration Setup

Before running the stack, you need the following configuration files at the root of the `flood-monitor-bridge` directory:

### 1. `.env` file
Stores credentials for the database setup.
```env
DOCKER_INFLUXDB_INIT_MODE=setup
DOCKER_INFLUXDB_INIT_USERNAME=admin
DOCKER_INFLUXDB_INIT_PASSWORD=password123
DOCKER_INFLUXDB_INIT_ORG=kabir-das-org
DOCKER_INFLUXDB_INIT_BUCKET=flood_monitoring
DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=my-super-secret-auth-token
```

### 2. `serviceAccountKey.json`
Firebase Admin SDK credentials. Obtain this from the Google Cloud / Firebase console under "Service Accounts" and save the JSON file here.

### 3. `sensor_config.yaml`
Defines the sensors the bridge should track.
```yaml
sensors:
  - id: "floodmonitor1"
    name: "Guwahati Central Station"
    firebase_path: "sensors/floodmonitor1"
```

---

## 🗄️ Database (InfluxDB) Setup

The database initializes automatically when the Docker stack is brought up for the first time. The credentials defined in the `.env` file are utilized by the `influxdb:2` image to bootstrap:
- **Username:** `admin` | **Password:** `password123`
- **Bucket:** `flood_monitoring`
- **Organization:** `kabir-das-org`
- **Auth Token:** `my-super-secret-auth-token`

No manual configuration is needed unless you destroy the `influxdb_data` volume.

---

## 📈 Grafana Setup

Grafana is spun up alongside the database. To set up the dashboards:

1. **Login:** Access Grafana (Credentials: `admin` / `admin`).
2. **Add Data Source:**
   - Go to Data Sources -> Add InfluxDB.
   - Query Language: `Flux`
   - URL: `http://influxdb:8086`
   - Disable Basic Auth.
   - InfluxDB Details:
     - Organization: `kabir-das-org`
     - Token: `my-super-secret-auth-token`
     - Default Bucket: `flood_monitoring`
3. **Import Dashboard:**
   - Go to Dashboards -> Import.
   - Upload the included `grafana_dashboard.json` file.
   - Select the newly created InfluxDB data source if prompted.

---

## 🚀 Deployment Instructions

### Option A: Local Development Stack (`docker-compose.yml`)
Runs the services directly binding to localhost ports. Ideal for active development.

**Command:**
```bash
docker compose up -d --build
```

**Access Points:**
- **Public Dashboard SPA:** `http://localhost:5173`
- **Grafana:** `http://localhost:3000`
- **InfluxDB UI:** `http://localhost:8086`

### Option B: Production Stack (`docker-compose.prod.yml`)
Designed for EC2/VPS deployment. Services are secured behind the Nginx Gateway.

**Command:**
```bash
docker compose -f docker-compose.prod.yml up -d --build
```

**Access Points (All via Port 80):**
- **Public Dashboard SPA:** `http://<server-ip>/`
- **Grafana:** `http://<server-ip>/grafana/`
- **Dozzle (Logs):** `http://<server-ip>/dozzle/`
- **InfluxDB API:** Backwards routed via `/influxdb/` (UI strictly on `:8086` if firewall permits).

---

## 🛠️ Development & Simulation

We include powerful tools to test the bridge without waiting for real rain.

### 🌊 Simulate Data (`src/simulate_data.py`)
Generates realistic sensor patterns (Sine Waves) and pushes them to Firebase.

**Instant Batch (Fast Mode):** generates 4 hours of data instantly.
```bash
docker compose exec bridge python src/simulate_data.py --mode run --sensor floodmonitor1 --count 120 --interval 120 --delay 0.1 --past
```
*Note:* `--past` backfills data ending "now", `--delay 0.1` triggers batch mode.

**Real-Time Simulation:** 1 record every second.
```bash
docker compose exec bridge python src/simulate_data.py --mode run --sensor floodmonitor1 --count 100 --interval 5 --delay 1.0
```

### 🔍 Verify Data (`src/verify_data.py`)
Checks InfluxDB to confirm data arrival, integrity, and the State Recovery key check.
```bash
docker compose exec bridge python src/verify_data.py
```

---

## 📊 Useful Flux Queries (InfluxDB)

**View Last Synced Firebase Key (Debug State Recovery):**
```flux
from(bucket: "flood_monitoring")
  |> range(start: -30d)
  |> filter(fn: (r) => r["_measurement"] == "sensor_reading")
  |> filter(fn: (r) => r["_field"] == "fb_key")
  |> last()
  |> group(columns: ["sensor_id"])
  |> yield(name: "last_synced_keys")
```

**Check Recent Measurement Trends:**
```flux
from(bucket: "flood_monitoring")
  |> range(start: -1h)
  |> filter(fn: (r) => r["_measurement"] == "sensor_reading")
  |> filter(fn: (r) => r["_field"] == "dist_cm")
  |> aggregateWindow(every: 1m, fn: mean, createEmpty: false)
  |> yield(name: "recent_trend")
```

---
*Maintained by the HimDhara Development Team.*
