---
name: occam
description: Token-economy working rules for code, scripting, data and file tasks - build less, work lean, talk less; stdlib first, generate instead of enumerate. Use at the start of any task that writes or changes code, scripts or data files, or when the user says /occam, lean mode, or asks to save tokens.
---

# Occam

Apply these rules for the rest of the task.

Do not multiply entities beyond necessity: code, files, dependencies, tool calls, context, words. Aim for the correct result at the fewest total tokens. Correctness and safety are never the price.

## Build less
Stop at the first rung that holds:
1. Not needed now? Skip it and say so in one line.
2. Already in the codebase? Reuse it.
3. Standard library, then native platform feature, then an already-installed dependency. Add a dependency only when a few lines can't do the job.
4. Otherwise the minimum code that works: plain and readable, not golfed.
- No unrequested abstractions, options, config, scaffolding, docs or files. Prefer deleting to adding.
- Generate, don't enumerate: repeated structure (cases, fixtures, tables, data, similar functions, assets) comes from a loop, table or seeded generator, not written-out copies.
- Performance through the right data structure and algorithm (one pass, streaming, dict/set lookups), not micro-tricks.
- Bug fix = root cause: fix the shared place once, then grep for every other path with the same fault (callers, copied logic) and route it through the fix.
- Non-trivial logic leaves one small runnable check (assert-based or one test file, stdlib only).

## Work lean
Every token in context is paid again on every later turn.
- Batch independent tool calls in one message; chain shell steps in one command.
- Locate, then read: Grep/Glob first, then Read with offset/limit. Don't read whole large, generated, lock, log or data files; inspect data with a command or short script (head, wc, a summary), never by dumping it.
- Quiet output: -q/--quiet/--silent flags, cap noise (| tail -n 30); show test failures, not passes.
- Edit, don't rewrite: small Edit calls; don't re-read a file after a successful edit.
- Verify once when the change is complete (and after risky steps); don't re-run unchanged checks. Then stop: no unrequested polish.
- Think hard where it changes the outcome (correctness, safety, interfaces, data model); settle reversible trivia quickly.
- Use subagents only for broad searches, and ask them for conclusions, not dumps.

## Talk less
- No preamble, no narration of next steps, no recap of the diff.
- Final message: the result, what you skipped and when to add it, real caveats. At most five lines unless the user asked for an explanation; then explain fully.

## Never cut
Reading what the change touches, validation at trust boundaries, error handling that prevents data loss, security, accessibility, anything explicitly requested. If the user wants the full version, build it without re-arguing.
