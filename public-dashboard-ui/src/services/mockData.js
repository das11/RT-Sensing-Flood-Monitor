export const SENSORS = [
    {
        id: "sensor-1",
        name: "River Bridge North",
        description: "Main sensor monitoring the northern bridge support.",
        position: [26.1445, 91.7362], // Guwahati, Assam (approx)
        level: 350, // cm
        thresholds: {
            low: 200,
            medium: 400,
            high: 600,
        },
        lastUpdated: "2 mins ago",
    },
    {
        id: "sensor-2",
        name: "Urban Drain South",
        description: "Monitoring water levels in the southern drainage system.",
        position: [26.1158, 91.7086],
        level: 520, // cm - High
        thresholds: {
            low: 150,
            medium: 300,
            high: 500,
        },
        lastUpdated: "5 mins ago",
    },
    {
        id: "sensor-3",
        name: "Market Area Flood Gauge",
        description: "Located in the central market for early flood warning.",
        position: [26.1832, 91.7505],
        level: 120, // cm - Low
        thresholds: {
            low: 100,
            medium: 250,
            high: 400,
        },
        lastUpdated: "Just now",
    },
];

export const getSensor = (id) => SENSORS.find((s) => s.id === id);
