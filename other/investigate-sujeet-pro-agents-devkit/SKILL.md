---
name: investigate
description: >-
  Investigate, diagnose, RCA, "why is X slow/broken/down", "what changed" for any production
  symptom. Triggers on a free-text symptom + service, a Datadog incident/monitor/dashboard/log URL,
  a Slack alert permalink, a Statsig gate/experiment URL, or a Mixpanel/Snowflake/Looker question.
  Read-only — never modifies a monitor, dashboard, flag, or experiment, and never triggers a
  rollback or restart (recommends; the human executes). Pins an explicit time window on every query,
  correlates >=2 independent signals before naming a root cause, and states confidence (low/med/high)
  with anchored evidence and <=15-word verbatim quotes. Produces a timeline + hypothesis + a
  lowest-blast-radius next action.
allowed-tools: Read, Grep, Glob, Bash, WebFetch, Agent, Workflow
argument-hint: "<symptom-or-url> [--use incident|rca|experiment|datadog|mixpanel|statsig|snowflake|looker] [--window <duration>] [--service <name>] [--deep]"
---

# investigate — diagnose any production symptom (read-only)

Polymorphic on the input. **Read-only, always.** Never modifies a monitor / dashboard / flag / experiment; never triggers a rollback or restart — it *recommends*, the human executes. Two non-negotiables drive everything below: **a two-source minimum before naming a root cause**, and **an explicit pinned time window on every query** (no "recent", no "lately").

The full operating contract lives in this skill folder — read these as you need them:

| Aspect | File |
|---|---|
| How you investigate (voice, confidence, blast-radius ordering) | `persona.md` |
| The phased process + Workflow multi-source fan-out | `workflow.md` |
| Hard rules + refusals + safety | `rules.md` |
| Input routing (symptom / Datadog / Slack / Statsig / analytics) + MCP map | `dispatch.md` |

## Quick start

1. **Read `dispatch.md`** and classify the input → pick the sub-flow + the data sources it implies.
2. **Pin the window.** Resolve an explicit `[T_start, T_end]` from `--window`, the alert's fire time, or the symptom's first-seen. If none can be derived, **ask** — don't guess (`rules.md`).
3. **Read `persona.md`** — adopt the correlate-before-concluding investigator stance.
4. **Run the workflow in `workflow.md`.** For any non-trivial symptom, fan out one `context-gatherer`/`investigator` agent **per data source** with the **Workflow tool** — each blind to the others — then form a hypothesis that requires **≥2 agreeing signals**, then have a skeptic try to refute it.
5. **Report** a timeline + hypothesis (with confidence + evidence count) + a next action ordered by blast radius. Nothing is posted or changed; publishing a report is gated per `rules.md`.

## Workflow is the default for real symptoms

"Always have a workflow." A symptom worth investigating gets the multi-source Workflow in `workflow.md`: each agent searches a **different source in isolation** (Datadog logs/metrics/traces, recent deploys via `gh`, Slack chatter, Statsig audit log, Mixpanel/Snowflake/Looker as relevant), the orchestrator correlates the independent results, and a skeptic hunts for a contradicting signal before the hypothesis survives. Blind, parallel sweeps are what stop you from anchoring on the first plausible cause. Skip the Workflow only for a trivial single-source lookup (e.g. "what's the p99 on service X right now"), and say so.

## Modes / sub-flows

- **default** — investigate, correlate, report a timeline + leading hypothesis + next action. Nothing posted or changed.
- **`--use incident`** — the common path: symptom + service → Datadog + recent deploys (`gh`) + Slack, correlate, hypothesize.
- **`--use rca`** — full root-cause: incident sweep + Statsig audit-log (±2h around the window) + git-blame on suspect deploys via `gh`/`git` + optional Mixpanel user-impact.
- **`--use experiment`** — a Statsig/Mixpanel experiment is the suspect: pull its results/audit history and correlate with the symptom window.
- **`--use datadog|mixpanel|statsig|snowflake|looker`** — scope the sweep to one source (still pins the window, still read-only).
- **`--window <duration>`** — set the investigation window explicitly (e.g. `--window 6h`, `--window 2026-06-04T14:00Z..2026-06-04T15:30Z`).
- **`--deep`** — stronger reasoning profile; auto-selected for multi-service, ambiguous, or data-loss-suspected symptoms.
