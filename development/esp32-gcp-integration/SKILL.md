---
name: ESP32 to GCP Integration Guide
description: |
  This skill provides ESP32 to Google Cloud integration patterns and troubleshooting. Use when working with ESP32 sensors connecting to Cloud Run, debugging WiFi or HTTPS issues, or implementing sensor firmware. Triggers when user mentions "ESP32 not connecting", "sensor to cloud", "ESP32 HTTPS", "WiFi issues", "firmware debugging", or needs help with ESP32-to-GCP communication.
version: 1.0.0
---

# ESP32 to GCP Integration Guide

## Architecture Overview

```
ESP32 Sensor ──WiFi──► Internet ──HTTPS──► Cloud Run API
     │                                          │
     └── Readings ──JSON POST──────────────────►│
     ◄── 200 OK ────────────────────────────────┘
```

## Complete ESP32 Sketch Template

```cpp
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// Configuration
const char* WIFI_SSID = "your-ssid";
const char* WIFI_PASS = "your-password";
const char* API_ENDPOINT = "https://your-service.run.app/api/telemetry";
const char* DEVICE_ID = "esp32-001";
const char* API_KEY = "your-api-key";

// Timing
const unsigned long SEND_INTERVAL = 30000;  // 30 seconds
unsigned long lastSend = 0;

WiFiClientSecure client;

void setup() {
  Serial.begin(115200);
  delay(1000);

  connectWiFi();

  // For testing only - use proper CA cert in production
  client.setInsecure();
}

void loop() {
  // Reconnect WiFi if needed
  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }

  // Send telemetry at interval
  if (millis() - lastSend >= SEND_INTERVAL) {
    sendTelemetry();
    lastSend = millis();
  }

  delay(100);
}

void connectWiFi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 30) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println(" Connected!");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println(" Failed!");
    delay(5000);
    ESP.restart();
  }
}

void sendTelemetry() {
  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;
  http.begin(client, API_ENDPOINT);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("X-API-Key", API_KEY);
  http.addHeader("X-Device-ID", DEVICE_ID);

  // Build JSON payload
  StaticJsonDocument<256> doc;
  doc["deviceId"] = DEVICE_ID;
  doc["timestamp"] = millis();

  JsonObject readings = doc.createNestedObject("readings");
  readings["temperature"] = readTemperature();
  readings["humidity"] = readHumidity();

  JsonObject meta = doc.createNestedObject("meta");
  meta["rssi"] = WiFi.RSSI();
  meta["uptime"] = millis();

  String payload;
  serializeJson(doc, payload);

  Serial.print("Sending: ");
  Serial.println(payload);

  int httpCode = http.POST(payload);

  if (httpCode > 0) {
    Serial.printf("Response: %d\n", httpCode);
    if (httpCode == 200) {
      Serial.println(http.getString());
    }
  } else {
    Serial.printf("Error: %s\n", http.errorToString(httpCode).c_str());
  }

  http.end();
}

float readTemperature() {
  // Replace with actual sensor reading
  return 25.0 + random(-50, 50) / 100.0;
}

float readHumidity() {
  // Replace with actual sensor reading
  return 60.0 + random(-100, 100) / 100.0;
}
```

## Common Issues & Solutions

### 1. WiFi Won't Connect

**Debug Code**:
```cpp
void debugWiFi() {
  Serial.printf("WiFi Status: %d\n", WiFi.status());
  // 0 = WL_IDLE_STATUS
  // 1 = WL_NO_SSID_AVAIL - SSID not found
  // 4 = WL_CONNECT_FAILED - Wrong password
  // 6 = WL_DISCONNECTED
  // 3 = WL_CONNECTED - Success

  if (WiFi.status() == WL_CONNECTED) {
    Serial.printf("IP: %s\n", WiFi.localIP().toString().c_str());
    Serial.printf("RSSI: %d dBm\n", WiFi.RSSI());
  }
}
```

**Fixes**:
- Verify SSID/password are correct
- ESP32 only supports 2.4GHz (not 5GHz)
- Check router isn't blocking by MAC address
- Try static IP if DHCP fails:
```cpp
IPAddress local_IP(192, 168, 1, 100);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);
WiFi.config(local_IP, gateway, subnet);
```

### 2. HTTPS Connection Fails

**Symptoms**: Connection refused, SSL errors

**With Root CA (Production)**:
```cpp
// Google Trust Services root CA for *.run.app
const char* rootCA = R"(
-----BEGIN CERTIFICATE-----
MIIFVzCCAz+gAwIBAgINAgPlk28xsBNJiGuiFzANBgkqhkiG9w0BAQwFADBHMQsw
CQYDVQQGEwJVUzEiMCAGA1UEChMZR29vZ2xlIFRydXN0IFNlcnZpY2VzIExMQzEU
MBIGA1UEAxMLR1RTIFJvb3QgUjEwHhcNMTYwNjIyMDAwMDAwWhcNMzYwNjIyMDAw
MDAwWjBHMQswCQYDVQQGEwJVUzEiMCAGA1UEChMZR29vZ2xlIFRydXN0IFNlcnZp
Y2VzIExMQzEUMBIGA1UEAxMLR1RTIFJvb3QgUjEwggIiMA0GCSqGSIb3DQEBAQUA
... (full cert) ...
-----END CERTIFICATE-----
)";

client.setCACert(rootCA);
```

**Testing Without Cert** (Development only):
```cpp
client.setInsecure();  // Skip certificate verification
```

### 3. HTTP Error Codes

```cpp
int httpCode = http.POST(payload);

switch(httpCode) {
  case 200: case 201:
    Serial.println("Success!");
    break;
  case 400:
    Serial.println("Bad Request - check JSON format");
    break;
  case 401:
    Serial.println("Unauthorized - check API key");
    break;
  case 403:
    Serial.println("Forbidden - check permissions");
    break;
  case 404:
    Serial.println("Not Found - check endpoint URL");
    break;
  case 500:
    Serial.println("Server Error - check Cloud Run logs");
    break;
  case -1:
    Serial.println("Connection failed");
    break;
  case -11:
    Serial.println("Connection timed out");
    break;
  default:
    Serial.printf("HTTP Error: %d\n", httpCode);
}
```

### 4. Memory Issues

**Debug Memory**:
```cpp
void checkMemory() {
  Serial.printf("Free heap: %d\n", ESP.getFreeHeap());
  Serial.printf("Min free heap: %d\n", ESP.getMinFreeHeap());
  Serial.printf("Max alloc: %d\n", ESP.getMaxAllocHeap());
}
```

**Prevent Memory Leaks**:
```cpp
// ALWAYS end HTTP connection
http.end();

// ALWAYS close client
client.stop();

// Use char arrays instead of String for less fragmentation
char buffer[256];
serializeJson(doc, buffer, sizeof(buffer));
```

### 5. DNS Resolution Fails

```cpp
IPAddress ip;
if (WiFi.hostByName("your-service.run.app", ip)) {
  Serial.print("Resolved: ");
  Serial.println(ip);
} else {
  Serial.println("DNS failed!");

  // Try custom DNS
  WiFi.disconnect();
  IPAddress dns1(8, 8, 8, 8);  // Google DNS
  IPAddress dns2(8, 8, 4, 4);
  WiFi.config(INADDR_NONE, INADDR_NONE, INADDR_NONE, dns1, dns2);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
}
```

## Reliability Patterns

### Watchdog Timer
```cpp
#include <esp_task_wdt.h>

void setup() {
  // 30 second watchdog
  esp_task_wdt_init(30, true);
  esp_task_wdt_add(NULL);
}

void loop() {
  esp_task_wdt_reset();  // Feed the watchdog
  // ... your code ...
}
```

### Exponential Backoff
```cpp
int retryDelay = 1000;  // Start at 1 second
const int maxDelay = 60000;  // Max 1 minute

void sendWithRetry() {
  int httpCode = http.POST(payload);

  if (httpCode == 200) {
    retryDelay = 1000;  // Reset on success
  } else {
    Serial.printf("Failed, retrying in %dms\n", retryDelay);
    delay(retryDelay);
    retryDelay = min(retryDelay * 2, maxDelay);  // Double delay
    sendWithRetry();  // Retry
  }
}
```

### Deep Sleep for Battery
```cpp
const int SLEEP_SECONDS = 300;  // 5 minutes

void loop() {
  sendTelemetry();

  Serial.println("Going to sleep...");
  esp_deep_sleep(SLEEP_SECONDS * 1000000ULL);
  // Never reaches here - wakes up in setup()
}
```

## Telemetry Payload Schema

### Minimal Payload
```json
{
  "deviceId": "esp32-001",
  "temperature": 25.5
}
```

### Full Payload
```json
{
  "deviceId": "esp32-001",
  "timestamp": 1705337600000,
  "type": "telemetry",
  "readings": {
    "temperature": 25.5,
    "humidity": 60.2,
    "pressure": 1013.25,
    "light": 450
  },
  "meta": {
    "firmware": "1.2.0",
    "rssi": -65,
    "battery": 85,
    "uptime": 3600000,
    "heap": 180000
  }
}
```

## Cloud Run Backend Handler

```javascript
const express = require('express');
const app = express();
app.use(express.json());

// Validate device
const validateDevice = (req, res, next) => {
  const apiKey = req.headers['x-api-key'];
  const deviceId = req.headers['x-device-id'];

  if (!apiKey || !deviceId) {
    return res.status(401).json({ error: 'Missing credentials' });
  }

  // Validate against your device registry
  // ...

  req.deviceId = deviceId;
  next();
};

app.post('/api/telemetry', validateDevice, async (req, res) => {
  const telemetry = {
    ...req.body,
    deviceId: req.deviceId,
    receivedAt: Date.now()
  };

  console.log('Telemetry received:', telemetry);

  // Publish to Pub/Sub
  await pubsub.topic('telemetry').publish(
    Buffer.from(JSON.stringify(telemetry))
  );

  res.status(200).json({
    status: 'received',
    messageId: '...'
  });
});

app.get('/health', (req, res) => {
  res.status(200).json({ status: 'healthy' });
});

const PORT = process.env.PORT || 8080;
app.listen(PORT);
```

## Diagnostic Sketch

```cpp
void runDiagnostic() {
  Serial.println("=== ESP32 Diagnostic ===\n");

  // Chip info
  Serial.printf("Chip: %s Rev %d\n", ESP.getChipModel(), ESP.getChipRevision());
  Serial.printf("Cores: %d\n", ESP.getChipCores());
  Serial.printf("Flash: %d MB\n", ESP.getFlashChipSize() / 1024 / 1024);

  // Memory
  Serial.printf("Free Heap: %d bytes\n", ESP.getFreeHeap());

  // WiFi
  Serial.printf("WiFi: %s\n", WiFi.status() == WL_CONNECTED ? "Connected" : "Disconnected");
  if (WiFi.status() == WL_CONNECTED) {
    Serial.printf("  SSID: %s\n", WiFi.SSID().c_str());
    Serial.printf("  IP: %s\n", WiFi.localIP().toString().c_str());
    Serial.printf("  RSSI: %d dBm\n", WiFi.RSSI());
  }

  // DNS
  IPAddress ip;
  Serial.printf("DNS: %s\n",
    WiFi.hostByName("google.com", ip) ? "OK" : "FAILED");

  // HTTPS
  Serial.print("HTTPS: ");
  WiFiClientSecure testClient;
  testClient.setInsecure();
  if (testClient.connect("www.google.com", 443)) {
    Serial.println("OK");
    testClient.stop();
  } else {
    Serial.println("FAILED");
  }

  Serial.println("\n=== End Diagnostic ===");
}
```
