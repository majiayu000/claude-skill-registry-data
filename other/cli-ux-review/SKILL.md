---
name: cli-ux-review
description: Audit a command-line tool for user-friendliness — clear situation / next-step / options in every output, colour-highlighted runnable commands, no raw jargon, no silent hangs. Invoke for "CLI UX audit", "review my CLI", "is this CLI intuitive", or before any CLI release.
---

# CLI UX Review

Audits a CLI against a fixed rubric, from the perspective of a non-developer
who has never used it.

## When to invoke
- "CLI UX audit" / "review my CLI" / "is this CLI intuitive"
- Before every CLI release
- After adding or changing any CLI command

## The frame
Every command output must answer three questions:
**What is the situation? · What are the next steps? · What can I do?**

Quality bar: a command ends the way Codex ends a session — a line of plain
status, then the exact next command, rendered in a distinct colour so the eye
lands on "type this."

## Rubric (score each command against all 7)
1. **Next step present.** Every success / terminal state ends with the next
   command, or an explicit "you are done." No command stalls silently.
2. **Commands are colour-highlighted.** Runnable commands render in one
   consistent accent (cyan + bold). Never bare text, never literal backticks.
3. **No raw internals.** No enum values, state codes, or jargon in user output.
   Human words plus a one-line legend ("dirty" becomes "local edits").
4. **No silent hang.** Long-running or stdio commands announce themselves on a
   TTY, so the terminal never looks frozen.
5. **Consistent primitives.** One glyph set, one row/table helper, one next-step
   block, shared across commands, not re-invented per command.
6. **Errors embed the fix.** Every error names the exact command that resolves
   it.
7. **Guided first run.** Bare invocation or a not-logged-in state shows a
   numbered quickstart.

## How to run
1. Inventory every command and every output path. Read the source, not just
   `--help`.
2. For each command, walk the success path, every error path, and empty states.
3. Score against the 7 rubric points. Cite `file:line` for each finding.
4. Where it fails, write the concrete before / after with the exact strings.
5. Output: cross-cutting issues, a per-command table, ranked before/after fixes,
   and an execution plan.

## Output format
A findings doc: TL;DR and core problem, cross-cutting issues table, per-command
findings, before/after for each fix, execution plan. Never write "looks fine"
without having walked the actual output path that proves it.
