---
name: persistent-planning
description: Advisory persistent planning for complex, multi-step Codex work. Use only when a task needs durable working notes across phases or sessions; subordinate to AGENTS.md, project-lifecycle, repo-preflight, diff-scope-guardian, debug-repro-loop, closeout-review, and explicit user instructions.
---

# persistent-planning

Source repo: https://github.com/mxyhi/ok-skills
Source path: planning-with-files/SKILL.md
Source commit: 7b5e271abd2d0a699331047874b89d2ff2fa5b71
Local adaptation note: Adapted into a constrained operator skill. It preserves the useful idea of durable planning files, but changes the default location to `.planning/<task-id>/` and makes planning advisory rather than mandatory.

## Purpose

Use a small set of persistent Markdown notes when the active task is complex enough that context, findings, and phase status may otherwise be lost.

This skill does not replace the lifecycle protocol. For project-level work, the Goal Contract and lifecycle gates remain authoritative.

## Activation

Use when at least one is true:
- The task is multi-step and likely to span several tool calls, phases, or sessions.
- The task has enough findings, decisions, or verification evidence that a transient chat summary is fragile.
- The user explicitly asks for durable planning, persistent notes, or resume-ready task state.

Do not activate for simple questions, quick lookups, single-step edits, or when the user says no planning.

## Default File Layout

Default directory:

```text
.planning/<task-id>/
```

Default files:

```text
.planning/<task-id>/task_plan.md
.planning/<task-id>/findings.md
.planning/<task-id>/progress.md
```

Use a short task id derived from the user goal, such as `2026-05-24-close-pack-audit` or `upload-refresh-fix`.

## Workflow

1. Confirm the task needs persistent planning under the activation rules.
2. Create or reuse `.planning/<task-id>/`.
3. Keep `task_plan.md` focused on goal, constraints, phases, and verification points.
4. Keep `findings.md` focused on durable discoveries, source paths, and evidence.
5. Keep `progress.md` focused on phase status, commands run, tests, blockers, and handoff notes.
6. Re-read the relevant planning file before major decisions or after a context transition.
7. Update planning files only when the note would help a future continuation or audit.

## Forbidden actions

- Do not create root-level `task_plan.md`, `findings.md`, or `progress.md` unless the user explicitly approves that exact location.
- Do not use planning files to bypass AGENTS.md, project-lifecycle, or the active Goal Contract.
- Do not force planning for simple tasks.
- Do not turn planning into a broad architecture document unless the user requested that artifact.
- Do not write unrelated repo documentation, edit AGENTS, update CONTEXT.md, create ADR, publish, deploy, git push, or run setup as part of this skill.

## Stop conditions

Stop and do not activate when:
- The task is single-step or can be answered directly.
- The user says no planning, quick answer only, audit only, or read-only with no file writes.
- There is no clear task id or no safe workspace location for `.planning/<task-id>/`.
- Creating planning files would violate project-local instructions or the current approval boundary.

## Output Pattern

When active, report:

```text
Persistent planning: ACTIVE
Plan directory: .planning/<task-id>/
Files used: task_plan.md, findings.md, progress.md
Lifecycle relationship: advisory; Goal Contract remains authoritative
```
