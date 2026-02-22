# Implementation Master Plan: Real-Time Multi-Sensor Dashboard

**Project Goal:** Visualize distributed flood monitoring sensor data in Grafana via a Dockerized ETL bridge.
**Current Status:** Feasibility Proven. InfluxDB Dev Account Ready.
**Repository:** *[To be created]*
**Package Manager:** `uv` (Astral)

---

## Phase 1: Infrastructure & Foundation
**Objective:** Secure connectivity and prepare the data destination.

- [ ] **1.1. Repository Setup**
    - Initialize Git repository.
    - Initialize `uv` project:
      ```bash
      uv init flood-monitor-bridge
      ```
    - Create `.gitignore` (ensure `serviceAccountKey.json`, `.env`, and `.venv/` are ignored).
    - Create project structure (`/src`, `/docker`, `/docs`).

- [ ] **1.2. Firebase Access Configuration**
    - Generate a new **Firebase Service Account Key** (JSON) with `read-only` access to the Realtime Database.
    - Verify access to the specific database URL: `https://fmsiitg-b2890-default-rtdb.asia-southeast1.firebasedatabase.app/`.

- [ ] **1.3. InfluxDB Schema Design**
    - Create a dedicated bucket named `flood_monitoring`.
    - Create an **All-Access Token** (for admin) and a **Write-Only Token** (for the Bridge).
    - **Schema Strategy:**
        - **Measurement:** `sensor_reading`
        - **Tags:** `sensor_id` (e.g., `floodmonitor1`), `location` (optional)
        - **Fields:** `dist_cm` (int), `bat_volt` (float), `solar_volt` (float)

---

## Phase 2: Bridge Service Development (The Core)
**Objective:** Build the Python ETL that handles *multiple* data streams dynamically.

- [ ] **2.1. Dependency Management (uv)**
    - Add required packages using `uv`:
      ```bash
      uv add firebase-admin influxdb-client python-dotenv
      ```
    - This automatically creates/updates `pyproject.toml` and `uv.lock`.

- [ ] **2.2. Multi-Sensor Listener Logic**
    - Update Python script to listen to the root path `/` (or a configured list of paths).
    - **Dynamic Parsing:** Implement logic to parse the event path.
        - *Input:* Event at `/floodmonitor1/-Oa3TR...`
        - *Action:* Extract `floodmonitor1` and use it as the `sensor_id` tag.
    - *Constraint:* Ignore keys that do not match the expected sensor naming convention (Regex validation).

- [ ] **2.3. Data Normalization Upgrade**
    - Implement the "R" stripper: `R0845` -> `845` (Integer).
    - Implement timestamp converter: Unix Epoch String -> InfluxDB DateTime object.
    - Handle "missing keys" gracefully (e.g., if `bat_volt` is missing, default to `0.0` or skip).

- [ ] **2.4. InfluxDB Batch Writing**
    - Implement the `sensor_id` tag in the Influx Point structure.
    - *Code Snippet Logic:*
      ```python
      Point("sensor_reading") \
          .tag("sensor_id", sensor_name) \
          .field("dist_cm", clean_dist) \
          .time(time_obj)
      ```
    - Add exception handling (log errors to stdout/stderr without crashing the script).

---

## Phase 3: Dockerization & Ops
**Objective:** Make the bridge deployable anywhere with a single command using a multi-stage `uv` build.

- [ ] **3.1. Container Configuration (Dockerfile)**
    - Create a `Dockerfile` optimized for `uv`.
    - **Stage 1 (Builder):** Use `ghcr.io/astral-sh/uv:python3.11-bookworm-slim`.
        - Copy `pyproject.toml` and `uv.lock`.
        - Run `uv sync --frozen --no-install-project` to install dependencies.
    - **Stage 2 (Runner):** Copy the virtual environment from Stage 1.
        - `ENV VIRTUAL_ENV=/app/.venv`
        - `ENV PATH="$VIRTUAL_ENV/bin:$PATH"`
        - Copy `src/` code.
        - CMD: `["python", "src/main.py"]`

- [ ] **3.2. Environment Management**
    - Create `.env.example` file.
    - **Required Variables:**
        - `FIREBASE_DB_URL`
        - `INFLUX_URL`
        - `INFLUX_TOKEN`
        - `INFLUX_ORG`
        - `INFLUX_BUCKET`
    - **Volume Mount:** Ensure `serviceAccountKey.json` is mounted at runtime, NOT built into the image.

- [ ] **3.3. Docker Compose Setup**
    - Create `docker-compose.yml`.
    - Define restart policy: `restart: always` (Crucial for unsupervised operation).
    - Service definition example:
      ```yaml
      services:
        bridge:
          build: .
          restart: always
          volumes:
            - ./serviceAccountKey.json:/app/serviceAccountKey.json
          env_file: .env
      ```

---

## Phase 4: Visualization (Grafana)
**Objective:** Create a single "Smart Dashboard" that works for all sensors.

- [ ] **4.1. Data Source Connection**
    - Connect Grafana to InfluxDB using **Flux** language.

- [ ] **4.2. Variable Setup (The "Dropdown")**
    - Create a Dashboard Variable named `$sensor`.
    - **Query:**
      ```flux
      import "influxdata/influxdb/schema"
      schema.tagValues(bucket: "flood_monitoring", tag: "sensor_id")
      ```
    - *Result:* A dropdown list containing `floodmonitor1`, `floodmonitor2`, etc.
    - Enable "Multi-value" and "Include All" options.

- [ ] **4.3. Primary Panels Configuration**
    - **Distance Trend:** Flux query filtering by `r.sensor_id == "$sensor"`.
    - **Battery/Solar Voltage:** Multi-line graph for power stats.
    - **Current Status:** Stat panel showing the *latest* `ultrasound_cm` value.

- [ ] **4.4. Thresholds & Alerts**
    - Define thresholds (e.g., Red zone if distance < 200cm).
    - (Optional) Configure email/Telegram alert channel.

---

## Phase 5: Testing & Handover
**Objective:** Validate against real scenarios and document.

- [ ] **5.1. Load Testing**
    - Simulate data inputs for `floodmonitor1` and `floodmonitor2` simultaneously.
    - Verify both appear in the Grafana dropdown immediately.

- [ ] **5.2. Resilience Testing**
    - Kill the Docker container and ensure it auto-restarts.
    - Disconnect internet briefly and ensure script reconnects to Firebase stream.

- [ ] **5.3. Documentation**
    - Write `README.md` with:
        - **Quick Start:** `uv sync` -> `uv run src/main.py`.
        - **Docker Start:** `docker compose up -d`.
        - **Adding Sensors:** "No code change required. Just push data to a new key in Firebase."
    - Deliver `deployment.zip` containing all source code and Docker configs.

---

### *Phase 6: Future Scope (Post-MVP)*
- *Image Integration:* Create a separate service to watch Firebase Storage buckets, generate signed URLs, and push those URLs to InfluxDB/Grafana for display in the "Text/HTML" panel.