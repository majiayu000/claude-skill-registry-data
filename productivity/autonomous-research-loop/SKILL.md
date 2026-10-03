---
name: autonomous-research-loop
description: Run, maintain, or extend the paper-only autonomous research workflow for baseline, full experiment, and related comparison reporting across scripts, EXE packaging, startup flow, and operator panel actions. Use only for paper-research automation. Never use for live trading enablement or automatic tuning.
---

# Autonomous Research Loop

## Binding sources

- **`docs/FINAL_SYSTEM_VISION.md`** — **continuous research / testnet data** for **L6** and **L9–10**; autonomy must stay **bounded**.
- **`AGENTS.md`** — paper-first; loops stop on operator/error/config; no unbounded hidden agents.

## Purpose

Use this skill to manage the repository's autonomous paper-only research workflow.

This path supports **research mode continuity** and operator observability in **`docs/FINAL_SYSTEM_VISION.md`** (Layers 6, 9–10): long-running paper study, not live trading.

It covers the current research surface:
- baseline safe runs
- scorer experiment runs
- research-loop summaries and concentration reporting
- EXE build and Windows startup flow
- operator panel actions that trigger the same research paths

## Use When

Use this skill when the task is one or more of:
- run or refine the autonomous paper-research loop
- improve baseline vs experiment orchestration
- improve compact experiment summaries
- package or launch the loop on Windows
- improve startup behavior, single-instance safety, or local research logs
- wire the same loop cleanly into the operator panel

## Do Not Use When

Do not use this skill for:
- live trading automation
- exchange order execution changes
- hard risk weakening
- auto-tuning or auto-learning application
- strategy logic rewrites unrelated to research-loop operation
- operator-panel changes that do not touch research workflow behavior

## Safety Contract

Never violate these rules:
- `PAPER_TRADING=true` remains the safe default
- `AI_MODE=OFF`, `LEARNING_MODE=OFF`, and `SCORER_CONFIDENCE_EXPERIMENT=false` remain repo defaults
- baseline and experiment flows stay clearly separated
- experiments stay opt-in and labeled
- no hidden runtime behavior change
- no secret logging or secret packaging

## Primary Workflow

1. Read `AGENTS.md`.
2. Inspect the current research scripts, reporting path, EXE helpers, and any touched operator-panel action.
3. Preserve the baseline path first.
4. Make the smallest safe orchestration or reporting change.
5. Run the quality gate if scripts or code changed.
6. Verify baseline path still works.
7. Verify experiment or trial path still works if touched.
8. Summarize the operational outcome, not a file dump.

## Required Checks

- Baseline and experiment outputs remain distinguishable.
- Trial labels remain explicit in logs, summaries, and panel views.
- EXE or startup helpers do not mutate repo defaults.
- Research summaries stay compact and decision-oriented.
- Windows helpers remain readable, local-safe, and paper-only.

## Expected Output

- `What Changed:` file-level summary.
- `Autonomous Workflow:` what runs in what order now.
- `Trial Visibility:` how baseline and experiment stay distinct.
- `Safety Check:` explicit confirmation that defaults and hard controls remain intact.
