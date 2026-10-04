---
name: lorawan
description: "Long Range Wide Area Network: chirp spread spectrum (CSS), device classes A/B/C, link budget, ADR, gateways, and The Things Network"
category: iot
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/iot/lorawan/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# LoRa & LoRaWAN

## Scope
LoRa physical layer modulation and LoRaWAN MAC protocol for battery-operated wireless IoT devices requiring long transmission range ($>10\text{ km}$) and low data rates.

## Physics & Protocol Specification
- **LoRa Physical Layer (CSS)**: Chirp Spread Spectrum modulation defined by Spreading Factor ($SF7 - SF12$), Bandwidth ($BW = 125/250/500\text{ kHz}$), and Coding Rate ($CR = 4/5 - 4/8$). Link budget $>150\text{ dB}$.
- **Device Classes**:
  - Class A (All): Battery-powered; downlink permitted only in two short receive windows ($RX1, RX2$) following an uplink.
  - Class B (Beacon): Scheduled downlink receive slots synchronized by gateway periodic beacons.
  - Class C (Continuous): Continuously listening; mains-powered.
- **Adaptive Data Rate (ADR)**: Network server dynamically adjusts node spreading factor and transmit power to minimize energy consumption.

## Tools & Standards
- **Standards**: LoRaWAN 1.0.4 / 1.1 Specification (LoRa Alliance).
- **Network Servers**: ChirpStack, The Things Network (TTN), AWS IoT Core for LoRaWAN.
