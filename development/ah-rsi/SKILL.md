---
name: ah-rsi
description: "Inspect, correct, or debug the Academic Harness local recursive self-improvement loop. Use when the user asks what the harness has learned about their research workflow, wants a learned rule forgotten or changed, asks why a lesson was injected, or asks to diagnose recurring failures across literature, hypotheses, data analysis, statistics, manuscripts, grants, or reviews."
---

# Academic Harness local RSI

The preset captures tool outcomes and explicit corrections on this machine, diagnoses recurring research failures, admits short lessons automatically, and injects them into later turns. There is no approval step. The loop only edits its own lesson store; it never edits the plugin, the vendored `ah` engine, the project, or the audit/evaluation code.

## What it learns

- Repeated `ah` audit findings (numeric, citation, structure, evidence)
- Tool errors and retries (`latex_compile`, `citation`, `manuscript_citations`, `integrity_check`, `stat_audit`, `figure_audit`, `repo_audit`)
- Integrity verdicts (`retracted`, `expression_of_concern`, `correction`, `unknown`)
- Gate handoffs
- Explicit user preferences ("always cite primary sources", "never use passive voice")
- Task-class failures for literature, hypotheses, experiments, data analysis, statistics, manuscripts, grants, review responses, reproducibility, and data management

## Commands

| Need | Tool |
|---|---|
| What has been learned | `ah_rsi` `action=status` or `action=report` |
| List lessons | `ah_rsi` `action=lessons` |
| Preview injection | `ah_rsi` `action=inject_preview` `task_class=...` |
| Diagnose now | `ah_rsi` `action=diagnose` |
| Retract a learned rule | `ah_rsi` `action=forget` `lesson_id=...` or `pattern=...` |
| Roll back a learned rule | `ah_rsi` `action=rollback` `lesson_id=...` |
| Offline report / benchmarks | `academic-harness-rsi status`, `report`, `benchmark synthetic`, `benchmark replay` |

Explicit preferences are captured automatically from the user's own message. Do not invent a preference, and do not use `ah_rsi` to add task content. Use `forget` only when the user explicitly retracts a rule; `rollback` is the explicit retirement path for an experimental lesson. The offline CLI (`academic-harness-rsi feedback --text ...`) is the manual path and requires a durable cue such as always, never, from now on, remember, prefer, make sure, or an imperative do not/don't.

## Boundaries

- Each turn records injected-token cost, an oracle manifest, and a reached-action proxy; reached means the prescribed tool ran, not that the lesson was followed or that the outcome improved.
- Lessons are guidance, not evidence. Never cite a lesson as support for a scientific claim.
- A lesson never overrides the current request, project rules, protected paths, the `ah` gate, or safety rules.
- The store is `$DSH_HOME/ah-rsi` (override `AH_RSI_STORE`), local-only by default. `AH_RSI=observe` captures without injection; `AH_RSI=off` disables the loop.
- The judge is local and heuristic: tool outcomes, corrections, and gate signals. Remote evaluation is opt-in (`AH_RSI_REMOTE=1`) and not required.
- `benchmark synthetic` tests the RSI pipeline, not the model. `benchmark replay` reports observational statistics over captured episodes, not causal proof of improvement.

## When the user asks whether RSI worked

Report the mode, episode counts, active/trial/retired lessons, injection and control rates, and any auto-rollback. Do not claim improvement without a held-out or controlled comparison; say what the local evidence does and does not establish.
