---
name: fof-preflight
description: Diff-aware guardrail checker for Fear-of-Falling (FOF) changes; fails closed on raw data edits, Kxx intro/req_cols mismatches, and output discipline risks.
metadata:
  short-description: Diff-aware FOF guardrail preflight (fail-closed).
---

## How to use
Run from the Fear-of-Falling subproject root or repo root.

Example:
```bash
python .codex/skills/fof-preflight/scripts/preflight.py
```

## Inputs
- Git working tree diff (`git diff --name-only --diff-filter=ACMRTUXB`).
- Kxx R scripts under `Fear-of-Falling/R-scripts/` (or `R-scripts/`).
- Policy sources: `Fear-of-Falling/CLAUDE.md`, `Fear-of-Falling/QC_CHECKLIST.md`.

## Outputs
- Console summary with PASS/WARN/FAIL.
- Exit code 0 only if no FAIL conditions are found.

## Failure modes
- Not a git repo or diff fails.
- Any change under `data/` or `data/external/`.
- Kxx `.R` scripts missing the standard intro/Required vars block.
- Required vars list cannot be parsed unambiguously.
- `req_cols <- c(...)` cannot be parsed or has multiple definitions.
- Required vars list does not match `req_cols` 1:1.
- Suspicious `outputs/` usage not under `R-scripts/<script>/outputs/`.

## Safety/guardrails
- FAIL CLOSED: if a rule cannot be verified, the script exits 1 with context.
- No external APIs or network calls.
- Does not modify data or outputs.
- If other raw-data root paths are discovered in docs/scripts, do not add them
  without explicit user confirmation (fail closed and request clarification).

Sources: `Fear-of-Falling/CLAUDE.md`, `Fear-of-Falling/QC_CHECKLIST.md`.
