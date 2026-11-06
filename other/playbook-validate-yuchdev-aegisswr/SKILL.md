---
name: playbook-validate
description: User-invoked as /playbook-validate <path>. Validates an Aegis remediation playbook (YAML/JSON) for step ordering, required fields, idempotency, and rollback coverage. Use before a playbook is trusted to run automated remediation.
allowed-tools: Read, Grep, Glob, Bash
invocation: /playbook-validate <path>
---

# Playbook Validate

Validate the playbook file at the path the user supplied (`$ARGUMENTS`). A
playbook drives automated or semi-automated remediation during an incident, so
a malformed one is a safety hazard.

## Resources

- **[references/playbook-schema.md](references/playbook-schema.md)** — the full
  field vocabulary, the blocking-error vs warning rules, and the ordering
  heuristic. The `Checks` below are the summary; this is the authority.
- **[examples/valid-playbook.yaml](examples/valid-playbook.yaml)** — a playbook
  that passes every rule (expect **VALID**).
- **[examples/invalid-playbook.annotated.yaml](examples/invalid-playbook.annotated.yaml)**
  — parses as YAML but breaks four rules, each tagged inline (expect **INVALID**).
  Use these two as the reference shape when judging an unfamiliar file.

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
6. **Consensus weights** - consensus weight is a `default_weight` `ClassVar`
   on each agent class (`src/aegis_swr/agents/`), not a file. Check that every
   registered agent declares a numeric weight and that the built-in roster's
   weights sum to ~1.0 (±0.01), with no single agent above a sane ceiling.
   Example roster:
   ```text
   { "os_kernel": 0.35, "code_analyst": 0.35,
                     "log_historian": 0.20, "skeptic":  0.15 } }
   ```
   (sum = 1.00 ✓ | max single weight = 0.35 ✓)

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

## Completion checklist

- [ ] Every playbook-level required field checked: `id`, `name`, `trigger`, `steps`, `owner`, `severity`
- [ ] Every step checked for all 7 required fields (`id`, `description`, `action`, `idempotent`, `rollback`, `requires_authorisation`, `timeout`)
- [ ] Step ordering validated against `detect/confirm → contain → remediate → verify` - no remediation before the trigger is confirmed
- [ ] No state-changing step (`idempotent: false` or `requires_authorisation: true`) uses the `read-only: no state change` rollback sentinel
- [ ] Every step has a bounded `timeout`
- [ ] Consensus weights (`default_weight` ClassVars in `src/aegis_swr/agents/`): every registered agent declares a numeric weight and the built-in roster sums to `1.0 ± 0.01`
- [ ] Verdict defaults to INVALID on any missing required field or missing rollback; warnings listed separately and do not block
