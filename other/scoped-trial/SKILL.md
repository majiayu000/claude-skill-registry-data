---
name: scoped-trial
description: Maintain or extend the paper-only scoped scorer-confidence trial that applies the experiment only to explicit matching conditions such as strategy leader, regime, action, or signal structure. Use when working on scoped trial flags, scope matching, or baseline vs full vs scoped comparison reporting.
---

# Scoped Trial

## Binding sources

- **`docs/FINAL_SYSTEM_VISION.md`** — scoped experiments feed **continuous research** data for **L6** analysis; must stay **traceable** (baseline vs full vs scoped).
- **`AGENTS.md`** — default-off; paper-only; no collapsing modes into an ambiguous black box.

## Purpose

Use this skill to manage the narrow paper-only rollout candidate path for scorer-confidence experiments.

The scoped trial exists to test whether a concentrated benefit can be isolated without changing the baseline or globally enabling the experiment.

## Use When

Use this skill when:
- editing scoped trial config or scope parsing
- editing scope matching behavior
- comparing baseline vs full experiment vs scoped trial
- improving operator visibility around scoped trials

## Do Not Use When

Do not use this skill for:
- baseline scorer changes
- full experiment governance-only summaries
- generic strategy or risk changes unrelated to scoped trial behavior

## Safety Contract

- Scoped trial remains off by default.
- Baseline behavior remains untouched unless the scope explicitly matches and the trial is enabled.
- Scoped trial stays paper-only.
- Full experiment and scoped trial must not silently collapse into one ambiguous mode.
- No auto-enable, no auto-tuning, no default changes.

## Primary Workflow

1. Read `AGENTS.md`.
2. Inspect scope flags, matching logic, and current comparison outputs.
3. Preserve baseline and full-experiment paths first.
4. Keep scope syntax explicit and operator-readable.
5. Verify logs and summaries show whether the scope matched.

## Required Checks

- Scoped trial is clearly labeled in logs, journal, summaries, and panel views.
- Scope fields stay explicit, readable, and bounded.
- Baseline vs full vs scoped reporting stays comparable.
- Match and miss paths both remain explainable.

## Expected Output

- `Scoped Mode:` what the scope can match.
- `Comparison Layer:` how baseline, full, and scoped views differ.
- `Safety Check:` default-off and paper-only confirmation.
