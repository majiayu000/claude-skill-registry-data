---
name: matter
description: "Matter standard: IPv6-based smart home interoperability over Wi-Fi, Thread, and Ethernet, data model, security, and Commissioning"
category: iot
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/iot/matter/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Matter IoT Interoperability Standard

## Scope
Matter is an open-source, unified, application-layer connectivity standard running over IPv6 (Thread, Wi-Fi, Ethernet) to ensure seamless smart home interoperability.

## Matter Architecture & Security
- **Underlying Transports**: Thread (low-power mesh, IEEE 802.15.4), Wi-Fi (high bandwidth), Ethernet; BLE used exclusively for initial device commissioning.
- **Data Model**: Nodes $\to$ Endpoints $\to$ Clusters (Server/Client) $\to$ Attributes, Commands, and Events.
- **Security & Multi-Admin**: Certificate-Based Device Attestation (DAC); encrypted end-to-end sessions (PASE, CASE); Multi-Admin allows simultaneous control by Apple Home, Google Home, and Home Assistant.

## Tools & Standards
- **Standards**: Matter 1.3 Specification (Connectivity Standards Alliance - CSA).
- **Software**: Project CHIP / connectedhomeip open-source SDK, Matter Controller.
