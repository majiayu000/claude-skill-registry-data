---
name: risk-check
description: Verify that the trading-bot still enforces paper-only execution, hard risk gates, sizing limits, and exposure controls across runtime, experiments, operator panel actions, and startup flows. Use after touching config, risk, execution, main flow, panel actions, or experiment controls.
---

# Risk Check

## Binding sources

- **`docs/FINAL_SYSTEM_VISION.md`** — **Layer 7** hard gates; must never be bypassed by **L5** or **L6**.
- **`AGENTS.md`** — mandatory validation order; **live** not default.

## Purpose

Use this skill to confirm that safety still holds across the current system, not just inside `app/risk`.

In **`docs/FINAL_SYSTEM_VISION.md`**, hard gates map to **Layer 7**; this skill verifies they remain **non-bypassable** per **`AGENTS.md`**.

That includes:
- hard risk checks before position entry
- paper-only position lifecycle and portfolio exposure controls
- execution-quality gating
- AI and experiment isolation
- operator panel actions and startup flows

## Use When

Use this skill when changes touch:
- `app/risk`, `app/execution`, `app/config`, `app/main.py`
- `app/operator_panel.py` or any action that can trigger runs or resets
- experiment flags, scorer confidence modes, or scoped-trial handling
- startup, EXE, or autonomous research helpers

## Do Not Use When

Do not use this skill for:
- pure documentation changes
- isolated UI styling changes with no behavior or settings impact
- unrelated skill-documentation edits

## Required Checks

- Confirm `PAPER_TRADING=true` remains the repo default.
- Confirm no live order path was added or exposed.
- Confirm hard risk validation still cannot be bypassed by AI, experiments, panel actions, or startup flows.
- Confirm learning does not auto-apply or alter hard caps.
- Confirm position sizing respects max risk, max positions, and exposure caps.
- Confirm scoped trial and full experiment only affect their intended paper-only comparison paths.

## Expected Output

- `Default Mode:` pass/fail.
- `Hard Gates:` pass/fail with reasons.
- `Exposure Controls:` pass/fail with reasons.
- `Experiment Constraints:` pass/fail with reasons.
- `Risk Verdict:` safe / unsafe / needs follow-up.
