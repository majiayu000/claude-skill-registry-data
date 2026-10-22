---
name: tddp-control-plane-audit
description: Analyze embedded UDP/TCP control planes such as TDDP by reconstructing framing, crypto, integrity, dispatch, authorization, and dangerous sink reachability with safe evidence-first methods.
---

# TDDP/control-plane audit

Use this skill for proprietary embedded control or debug protocols. Keep the work vendor-neutral and separate protocol acceptance from authentication.

## Workflow

1. Preserve hashes, extraction provenance, firmware identity, and captures. Work on derived copies; never execute firmware binaries.
2. Locate service initialization, socket bind, receive loop, interface scope, feature gates, and event registration. Confirm runtime exposure separately from static binding.
3. Recover framing from parser code and captures: version, type, lengths, sequence, command/category, integrity fields, encryption boundaries, padding, and bounds checks. State offsets and endianness explicitly.
4. Reconstruct decode/integrity data flow. Identify algorithm, key origin, IV/nonce, covered bytes, and whether the check is keyed. Label obfuscation, integrity, and authentication separately.
5. Recover command tables, indirect calls, registration conditions, and handler arguments. Classify commands as read-only, disruptive, persistent-write, or unknown.
6. Trace every state-changing handler to sinks (erase, reset, reboot, config, credential, upgrade) and identify the first proven authorization gate. Treat source-IP locks and shared keys as non-authentication unless private proof is demonstrated.
7. If runtime validation is necessary, choose one benign read-only command, one datagram, no retries, and capture exact bytes/timing. Never construct a destructive packet merely to prove reachability.

## Reporting

Produce service/packet/table/call-graph inventories, a symbolic acceptance rule, a sink authorization table, and confidence labels: `PROVEN FROM CODE`, `VERIFIED IN FIRMWARE`, `OBSERVED ON DEVICE`, `HIGH-CONFIDENCE INFERRED`, and `UNKNOWN`. Do not publish ready-to-run destructive transmitters in the analysis report.
