import React, { useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import "./Map.css";
import PropTypes from "prop-types";
import L from "leaflet";

// Fix for default marker icon in React-Leaflet
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
});
L.Marker.prototype.options.icon = DefaultIcon;

// Component to handle map view updates when location changes
const ChangeView = ({ center }) => {
    const map = useMap();
    useEffect(() => {
        map.setView(center, 14);
    }, [center, map]);
    return null;
};

const Map = ({ location, sensorName }) => {
    return (
        <div className="map-wrapper">
            <MapContainer
                center={location}
                zoom={13}
                className="map-wrapper"
                scrollWheelZoom={false}
            >
                <ChangeView center={location} />
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                <Marker position={location}>
                    <Popup>
                        <div className="map-popup-title">{sensorName}</div>
                        <div className="map-popup-coord">
                            Lat: {location[0]}, Lng: {location[1]}
                        </div>
                    </Popup>
                </Marker>
            </MapContainer>
        </div>
    );
};

Map.propTypes = {
    location: PropTypes.arrayOf(PropTypes.number).isRequired,
    sensorName: PropTypes.string.isRequired,
};

export default Map;
