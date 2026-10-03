---
name: crav1-review-plan
description: >-
  Start the crav1-plan-reviewer-agent subagent on plan.md and tasks.md against
  spec.md. Use after /crav1-plan-from-spec. Numbered plan issues (P#) for
  /crav1-tighten-plan. Do not write application code. Do not answer new
  product questions.
disable-model-invocation: true
icon: search
color: orange
---

# Start plan reviewer

This skill is the **command**. You are the parent. Immediately delegate to the **crav1-plan-reviewer-agent** subagent. Load `.claude/agents/crav1-plan-reviewer-agent.md` (drop-in) or this plugin’s `agents/crav1-plan-reviewer-agent.md`. Do not review in your own voice as a substitute. Do not edit files. Do not write application code. Do not resolve product questions (those belong on the spec).

## Find the spec folder

Use the folder the user @-mentions. Otherwise the most recently edited tree under `docs/specs/` excluding `_template/`. If several, ask which slug, then delegate.

Need `spec.md`, `plan.md`, and `tasks.md`. If plan/tasks are missing, stop (`/crav1-plan-from-spec`). Do not invent a plan in this command.

Pass the subagent these paths (read-only): `spec.md`, `plan.md`, `tasks.md`, plus `diagrams.md` / `adr/` if present. Also point it at this skill’s `assets/` (drop-in also `.claude/agent-assets/crav1-plan-reviewer-agent/`; plugin also `agent-assets/crav1-plan-reviewer-agent/`) for **expected plan/tasks shape**, not as the files under review.

## What to tell the subagent

Instruct it to follow its own prompt and to finish with numbered **Issues for `/crav1-tighten-plan`** (`P1`, `P2`, …), one finding each. Mark any finding that is really a spec defect as **spec** (do not pretend the plan can fix it). No single global patch recommendation.

## After it returns

Show the subagent’s review. Then tell them the next command is `/crav1-tighten-plan` to walk **plan** `P#`s one by one. Spec-tagged findings: `/crav1-tighten-spec` or `/crav1-resolve-questions` — do not start those in this turn unless they already asked.
