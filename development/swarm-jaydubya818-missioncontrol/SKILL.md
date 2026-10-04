---
name: swarm
description: "Use when authorized independent workers can run without shared mutable state."
license: MIT
metadata:
  author: jstack-maintainers
  source: michael-denyer/pstack-claude
  source-version: "0.9.30"
  source-commit: 45f768349a6d7d7e71509fee3f5bccfad54b3bad
  owner: software-factory
  risk: medium
  capabilities: jstack,multi-agent-workflow
---

# Swarm

On Codex, Cursor, or another non-Claude runtime, read the [runtime mapping](../poteto-mode/references/harness-tools.md), including its per-skill notes, before following this skill.

Fan out N parallel workers. They may cover separate slices, race the same brief, or mix both. The parent waits, aggregates, and returns one report.

## Start

Open a todolist with one entry per phase before launching anything.

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report the swarm must return.
2. Choose the shape. Partition into slices, race N workers on identical briefs, or mix both. For a race or mixed shape, declare `first pass`, `rank all`, or `best-of` before spawning.
3. Set N from the user or derive it from the shape. N is total workers, not the number that run at once.
4. Pick the worker model from `swarm workers` in `~/.claude/jstack-models.md` when present. Otherwise use the default in [Models](#models). For a model race, name each arm's model up front.
5. Give each worker its own writable output when it writes.

## Phase B: Fan out

Spawn all N workers in one message with `subagent_type: "general-purpose"`, `run_in_background: true`, and the configured model. Claude Code subagents all run on this machine, so isolation comes from the worktree or output directory assigned in Phase A, not from a remote environment.

When a worker must start from a non-default branch, check that branch out in the worker's own worktree and name the worktree path in its brief.

Every brief stands alone. Include the goal, scope, exact slice or race arm, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence.

If a worker drops out, proceed with N-1 and note it.

## Phase C: Aggregate

Read the terminal results. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front. Use first pass, rank all, or best-of. Do not paste raw worker dumps.

Keep a compact result table, one-line evidenced issues, and explicit gaps or dropouts.

## Phase D: Report

Return one consolidated in-chat report with the table, issue one-liners, gaps or dropouts, and the race rule when used.

## Models

Role defaults originate from the upstream `plugins/pstack/models.json`. Refresh them through `scripts/vendor_jstack.py` after reviewing the upstream change. A matching role line in `~/.claude/jstack-models.md` overrides each at runtime; see `/setup-jstack`.

- swarm workers: `claude-opus-5`
