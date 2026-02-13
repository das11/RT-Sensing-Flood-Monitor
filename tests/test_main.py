
import unittest
import sys
import os
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from main import clean_sensor_data

class TestSensorData(unittest.TestCase):
    def test_clean_sensor_data_valid(self):
        key = "/floodmonitor1/-Oa3TR"
        data = {
            "dist_cm": "R0845",
            "bat_volt": 12.5,
            "solar_volt": 14.2,
            "timestamp": 1700000000
        }
        point = clean_sensor_data(key, data)
        self.assertIsNotNone(point)
        # Check conversion of R0845 -> 845
        # InfluxDB Point objects store fields in a private dict usually, 
        # but we can't easily access them without the client serialization.
        # We can check the line protocol string or internal attributes if available.
        # For now, let's trust the function didn't crash and returned a Point.
        # To strictly verify, we might need to inspect the object.
        print(f"Point: {point.to_line_protocol()}")
        self.assertIn("sensor_id=floodmonitor1", point.to_line_protocol())
        self.assertIn("dist_cm=845i", point.to_line_protocol()) # i for integer

    def test_clean_sensor_data_integer_dist(self):
        key = "/floodmonitor2/123"
        data = {"dist_cm": 500, "bat_volt": 0}
        point = clean_sensor_data(key, data)
        self.assertIn("dist_cm=500i", point.to_line_protocol())

    def test_clean_sensor_data_invalid_dist(self):
        key = "/floodmonitor1/123"
        data = {"dist_cm": "Error"}
        point = clean_sensor_data(key, data)
        # Should default to 0
        self.assertIn("dist_cm=0i", point.to_line_protocol())

    def test_timestamp_parsing(self):
        key = "/s1/1"
        data = {"dist_cm": 100, "timestamp": "1700000000"}
        point = clean_sensor_data(key, data)
        # Check if timestamp is correct in line protocol
        # 1700000000 seconds = 1700000000000000000 nanoseconds
        self.assertIn("1700000000000000000", point.to_line_protocol())

if __name__ == '__main__':
    unittest.main()
