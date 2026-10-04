---
name: live-validation
description: Use when building or changing anything in Athena that calls an external API (Anthropic, Voyage, EDGAR), when swapping a mock for a live client, when tuning retrieval knobs or constants, or before claiming behavioral work is validated.
---

# Live Validation Discipline

## Overview

Two house rules govern all behavioral and external-API work:

1. **Mocked-build-then-review-then-apply.** External API calls are mocked in
   the initial build; the build is reviewed before any live spend.
2. **Live-validate-twice.** Behavioral work is validated against the real
   corpus, and any behavioral fix is re-validated twice: confirm the defect
   cleared AND that the adjacent legitimate behavior still emits.

## Mocked build → review → live swap

- Ship the initial build with a deterministic fake (precedent: COMPARE
  shipped `MockColumnAnswerer`; FIND's contract is zero model calls forever).
- Design ONE named live-swap point so going live is a single reviewed change
  (COMPARE's is `get_column_answerer()` in router.py). Nothing else changes
  for the live build.
- No live tokens are spent until the mocked build has had its review pass.

## Live-validate-twice (precedent: commit 7973c0a, ADR-0012 validation)

- Run the behavior against the real corpus, not fixtures.
- After any behavioral fix, re-run twice; both passes must show the defect
  cleared AND the neighboring legitimate outcome still emitting (e.g. the
  false no-change cleared while the legitimate no-change case still fired).
- Hunt the defect that *looks like success*: under-reporting. A starved but
  fluent, fully-cited answer passes casual review — diff it against a wider
  retrieval (ADR-0012 mandates k=6–8 vs the 2-passage column) and include a
  specimen with known-rich disclosure (GOOG on AI risk is the named one).

## Tuning retrieval knobs (precedent: commit 3687d8d)

- Knobs are min()-clamped constants; tune by editing the constant on
  purpose, never via a runtime argument drifting upward.
- Record **before/after evidence**: rerun the same queries at old and new
  values and confirm the named misses now surface (HD on tariffs, GOOG on
  AI risk) — and write the measured numbers into the code comment or commit
  message so the next tuner inherits the evidence.
- Raising recall raises cost with it; say what the change costs.

## Red flags

- A live API key touched before the mocked build was reviewed.
- "Validated" claimed from one lucky run, or from fixtures only.
- A knob widened without a before/after rerun of the known specimens.
- A fix validated only for the defect, not for the legitimate neighbor
  outcome it might have suppressed.
