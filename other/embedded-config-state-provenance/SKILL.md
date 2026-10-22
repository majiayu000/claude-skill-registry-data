---
name: embedded-config-state-provenance
description: Trace embedded firmware configuration and credential provenance across factory defaults, running state, NVRAM/flash, reset, migration, reboot, and persistence boundaries.
---

# Configuration/state provenance

Use this skill to determine which configuration representation is authoritative and how it changes. Do not expose unrelated secrets.

## Workflow

1. Inventory default resources, schemas, block IDs, partitions, NVRAM/UCI-like stores, serializers, checksums, compression, and version markers. Preserve originals and hashes.
2. Trace readers and writers for each target field from parser/dispatcher through validation, in-memory structures, commit/flush, and reboot reload. Record addresses, offsets, widths, and evidence.
3. Separate factory/default, persistent user, running/in-memory, backup/restore, and recovery representations. Do not identify a credential field from a name alone; require a code/data-flow link.
4. Model reset and initialization paths: event source, default loader, erase operation, field/block replacement, commit, reboot scheduling, and post-reset state. Compare web, button, RPC, and internal callers without invoking destructive operations.
5. For credentials, distinguish plaintext, transformed value, hash/verifier, encrypted value, token, and session material. Trace where information is lost and whether equivalent inputs persist identically.

## Evidence discipline

Use exact source paths, function addresses, block identifiers, and byte comparisons. Redact unrelated Wi-Fi/admin secrets. Mark claims `PROVEN FROM CODE`, `VERIFIED FROM CONFIG DATA`, `OBSERVED ON DEVICE`, `DERIVED`, or `UNKNOWN`; distinguish inferred copy relationships from confirmed writes. Prepare pre/post snapshots and a minimal approved experiment only when static evidence cannot resolve persistence.
