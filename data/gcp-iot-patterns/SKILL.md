---
name: GCP IoT Architecture Patterns
description: |
  This skill provides guidance on GCP IoT architecture patterns and best practices. Use this skill when working with ESP32 sensors, Cloud Run backends, Pub/Sub messaging, or Firebase frontends. Triggers when user asks about "IoT architecture", "GCP best practices", "sensor to cloud", "telemetry patterns", "realtime IoT", or needs guidance on designing IoT systems on Google Cloud.
version: 1.0.0
---

# GCP IoT Architecture Patterns

## Reference Architecture

### Standard IoT Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Google Cloud Platform                          │
│                                                                           │
│   ┌─────────┐      ┌─────────────┐      ┌─────────────┐                │
│   │ ESP32   │ ───► │ Cloud Run   │ ───► │  Pub/Sub    │                │
│   │ Sensors │ HTTPS│ API Gateway │      │  Topic      │                │
│   └─────────┘      └─────────────┘      └──────┬──────┘                │
│                                                 │                        │
│                    ┌────────────────────────────┼────────────────┐      │
│                    │                            │                │      │
│                    ▼                            ▼                ▼      │
│            ┌─────────────┐             ┌─────────────┐   ┌───────────┐ │
│            │  Firestore  │             │   Push to   │   │  BigQuery │ │
│            │  Database   │             │  WebSocket  │   │ Analytics │ │
│            └─────────────┘             └──────┬──────┘   └───────────┘ │
│                    │                          │                        │
│                    └──────────────────────────┼────────────────────────┤
│                                               │                        │
└───────────────────────────────────────────────┼────────────────────────┘
                                                │
                                                ▼
                                        ┌─────────────┐
                                        │   React     │
                                        │  Frontend   │
                                        │ (Firebase)  │
                                        └─────────────┘
```

## Pattern 1: Direct Push (Recommended for < 1000 devices)

**Flow**: ESP32 → Cloud Run → Pub/Sub (Push) → WebSocket Service → Frontend

**Pros**:
- Low latency (< 500ms end-to-end)
- Simple architecture
- Cost-effective for small deployments

**Cons**:
- Limited buffering
- Single region

**Implementation**:
```javascript
// Cloud Run: Receive telemetry and publish
app.post('/api/telemetry', async (req, res) => {
  const { deviceId, readings } = req.body;

  await pubsub.topic('telemetry').publish(
    Buffer.from(JSON.stringify({ deviceId, readings, timestamp: Date.now() }))
  );

  res.status(200).json({ status: 'received' });
});
```

## Pattern 2: Fan-Out with Processing

**Flow**: ESP32 → Cloud Run → Pub/Sub → Cloud Functions → Multiple Destinations

**Use When**:
- Need to store in database AND send to frontend
- Processing/transformation required
- Multiple subscribers need the data

```javascript
// Cloud Function: Process and fan-out
exports.processTelemetry = async (message) => {
  const data = JSON.parse(Buffer.from(message.data, 'base64'));

  // Store in Firestore
  await db.collection('telemetry').add(data);

  // Update device status
  await db.collection('devices').doc(data.deviceId).set({
    lastSeen: FieldValue.serverTimestamp(),
    status: 'online'
  }, { merge: true });

  // Publish to frontend topic
  await pubsub.topic('frontend-updates').publish(
    Buffer.from(JSON.stringify(data))
  );
};
```

## Pattern 3: Batch Processing (High Volume)

**Flow**: ESP32 → Cloud Run → Pub/Sub → Dataflow → BigQuery + Firestore

**Use When**:
- 1000+ devices
- Need analytics/historical data
- High message volume (> 10 msg/sec)

## Device Status Patterns

### Heartbeat Pattern

```cpp
// ESP32: Send heartbeat every 30 seconds
void loop() {
  if (millis() - lastHeartbeat > 30000) {
    sendHeartbeat();
    lastHeartbeat = millis();
  }
}
```

```javascript
// Cloud Function: Mark offline if no heartbeat
exports.checkDeviceStatus = functions.pubsub
  .schedule('every 1 minutes')
  .onRun(async () => {
    const cutoff = Date.now() - 60000; // 1 minute
    const devices = await db.collection('devices')
      .where('lastSeen', '<', new Date(cutoff))
      .where('status', '==', 'online')
      .get();

    const batch = db.batch();
    devices.forEach(doc => {
      batch.update(doc.ref, { status: 'offline' });
    });
    await batch.commit();
  });
```

### Last Will Pattern (MQTT-style)

Store expected disconnect behavior:
```javascript
// On device connect
await db.collection('devices').doc(deviceId).set({
  status: 'online',
  lastWill: 'offline'
}, { merge: true });
```

## Pub/Sub Configuration

### Topic Setup
```bash
# Create telemetry topic
gcloud pubsub topics create telemetry --project=$PROJECT_ID

# Create push subscription for websocket
gcloud pubsub subscriptions create telemetry-ws-push \
  --topic=telemetry \
  --push-endpoint=https://ws-service.run.app/pubsub \
  --push-auth-service-account=push-invoker@$PROJECT_ID.iam.gserviceaccount.com \
  --ack-deadline=10 \
  --project=$PROJECT_ID

# Create pull subscription for processing
gcloud pubsub subscriptions create telemetry-process \
  --topic=telemetry \
  --ack-deadline=60 \
  --project=$PROJECT_ID
```

### Dead Letter Queue
```bash
# Create dead letter topic
gcloud pubsub topics create telemetry-dead-letter

# Update subscription with dead letter
gcloud pubsub subscriptions update telemetry-ws-push \
  --dead-letter-topic=telemetry-dead-letter \
  --max-delivery-attempts=5
```

## Cloud Run Configuration

### Recommended Settings for IoT API

```yaml
# service.yaml
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "1"  # Avoid cold starts
        autoscaling.knative.dev/maxScale: "10"
    spec:
      containerConcurrency: 80
      timeoutSeconds: 60
      containers:
        - resources:
            limits:
              memory: 512Mi
              cpu: "1"
```

### WebSocket Service Config

```bash
# Enable session affinity for socket.io
gcloud run services update ws-service \
  --session-affinity \
  --min-instances=1
```

## Security Best Practices

### Device Authentication

```cpp
// ESP32: Include API key in header
http.addHeader("X-API-Key", API_KEY);
http.addHeader("X-Device-ID", DEVICE_ID);
```

```javascript
// Cloud Run: Validate device
app.use('/api/telemetry', (req, res, next) => {
  const apiKey = req.headers['x-api-key'];
  const deviceId = req.headers['x-device-id'];

  if (!validateDevice(apiKey, deviceId)) {
    return res.status(401).json({ error: 'Unauthorized device' });
  }
  next();
});
```

### Use Secret Manager

```bash
# Store secrets
echo -n "my-api-key" | gcloud secrets create api-key --data-file=-

# Access in Cloud Run
gcloud run services update my-service \
  --set-secrets=API_KEY=api-key:latest
```

## Cost Optimization

| Component | Free Tier | Optimization |
|-----------|-----------|--------------|
| Cloud Run | 2M requests/mo | Batch telemetry, use min-instances=0 for dev |
| Pub/Sub | 10GB/mo | Compress messages, batch publishes |
| Firestore | 50K reads/day | Cache reads, batch writes |
| Functions | 2M invocations/mo | Use Cloud Run for high-volume |

## Monitoring Setup

```bash
# Create uptime check
gcloud monitoring uptime-check-configs create api-health \
  --display-name="IoT API Health" \
  --http-check=request-method=GET,path=/health,use-ssl=true \
  --monitored-resource=gce_instance

# Create alert for errors
gcloud alpha monitoring policies create \
  --notification-channels=[CHANNEL] \
  --condition-display-name="High Error Rate" \
  --condition-filter='resource.type="cloud_run_revision" AND metric.type="run.googleapis.com/request_count" AND metric.labels.response_code_class="5xx"'
```

## Telemetry Schema

### Recommended JSON Structure

```json
{
  "deviceId": "esp32-001",
  "timestamp": 1705337600000,
  "type": "telemetry",
  "readings": {
    "temperature": 25.5,
    "humidity": 60.2,
    "pressure": 1013.25
  },
  "meta": {
    "firmware": "1.2.0",
    "rssi": -65,
    "battery": 85,
    "uptime": 3600000
  }
}
```

### Firestore Document Structure

```
/devices/{deviceId}
  - status: "online" | "offline"
  - lastSeen: Timestamp
  - firmware: "1.2.0"
  - config: { ... }

/devices/{deviceId}/telemetry/{timestamp}
  - readings: { temperature, humidity, ... }
  - meta: { rssi, battery, ... }
```

## Common Anti-Patterns

❌ **Don't**: Poll from frontend every second
✅ **Do**: Use realtime listeners (Firestore onSnapshot, WebSocket)

❌ **Don't**: Store every reading in Firestore
✅ **Do**: Aggregate/downsample for long-term storage

❌ **Don't**: Use single Cloud Run instance for everything
✅ **Do**: Separate API gateway from WebSocket service

❌ **Don't**: Hardcode credentials in ESP32
✅ **Do**: Use secure provisioning and API keys
