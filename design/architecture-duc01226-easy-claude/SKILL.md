---
name: architecture
version: 1.0.0
description: '[Architecture] Use when a workflow step or the user asks for --mode=design (solution architecture), --mode=review (compliance: layers, boundaries, CQRS, tenancy), --mode=scalability (scale grade, coupling) or --mode=full (whole-project audit).'
---

> **[BLOCKING] Mode routing — detect FIRST.** Explicit `--mode=design`, `--mode=review`, `--mode=scalability` or `--mode=full` selects that mode; read its reference file in full before anything else (see [Mode Dispatch](#mode-dispatch)). No mode: show the mode table below and stop — ask nothing, run nothing, never guess a mode. `/architecture --mode=design`, `--mode=review`, `--mode=scalability` and `--mode=full` are the former `/architecture-design`, `/architecture-review`, `/architecture-scalability-review` and `/architecture-review-full`: those slash commands no longer exist, and each mode works called directly with no workflow.

## Quick Summary

**Goal:** One architecture skill with four independent modes — design a solution architecture, review a change for architecture compliance, grade a project's architecture and scalability, or audit a whole project — each running exactly its own contract.

**Summary:**

- Each mode is a self-contained contract in `references/mode-<x>.md`; the reference is the whole invocation contract — inputs, outputs, flags, report paths, round caps and `AskUserQuestion` behavior are that reference's, unchanged from the skill it came from.
- `--mode=full` composes the other modes: its three face sub-agents each run `--mode=scalability` or `--mode=review` (reading that mode's reference) plus `production-readiness-review`; it never re-implements a face.
- No mode is never an expensive default: print the table, stop.

## Mode Dispatch

Detect the mode from the invocation arguments before any other work; do not load a mode file the invocation did not select.

| Mode | Purpose | Read in full FIRST |
| --- | --- | --- |
| _(none)_ | Show this table; ask nothing; run nothing | — |
| `--mode=design [brief]` | Solution architecture design across backend, frontend, data, integration, deployment: ≥3 researched options per concern, ADRs, scaffold/harness handoff, user validation interview. Formerly `/architecture-design` | `references/mode-design.md` |
| `--mode=review [scope] [--report-only]` | Architecture compliance review of a change (layers, service boundaries, CQRS, tenancy, ADRs, scalability/coupling regression): PASS/WARN/BLOCKED report. `--report-only` = read-only leaf for a caller that owns every fix. Formerly `/architecture-review` | `references/mode-review.md` |
| `--mode=scalability [init\|audit] [scope]` | Architecture + scalability grade of a project or planned architecture: `/20` scorecard, G1-G7 gates, distributed-monolith risk, module isolation, coupling, horizontal scaling. Formerly `/architecture-scalability-review` | `references/mode-scalability.md` |
| `--mode=full [scope]` | Whole-project architecture + scalability + production-readiness audit: three read-only faces in parallel, dedup, one consolidated report with one combined verdict. Formerly `/architecture-review-full` | `references/mode-full.md` |

- **[BLOCKING]** When `--mode=design`, read `references/mode-design.md` in full FIRST and follow it alone; it owns the design steps, the ADR outputs and the Step-12 user-validation interview.
- **[BLOCKING]** When `--mode=review`, read `references/mode-review.md` in full FIRST and follow it alone; it owns `--report-only`, the 13-category review, the Phase-5 validation gate and the round caps.
- **[BLOCKING]** When `--mode=scalability`, read `references/mode-scalability.md` in full FIRST and follow it alone; it owns the `/20` scorecard (scored from `references/scorecard.md`), the gates and the `mode=init` / `mode=audit` run types.
- **[BLOCKING]** When `--mode=full`, read `references/mode-full.md` in full FIRST and follow it alone; it runs INLINE, fans the faces out as sub-agents and synthesizes one report.
- The `mode=init` / `mode=audit` tokens of the scalability mode are its run type, separate from the skill-level `--mode=scalability` that selects it.
- Modes are separate invocations: no mode chains into another except `--mode=full`, whose faces run the `scalability` and `review` modes as sub-agents.

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** run exactly one architecture mode per invocation, from its own reference, with that mode's contract unchanged.

- **MUST ATTENTION** detect the mode FIRST; read `references/mode-<x>.md` in full before any other work — why: the reference is the whole contract, and default/no-mode loads none of it.
- **MUST ATTENTION** no mode = print the table and stop; NEVER guess a mode, ask a question or start an audit — why: `full` is an expensive whole-project run nobody asked for.
- **MUST ATTENTION** `--mode=full` composes the other modes (face sub-agents read their references); NEVER copy a mode body into another.
- **MUST ATTENTION** follow the mode's own gates, flags, report paths and round caps verbatim; the old slash commands no longer exist.
