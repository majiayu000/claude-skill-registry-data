---
name: IoT
description: Assist with IoT device setup, protocols, security hardening, and home automation integration.
metadata: {"clawdbot":{"emoji":"📡","os":["linux","darwin","win32"]}}
---

## Protocol Selection
- MQTT for lightweight messaging — pub/sub, low bandwidth, ideal for sensors
- CoAP for constrained devices — UDP-based, REST-like, very low power
- HTTP/REST for capable devices — familiar but heavier, use when bandwidth allows
- WebSocket for real-time bidirectional — dashboards, live updates
- Zigbee/Z-Wave for mesh networks — no WiFi needed, battery-friendly

## MQTT Essentials
- Broker is the central hub — Mosquitto most common self-hosted
- Topics are hierarchical — home/livingroom/temperature
- QoS levels: 0 (fire-forget), 1 (at least once), 2 (exactly once)
- Retain flag keeps last message — new subscribers get current state
- Will message announces disconnection — device offline detection

## Security (Critical)
- Never expose MQTT broker to internet without auth — bots scan constantly
- TLS mandatory for any external access — encrypt all traffic
- Unique credentials per device — revoke one without affecting others
- Firmware updates must be signed — prevent malicious updates
- Segment IoT on separate VLAN — isolate from main network

## Common Vulnerabilities
- Default credentials left unchanged — first thing attackers try
- Unencrypted protocols on network — credentials sniffable
- No firmware update mechanism — stuck with known vulnerabilities
- Cloud dependency without fallback — device useless when server down
- Debug ports left enabled — UART, JTAG exposed

## Home Assistant Integration
- MQTT discovery auto-configures devices — follow HA format
- ESPHome for custom ESP devices — YAML config, OTA updates
- Zigbee2MQTT bridges Zigbee to MQTT — hundreds of devices supported
- Tasmota for off-the-shelf flashing — many WiFi devices supported

## ESP32/ESP8266 Development
- Arduino framework most accessible — huge library ecosystem
- ESP-IDF for production — FreeRTOS, more control, steeper curve
- PlatformIO over Arduino IDE — better dependency management
- Deep sleep for battery life — microamps when sleeping
- OTA updates essential — don't require physical access

## Power Management
- Battery devices need deep sleep — wake on timer or interrupt
- Calculate power budget — mAh capacity vs average consumption
- Solar charging viable — small panel can sustain low-power sensors
- Supercapacitors for burst power — supplement weak batteries
- Monitor battery voltage — alert before device dies

## Connectivity Patterns
- WiFi: high bandwidth, high power — plugged devices
- Zigbee/Z-Wave: mesh, low power — battery sensors
- LoRa: long range, low bandwidth — outdoor, agricultural
- BLE: short range, low power — wearables, beacons
- Thread/Matter: new standard — Apple/Google/Amazon unified

## Reliability
- Watchdog timer prevents freezes — reset if loop stalls
- Persistent storage for state — survive power cycles
- Heartbeat/ping monitoring — detect silent failures
- Graceful degradation — work offline when cloud unavailable
- Redundant sensors for critical systems — don't trust single point

## Data Considerations
- Sample rate vs storage — don't over-collect
- Local processing when possible — reduce bandwidth, latency
- Time synchronization critical — NTP for timestamps
- Aggregate before sending — reduce message count
- Retain important data locally — survive connectivity loss

## Debugging
- Serial output for development — remove in production
- MQTT debug topics — publish diagnostics
- LED status indicators — quick visual feedback
- Remote logging carefully — don't flood network
- Simulate sensors for testing — don't wait for real conditions

## Vendor Lock-in
- Prefer local API devices — Tuya local, Shelly, Tasmota-compatible
- Cloud-only devices risky — company shutdowns brick devices
- Open protocols over proprietary — MQTT, Zigbee over custom
- Check if flashable — many devices accept custom firmware
- Matter promises interoperability — but still maturing
