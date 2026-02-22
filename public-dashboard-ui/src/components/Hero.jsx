import React from "react";
import { Link } from "react-router-dom";
import { ArrowDown, Activity, ShieldCheck, Waves } from "lucide-react";
import mainLogo from "../assets/logos/Main Logo.png";
import "./Hero.css";

const Hero = ({ onCtaClick }) => {
    return (
        <section className="hero-section">
            {/* Background Animated Elements are now global in App.js */}

            <div className="hero-container">

                {/* Left: Text Content */}
                <div className="hero-text-content">
                    <img src={mainLogo} alt="Guwahati Flood Monitoring Network" className="hero-main-logo" />
                    <div className="hero-pill">
                        <span className="relative flex h-3 w-3">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                            <span className="relative inline-flex rounded-full h-3 w-3 bg-blue-500"></span>
                        </span>
                        Net-Zero Latency Monitoring
                    </div>

                    <h1 className="hero-title">
                        <span className="hero-title-highlight">Himधारा</span><br />
                        Intelligent Flood Monitoring
                    </h1>

                    <p className="hero-description">
                        Digital Flood Monitoring and Forecasting System for Himalayan Rivers.
                        Access accurate water-level insights instantly, ensuring safety for everyone.
                    </p>

                    <div className="hero-actions">
                        <button className="btn-primary" onClick={onCtaClick}>
                            View Live Dashboard
                            <ArrowDown size={18} />
                        </button>
                        <Link to="/about" className="btn-secondary">
                            Learn More
                        </Link>
                    </div>
                </div>

                {/* Right: Visuals */}
                <div className="hero-visuals">
                    <div className="glass-card">
                        {/* Visual Representation of Data */}
                        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem' }}>
                            <div style={{ width: '48px', height: '48px', background: '#ecfdf5', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                <Waves color="#10b981" size={24} />
                            </div>
                            <div>
                                <div style={{ fontSize: '0.875rem', color: '#64748b' }}>River Status</div>
                                <div style={{ fontSize: '1.125rem', fontWeight: '700', color: '#0f172a' }}>Normal Flow</div>
                            </div>
                        </div>

                        <div style={{ height: '8px', width: '100%', background: '#f1f5f9', borderRadius: '4px', overflow: 'hidden', marginBottom: '1.5rem' }}>
                            <div style={{ height: '100%', width: '45%', background: '#10b981' }}></div>
                        </div>

                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem' }}>
                            <span style={{ color: '#94a3b8' }}>Current Level</span>
                            <span style={{ fontWeight: '600', color: '#10b981' }}>3.2 Meters</span>
                        </div>
                    </div>

                    {/* Floating Elements */}
                    <div className="floating-badge badge-top-right">
                        <ShieldCheck size={20} color="#3b82f6" />
                        <span>99.9% Uptime</span>
                    </div>

                    <div className="floating-badge badge-bottom-left">
                        <Activity size={20} color="#f59e0b" />
                        <span>Live Data</span>
                    </div>
                </div>

            </div>

            <div className="scroll-indicator-wrapper" onClick={onCtaClick}>
                <span>Scroll to Explore</span>
                <ArrowDown size={20} className="animate-bounce" />
            </div>
        </section>
    );
};

export default Hero;
