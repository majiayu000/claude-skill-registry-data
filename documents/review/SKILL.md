---
name: review
description: Review the trading-bot workspace for architecture, correctness, safety, maintainability, and next-step risk across the current paper-research stack. Use when changes touch execution, risk, operator panel, autonomous research, experiments, storage, or reporting and a structured findings-first review is needed.
---

# Review

## Binding sources

- **`docs/FINAL_SYSTEM_VISION.md`** — 10-layer vision (**L5** AI support; **L6** learning/optimization).
- **`AGENTS.md`** — enforceable boundaries; verify **bounded autonomy**, **no black-box** paths, **strategy quality** signals, **L7** ordering, paper/live defaults.

## Purpose

Use this skill to run a disciplined review of the current repository, not just a quick style pass.

The review should reflect the current architecture **and** stay aligned with **`docs/FINAL_SYSTEM_VISION.md`** (10-layer vision: notably **Layer 5** = AI support, **Layer 6** = learning/optimization) and enforceable rules in **`AGENTS.md`**:
- paper-only execution and position lifecycle
- hard risk gates and portfolio exposure controls
- experiment governance and scoped trials
- autonomous research loop, EXE startup path, and operator panel
- reporting, shadow analytics, and manual-review summaries
- operator observability, decision transparency, and research continuity as first-class goals

## Use When

Use this skill when:
- a change spans more than one subsystem
- execution, risk, storage, analytics, or reporting were touched
- operator panel or autonomous research workflows changed
- experiment behavior, governance, or scoped-trial logic changed
- you need a findings-first review before commit or handoff

## Do Not Use When

Do not use this skill for:
- trivial wording or formatting edits
- isolated markdown-only changes with no operational effect
- exploratory brainstorming before any implementation exists

## Primary Workflow

1. Read `AGENTS.md` and, for cross-cutting changes, skim `docs/FINAL_SYSTEM_VISION.md` for the layers involved.
2. Identify which architecture boundaries the change crosses.
3. Review the diff with findings first, ordered by severity.
4. Check whether paper-only safety, risk ordering, and experiment isolation still hold.
5. Check whether operator-facing reporting still matches actual behavior.
6. Call out the smallest high-value next step only after findings.

## Required Checks

- Confirm risk validation still sits before any new position open path.
- Confirm paper position lifecycle, sizing, and exposure reporting stay coherent.
- Confirm experiments remain opt-in and advisory where intended.
- Confirm operator panel summaries do not imply behavior the backend does not perform.
- Confirm docs, scripts, and panel actions still match the current workflow.
- Confirm no secrets, local state, or generated artifacts were accidentally pulled into tracked files.
- Confirm new autonomy or scheduling stays **bounded** (config/operator stops, documented limits).
- Confirm decision/score paths remain **traceable** (journal / `decision_support` / panel), not opaque.
- Confirm framing still matches the **10-layer vision**, not a narrow “dashboard-only” product.

## Expected Output

- `Findings:` prioritized issues with file references, or explicit no-findings.
- `Open Questions:` only unresolved assumptions that affect correctness or safety.
- `Residual Risk:` concise note on remaining testing or observability gaps.
- `Next Step:` 1 to 3 concrete follow-ups only if useful.
