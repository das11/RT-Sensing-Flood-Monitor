import React, { useState, useRef, useEffect } from "react";
import { Routes, Route } from "react-router-dom";
import Hero from "./components/Hero";
import Gauge from "./components/Gauge";
import Map from "./components/Map";
import SensorPicker from "./components/SensorPicker";
import SENSORS from "./config/sensors.json";
import { fetchLatestReading } from "./services/influxService";
import WaterLevelGraph from "./components/WaterLevelGraph";
import ImageTimeline from "./components/ImageTimeline";
import AboutHimdhara from "./components/AboutHimdhara";
import SupportersSection from "./components/SupportersSection";
import mainLogo from "./assets/logos/Main Logo.png";
import "./App.css";

/* ── Dashboard (the original home page) ── */
function Dashboard() {
  const [selectedSensorId, setSelectedSensorId] = useState(SENSORS[0].id);
  const [sensorData, setSensorData] = useState({
    level: 0,
    lastUpdated: "Loading...",
    battery: 0,
    solar: 0
  });

  const selectedSensorConfig = SENSORS.find(s => s.id === selectedSensorId);
  const selectedSensor = { ...selectedSensorConfig, ...sensorData };
  const dashboardRef = useRef(null);

  // Header Visibility State
  const [showHeader, setShowHeader] = useState(false);
  const [currentDate, setCurrentDate] = useState("");

  // Poll for Data
  useEffect(() => {
    let isMounted = true;

    const fetchData = async () => {
      if (!selectedSensorConfig) return;
      const queryId = selectedSensorConfig.station_id || selectedSensorConfig.id;
      const data = await fetchLatestReading(queryId);

      if (isMounted) {
        if (data) {
          setSensorData(data);
        } else {
          if (selectedSensorConfig.default_data) {
            setSensorData({ ...selectedSensorConfig.default_data, lastUpdated: "OFFLINE" });
          } else {
            setSensorData(prev => ({ ...prev, lastUpdated: "OFFLINE" }));
          }
        }
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => { isMounted = false; clearInterval(interval); };
  }, [selectedSensorId]);

  // Handle Scroll for Header & Date
  useEffect(() => {
    const dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    setCurrentDate(new Date().toLocaleDateString('en-US', dateOptions));

    const handleScroll = () => {
      setShowHeader(window.scrollY > 50);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const scrollToDashboard = () => {
    dashboardRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <>
      {/* Dynamic Floating Header */}
      <div className={`dynamic-header ${showHeader ? 'visible' : ''}`}>
        <div style={{ display: 'flex', alignItems: 'center', borderRight: '1px solid #e2e8f0', paddingRight: '1.5rem' }}>
          <img src={mainLogo} alt="HimDhara" className="header-logo" />
          <span className="header-title">Himधारा</span>
        </div>
        <div className="header-date" style={{ borderRight: '1px solid #e2e8f0', paddingRight: '1.5rem', marginRight: '0' }}>{currentDate}</div>
        <div className={`header-live ${selectedSensor.lastUpdated === "OFFLINE" ? "offline" : ""}`}>
          <span className={`live-pulse ${selectedSensor.lastUpdated === "OFFLINE" ? "bg-yellow-500 shadow-yellow-500" : ""}`}></span>
          {selectedSensor.lastUpdated === "OFFLINE" ? "System Offline" : "Live Monitoring"}
        </div>
      </div>

      <Hero onCtaClick={scrollToDashboard} />

      {/* Dashboard Section */}
      <main className="main-content" ref={dashboardRef}>
        <section className="dashboard-section">
          <div className="dashboard-grid">

            {/* 1. Left Column (60%) */}
            <div className="left-column">

              {/* Top Card: Controls */}
              <div className="glass-panel controls-panel">
                <div className="combined-controls-area">
                  <div className="controls-card vibrant">
                    <SensorPicker
                      sensors={SENSORS}
                      selectedId={selectedSensorId}
                      onSelect={setSelectedSensorId}
                    />
                  </div>
                  <div className="controls-card details">
                    <h2 className="section-label">Sensor Details</h2>
                    <h1 className="info-title">{selectedSensor.name}</h1>
                    <p className="info-desc">{selectedSensor.description}</p>
                    <div className="info-meta">
                      <span className={`flex items-center gap-2 ${selectedSensor.lastUpdated === "OFFLINE" ? "text-yellow-500" : "text-gray-500"}`}>
                        <span className={`w-2 h-2 rounded-full ${selectedSensor.lastUpdated === "OFFLINE" ? "bg-yellow-500" : "bg-green-500"}`}></span>
                        Updated: {selectedSensor.lastUpdated}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Bottom Card: Gauge */}
              <div className="glass-panel gauge-panel">
                <div className="combined-gauge-area">
                  <Gauge
                    level={selectedSensor.level}
                    thresholds={selectedSensor.thresholds}
                  />
                </div>
              </div>

            </div>

            {/* 2. Map Panel */}
            <div className="glass-panel grid-item-map">
              <Map
                location={selectedSensor.position}
                sensorName={selectedSensor.name}
              />
            </div>

          </div>
        </section>

        {/* Section 3: Water Level Graph */}
        <section className="graph-section">
          <div className="dashboard-full-width">
            <WaterLevelGraph
              sensorId={selectedSensorConfig?.station_id || selectedSensorConfig?.id}
              sensorName={selectedSensor.name}
            />
          </div>
        </section>

        {/* Section 4: Image Timeline (only for sensors with cameras) */}
        {selectedSensorConfig?.image_views && (
          <section className="graph-section">
            <div className="dashboard-full-width">
              <ImageTimeline
                sensorId={selectedSensorConfig?.station_id || selectedSensorConfig?.id}
                imageViews={selectedSensorConfig.image_views}
              />
            </div>
          </section>
        )}

        {/* Section 5: Supporters */}
        <SupportersSection />
      </main>

      <footer className="app-footer">
        <div className="footer-links">
          <a href="/grafana" target="_blank" rel="noopener noreferrer" className="grafana-link">
            <span className="grafana-icon">📊</span>
            In-depth Technical Dashboard (Grafana)
          </a>
        </div>
        <p>&copy; 2026 Himधारा - Guwahati Flood Monitoring Network. All rights reserved.</p>
        <div className="built-by-tag">
          Built by <a href="https://www.linkedin.com/in/kabir-das-764274a1/" target="_blank" rel="noopener noreferrer" className="linkedin-link">Kabir Das</a>
        </div>
      </footer>
    </>
  );
}

/* ── App Shell (shared background + routing) ── */
function App() {
  return (
    <div className="app-container">
      {/* Global Background Elements */}
      <div className="global-aurora-bg">
        <div className="global-blob blob-1"></div>
        <div className="global-blob blob-2"></div>
        <div className="global-blob blob-3"></div>
      </div>

      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/about" element={<AboutHimdhara />} />
      </Routes>
    </div>
  );
}

export default App;
