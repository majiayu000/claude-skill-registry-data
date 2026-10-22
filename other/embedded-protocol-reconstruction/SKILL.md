---
name: embedded-protocol-reconstruction
description: Recover embedded binary packet formats, protocol crypto, integrity checks, dispatch tables, and source-to-sink behavior from firmware and captures. Use for UDP/TCP/IPC management protocols.
---

# Embedded Protocol Reconstruction

Use this skill when a native service must be reconstructed from parsers,
crypto primitives, tables, strings, disassembly, and packet captures.

## Workflow

1. Identify service initialization, socket creation, bind/interface policy, receive loop, and callback registration.
2. Recover header offsets, widths, endianness, lengths, sequence fields, command/category fields, checksums, and payload boundaries.
3. Trace validation in order: framing, bounds, source state, decode, integrity, authentication, category selection, command lookup, handler.
4. Decode command tables and classify each handler read-only, configuration-changing, reboot/reset, or unknown. Resolve metadata through field consumers rather than names.
5. Identify crypto algorithms from operations/constants and trace every key to provenance: packet, fixed firmware, configuration, hardware, or runtime state.
6. Build an offline parser/builder and deterministic self-tests before any live traffic.
7. Perform at most one narrowly scoped read-only validation request; never fuzz or transmit a state-changing command without explicit authorization.

## Authentication distinction

Protocol version checks, encoding/obfuscation, checksums, unkeyed hashes,
and source-IP locks are not authentication unless a private secret is
required and verified. Document this distinction at each gate.

## Reporting

Provide a receive-to-sink call graph, packet schema, command inventory,
key-material provenance, authorization gates, runtime limitations, and
evidence links. Label findings `PROVEN FROM CODE`, `VERIFIED BY PCAP`,
`VERIFIED ON DEVICE`, `HIGH-CONFIDENCE INFERRED`, or `UNKNOWN`.
