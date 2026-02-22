



<div style="text-align: center; margin-top: 40%"> 
	<img src="file:////Users/interfacev2/Downloads/OnSite Color Guidelines.avif" alt="Company Logo" width="200"/> 
</div>

<div style="text-align:center; font-weight:bold; font-size:1.5rem; margin-top:20px; margin-bottom:20px">
Solution Summary - RT Sensing Data Dashboard
</div>


<div style="text-align: center; page-break-after: always;">
	<table style="margin: auto; border-collapse: collapse; width: 80%;"> 
		<thead> 
			<tr> 
				<th style="border: 1px solid black; padding: 8px;">Version</th> 
				<th style="border: 1px solid black; padding: 8px;">Date</th> 
				<th style="border: 1px solid black; padding: 8px;">Prepared By</th>
				<th style="border: 1px solid black; padding: 8px;">Description</th> 
			</tr>
		</thead> 
		<tbody> 
			<tr> 
				<td style="border: 1px solid black; padding: 8px;">1.0</td>
				<td style="border: 1px solid black; padding: 8px;">2026-02-01</td> 
				<td style="border: 1px solid black; padding: 8px;">Onsite Academy Pvt. Ltd.</td> 
				<td style="border: 1px solid black; padding: 8px;">Initial document draft</td> 
			</tr>
		</tbody> 
	</table>
</div>
---

# Real-Time IoT Sensor Visualization Pipeline

## 1. Executive Summary

This document outlines the architecture for a real-time monitoring system to visualize the sensor data. The solution bridges the existing **Firebase Realtime Database (RTDB)** ingestion layer with **Grafana**, a robust visualization platform.

To address specific constraints and ensure high-performance historical trending, an intermediate **Time-Series Data Layer (InfluxDB)** and a **Transformation Service** are introduced.

## 2. Problem Statement & Constraints

- **Source Data Format:** The sensor emits json data containing alphanumeric strings which prevents direct mathematical aggregation or graphing in standard visualization tools.
- **Database Nature:** Firebase RTDB is a document store optimized for app state synchronization, not for time-series analytics.
- **Latency:** The client requires near real-time visualization (2-minute intervals).

## 3. Proposed Architecture

I propose a decoupled **ETL (Extract, Transform, Load)** architecture.

1. **Ingestion:** Sensor pushes raw data to Firebase.
2. **Processing (The Bridge):** A lightweight Python service listens to Firebase changes in real-time, strips the "R" prefix, and formats the timestamp.
3. **Storage:** Cleaned numerical data is stored in **InfluxDB**, a database optimized for time-stamped data.
4. **Visualization:** **Grafana** queries InfluxDB to render dashboards, alerts, and historical trends.

### Architecture Diagram

![[Solution Draft 2026-02-01 20.52.38.excalidraw|250]]

## 4. Component Breakdown

| **Component**     | **Role**          |
| ----------------- | ----------------- |
| **Firebase RTDB** | **Buffer**        |
| **Python Bridge** | **Transformer**   |
| **InfluxDB**      | **TimeSeries DB** |
| **Grafana**       | **UI**            |

## 5. Data Flow Lifecycle

1. **Emission:** The sensor wakes up and sends the json payload to Firebase RTDB
2. **Trigger:** The ETL bridge that acts the real time event listener
3. **Transformation:**
    - Logic: `int("R0845".replace("R", ""))` yields `845`.
    - Time: `1758864127` converted to `2025-09-24T...`.
    - Any other required transformations
4. **Ingestion:** The Bridge writes the normalized data points to InfluxDB
5. **Rendering:** Grafana's dashboard auto-refreshes, queries InfluxDB, and plots the new point.

## 6. Scope of Work & Deliverables

This section defines the specific boundaries of the implementation phase.

### In-Scope Deliverables
* **Infrastructure Configuration:**
    * Setup of InfluxDB Cloud bucket and retention policies
    * Configuration of Grafana data source connections.
* **Bridge Service Development:**
    * Bridge ETL service development to listen to the specified Firebase node.
    * Data Normalization within then Bridge ETL service.
    * Containerization (Docker) for deployment stability.
* **Dashboard Creation:**
    * One (1) Primary Dashboard displaying **max. 5 metrics**:
        * Real-time Distance (cm) line chart etc
* **Historical Data Migration:** 
	* Existing data in Firebase prior to the deployment date will be backfilled into InfluxDB.
* **Documentation:**
    * Deployment guide (How to run the Docker container).
    * Environment variable configuration guide.

### Out-of-Scope
* **Hardware/Firmware Modification:** No changes will be made to the physical sensor or its firmware logic.
* **Hosting Costs:** The client is responsible for any cloud hosting fees (InfluxDB/Grafana Cloud/VPS).

## 7. Timeline

The estimated timeline for implementation is **3-4 weeks**, broken down as follows:

| Phase       | Activity                                  | Duration |
| :---------- | :---------------------------------------- | :------- |
| **Phase 1** | Infrastructure Setup (InfluxDB & Grafana) | Wk 1     |
| **Phase 2** | Bridge Service Development & Testing      | Wk 2     |
| **Phase 3** | Dockerization & Deployment                | Wk 3     |
| **Phase 4** | Dashboard Visualization & Refining        | Wk 4     |

## 8. Cost Estimates

*Note: These are estimates for the infrastructure running costs. Free tier's used wherever possible for development*

### **Total build cost :  ₹50,000**

## 9 Payment Terms

1. **₹30,000** as per generated invoice(Tentatively Wk 0 - Wk 2).
2. **₹20,000 final payment** before delivery/access hand-over.

All payments are non-refundable, as effort and time are committed progressively.


## 9. Assumptions & Disclaimers

* **Data Integrity:** The solution assumes the JSON structure from the sensor remains consistent. Any changes to key names (e.g., `ultrasound_cm` changing to `dist_cm`) will require updates to the Bridge service.
* **Connectivity:** The solution relies on a stable internet connection for the Bridge service to communicate with both Firebase and InfluxDB.
* **API Limits:** The solution is designed within standard API rate limits. Significant scaling of sensor quantities may require changes.
* **Maintenance:** Post-deployment maintenance (software updates, security patches) is not included unless a support contract is established.

## 10. The team

- [Bhargav Choudhury, MD, (Onsite)](https://www.linkedin.com/in/bchoudhury/)
- [Kabir Das, Solutions Architect (Consultant to Onsite)](https://www.linkedin.com/in/kabir-das-764274a1/)
- [Jayatu Bhuyan, Co-founder, (Onsite)](https://www.linkedin.com/in/jayatu-bhuyan-9b696479/)



---

## Annexure - I

### Operational Costs

* **InfluxDB Cloud:** Free Tier (suitable for current load) or Usage-based starting at ~$20/mo if retention increases.
* **Grafana Cloud:** Free Tier (includes 3 users) or Pro starting at ~$29/mo.
* **VPS for Bridge Service:** $10-$15/mo.
