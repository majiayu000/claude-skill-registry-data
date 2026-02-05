---
name: telemetry-contracts
description: Enforce telemetry contract stability (event naming, JSONL envelopes, /api/health + /api/status shape). Use when investigating telemetry drift, adding new telemetry fields, or updating z-server ingestion/UI.
---

# Telemetry Contracts

## Scope

This Skill helps keep telemetry reliable over time by:

- identifying the contract surfaces (events + endpoints)
- updating code + tests together
- validating that drift risks are addressed

Out of scope:

- designing brand-new telemetry systems (that’s a separate design task)

## Inputs

- Which server/module emits telemetry (file path(s) if known)
- What changed (new fields, renamed events, endpoint shape change)
- Which consumer(s) are impacted (e.g. z-server, UI dashboards, tests)

## Procedure

1. Locate current contract docs + recent telemetry work.
   - Start from the most recent telemetry session docs under `docs/sessions/`.
2. Identify the contract surfaces that must remain stable:
   - telemetry JSONL envelope shape
   - event names + required fields
   - `/api/health` and `/api/status` payload shape
3. Update emitter and consumer in lockstep.
4. Add/adjust the smallest test(s) that enforce the contract.
5. Record the rationale (why the shape changed, migration plan if needed).

## Validation

- Run the most targeted test suite(s) that cover telemetry shape.
- If the change affects diagrams/docs, update the relevant session diagrams.

## Escalation / Research request

Ask for dedicated research if:

- a contract change affects multiple servers and you need a migration strategy
- you need a formal schema/versioning plan

## References

- Telemetry explainer session: `docs/sessions/2025-12-13-telemetry-setup-explainer/`
- AGI workflows: `docs/agi/WORKFLOWS.md`
