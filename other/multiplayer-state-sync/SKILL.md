---
name: multiplayer-state-sync
description: "Designs state synchronization and reconciliation for multiplayer games. Use when replicated entities, client prediction, interpolation, or bandwidth budgets cause divergence."
---

# Multiplayer State Sync

## Use when
Clients see different worlds because ownership, update frequency, correction rules, or authoritative state are unclear.

## Workflow
1. Label each state field as server-authoritative, owner-predicted, interpolated, or locally cosmetic.
2. Define snapshot cadence, interpolation buffers, reliable versus unreliable messages, and behavior for missing or out-of-order updates.
3. Set a bandwidth budget by entity type and use quantization or relevance filtering only with measured error bounds.
4. Simulate latency, jitter, packet loss, joins, disconnects, and authority transfer in a controlled network harness.

## Required output
A replication table, message contract, reconciliation policy, traffic budget, and network-condition test matrix.

## Validation
- Authority for every replicated field is unambiguous.
- Corrections do not duplicate irreversible events or violate ownership.
- Tests include adverse latency and reconnect/rejoin behavior.

## Guardrails
Do not trust client-reported inventory, economy, combat outcomes, or permissions without server validation.
