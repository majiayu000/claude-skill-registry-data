---
name: ble-gatt-integration
description: Use when integrating, designing, or debugging BLE GATT services, characteristics, descriptors, MTU, notifications, indications, pairing, connection parameters, or throughput
---

# BLE GATT Integration

## Overview

Use this skill to debug BLE GATT by separating advertising, connection,
discovery, attributes, permissions, MTU, security, and data flow. GATT failures
are often permission or state-machine mismatches, not radio failures.

## When To Use

Use this skill when:

- The user is creating or debugging BLE services, characteristics, descriptors,
  notifications, indications, reads, writes, or subscriptions.
- The issue involves missing services, write failures, CCCD problems, MTU, data
  truncation, pairing, bonding, connection parameters, or low throughput.
- The stack is Zephyr, ESP-IDF, nRF Connect SDK, NimBLE, BlueZ, Android, iOS, or
  a vendor BLE SDK.

Do not use this skill when the device cannot advertise or connect at all. Start
with platform-specific radio and controller bring-up first.

## First Questions

Ask for:

- BLE stack, device role, central/client app, peripheral firmware, and logs.
- Advertising data, connection status, service UUIDs, characteristic UUIDs, and
  properties.
- Attribute permissions, security level, pairing/bonding state, and CCCD state.
- MTU, connection interval, PHY, data length extension, and payload size.
- Sniffer trace or client error if available.

## Debug Workflow

1. Prove discovery.
   Confirm advertising, connection, primary service discovery, and attribute
   handles using a known BLE client.

1. Check attribute contract.
   Verify UUIDs, properties, permissions, descriptors, lengths, and endian/unit
   conventions.

1. Separate reads, writes, and subscriptions.
   Test read, write-with-response, write-without-response, notify, and indicate
   one at a time.

1. Validate security.
   Match permissions to pairing, bonding, encryption, MITM, and key storage.

1. Tune transport parameters.
   For throughput, check MTU, connection interval, PHY, data length, buffering,
   and application pacing.

1. Test client diversity.
   Compare behavior on at least one generic tool and the real Android/iOS/client
   app.

## Common Failures

- Characteristic lacks the property needed by the client operation.
- CCCD is not enabled before notifications are sent.
- Attribute requires encryption but the client is not paired or bonded.
- Payload exceeds negotiated MTU minus ATT overhead.
- Indications are sent before the previous confirmation arrives.
- Android/iOS cached an old GATT table after firmware changed.

## Verification

Before claiming BLE GATT works:

- State stack, role, service/characteristic UUIDs, permissions, and MTU.
- Confirm discovery and each required operation with logs or a client trace.
- Confirm security and bonding behavior if protected attributes are used.
- Confirm throughput parameters if performance is part of the requirement.

## Example

User:

```text
BLE notify 开了但手机收不到数据。
```

Agent:

1. Checks characteristic properties, CCCD subscription, and connection state.
1. Verifies MTU and payload length.
1. Uses a generic BLE client before debugging the mobile app.
