import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
    ArrowLeft,
    Waves,
    Gauge,
    Radar,
    Droplets,
    Wind,
    Thermometer,
    BrainCircuit,
    AlertTriangle,
    ShieldCheck,
    Mountain,
    Anchor,
    Satellite,
    Activity,
} from "lucide-react";
import "./AboutHimdhara.css";

const fadeUp = {
    hidden: { opacity: 0, y: 30 },
    visible: (i = 0) => ({
        opacity: 1,
        y: 0,
        transition: { delay: i * 0.1, duration: 0.6, ease: "easeOut" },
    }),
};

const AboutHimdhara = () => {
    return (
        <div className="about-page">
            {/* Back Navigation */}
            <Link to="/" className="about-back-link">
                <ArrowLeft size={18} />
                <span>Back to Dashboard</span>
            </Link>

            {/* Hero Header */}
            <motion.header
                className="about-hero"
                initial="hidden"
                animate="visible"
                variants={fadeUp}
            >
                <div className="about-hero-pill">
                    <Mountain size={16} />
                    Indigenous Technology
                </div>
                <h1 className="about-hero-title">
                    <span className="about-title-highlight">Himधारा</span>
                </h1>
                <p className="about-hero-subtitle">
                    Digital Flood Monitoring and Forecasting System for Himalayan Rivers
                </p>
            </motion.header>

            {/* Main Content */}
            <div className="about-content">

                {/* Introduction */}
                <motion.section
                    className="about-glass-card about-intro"
                    initial="hidden"
                    whileInView="visible"
                    viewport={{ once: true, amount: 0.3 }}
                    variants={fadeUp}
                >
                    <p>
                        A unique indigenous digital flood monitoring and forecasting system has been developed for Himalayan rivers integrating real-time sensing, robust communication systems, and physics-based artificial intelligence for capturing, predicting, and managing flash floods and associated disaster risks. This system is designed to create a resilient human–infrastructure nexus for early warning and disaster preparedness.
                    </p>
                    <p>
                        Under changing climate scenarios, flood-induced casualties and infrastructure damage have shown an increasing trend across the Himalayan region. To address this challenge, a cost-effective and scalable flood monitoring technology has been indigenously developed and deployed in gauge-deficient, densely populated river reaches in Arunachal Pradesh. The system has been implemented with technological support from <strong>Sony International Limited, Japan</strong>, and financial support from the <strong>National Mission on Himalayan Studies (NMHS)</strong>, through the <strong>Technology Innovation Hub (TIH), IIT Guwahati</strong>.
                    </p>
                    <p>
                        The technology is specifically designed to function under extreme Himalayan conditions, including communication failures such as GSM network outages and loss of conventional telemetry links. The system incorporates redundant communication protocols and autonomous operational capability, ensuring uninterrupted monitoring and data acquisition even during extreme flood events.
                    </p>
                </motion.section>

                {/* Three-Tier Framework */}
                <motion.section
                    className="about-section"
                    initial="hidden"
                    whileInView="visible"
                    viewport={{ once: true, amount: 0.2 }}
                    variants={fadeUp}
                >
                    <h2 className="about-section-title">
                        <Activity size={22} className="about-section-icon" />
                        Three-Tier Measurement Framework
                    </h2>
                    <p className="about-section-desc">
                        The system integrates a three-tier measurement and observation framework:
                    </p>

                    <div className="tier-grid">
                        {/* Tier 1 */}
                        <motion.div className="tier-card tier-1" custom={0} variants={fadeUp}>
                            <div className="tier-badge">Tier 1</div>
                            <h3 className="tier-title">
                                <Anchor size={20} />
                                High-Resolution River Morphology & Bathymetry
                            </h3>
                            <ul className="tier-list">
                                <li>
                                    <Radar size={16} />
                                    Detailed bathymetric mapping using underwater Remotely Operated Vehicles (ROVs)
                                </li>
                                <li>
                                    <Mountain size={16} />
                                    River cross-section and bedform mapping in inaccessible and hazardous regions
                                </li>
                            </ul>
                        </motion.div>

                        {/* Tier 2 */}
                        <motion.div className="tier-card tier-2" custom={1} variants={fadeUp}>
                            <div className="tier-badge">Tier 2</div>
                            <h3 className="tier-title">
                                <Waves size={20} />
                                Rapid Longitudinal River Survey
                            </h3>
                            <ul className="tier-list">
                                <li>
                                    <Satellite size={16} />
                                    Floating ROV-based surveys for capturing longitudinal profiles
                                </li>
                                <li>
                                    <Wind size={16} />
                                    Measurement of flow velocity, water surface slope, and debris transport dynamics
                                </li>
                            </ul>
                        </motion.div>

                        {/* Tier 3 */}
                        <motion.div className="tier-card tier-3" custom={2} variants={fadeUp}>
                            <div className="tier-badge">Tier 3</div>
                            <h3 className="tier-title">
                                <Gauge size={20} />
                                Real-Time Hydrological & Environmental Monitoring
                            </h3>
                            <p className="tier-subtitle">Continuous measurement of:</p>
                            <ul className="tier-list compact">
                                <li><Droplets size={16} /> Water level</li>
                                <li><Wind size={16} /> Flow velocity</li>
                                <li><Activity size={16} /> Sediment transport indicators</li>
                                <li><Waves size={16} /> Floating debris characteristics</li>
                                <li><Thermometer size={16} /> Water quality parameters (temperature, turbidity, conductivity, etc.)</li>
                            </ul>
                        </motion.div>
                    </div>

                    <motion.p
                        className="about-highlight-text"
                        custom={3}
                        variants={fadeUp}
                    >
                        This integrated system provides high-resolution, real-time data from otherwise inaccessible Himalayan terrain.
                    </motion.p>
                </motion.section>

                {/* AI & Forecasting */}
                <motion.section
                    className="about-section"
                    initial="hidden"
                    whileInView="visible"
                    viewport={{ once: true, amount: 0.2 }}
                    variants={fadeUp}
                >
                    <h2 className="about-section-title">
                        <BrainCircuit size={22} className="about-section-icon" />
                        Physics-Based AI Forecasting
                    </h2>
                    <p className="about-section-desc">
                        The collected data are assimilated into physics-based artificial intelligence models combining hydrodynamic equations and machine learning algorithms to provide:
                    </p>

                    <div className="ai-grid">
                        <div className="ai-card">
                            <Waves size={28} className="ai-icon" />
                            <h4>Real-Time Flood Forecasting</h4>
                        </div>
                        <div className="ai-card">
                            <AlertTriangle size={28} className="ai-icon" />
                            <h4>Flash Flood Early Warning</h4>
                        </div>
                        <div className="ai-card">
                            <ShieldCheck size={28} className="ai-icon" />
                            <h4>Disaster Risk Assessment</h4>
                        </div>
                        <div className="ai-card">
                            <Mountain size={28} className="ai-icon" />
                            <h4>Infrastructure Vulnerability Analysis</h4>
                        </div>
                    </div>
                </motion.section>

                {/* Scalability & Closing */}
                <motion.section
                    className="about-glass-card about-closing"
                    initial="hidden"
                    whileInView="visible"
                    viewport={{ once: true, amount: 0.3 }}
                    variants={fadeUp}
                >
                    <p>
                        The system is highly scalable and can be deployed across the <strong>Eastern Himalayas</strong> and other flood-prone mountainous regions with moderate budget requirements.
                    </p>
                    <p className="about-closing-statement">
                        This technology represents a major step toward developing a resilient, indigenous, and technologically advanced flood monitoring and disaster management framework for Himalayan river systems.
                    </p>
                </motion.section>
            </div>

            {/* Footer CTA */}
            <div className="about-footer-cta">
                <Link to="/" className="btn-primary about-cta-btn">
                    <ArrowLeft size={18} />
                    Return to Live Dashboard
                </Link>
            </div>

            {/* Footer */}
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
        </div>
    );
};

export default AboutHimdhara;
