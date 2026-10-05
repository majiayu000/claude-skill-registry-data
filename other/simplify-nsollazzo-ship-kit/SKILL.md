---
name: simplify
description: |
  Portable fallback simplifier for harnesses with no built-in `simplify`. Reviews the
  changed code for reuse, simplification, efficiency, and "altitude" (right level of
  abstraction) cleanups, then applies the fixes. Quality only — it does NOT hunt for
  correctness bugs; use the `code-review` skill for that. Use when asked to "simplify",
  "clean this up", "tidy the diff", or as the cleanup stage of a ship pipeline. Operates
  on recently changed code unless told otherwise. **If your harness ships its own
  `simplify` skill, prefer that one** — this exists so `ship`'s pipeline runs everywhere,
  not to compete with a native implementation.
license: MIT
metadata:
  author: Nicholas Sollazzo
  version: "3.0.0"
---

# Simplify — make the change cleaner without changing what it does

Improve the clarity and economy of the **changed** code while preserving behavior exactly.
This is a quality pass, not a bug hunt: if you spot a correctness bug, note it, but fixing
bugs is the `code-review` skill's job — stay in your lane.

> **Portability note.** Needs only a shell (`git`), file reading, and editing. No
> harness-specific tools assumed. A ship orchestrator should prefer a richer native
> `simplify` if the harness ships one, and use this as the fallback otherwise.

> **Sub-agents.** For a **large, multi-file** change, fan the cleanup out by area to
> parallel sub-agents (Claude Code `Agent`/Task, Codex `worker`, Grok parallel sub-agents,
> Hermes `delegate_task`, OpenClaw `sessions_spawn`) — give each a disjoint set of files so
> two agents never edit the same file, then reconcile so a shared helper isn't extracted
> twice. For a small change, just do it in one pass — fan-out isn't worth the overhead.

## What to look for

| Lens | Fix |
|------|-----|
| **Reuse** | A helper/util/type already does this — call it instead of re-implementing. |
| **Simplification** | Delete dead code, collapse needless indirection, flatten nesting, drop unused params/vars, replace a custom loop with a stdlib call. |
| **Efficiency** | Remove obviously redundant work (recomputing in a loop, a query per item, double iteration) — only when it doesn't change behavior or risk. |
| **Altitude** | Pull a leaked low-level detail behind the right boundary, or inline a one-use abstraction that adds nothing. Don't over-abstract single-use code. |
| **Naming / shape** | A clearer name or a smaller surface, where it genuinely reduces cognitive load. |

## Workflow

1. **Scope.** `git diff` (+ `git diff --cached`) for uncommitted work, or `git diff
   <base>...HEAD` for a branch. Only touch code in that change unless explicitly asked to
   go wider.
2. **Read the neighborhood.** Before extracting or replacing, read the existing helpers
   and callers so a "simplification" doesn't reinvent or break a shared utility.
3. **Apply surgical edits.** Each edit must preserve behavior. Match the surrounding
   style. Prefer the smallest change that removes the clutter.
4. **Don't over-reach.** Don't abstract on first repetition (wait for the third). Don't
   restyle untouched lines. Don't "improve" adjacent code outside the change.
5. **Report.** List what you changed and why, one line each. If the code is already clean,
   say "nothing to simplify" — that's a valid result, not a failure.

## Rules

- **Behavior-preserving only.** If a change could alter output, timing, or errors, it
  belongs to `code-review`, not here. Leave it and note it.
- **Subtraction beats addition.** The best simplification usually deletes code.
- **Conform to the codebase.** Existing conventions win over personal taste.
- **No new dependencies or speculative features.** Minimum change that removes the mess.
