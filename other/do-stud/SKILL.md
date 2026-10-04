---
name: "Do: Stud"
description: "Plan a non-trivial feature by interviewing to resolve unknowns, then studding every function as a runnable walking-skeleton (fake data, real wiring) so names, placement and contracts can be reviewed before any real logic is written. Stops for review; fill is a separate pass."
when_to_use: "When about to build a non-trivial feature and you want the shape agreed before real logic is written: it spans several functions/files, or you want a checkpoint before implementation starts."
arguments: ["outcome", "questions"]
argument-hint: "[desired outcome] [open questions to resolve]"
disable-model-invocation: true
model: sonnet
effort: medium
metadata:
  glyph: ᛊ
  family: do
allowed-tools:
  - "Read"
  - "Glob"
  - "Grep"
  - "Edit"
  - "Write"
  - "AskUserQuestion"
  - "Bash(~/.claude/library/scripts/find-scaffold.sh:*)"
disallowed-tools:
  - "Bash(git:*)"
  - "Bash(gh:*)"
---

# Stud: Part 1, plan then skeleton (command)

You were invoked deliberately by the user with an outcome in hand. Your job is to turn a decided-upon feature into a **reviewable runnable skeleton**, and to stop there. This is a planning ritual, not an implementation run: interview first, stud second, then hand back for review. Do **not** write real logic in this skill.

**Arguments:** `$outcome` is required; `$questions` is optional (trailing). If `$questions` is empty, skip the interview and go straight to the methodology.

The methodology itself (two-stage rationale, real homes, shared shapes, stubs, banners, verification, fill order, shared hard rules) lives in `~/.claude/library/references/stud/methodology.md`. Read it now and execute it for **$outcome**; this file adds only what is unique to the user-invoked path.

## 1. Interview to resolve the unknowns (before the methodology)

Before touching code, resolve **$questions** with the user. This is the part a mid-task pass can't do: you have the user's attention, so use it. Resolving `$questions` up front is this skill's whole advantage.

- Use `AskUserQuestion` for each open question; keep going until they're all resolved or explicitly parked.
- Feed the answers back into the outcome so the skeleton builds the *agreed* shape, not a guessed one.
- If a question can't be resolved now, note it as a **carried assumption** and flag it at handoff rather than silently picking an answer. Never invent answers to fill the gap.

## 2. Execute the methodology

Homes, shapes, stubs, banners, then verify the skeleton runs; all per the methodology reference.

## 3. STOP and hand back for review

This skill ends at a reviewable skeleton. **Do not start Stage 2.** Fill in `templates/handoff.md` and wait for the user:

- **What ran:** the flow the skeleton exercised.
- **Carried assumptions:** every unresolved item from the interview, flagged.
- **Seam inventory:** from `find-scaffold.sh --seams`.
- **Proposed fill order:** per the methodology's Stage 2 preview.

## Unique mistakes on this path

- **Skipping the interview.** You have the user in the loop; resolving `$questions` up front is this skill's whole advantage. Don't guess what you could ask.
- **Bleeding into Stage 2.** This skill stops at a reviewable skeleton; the user approves the fill order before any real logic.
