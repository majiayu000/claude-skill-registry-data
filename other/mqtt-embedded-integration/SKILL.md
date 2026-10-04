---
name: mqtt-embedded-integration
description: Use when integrating, porting, configuring, or debugging embedded MQTT clients, brokers, keepalive, QoS, TLS transport, reconnects, or publish-subscribe issues
---

# MQTT Embedded Integration

## Overview

Use this skill for MCU MQTT clients by separating network link, TCP/TLS transport, MQTT session state, topic design, QoS, keepalive, and reconnect policy. MQTT success requires more than one successful publish.

## When To Use

Use this skill when:

- The user wants MQTT on an MCU or embedded device.
- The task involves MQTT connect, publish, subscribe, keepalive, QoS, Last Will, retained messages, broker auth, TLS, reconnect, or offline buffering.
- The issue is connection drops, no messages, duplicate messages, memory growth, TLS failure, or reconnect storms.

Do not use this skill when basic IP connectivity is not working. Use `lwip-integration` or platform network debugging first.

## First Questions

Ask for:

- MQTT library/client and version.
- Network stack, RTOS, transport, and whether TLS is used.
- Broker address, port, auth method, and certificate model without asking for secrets.
- Client ID, topics, QoS levels, keepalive, and reconnect policy.
- Current logs, broker logs, packet capture, or error codes.
- RAM budget and maximum payload size.

## Integration Checklist

1. Prove network first.
   Confirm DNS/IP, TCP connect, and broker reachability before MQTT debugging.

1. Configure identity.
   Client ID must be unique and stable enough for the product.

1. Bound payloads and buffers.
   Topic length, payload size, QoS queues, and offline buffers must fit RAM.

1. Set keepalive and reconnect policy.
   Avoid reconnect storms; use backoff and clear session behavior intentionally.

1. Add TLS deliberately.
   Validate time, CA storage, certificate chain, SNI, and heap usage.

1. Verify broker behavior.
   Test subscribe, publish, QoS behavior, retained messages, and Last Will if used.

## Common Failures

- Two devices use the same client ID and kick each other off.
- TLS fails because device time is invalid.
- Keepalive too short for poor networks.
- QoS 1 duplicates are not handled idempotently.
- Offline queue grows without bounds.
- Topic wildcards subscribe to too much traffic for MCU RAM.

## Verification

Before claiming MQTT works:

- State client library, broker transport, TLS/auth mode, client ID policy, and keepalive.
- Confirm connect, subscribe, publish, disconnect, and reconnect behavior.
- Confirm max payload and buffer limits.
- Confirm TLS certificate/time handling if TLS is used.
- Confirm secrets were not logged or stored in examples.

## Example

User:

```text
MCU MQTT 能连上但过一会儿就掉线。
```

Agent:

1. Asks for client library, keepalive, network stack, broker logs, TLS state, and reconnect policy.
1. Checks ping/keepalive and duplicate client ID before changing payload logic.
1. Verifies reconnect with backoff and subscription restoration.
