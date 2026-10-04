---
name: docs-manager
version: 1.0.0
description: '[Documentation] Use when a workflow step or the user asks for a documentation update of docs impacted by code/spec/test changes (--mode=update), or first-time init of the reference-doc set from project-config (--mode=init).'
---

> **[BLOCKING] Mode routing — detect FIRST.** Explicit `--mode=update` or `--mode=init` selects that mode. `/docs-manager --mode=update` and `/docs-manager --mode=init` are the former `/docs-update` and `/docs-init`: those slash commands no longer exist, and each mode works called directly with no workflow. No mode flag and no natural-language request matching the `update` Intent column: show the [Mode Dispatch](#mode-dispatch) table and stop — ask nothing and run nothing (`init` is heavy and runs only on an explicit `--mode=init`). Read the mode file in full before anything else.

## Quick Summary

**Goal:** Keep project documentation true to the code: `--mode=update` syncs the docs a change impacts (reference docs, project config, Feature Specs, §8 TCs, derived indexes, demo guides); `--mode=init` initializes or reconciles the whole reference-doc set from project config.

**Workflow:** Detect the mode → read its `references/mode-<x>.md` in full → run that mode's ordered phases and gates → report with evidence.

**Key Rules:**

- One mode per invocation; the two modes share no body and a mode never loads the other's file.
- A natural-language request that matches the `update` Intent column selects `update`; `init` is selected only by an explicit `--mode=init`. No mode flag and no such request: show the [Mode Dispatch](#mode-dispatch) table and stop.
- `--mode=` (two dashes) selects the skill mode. The `update` caller flag `mode=update` (no dashes, see that mode's Additional Requests) only overrides `/spec` mode detection and never selects a skill mode.
- The `docs-manager` sub-agent (`subagent_type="docs-manager"`) is an agent, not this skill; it drives `/docs-manager --mode=update`.
- MUST ATTENTION keep claims evidence-based (`file:line`, confidence >80% to act) and task tracking live as each step starts and completes.

## Mode Dispatch

Detect the mode from the invocation arguments before any other work; do not load a mode file the invocation did not select.

| Mode | Purpose | Intent (natural-language triggers) | Read in full FIRST |
| --- | --- | --- | --- |
| `--mode=update [modules=… changed_files=… phases=… skip_phases=… tc_mode=… freshness={impact\|full\|off} base=…]` | Sync the docs impacted by code, spec or test changes: triage → impact-scoped project-context sync → `/spec` chain → demo guide → report. Formerly `/docs-update` | "update docs", "docs impacted by my changes", "sync docs after code change", "doc sync", "documentation update" | `references/mode-update.md` |
| `--mode=init` | First-time initialization or reconciliation of the whole project reference-doc set from project config; delegates each target to `scan`. Formerly `/docs-init` | _(explicit `--mode=init` only)_ | `references/mode-init.md` |

- **[BLOCKING]** When `--mode=update`, read `references/mode-update.md` in full FIRST; it owns the 9-task creation gate, the fixed phase order, the `$ARGUMENTS` caller flags, the Phase 5 report (`tmp/reports/docs-update-{YYMMDD}-{HHMM}.md`) and the nested-in-workflow behavior. Workflow invocation and standalone both run the full contract.
- **[BLOCKING]** When `--mode=init`, read `references/mode-init.md` in full FIRST; it owns the config validation, the always-on vs task-specific doc split, the applicability-gated `scan` delegation and the AI-discovery gate.
- One-doc rebuilds stay in `scan` (`/scan --target=<key>`); refreshing every selected reference doc at once stays in `scan-all`. `--mode=update` escalates to them and `--mode=init` delegates to `scan`; neither is a mode of this skill.

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** Keep project documentation true to the code through exactly one mode per invocation, reading that mode's reference in full first.

- **MANDATORY IMPORTANT MUST ATTENTION** `--mode=<x>` reads `references/mode-<x>.md` in full FIRST; no mode flag and no `update`-intent request shows the mode table and stops — never guess a mode, never start `init` without an explicit `--mode=init`
- **MANDATORY IMPORTANT MUST ATTENTION** break work into small todo tasks using `TaskCreate` BEFORE starting; follow the mode's own task list and fixed step order
- **MANDATORY IMPORTANT MUST ATTENTION** cite `file:line` evidence for every claim (confidence >80% to act)
- **MANDATORY IMPORTANT MUST ATTENTION** add a final review todo task to verify work quality

**[TASK-PLANNING]** Before acting, analyze task scope and systematically break it into small todo tasks and sub-tasks using TaskCreate.
