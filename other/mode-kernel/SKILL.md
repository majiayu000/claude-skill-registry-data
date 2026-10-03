---
name: mode-kernel
description: Central decision table for how a stop-and-wait gate behaves per Claude Code session mode (normal, autonomous/no-pause, planning, background). Trigger whenever agent-usage, debug-protocol, coding-standards, or perf-audit is about to apply its gate outside plain interactive mode.
---

# Mode Kernel — Gate Behavior Per Session Mode

Several skills in this library contain a "stop and don't act until asked" instruction: `agent-usage`'s approval gate, `debug-protocol`'s "deliver the diagnosis and stop," and the "don't fix unprompted" line in `coding-standards` (review mode) and `perf-audit`. Each defers to this file for how its gate behaves outside plain interactive mode, instead of restating mode-override logic individually.

## Self-improvement (do this first and last)
1. **At start:** read `learnings.md` in this skill's folder if it exists. Apply relevant lessons.
2. **At end of every use:** append one dated bullet — a mode where a gate held or silently eroded, a case this table didn't cover. Merge instead of duplicating; delete disproven bullets.

## Normal interactive mode

No adjustment. The gate applies exactly as written in the owning skill.

## Autonomous / no-pause modes

Some tools offer a mode that biases toward acting without pausing for clarifying questions. That bias does not override any gate in this library. A gate-bearing skill's "stop and ask" is a specific, deliberately-authored standing rule — it takes precedence over a generic proceed-by-default bias, the same way such modes already carve out destructive/shared-state actions for confirmation regardless of their own default. Treat every gate here as one of those carve-outs.

## Planning modes

Some tools' planning phase defaults to launching research/exploration subagents as part of its own built-in instructions — a direct, named push toward agent use, not just a general bias. It is overridden the same way: `agent-usage`'s default-never rule and its Exception 1/2 gating apply inside planning too. Explore inline (read/search directly) during planning; only invoke a planning phase's own research subagents when Exception 1 (explicit user request) or Exception 2 (judged need, approval-gated) actually applies — not because the mode's own text suggests it by default.

Other gates (`debug-protocol`, `coding-standards`, `perf-audit`) are rarely reached mid-planning, since planning is read-only — no adjustment needed beyond the agent-usage point above.

## Background / non-interactive contexts

Covers a scheduled/looped run, or a subagent's own turn — any context with no user present to answer synchronously. A gate that requires a live answer cannot fire as designed here:

- **`agent-usage`'s approval gate:** Case 1 (forced compaction) is actionable without a live answer, since it's closer to a necessity than a judgment call — proceed if genuinely needed. Case 2 (disposable context) defaults to **not** delegating; if the tension is real, flag it in the next status output for a human to see later, rather than making a silent, unreviewable call.
- **`debug-protocol`'s "stop after diagnosis":** if there's no user to hand the diagnosis to, this only applies when the invoking task was explicitly scoped to "diagnose only" — otherwise proceed to the fix, since there's no one to ask and no one to leave the finding stranded with.
- **`coding-standards` / `perf-audit`'s "don't fix unprompted":** stays in force — report findings, do not apply fixes, even with no user present. Unlike the other two, this gate protects against scope overreach, not against acting without permission on a task already scoped — so it holds regardless of who's watching.

## Adding a new gate-bearing skill

If a future skill introduces its own "stop and wait" instruction, point it here rather than writing new mode-override text inline — one line: "Gate behavior across session modes: see `mode-kernel`."
