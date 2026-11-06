---
name: playbook-validate
description: >-
  User-invoked as /playbook-validate <path>. Validates an Aegis remediation
  playbook (YAML/JSON) for step ordering, required fields, idempotency, and
  rollback coverage. Use before a playbook is trusted to run automated
  remediation.
allowed-tools: Read, Grep, Glob, Bash
invocation: /playbook-validate <path>
---

# Playbook Validate

Validate the playbook file at the path the user supplied (`$ARGUMENTS`). A
playbook drives automated or semi-automated remediation during an incident, so
a malformed one is a safety hazard.

## Checks

1. **Required fields** - each playbook has: `id`, `name`, `trigger`
   (fault class / `IncidentMode` / signal), `steps`, `owner`, `severity`.
   Each step has: `id`, `description`, `action`, `idempotent` (bool),
   `rollback`, `requires_authorisation` (bool), `timeout`.
2. **Step ordering** - steps form a sane sequence: detect/confirm → contain →
   remediate → verify. No remediation step runs before the triggering condition
   is confirmed.
3. **Idempotency** - every step declares `idempotent`; any non-idempotent step
   documents why re-running is unsafe and how it is guarded.
4. **Rollback** - every state-changing step has a `rollback` (or an explicit,
   justified `rollback: none` for read-only steps).
5. **Authorisation** - any production-affecting step sets
   `requires_authorisation: true`; cross-check against the `AEGIS_PROD_CONFIRMED`
   guard convention.
6. **Consensus weights** - consensus weight is a `default_weight` `ClassVar` on
   each agent class (`src/aegis_swr/agents/`), not a file: check every registered
   agent declares a numeric weight and the built-in roster sums to ~1.0 (±0.01).

## Output

```
## Playbook Validation - <file>
**Verdict: VALID | INVALID**
### Errors (blocking)
- <field/step> - <problem>
### Warnings
- <improvement>
### Coverage
- steps: N | with rollback: N | idempotent: N | needs-auth: N
```
Default to INVALID if any required field is missing or any state-changing step
lacks a rollback.
