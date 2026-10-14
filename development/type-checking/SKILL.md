---
name: type-checking
description: "Type checking: strict TS + typed Python; runtime validation at I/O boundaries; verify with build."
---

# type-checking

Types are checked in CI, not in the author's head: strict configs, zero new violations, runtime parsing at boundaries.

## Activate when

- Configuring or interpreting mypy/pyright/tsc, or reviewing type-safety of a change.

## Do NOT activate for

- Runtime validation design (see backend/validation); lint style (see linting).

## Inspection

Read the type configs (strictness flags, ignores, per-file overrides) and the current violation baseline. Know what the checker actually proves here.

## Decision rules

- Strictest sustainable baseline; new code adds zero violations; `ignore`/`@ts-ignore`/`cast` needs a justification comment and narrowest scope.
- Types prove compile-time shape only — every external input still gets runtime parsing (see backend/validation).
- Fix the cause (better types, narrower unions), not the symptom (casts, ignores). Gradual-typing migrations track ignore-count down, never up.

## Procedure

1. Run the repo checker on the change; triage: real bug → fix types + code; false positive → narrowest justified suppression.
2. Remove one legacy suppression per touch where safe; keep the baseline ratcheting down.
3. Verify: checker green in CI, suppression count not increased, boundary parsing tests cover the changed I/O.

## Failure modes

- Casts laundering untrusted data; ignore-file growth; checker green locally but different version in CI; types trusted as runtime validation.

## Escalation

Language specifics → languages/typescript, languages/python; boundary design → backend/validation.

## References

- Related: `../../languages/typescript/`, `../../languages/python/`, `../../backend/validation/`.
