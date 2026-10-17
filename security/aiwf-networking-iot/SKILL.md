---
name: aiwf-networking-iot
description: Use for LAN, Wi-Fi, device networking, IoT telemetry, HTTP, MQTT, WebSockets, RTSP, robotics networking, secure binding, reliability, and field connectivity.
---

# AIWF Networking IoT

## Core Rule

Map the network before changing code. Identify devices, addresses, transport, protocol, auth, ports, firewall/NAT/VPN boundaries, retry behavior, offline behavior, telemetry, and operator-visible failure states.

## Workflow

1. Classify the connection: local-only app, LAN device, robot telemetry, IoT broker, web API, camera stream, remote support path, or customer-site network.
2. Inventory endpoints: hostnames/IPs, ports, protocols, TLS, credentials, certificates, broker topics, route paths, and which side initiates the connection.
3. Define reliability behavior: timeout, retry/backoff, queueing, deduplication, reconnect, heartbeat, last-known-good state, and offline mode.
4. Check security boundaries with `aiwf-security-guardrails` when auth, tokens, public exposure, uploads, remote control, or customer data are involved.
5. Validate with local probes before public exposure.

## Guardrails

- Bind services to localhost by default. Do not expose public network services, open firewall rules, or publish credentials unless Shawn explicitly asks.
- Keep control commands and telemetry distinct. Remote control needs stronger auth, audit logging, and stop/rollback paths than read-only status.
- Treat MQTT topics, HTTP paths, WebSocket events, and RTSP stream URLs as contracts. Document payload shape, QoS/retention where relevant, and failure behavior.
- For robots and edge devices, assume intermittent connectivity unless the site proves otherwise.
- Avoid hard-coding IP addresses in reusable software; prefer config with safe defaults.
- Add `aiwf-field-pilot-readiness` for customer-site deployment, partner pilots, or field tests.

## Validation Defaults

Use the project's normal probes first. Useful checks:

```powershell
Test-NetConnection <host> -Port <port>
curl.exe -v http://127.0.0.1:<port>/health
python -m pytest <network-tests>
```

Do not run scans against third-party networks. Keep diagnostics to owned hosts, localhost, or user-approved devices.

## Primary Source Anchors

- Ai Embedded Systems services page: https://aiembeddedsystems.com/services/
- HTTP Semantics RFC 9110: https://www.rfc-editor.org/info/rfc9110/
- IETF HTTP specs: https://httpwg.org/specs/
- MQTT 5.0 OASIS Standard: https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html

Verify protocol versions and local implementation libraries before making version-specific claims.
