import React from 'react';
import logo1 from '../assets/logos/spons_logo1.png';
import logo2 from '../assets/logos/spons_logo2.jpg';
import logo3 from '../assets/logos/spons_logo3.png';
import logo4 from '../assets/logos/spons_logo4.png';
import './SupportersSection.css';

const SupportersSection = () => {
  return (
    <section className="supporters-section">
      <div className="supporters-container">
        <h2 className="supporters-title">Supported By</h2>
        <p className="supporters-subtitle">Our partners in making this project possible.</p>
        <div className="supporters-logos">
          <img src={logo1} alt="Supporter 1" className="supporter-logo" />
          <img src={logo3} alt="Supporter 3" className="supporter-logo" />
          <img src={logo4} alt="Supporter 4" className="supporter-logo" />
        </div>
      </div>
    </section>
  );
};

export default SupportersSection;
