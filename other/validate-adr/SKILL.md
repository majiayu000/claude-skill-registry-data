---
name: validate-adr
description: Validate Architecture Decision Records against 11 enterprise rules before marking as Accepted
version: 2.0.0
tags: [validation, adr, architecture, phase-5]
trigger_keywords: [validate, adr, architecture decision]
requires_approval: false
estimated_duration: 5-10 seconds
---

# Skill: Validate ADR

## Purpose

Run the enterprise ADR Validator against one or more ADR files to check compliance with 11 validation rules.

## When to use

- After generating any ADR in Phase 5
- Before marking an ADR as **Accepted**
- When the user explicitly requests ADR validation
- As part of the Phase 5 gate check

## How to run

```bash
# Single ADR
node packs/enterprise-architecture-pack/validators/adr-validator/src/index.ts \
  --format=console docs/adr/ADR-001-isolation.md

# All ADRs in directory
node packs/enterprise-architecture-pack/validators/adr-validator/src/index.ts \
  --strict docs/adr/
```

## Rules checked

| Rule ID | Severity | Check |
|---|---|---|
| ADR-STR-001 | error | Required sections (Context, Decision) present |
| ADR-STR-002 | error | ADR has a title |
| ADR-STR-003 | warning | Context section is not empty (≥50 chars) |
| ADR-ENT-001 | error | ≥2 alternatives documented |
| ADR-ENT-002 | error | Alternatives include rejection reasons |
| ADR-ENT-003 | error | Compliance Impact section present |
| ADR-ENT-004 | error | Valid status (Proposed/Accepted/Deprecated/Superseded) |
| ADR-ENT-005 | error | ISO 8601 date format (YYYY-MM-DD) |
| ADR-COMP-001 | warning | Security ADRs reference a compliance standard |
| ADR-COMP-002 | warning | Consequences section present |
| ADR-COMP-003 | warning | Regulated ADRs name their deciders |

## Output interpretation

**Console format:**
```
✓ docs/adr/ADR-001-isolation.md — PASS
✗ docs/adr/ADR-002-saga.md — FAIL
  ✗ [ADR-ENT-001] Enterprise ADRs must document at least 2 alternatives.
     → Add a table with at least 2 alternative approaches...
```

**Gate rule:** An ADR with any `error`-severity violation cannot be marked as Accepted.
Fix all errors, re-run the validator, confirm ALL PASSED, then mark the ADR as Accepted.

## Integration with Phase 5

After generating an ADR:
1. Save the file: `docs/adr/ADR-NNN-title.md`
2. Load `@skill validate-adr`
3. Run the validator (terminal command or code execution)
4. If FAIL: fix violations, re-run validator
5. If PASS: mark ADR as Accepted, proceed to next decision
