// from(bucket: "flood_monitoring")
//   |> range(start: 0)
//   |> filter(fn: (r) => r["_measurement"] == "sensor_reading")
//   |> filter(fn: (r) => r["_field"] == "dist_cm")
//   |> limit(n: 100) // First 100 records to avoid browser crash
//   |> yield(name: "raw_data")


// from(bucket: "flood_monitoring")
//   |> range(start: 1970-01-01T00:00:00Z, stop: 2200-01-01T00:00:00Z)
//   |> filter(fn: (r) => r["_measurement"] == "sensor_reading")
//   |> filter(fn: (r) => r["_field"] == "dist_cm")
//   |> group(columns: ["sensor_id"])
//   |> count()
//   |> yield(name: "counts")


// from(bucket: "flood_monitoring")
//   |> range(start: 1970-01-01T00:00:00Z, stop: 2200-01-01T00:00:00Z)
//   |> filter(fn: (r) => r["_measurement"] == "sensor_reading")
//   |> filter(fn: (r) => r["_field"] == "dist_cm")
//   |> group(columns: ["sensor_id"])
//   |> last()
//   |> yield(name: "latest_values")


from(bucket: "flood_monitoring")
  |> range(start: 0) // Covers all history
  |> filter(fn: (r) => r["_measurement"] == "sensor_reading")
  |> filter(fn: (r) => r["_field"] == "dist_cm")
  |> filter(fn: (r) => r["sensor_id"] == "floodmonitor1") // <--- Change to LoRaWAN or floodmonitor2
//   |> filter(fn: (r) => r["sensor_id"] == "LoRaWAN")
//   |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
  |> yield(name: "mean")



// data = from(bucket: "flood_monitoring") |> range(start: -1d)
// 
// // Tab 1: Raw Min
// data |> min() |> yield(name: "minimum_value")
// 
// // Tab 2: Raw Max
// data |> max() |> yield(name: "maximum_value")
