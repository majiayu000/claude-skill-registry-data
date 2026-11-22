---
name: gotcha
description: Capture a non-obvious constraint or a new canonical exemplar in .agentic/gotchas.md, with an evidence path and verified date.
user-invocable: true
argument-hint: "<the trap or exemplar to record>"
---

# Capture a gotcha or exemplar

Admission test — record it ONLY if all three hold:
1. The code cannot express it (otherwise: add a type, lint rule, or test instead —
   propose that to the user first).
2. An agent without this fact would plausibly do the wrong thing.
3. You can point at a concrete file as evidence.

## Constraint entry

Append under `## Constraints` in `.agentic/gotchas.md`:
- `### <one-line title>` naming the trap
- **Claim:** the constraint + what goes wrong if violated (one or two sentences)
- **Evidence:** repo-relative path you verified THIS session
- **Verified:** today's date

## Exemplar entry

Add a row to the `## Exemplars` table: shape name, path, today's date. An exemplar
must be a current, well-formed instance of the pattern — if the best example has
warts, note them in a constraint entry rather than pointing at a worse file.

## Hygiene

While in the file, scan existing entries touching the same area: if one is now
wrong or the constraint has been lifted, correct or delete it in the same edit.
Entries are cheap; stale entries are expensive.
