---
name: mqtt
description: "Message Queuing Telemetry Transport: broker architecture, topics, QoS levels 0/1/2, retain flags, Last Will and Testament (LWT), and MQTT-SN"
category: iot
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/iot/mqtt/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# MQTT Protocol & IoT Messaging

## Scope
MQTT is the dominant lightweight publish/subscribe network protocol designed for constrained devices and low-bandwidth, high-latency, or unreliable networks.

## Protocol Specification (MQTT 3.1.1 / 5.0)
- **Quality of Service (QoS)**:
  - QoS 0 (At most once): Fire and forget; no acknowledgment.
  - QoS 1 (At least once): Guaranteed delivery; acknowledged via `PUBACK`; duplicate delivery possible.
  - QoS 2 (Exactly once): Guaranteed delivery without duplicates; 4-way handshake (`PUBLISH` $\to$ `PUBREC` $\to$ `PUBREL` $\to$ `PUBCOMP`).
- **Core Features**:
  - Hierarchical Topics: `factory/line1/sensor/temperature` (wildcards `+` single-level, `#` multi-level).
  - Retain Flag: Broker stores latest message on topic for new subscribers.
  - Last Will and Testament (LWT): Broker publishes designated message if client disconnects ungracefully.
  - Keep-Alive & Ping: PINGREQ/PINGRESP packets detecting half-open TCP connections.

## Tools & Standards
- **Brokers**: EMQX, Eclipse Mosquitto, HiveMQ.
- **Standards**: OASIS MQTT Version 5.0 / 3.1.1.
