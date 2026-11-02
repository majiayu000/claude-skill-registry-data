---
name: event-schema-evolution
description: Plan backward-compatible event schema changes for producers and consumers with versioning, replay, and unknown-field handling.
---

# Event Schema Evolution

## Goal

Let event-driven systems evolve without breaking delayed consumers, archived events, or rolling deployments.

## Inputs to inspect

Event envelopes and schemas, producer/consumer versions, queues/topics, retention window, and replay requirements.

## Workflow

1. Inventory event types and active consumers, including delayed jobs, analytics, dead-letter queues, archived payloads, and replay tools.
2. Classify the proposed change as additive, semantic, or breaking; inspect field optionality, enum expansion, units, and identifier meaning.
3. Define producer rollout and consumer compatibility order, including mixed-version windows and fallback behavior for older readers.
4. Create fixtures from prior event versions and test parsing, defaults, replay, unknown fields, and duplicate delivery.
5. Document deprecation windows and schema ownership; add compatibility checks to CI for the project's supported history window.

## Validation checklist

- [ ] Old stored events remain readable for the promised retention/replay horizon.
- [ ] Additive fields have safe defaults and do not change existing field meaning.
- [ ] Consumers define behavior for unknown enum values and missing optional fields.
- [ ] Producer and consumer deployment order is tested under mixed versions.
- [ ] Replay/idempotency semantics are preserved across schema migration.

## Required output

Produce a compatibility matrix, event schema diff, rollout sequence, historical fixtures, and deprecation policy.

## Boundaries and failure handling

Do not repurpose a field under the same schema version; do not assume a change is safe merely because the latest producer and consumer both work.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
