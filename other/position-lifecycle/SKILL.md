---
name: position-lifecycle
description: Maintain or extend the paper-only position simulation, sizing, portfolio exposure tracking, and related reporting surfaces. Use when working on open-position state, trade lifecycle, portfolio metrics, or position visibility in reporting and the operator panel. Never use for live order enablement.
---

# Position Lifecycle

## Binding sources

- **`docs/FINAL_SYSTEM_VISION.md`** — execution and portfolio paths align with **L7–L8** in the full vision; this repo: **paper-first**, **L7** gates before open.
- **`AGENTS.md`** — no live enablement by default; lifecycle must stay **inspectable** in journals/reporting.

## Purpose

Use this skill to work on the current paper position stack:
- simulated entry and exit
- stop-loss and take-profit handling
- open-position state
- sizing and exposure tracking
- portfolio metrics and operator visibility

This skill is about realistic paper lifecycle behavior, not live execution.

## Use When

Use this skill when:
- editing `app/execution/trader.py`
- editing position models or persistence
- editing sizing or exposure reporting tied to open positions
- editing portfolio or recent-trade visibility in reporting or the operator panel

## Do Not Use When

Do not use this skill for:
- live exchange execution work
- raw strategy logic changes
- experiment governance-only work
- unrelated UI changes with no position or portfolio effect

## Safety Contract

- Keep the lifecycle fully paper-only.
- Open positions only after the existing signal, risk, and quality gates pass.
- Do not weaken hard risk, exposure limits, or concurrent-position limits.
- Keep realized and unrealized PnL reporting explainable and local.
- Never imply that paper fills are real exchange fills.

## Primary Workflow

1. Read `AGENTS.md`.
2. Inspect the touched lifecycle boundary: execution, storage, analytics, reporting, or panel visibility.
3. Preserve open-position update order before adding new metrics or summaries.
4. Keep state transitions explicit: open, update, close, reason.
5. Verify portfolio summaries still match stored position state.

## Required Checks

- Entry only happens after current hard gates and quality gate pass.
- Open-position counts, exposure, and capital usage remain internally consistent.
- Strategy and regime exposure reporting match the stored positions.
- Recent trades, portfolio summaries, and panel cards remain aligned.
- No live order path or secret handling was introduced.

## Expected Output

- `Lifecycle Scope:` what part of the paper position flow changed.
- `Portfolio Impact:` sizing, exposure, or metrics impact.
- `Safety Check:` paper-only and hard-risk confirmation.
