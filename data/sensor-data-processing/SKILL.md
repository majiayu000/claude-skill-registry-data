---
name: Sensor Data Processing
description: Handling ingestion, storage, and analysis of time-series data from IoT devices using TimescaleDB, stream processing, aggregation, and anomaly detection for scalable IoT data pipelines.
---

# Sensor Data Processing

> **Current Level:** Advanced  
> **Domain:** IoT / Data Engineering

---

## Overview

Sensor data processing handles ingestion, storage, and analysis of time-series data from IoT devices. This guide covers TimescaleDB, stream processing, and anomaly detection for building efficient data pipelines that handle high-volume sensor data.

## Data Ingestion Patterns

```python
# mqtt_ingestion.py
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import psycopg2

class SensorDataIngestion:
    def __init__(self, broker_url, db_config):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        self.conn = psycopg2.connect(**db_config)
        self.cursor = self.conn.cursor()
        
        self.client.connect(broker_url, 1883, 60)
    
    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        client.subscribe("sensors/#")
    
    def on_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode())
            self.store_sensor_data(msg.topic, data)
        except Exception as e:
            print(f"Error processing message: {e}")
    
    def store_sensor_data(self, topic, data):
        query = """
            INSERT INTO sensor_data (device_id, sensor_type, value, unit, timestamp)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        self.cursor.execute(query, (
            data.get('device_id'),
            data.get('sensor_type'),
            data.get('value'),
            data.get('unit'),
            datetime.fromtimestamp(data.get('timestamp', datetime.now().timestamp()))
        ))
        
        self.conn.commit()
    
    def start(self):
        self.client.loop_forever()

# Usage
ingestion = SensorDataIngestion(
    broker_url='mqtt://broker.hivemq.com',
    db_config={
        'host': 'localhost',
        'database': 'iot_data',
        'user': 'postgres',
        'password': 'password'
    }
)
ingestion.start()
```

## Time-Series Data Storage

### TimescaleDB Schema

```sql
-- Create extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- sensor_data table
CREATE TABLE sensor_data (
  time TIMESTAMPTZ NOT NULL,
  device_id VARCHAR(255) NOT NULL,
  sensor_type VARCHAR(100) NOT NULL,
  value DOUBLE PRECISION NOT NULL,
  unit VARCHAR(50),
  metadata JSONB,
  
  PRIMARY KEY (time, device_id, sensor_type)
);

-- Convert to hypertable
SELECT create_hypertable('sensor_data', 'time');

-- Create indexes
CREATE INDEX idx_device_time ON sensor_data (device_id, time DESC);
CREATE INDEX idx_sensor_type ON sensor_data (sensor_type, time DESC);

-- Continuous aggregates
CREATE MATERIALIZED VIEW sensor_data_hourly
WITH (timescaledb.continuous) AS
SELECT 
  time_bucket('1 hour', time) AS hour,
  device_id,
  sensor_type,
  AVG(value) as avg_value,
  MIN(value) as min_value,
  MAX(value) as max_value,
  COUNT(*) as sample_count
FROM sensor_data
GROUP BY hour, device_id, sensor_type;

-- Retention policy
SELECT add_retention_policy('sensor_data', INTERVAL '90 days');

-- Compression policy
SELECT add_compression_policy('sensor_data', INTERVAL '7 days');
```

### Data Access Layer

```python
# timescale_repository.py
from datetime import datetime, timedelta
import psycopg2
from typing import List, Dict

class TimescaleRepository:
    def __init__(self, db_config):
        self.conn = psycopg2.connect(**db_config)
    
    def insert_sensor_data(self, device_id: str, sensor_type: str, 
                          value: float, unit: str, metadata: dict = None):
        query = """
            INSERT INTO sensor_data (time, device_id, sensor_type, value, unit, metadata)
            VALUES (NOW(), %s, %s, %s, %s, %s)
        """
        
        with self.conn.cursor() as cursor:
            cursor.execute(query, (device_id, sensor_type, value, unit, 
                                 json.dumps(metadata) if metadata else None))
            self.conn.commit()
    
    def get_latest_reading(self, device_id: str, sensor_type: str) -> Dict:
        query = """
            SELECT time, value, unit
            FROM sensor_data
            WHERE device_id = %s AND sensor_type = %s
            ORDER BY time DESC
            LIMIT 1
        """
        
        with self.conn.cursor() as cursor:
            cursor.execute(query, (device_id, sensor_type))
            row = cursor.fetchone()
            
            if row:
                return {
                    'time': row[0],
                    'value': row[1],
                    'unit': row[2]
                }
            return None
    
    def get_time_series(self, device_id: str, sensor_type: str, 
                       start_time: datetime, end_time: datetime) -> List[Dict]:
        query = """
            SELECT time, value, unit
            FROM sensor_data
            WHERE device_id = %s 
              AND sensor_type = %s
              AND time BETWEEN %s AND %s
            ORDER BY time ASC
        """
        
        with self.conn.cursor() as cursor:
            cursor.execute(query, (device_id, sensor_type, start_time, end_time))
            rows = cursor.fetchall()
            
            return [
                {'time': row[0], 'value': row[1], 'unit': row[2]}
                for row in rows
            ]
    
    def get_aggregated_data(self, device_id: str, sensor_type: str, 
                           interval: str, start_time: datetime, end_time: datetime):
        query = f"""
            SELECT 
                time_bucket('{interval}', time) AS bucket,
                AVG(value) as avg_value,
                MIN(value) as min_value,
                MAX(value) as max_value,
                COUNT(*) as count
            FROM sensor_data
            WHERE device_id = %s 
              AND sensor_type = %s
              AND time BETWEEN %s AND %s
            GROUP BY bucket
            ORDER BY bucket ASC
        """
        
        with self.conn.cursor() as cursor:
            cursor.execute(query, (device_id, sensor_type, start_time, end_time))
            rows = cursor.fetchall()
            
            return [
                {
                    'time': row[0],
                    'avg': row[1],
                    'min': row[2],
                    'max': row[3],
                    'count': row[4]
                }
                for row in rows
            ]
```

## Data Validation

```python
# data_validator.py
from typing import Dict, List
import numpy as np

class SensorDataValidator:
    def __init__(self):
        self.validation_rules = {
            'temperature': {'min': -50, 'max': 100, 'unit': 'celsius'},
            'humidity': {'min': 0, 'max': 100, 'unit': 'percent'},
            'pressure': {'min': 800, 'max': 1200, 'unit': 'hPa'}
        }
    
    def validate(self, sensor_type: str, value: float, unit: str) -> Dict:
        if sensor_type not in self.validation_rules:
            return {'valid': True, 'warnings': []}
        
        rules = self.validation_rules[sensor_type]
        warnings = []
        
        # Check range
        if value < rules['min'] or value > rules['max']:
            warnings.append(f"Value {value} outside valid range [{rules['min']}, {rules['max']}]")
        
        # Check unit
        if unit != rules['unit']:
            warnings.append(f"Unexpected unit '{unit}', expected '{rules['unit']}'")
        
        return {
            'valid': len(warnings) == 0,
            'warnings': warnings
        }
    
    def detect_outliers(self, values: List[float], threshold: float = 3.0) -> List[int]:
        """Detect outliers using z-score method"""
        if len(values) < 3:
            return []
        
        mean = np.mean(values)
        std = np.std(values)
        
        if std == 0:
            return []
        
        z_scores = [(x - mean) / std for x in values]
        outliers = [i for i, z in enumerate(z_scores) if abs(z) > threshold]
        
        return outliers
```

## Real-time Processing

```python
# stream_processor.py
from kafka import KafkaConsumer, KafkaProducer
import json

class StreamProcessor:
    def __init__(self, kafka_brokers):
        self.consumer = KafkaConsumer(
            'sensor-data',
            bootstrap_servers=kafka_brokers,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_brokers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    
    def process_stream(self):
        window = []
        window_size = 10
        
        for message in self.consumer:
            data = message.value
            
            # Add to window
            window.append(data['value'])
            if len(window) > window_size:
                window.pop(0)
            
            # Calculate moving average
            moving_avg = sum(window) / len(window)
            
            # Detect anomalies
            if abs(data['value'] - moving_avg) > 2 * np.std(window):
                self.producer.send('anomalies', {
                    'device_id': data['device_id'],
                    'sensor_type': data['sensor_type'],
                    'value': data['value'],
                    'expected': moving_avg,
                    'timestamp': data['timestamp']
                })
            
            # Send processed data
            self.producer.send('processed-data', {
                **data,
                'moving_avg': moving_avg
            })
```

## Anomaly Detection

```python
# anomaly_detector.py
import numpy as np
from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.is_trained = False
    
    def train(self, historical_data: List[float]):
        """Train on historical normal data"""
        X = np.array(historical_data).reshape(-1, 1)
        self.model.fit(X)
        self.is_trained = True
    
    def detect(self, value: float) -> bool:
        """Returns True if anomaly detected"""
        if not self.is_trained:
            return False
        
        prediction = self.model.predict([[value]])
        return prediction[0] == -1  # -1 indicates anomaly
    
    def detect_batch(self, values: List[float]) -> List[bool]:
        """Detect anomalies in batch"""
        if not self.is_trained:
            return [False] * len(values)
        
        X = np.array(values).reshape(-1, 1)
        predictions = self.model.predict(X)
        return [p == -1 for p in predictions]

# Statistical anomaly detection
class StatisticalAnomalyDetector:
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.history = []
    
    def add_value(self, value: float):
        self.history.append(value)
        if len(self.history) > self.window_size:
            self.history.pop(0)
    
    def is_anomaly(self, value: float, threshold: float = 3.0) -> bool:
        """Z-score based anomaly detection"""
        if len(self.history) < 10:
            return False
        
        mean = np.mean(self.history)
        std = np.std(self.history)
        
        if std == 0:
            return False
        
        z_score = abs((value - mean) / std)
        return z_score > threshold
```

## Data Compression

```python
# data_compression.py
class DataCompression:
    @staticmethod
    def delta_encoding(values: List[float]) -> List[float]:
        """Delta encoding for time-series compression"""
        if not values:
            return []
        
        compressed = [values[0]]
        for i in range(1, len(values)):
            compressed.append(values[i] - values[i-1])
        
        return compressed
    
    @staticmethod
    def delta_decoding(compressed: List[float]) -> List[float]:
        """Decode delta-encoded data"""
        if not compressed:
            return []
        
        values = [compressed[0]]
        for i in range(1, len(compressed)):
            values.append(values[-1] + compressed[i])
        
        return values
    
    @staticmethod
    def downsample(values: List[float], factor: int) -> List[float]:
        """Downsample by averaging"""
        downsampled = []
        for i in range(0, len(values), factor):
            chunk = values[i:i+factor]
            downsampled.append(sum(chunk) / len(chunk))
        
        return downsampled
```

## Best Practices

1. **Time-Series DB** - Use TimescaleDB or InfluxDB
2. **Compression** - Enable compression for old data
3. **Retention** - Set appropriate retention policies
4. **Aggregation** - Pre-aggregate data for performance
5. **Validation** - Validate all incoming data
6. **Anomaly Detection** - Implement real-time detection
7. **Batch Processing** - Use for historical analysis
8. **Indexing** - Index by device and time
9. **Partitioning** - Partition by time
10. **Monitoring** - Monitor ingestion rates

---

## Quick Start

### TimescaleDB Setup

```sql
-- Create hypertable
CREATE TABLE sensor_data (
  time TIMESTAMPTZ NOT NULL,
  device_id TEXT NOT NULL,
  sensor_type TEXT NOT NULL,
  value DOUBLE PRECISION,
  metadata JSONB
);

-- Convert to hypertable
SELECT create_hypertable('sensor_data', 'time');

-- Insert data
INSERT INTO sensor_data (time, device_id, sensor_type, value)
VALUES (NOW(), 'device-001', 'temperature', 25.5);
```

### Stream Processing

```python
import paho.mqtt.client as mqtt
from timescaledb import TimescaleDB

def on_message(client, userdata, message):
    data = json.loads(message.payload)
    
    # Process and store
    db.insert_sensor_data(
        device_id=data['device_id'],
        sensor_type=data['type'],
        value=data['value'],
        timestamp=datetime.utcnow()
    )
    
    # Detect anomalies
    if is_anomaly(data['value']):
        send_alert(data)
```

---

## Production Checklist

- [ ] **Time-Series DB**: TimescaleDB or similar
- [ ] **Data Ingestion**: Efficient data ingestion
- [ ] **Stream Processing**: Real-time stream processing
- [ ] **Aggregation**: Pre-aggregate data
- [ ] **Retention**: Set retention policies
- [ ] **Validation**: Validate incoming data
- [ ] **Anomaly Detection**: Real-time anomaly detection
- [ ] **Batch Processing**: Batch processing for analysis
- [ ] **Indexing**: Index by device and time
- [ ] **Partitioning**: Partition by time
- [ ] **Monitoring**: Monitor ingestion rates
- [ ] **Documentation**: Document data pipeline

---

## Anti-patterns

### ❌ Don't: Regular Database

```sql
-- ❌ Bad - Regular table
CREATE TABLE sensor_data (
  id SERIAL PRIMARY KEY,
  device_id TEXT,
  value DOUBLE PRECISION,
  timestamp TIMESTAMP
);
-- Not optimized for time-series!
```

```sql
-- ✅ Good - Hypertable
CREATE TABLE sensor_data (
  time TIMESTAMPTZ NOT NULL,
  device_id TEXT NOT NULL,
  value DOUBLE PRECISION
);
SELECT create_hypertable('sensor_data', 'time');
-- Optimized for time-series!
```

### ❌ Don't: No Retention

```sql
-- ❌ Bad - Keep all data forever
-- Storage grows indefinitely!
```

```sql
-- ✅ Good - Retention policy
SELECT add_retention_policy('sensor_data', INTERVAL '1 year');
-- Auto-delete old data
```

---

## Integration Points

- **Real-time Monitoring** (`36-iot-integration/real-time-monitoring/`) - Monitoring dashboards
- **Edge Computing** (`36-iot-integration/edge-computing/`) - Edge processing
- **Database Optimization** (`04-database/database-optimization/`) - Query optimization

---

## Further Reading

- [TimescaleDB](https://www.timescale.com/)
- [Time-Series Data Best Practices](https://www.timescale.com/learn/time-series-data)

## Resources
- [InfluxDB](https://www.influxdata.com/)
- [Apache Kafka](https://kafka.apache.org/)
- [Scikit-learn](https://scikit-learn.org/)
