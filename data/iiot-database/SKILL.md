---
name: iiot-database
description: IIoT Database interaction patterns. TimescaleDB + Apache AGE queries, helper functions, mock data generation.
triggers:
  - "IIoT database"
  - "iiot-db"
  - "sensor readings"
  - "alarm graph"
  - "equipment hierarchy"
  - "cypher query"
  - "timescaledb query"
  - "iiot mock data"
---

# IIoT Database Skill

## Overview

This skill covers interaction with the unified IIoT database combining:
- **TimescaleDB** - Time-series sensor data (hypertables, continuous aggregates)
- **Apache AGE** - Graph relationships (asset hierarchy, event causality)
- **PostgreSQL** - Relational foundation with PostGIS

## Quick Start

### Connection

```bash
# Local Docker connection
docker exec -it tmnl_iiot_db psql -U iiot -d iiot_mock

# Or via psql (note: port 5433 to avoid conflict with main postgres)
psql postgresql://iiot:iiot_dev@localhost:5433/iiot_mock
```

### Start the Database

```bash
# From packages/tmnl/docker directory
cd docker
docker compose -f docker-compose.iiot.yml up -d

# View logs
docker compose -f docker-compose.iiot.yml logs -f

# Stop
docker compose -f docker-compose.iiot.yml down
```

---

## Schema Overview

### Equipment Hierarchy (Graph - Apache AGE)

```
plant → line → machine ← sensor
                  ↑
                alarm (via trigger)
```

### Time-Series Data (TimescaleDB)

```
sensor_readings (hypertable)
├── time        TIMESTAMPTZ
├── device_id   TEXT
├── value       DOUBLE PRECISION
└── quality     INTEGER

readings_1min (continuous aggregate)
├── bucket      TIMESTAMPTZ
├── device_id   TEXT
├── avg_value, min_value, max_value
└── sample_count
```

---

## Helper Functions

### `get_sensor_hierarchy(device_id)`

Returns the full hierarchy path for a sensor.

```sql
SELECT * FROM iiot.get_sensor_hierarchy('TMP-001');
```

**Output:**
| device_id | machine_name | line_name | plant_name |
|-----------|--------------|-----------|------------|
| TMP-001 | Welding Robot | Body Assembly | Chicago Assembly |

### `get_machine_sensors(machine_id)`

Returns all sensors monitoring a machine with their latest readings.

```sql
SELECT * FROM iiot.get_machine_sensors('MCH-001');
```

**Output:**
| device_id | sensor_type | unit | latest_value | latest_time | avg_1h | min_1h | max_1h |
|-----------|-------------|------|--------------|-------------|--------|--------|--------|
| TMP-001 | temperature | celsius | 25.3 | 2026-01-24 10:30:00 | 24.8 | 22.1 | 27.5 |
| VIB-001 | vibration | mm/s | 2.1 | 2026-01-24 10:30:00 | 1.9 | 0.5 | 3.2 |

### `alarm_graph_trigger()`

Automatically creates graph nodes for new alarms.

```sql
-- Insert alarm (trigger fires automatically)
INSERT INTO iiot.alarms (device_id, alarm_type, severity, message)
VALUES ('TMP-001', 'HIGH_TEMP', 3, 'Temperature exceeded threshold');

-- Verify in graph
SELECT * FROM cypher('iiot_graph', $$
    MATCH (a:alarm)-[:triggered_by]->(s:sensor)
    RETURN a.id, a.alarm_type, s.device_id
$$) AS (alarm_id agtype, alarm_type agtype, sensor_id agtype);
```

---

## Cypher Queries (Apache AGE)

### Basic Graph Queries

```sql
-- All sensors on a machine
SELECT * FROM cypher('iiot_graph', $$
    MATCH (m:machine {id: 'MCH-001'})<-[:monitors]-(s:sensor)
    RETURN s.device_id, s.type, s.unit
$$) AS (device_id agtype, type agtype, unit agtype);

-- Full path from sensor to plant
SELECT * FROM cypher('iiot_graph', $$
    MATCH (s:sensor {device_id: 'TMP-001'})-[:monitors]->(m:machine)
          <-[:contains]-(l:line)<-[:contains]-(p:plant)
    RETURN s.device_id, m.name, l.name, p.name
$$) AS (sensor agtype, machine agtype, line agtype, plant agtype);

-- All equipment in plant
SELECT * FROM cypher('iiot_graph', $$
    MATCH (p:plant {id: 'PLANT-A'})-[:contains*]->(n)
    RETURN labels(n)[0] AS type, n.id, n.name
$$) AS (type agtype, id agtype, name agtype);
```

### Alarm Analysis

```sql
-- Alarms with sensor context
SELECT * FROM cypher('iiot_graph', $$
    MATCH (a:alarm)-[:triggered_by]->(s:sensor)-[:monitors]->(m:machine)
    RETURN a.id, a.alarm_type, a.severity, s.device_id, m.name
    ORDER BY a.timestamp DESC
    LIMIT 10
$$) AS (alarm_id agtype, type agtype, severity agtype, sensor agtype, machine agtype);

-- Alarms by severity
SELECT * FROM cypher('iiot_graph', $$
    MATCH (a:alarm)
    RETURN a.severity, count(a) AS count
    ORDER BY a.severity DESC
$$) AS (severity agtype, count agtype);
```

---

## TimescaleDB Queries

### Recent Readings

```sql
-- Last hour of readings
SELECT time, device_id, value
FROM iiot.sensor_readings
WHERE device_id = 'TMP-001'
  AND time > NOW() - INTERVAL '1 hour'
ORDER BY time DESC;
```

### Aggregated Data

```sql
-- Hourly averages (uses continuous aggregate)
SELECT bucket, device_id, avg_value, min_value, max_value
FROM iiot.readings_1min
WHERE device_id = 'TMP-001'
  AND bucket > NOW() - INTERVAL '24 hours'
ORDER BY bucket;

-- Custom time bucket
SELECT
    time_bucket('15 minutes', time) AS bucket,
    device_id,
    AVG(value) AS avg_value,
    COUNT(*) AS samples
FROM iiot.sensor_readings
WHERE time > NOW() - INTERVAL '6 hours'
GROUP BY bucket, device_id
ORDER BY bucket;
```

### Anomaly Detection

```sql
-- Values outside 2 standard deviations
WITH stats AS (
    SELECT
        device_id,
        AVG(value) AS mean,
        STDDEV(value) AS stddev
    FROM iiot.sensor_readings
    WHERE time > NOW() - INTERVAL '7 days'
    GROUP BY device_id
)
SELECT r.time, r.device_id, r.value, s.mean, s.stddev
FROM iiot.sensor_readings r
JOIN stats s ON r.device_id = s.device_id
WHERE r.time > NOW() - INTERVAL '1 day'
  AND ABS(r.value - s.mean) > 2 * s.stddev
ORDER BY r.time DESC;
```

---

## Hybrid Queries (Graph + Time-Series)

### Machine Sensors with Readings

```sql
-- Get sensors from graph, join with time-series
WITH machine_sensors AS (
    SELECT ms.device_id::text AS device_id
    FROM cypher('iiot_graph', $$
        MATCH (m:machine {id: 'MCH-001'})<-[:monitors]-(s:sensor)
        RETURN s.device_id AS device_id
    $$) AS ms(device_id agtype)
)
SELECT
    ms.device_id,
    sr.time,
    sr.value
FROM machine_sensors ms
JOIN iiot.sensor_readings sr ON sr.device_id = ms.device_id
WHERE sr.time > NOW() - INTERVAL '1 hour'
ORDER BY sr.time DESC;
```

### Alarm Root Cause Analysis

```sql
-- Find readings around alarm time
WITH alarm_info AS (
    SELECT
        a.alarm_id::text AS alarm_id,
        a.sensor_id::text AS sensor_id,
        a.alarm_time::timestamptz AS alarm_time
    FROM cypher('iiot_graph', $$
        MATCH (a:alarm)-[:triggered_by]->(s:sensor)
        WHERE a.severity >= 3
        RETURN a.id AS alarm_id, s.device_id AS sensor_id, a.timestamp AS alarm_time
        LIMIT 1
    $$) AS a(alarm_id agtype, sensor_id agtype, alarm_time agtype)
)
SELECT
    ai.alarm_id,
    sr.time,
    sr.value,
    sr.time - ai.alarm_time AS offset_from_alarm
FROM alarm_info ai
JOIN iiot.sensor_readings sr ON sr.device_id = ai.sensor_id
WHERE sr.time BETWEEN ai.alarm_time - INTERVAL '5 minutes'
                  AND ai.alarm_time + INTERVAL '5 minutes'
ORDER BY sr.time;
```

---

## Mock Data Generation

### Generate Sensor Readings

```sql
-- Generate 10,000 temperature readings over 30 days
INSERT INTO iiot.sensor_readings (time, device_id, value, quality)
SELECT
    NOW() - (random() * INTERVAL '30 days'),
    'TMP-001',
    20 + (random() * 10),  -- 20-30°C
    CASE WHEN random() > 0.05 THEN 100 ELSE 50 END
FROM generate_series(1, 10000);

-- Generate vibration readings
INSERT INTO iiot.sensor_readings (time, device_id, value, quality)
SELECT
    NOW() - (random() * INTERVAL '30 days'),
    'VIB-001',
    random() * 5,  -- 0-5 mm/s
    CASE WHEN random() > 0.05 THEN 100 ELSE 50 END
FROM generate_series(1, 10000);
```

### Generate Alarms

```sql
-- Generate test alarms
INSERT INTO iiot.alarms (device_id, alarm_type, severity, message, triggered_at)
VALUES
    ('TMP-001', 'HIGH_TEMP', 3, 'Temperature exceeded 28°C', NOW() - INTERVAL '2 hours'),
    ('TMP-001', 'HIGH_TEMP', 2, 'Temperature approaching limit', NOW() - INTERVAL '1 hour'),
    ('VIB-001', 'HIGH_VIBRATION', 4, 'Excessive vibration detected', NOW() - INTERVAL '30 minutes');
```

### Refresh Continuous Aggregates

```sql
-- Force refresh after bulk insert
CALL refresh_continuous_aggregate('iiot.readings_1min', NULL, NULL);
```

---

## Maintenance Queries

### Check Hypertable Health

```sql
-- Chunk information
SELECT * FROM timescaledb_information.chunks
WHERE hypertable_name = 'sensor_readings';

-- Compression status
SELECT * FROM timescaledb_information.compression_settings
WHERE hypertable_name = 'sensor_readings';

-- Job status
SELECT * FROM timescaledb_information.jobs;
```

### Check Graph Status

```sql
-- Graph statistics
SELECT * FROM ag_catalog.ag_graph;

-- Label counts
SELECT * FROM cypher('iiot_graph', $$
    MATCH (n)
    RETURN labels(n)[0] AS label, count(n) AS count
$$) AS (label agtype, count agtype);

-- Edge counts
SELECT * FROM cypher('iiot_graph', $$
    MATCH ()-[r]->()
    RETURN type(r) AS type, count(r) AS count
$$) AS (type agtype, count agtype);
```

---

## Docker Commands

```bash
# Start database
docker compose -f docker/docker-compose.iiot.yml up -d

# View logs
docker logs tmnl_iiot_db -f

# Connect to psql
docker exec -it tmnl_iiot_db psql -U iiot -d iiot_mock

# Rebuild image (after init.sql changes)
docker compose -f docker/docker-compose.iiot.yml build --no-cache
docker compose -f docker/docker-compose.iiot.yml up -d

# Reset database (destroys data!)
docker compose -f docker/docker-compose.iiot.yml down -v
docker compose -f docker/docker-compose.iiot.yml up -d
```

---

## Troubleshooting

### "function cypher does not exist"

AGE extension not loaded. Check:
```sql
SHOW shared_preload_libraries;  -- Should include 'age'
SELECT * FROM pg_extension WHERE extname = 'age';
```

### "graph iiot_graph does not exist"

Graph wasn't created during init:
```sql
SELECT create_graph('iiot_graph');
```

### "operator does not exist: agtype @> agtype"

Missing search_path in function. Functions need:
```sql
SET LOCAL search_path = ag_catalog, iiot, public;
```

### Slow time-series queries

Check if indexes exist:
```sql
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'sensor_readings';
```

Add index if missing:
```sql
CREATE INDEX IF NOT EXISTS idx_readings_device_time
ON iiot.sensor_readings (device_id, time DESC);
```

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `iiot-isa95-hierarchy` | ISA-95 equipment hierarchy modeling |
| `iiot-unified-namespace` | UNS topic structure for NATS/MQTT |
| `nex-effect-services` | Building NEX services with Effect-TS |

---

## Canonical Files

| File | Purpose |
|------|---------|
| `docker/iiot-db/Dockerfile` | Custom PostgreSQL image build |
| `docker/iiot-db/init.sql` | Schema, functions, mock data |
| `docker/docker-compose.iiot.yml` | Database service definition |
