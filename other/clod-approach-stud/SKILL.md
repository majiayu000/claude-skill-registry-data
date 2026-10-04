---
name: "Approach: Stud"
description: "Studs every function of a planned feature in its real file as a runnable walking-skeleton (fake data, real wiring), so names, placement and contracts are reviewable before any real logic is written. Lays the skeleton, then checkpoints for review."
when_to_use: ">=1 of the following are true: (a) spans several functions/files; (b) touches existing code in more than one place; (c) user wants to review the approach before implementation; (d) user is learning the codebase"
user-invocable: false
metadata:
  family: clod-approach
# No model/effort override: fires inside an ongoing build, so it inherits the
# session the user chose for that work
allowed-tools:
  - "Read"
  - "Glob"
  - "Grep"
  - "Edit"
  - "Write"
  - "Bash(~/.claude/library/scripts/find-scaffold.sh:*)"
disallowed-tools:
  - "Bash(git:*)"
  - "Bash(gh:*)"
---

# Stud: Part 1, skeleton first (knowledge)

You reached for this skill mid-task because you're about to build something that spans several functions or files, and the shape should be reviewable before the logic. This is a **technique you apply**, not a ceremony you run: lay a runnable skeleton, prove the plumbing, then checkpoint so the shape can be reviewed before you fill it.

There is no interview here. You were triggered mid-flow, and the feature is already in play. If a genuine ambiguity blocks the skeleton, ask a single targeted question and move on; don't turn this into a planning session.

The methodology itself (two-stage rationale, real homes, shared shapes, stubs, banners, verification, fill order, shared hard rules) lives in `~/.claude/library/references/stud/methodology.md`. Read it now and execute it; this file adds only what is unique to the self-triggered path.

## Announce at start

State the mode-switch out loud so whoever's watching knows why the next diff is full of fakes and scaffold banners:

> "I'm laying down a runnable skeleton before filling in the logic (stud skill); I'll checkpoint the shape before writing any real logic."

This line is load-bearing in the knowledge path: the user didn't ask for a skeleton, so tell them they're getting one and why.

## Execute the methodology

Homes (reusing files already read this task), shapes, stubs, banners, then verify the skeleton runs; all per the methodology reference.

## Checkpoint before filling

You triggered this yourself mid-task, so don't barrel straight into Stage 2. Surface the shape and let it be reviewed **before** any real logic:

- Show what ran and the flow it exercised.
- List the seams the reviewer must sign off: `find-scaffold.sh --seams`.
- State the fill order you'd take next, per the methodology's Stage 2 preview.
- Then pause for the shape to be reviewed.

The whole reason you reached for a skeleton was to make the shape reviewable; skipping the checkpoint throws that away.

## Unique mistakes on this path

- **Skipping the announce.** The user didn't ask for a skeleton; if you don't say why the diff is full of fakes, it reads as broken code.
- **Barrelling into Stage 2.** The point of studding is a reviewable shape; filling without a checkpoint discards it.
- **Turning it into an interview.** You were triggered mid-flow; resolve real blockers with one targeted question, not a planning session.
