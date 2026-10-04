---
name: zigbee
description: "IEEE 802.15.4 mesh networking: coordinator, router, end-device roles, Zigbee Cluster Library (ZCL), and network pairing"
category: iot
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/iot/zigbee/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Zigbee Mesh Networks

## Scope
Zigbee is a low-power, short-range, wireless mesh networking standard based on IEEE 802.15.4, widely deployed in smart homes, building automation, and industrial sensing.

## Architecture & Topology
- **Device Roles**:
  - Zigbee Coordinator (ZC): Exactly one per network; establishes network, manages security keys.
  - Zigbee Router (ZR): Mains-powered; passes routing packets, extends network range.
  - Zigbee End Device (ZED): Battery-operated; sleeps most of the time; talks only through parent router.
- **Zigbee Cluster Library (ZCL)**: Standardized attributes and commands for interoperable profiles (Lighting, HVAC, Occupancy).

## Tools & Standards
- **Standards**: Zigbee 3.0 Specification (Connectivity Standards Alliance - CSA).
- **Hardware/Software**: TI CC2652, Silicon Labs EFR32, Zigbee2MQTT, ZHA.
