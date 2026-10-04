---
name: harness-ratchet
description: >
  Turn a repeated agent or prod failure into a permanent harness improvement
  (test/hook/script + optional AGENTS line + RULE-PROVENANCE). Use when user
  says harness-ratchet, ratchet this failure, never again, or after a live-fix
  that should become structural.
---

# Harness ratchet

## When

A bug or agent mistake is **repeatable** and should never land silently again.

## Protocol

1. Capture the failure in 3 bullets (symptom, root cause class, blast radius).  
2. Prefer **sensor** over prose:
   - unit/api test, fitness rule, golden case, hook deny, pre-release step  
3. If prose needed: ≤2 lines in `AGENTS.md` + row in `docs/team/harness/RULE-PROVENANCE.md`.  
4. Update `docs/team/harness/HARNESS-MAP.md` if a new guide/sensor appears.  
5. Run `npm run harness:score:report` and note delta.  
6. Append example line to `docs/team/harness/RATCHET-EXAMPLE.md` or BITACORA.

## Anti-patterns

- Adding AGENTS rules without a sensor  
- Disabling human gates “to unblock”  
- Ratcheting one-off non-repeatable noise  

## Done

Sensor fails on the old bug; score does not drop; provenance updated.
