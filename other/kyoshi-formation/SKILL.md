---
name: kyoshi-formation
description: Suki's fan formation for parallel work. Every Kyoshi Warrior holds a set position, and the squad returns one report. Use for swarm, /swarm, "swarm this", fanning out N parallel workers, coverage sweeps, races between identical briefs, review gauntlets, verifier lanes, and exploration partitions.
---

# Suki's Kyoshi formation

The Kyoshi Warriors fight as one fan. Each warrior holds a set position, nobody covers ground another warrior already holds, and Suki reads the whole line before she calls the result. Frame the formation, send every warrior out at once, gather what each one brings back, and give one report.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

## Start

Open a todolist with one entry per phase before launching anything.

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report the formation must return.
2. Choose the shape. Partition into slices, race N workers on identical briefs, or mix both. For a race or a mixed shape, declare the selection rule before spawning. It is one of `first pass`, `rank all`, or `best-of`.
3. Pick the worker model from the `suki` line in the avatar-setup sheet (`${CLAUDE_CONFIG_DIR:-~/.claude}/team-avatar-models.md` on Claude Code, `${CODEX_HOME:-~/.codex}/team-avatar-models.md` on Codex). With no sheet or no line, use `opus`. For `inherit`, omit `model` so the workers run on the parent model. If the Agent tool rejects a model name, use `opus` and say so. If it rejects `opus`, use the closest valid name of the same family from its error message. For a model race, name each arm's model up front, taking the arms from the sheet's `panel` line. Pick each worker's reasoning effort for the job, as the dispatch rules in `avatar-mode` describe. A value such as `opus @high` passes `high` as the Agent tool's `effort` parameter.
4. Give each worker its own writable output when it writes (a worktree, a branch, or an output directory). When workers verify or measure commits, each brief names the exact SHAs. A measurement brief also names the method (sample count, what one sample is, the order). The worker records both in its result.

## Phase B: Fan out

Spawn all N workers in one message with `run_in_background: true` and the model from Phase A, left unset for `inherit`. Dispatch each one as the character whose discipline fits its slice, as `subagent_type: "team-avatar:<character>"`. Toph takes read-only review and investigation lanes. Katara takes test and defect lanes. Zuko takes measurement lanes. Never send Toph a slice that edits files. Claude Code subagents all run on this machine, so isolation comes from the worktree or output directory assigned in Phase A, not from a remote environment.

When a worker must start from a non-default branch, check that branch out in the worker's own worktree and name the worktree path in its brief.

Every brief stands alone. It names the goal, the scope, the exact slice or race arm, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence. A worker that can prove a defect reports `ISSUES` and lists every issue it can prove, not only the first.

If a worker drops out, proceed with N-1 and note it.

When this skill runs inside a character that is itself a subagent, that character does not dispatch. It works the slices itself, one after another, labels the pass as sequential, and reports back.

## Phase C: Aggregate

Read the terminal results. Drop a result that does not record the SHAs and method its brief names, and respawn that worker once. After a second miss, record a gap. A gap does not count as a pass. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front. Do not paste raw worker dumps.

## Phase D: Report

Return one consolidated in-chat report. It holds a table of slices or arms with their verdicts, one line per issue, every gap or dropout, and the race rule when one was used. Write it per `tea-time`.
