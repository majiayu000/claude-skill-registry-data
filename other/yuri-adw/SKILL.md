---
name: yuri-adw
description: Invoke when user asks to run the ADW loop / agentic engineering loop / software factory workflow.
---

## When to use
- Invoke for end-to-end engineering tickets that need orchestrated planning, deterministic validation, and review.
- Use when output must pass gates, include evidence, and route failures through BUILD payloads.
- Prefer this loop when deterministic artifacts should dominate over agent claims.
- Do not run blindly; pause for owner clarification on missing scope, no acceptance criteria, or blocked dependencies.

## The loop
- `INTAKE -> SCOUT -> PLAN -> BUILD -> VALIDATE -> REVIEW -> SHIP`
- INTAKE: orchestrator decodes + sizes ticket.
- SCOUT: cheap R0 lane (Phoenix, deepseek-v4-flash) produces evidence pack; output is hypothesis.
- PLAN: orchestrator writes the micro-task plan AND, for the gate, an executable decision manifest — `{name, discrete:{dim:[options]}, paramSpace:{param:[lo,hi]}, value:"(config,params)=>number", ...}` (see `adw-gate.mjs --help` for the full schema; the gate scores a decision problem, not prose).
- PLAN GATE: run `node _SYSTEM/Scripts/adw-gate.mjs plan --input <manifest.json>` returning `gate, pass, score, cornerLawBite, predictionId, reasons`. Records a prediction to the ledger.
- BUILD: fan out micro-tasks to producer lanes (gpt-5.4-mini mechanical, gpt-5.3-codex-spark creative, Sonnet semantic; gpt-5.6-luna for rescue/hard delegation — note the provider-route registry classifies luna verifier/strategist, so prefer it for rescue over volume production).
- VALIDATE: deterministic code checks first (lint/type/tests), then ENERGY GATE.
- VALIDATE GATE: run `node _SYSTEM/Scripts/adw-gate.mjs validate --input <outcome.json>` returning `gate, pass, deltaU, contributions, reasons`. Records the outcome to the prediction-ledger ONLY when the input carries the plan's `predictionId`; writes an energy trace only when `YURI_ENERGY_OBSERVABILITY=1` (advisory-unless-armed).
- REVIEW: /codex:review with profile `sol` (`gpt-5.6-sol`) plus native `/code-review`; adjudicate claim-by-claim.
- SHIP: orchestrator only, scoped-pathspec commit, prediction-ledger report, closeout.

## Phase reference table
| Phase | Actor/lane | Command | Gate | Failure route |
|---|---|---|---|---|
| INTAKE | Orchestrator | decode ticket, define constraints, size tasks | none | missing clarity → request owner input |
| SCOUT | R0 lane: Phoenix / deepseek-v4-flash | gather evidence pack | none; all outputs are hypothesis | false/weak claim → ignore or recollect evidence |
| PLAN | Orchestrator | build manifest.json then run plan gate | `adw-gate.mjs plan --input <manifest.json>` | fail -> replan with counter-evidence (max 2 cycles), then HOLD |
| BUILD | Producer lanes: mini, spark, Sonnet (luna = rescue only — registry: verifier-strategist, mayExecuteWorkerTasks false) | execute micro-tasks; no self-verification | none | submit failure payload back to orchestrator for BUILD loop |
| VALIDATE | Orchestrator + deterministic tooling | lint/type/tests, then `adw-gate.mjs validate --input <outcome.json>` | validate gate pass -> deltaU+contributions record | fail -> immediate payload back to BUILD in same session |
| REVIEW | /codex:review (sol) + /code-review + third-family tie-break (Helios/Grok) on disputes | claim-by-claim adjudication | cross-family adversarial pass only | unresolved claim -> return to BUILD or owner |
| SHIP | Orchestrator | scoped `git add`, scoped `git commit`, ledger report | owner-ready, no blocking claims | conflict/uncertain evidence -> HOLD, no commit |

## Roles and lanes
- Keep roles per-task, not fixed per-lane.
- Scout, builder, validator, and verifier are separate responsibilities in each workcell.
- A person/agent may switch roles only with explicit handoff and role boundary log.

## Evidence rules
- Tag every claim as `CONFIRMED` or `PLAUSIBLE`.
- Lane output from SCOUT/BUILD is `PLAUSIBLE` by default and advisory only.
- Deterministic artifacts (`git diff`, tests, type/lint logs, execution logs) are `CONFIRMED`.
- Orchestrator must spot-check at least one claimed path before using SCOUT claims.
- Only `CONFIRMED` claims can pass REVIEW gates and drive SHIP.

## Bounded loops
- Replan only inside PLAN failure.
- Max 2 PLAN replans.
- Third PLAN failure => `HOLD` is a valid terminal state and stops autonomous progression.
- `HOLD` requires owner resolution, then resume as a fresh loop turn.

## Invocation per surface
- Claude Code session: invoke skill `yuri-adw` with the ticket text.
- Codex terminal: invoke skill `yuri-adw` with manifest/ticket context; run worker lanes as needed.
- OMP terminal: invoke skill `yuri-adw` with task + acceptance criteria.
- For all surfaces, pass inputs as plain task text + explicit constraints and expected deliverables.
