---
name: scriptify
description: >-
  Use when you (Claude) are about to perform — or notice you've already been
  performing — deterministic, reusable computation by emitting tokens: writing a
  one-off script, re-deriving the same math/graph/parsing/transform logic across
  turns or sessions, or hand-running a fixed multi-step deterministic chain.
  Captures that logic into a committed, tested script in a central location and
  switches you to invoking it instead of regenerating it. Trigger it proactively
  whenever you catch yourself rewriting similar throwaway scripts (e.g. several
  /tmp/*.py variants of one thing), doing nontrivial deterministic computation
  inline that will plausibly recur, or doing by hand what a script could do once
  — even if the user never says "make a script." This is the codemode ethos
  (wrap a deterministic chain, invoke it) applied beyond MCP calls.
---

# Scriptify

You are about to spend tokens *generating* logic that a computer should execute.
Stop and externalize it. Regenerating deterministic logic token-by-token is slow,
non-reproducible, and silently decays between sessions — the same engine rewritten
three times is three chances to introduce a subtle drift. Write it once, test it,
and invoke it.

## When this applies

The smell is **re-derivation of reusable, deterministic logic**:

- You've written a variant of this script before (the canonical tell: several
  `/tmp/foo.py`, `/tmp/foo2.py`, `/tmp/foo3.py` where only the input data changed).
- You're doing nontrivial deterministic computation inline — parsing, graph/critical-path
  math, schedule/cost rollups, format conversion, bulk record shaping — that will
  plausibly run again.
- You're hand-executing a fixed sequence of steps that has no judgment in it.

## When it does NOT apply

Don't bureaucratize one-shots. Skip this for a trivial calculation, genuinely
single-use logic, quick exploration you'll throw away, or anything whose core is
*judgment* rather than mechanism. The goal is to externalize the deterministic
engine, not to ban thinking. If you're unsure whether it'll recur, it's fine to
do it inline once and scriptify on the second occurrence.

## Procedure

### 1. Separate engine from data

Name the **deterministic engine** (the part that's identical no matter the
inputs) and the **project-specific data/config** (estimates, graphs, file paths,
thresholds). Only the engine becomes the script. The data stays as inputs *you*
supply each time — via argv or JSON on stdin. If you can't cleanly separate them,
the logic probably isn't reusable yet; reconsider whether to scriptify at all.

### 2. Choose its home

| The logic is…                                          | Put it in                                                                 |
| ------------------------------------------------------ | ------------------------------------------------------------------------- |
| General-purpose, useful across repos                   | `~/.claude/codemode/scripts/<name>.py` — run via `codemode_run_script`    |
| Owned by a specific skill                              | that skill's `bin/` or `scripts/` directory                               |
| Specific to one repo                                   | that repo's conventional scripts dir (match what's already there)         |

Never leave it as `/tmp` scratch you'll re-derive. If in doubt, default to
`~/.claude/codemode/scripts/` — it's global and aggregates across every repo.

### 3. Write the script

- **Stdlib-first.** Prefer zero third-party deps so it runs anywhere. Reach for a
  dependency only if it genuinely earns it.
- **Clear input/output contract.** A pure-function core, wrapped by a thin CLI:
  read inputs from argv or JSON on stdin, write results (human-readable, plus
  `--json` for machine use when relevant) to stdout. Make the contract obvious
  in a short module docstring — inputs, outputs, one example invocation.
- **Right language for the job.** Graph/math/data work → Python. Don't force a
  scheduler into bash just because the home is called `bin/`.

### 4. Verify it runs

Write a minimal self-check — assert the engine against one known input/output —
and actually run it. A script you didn't execute is unverified; say so rather than
claiming it works. Keep the test next to the script (`<name>.test.*` or a
`if __name__ == "__main__"` smoke block) so future-you can re-verify cheaply.

### 5. Report the invocation, and stop regenerating

Tell the user the exact command to run it and where it lives. From now on,
*invoke* it — assemble the inputs, run it, interpret the output. Do not
re-implement the engine inline again. If it's a proven, frequently-reused chain
that fits codemode, offer to promote it to a callable tool with
`register_tool` so it's reachable without remembering the path.

## Example

The triggering case for this skill: three `/tmp/sched*.py` rewrites of one
critical-path scheduler.

- **Engine (→ script):** expand epics into dependency-layered tasks; list-schedule
  them across N workers by critical-path priority; return makespan + per-epic
  windows; a duration model.
- **Data (→ inputs):** the epic/ticket graph, per-ticket time estimates, review
  overhead constants, the scope sets. These differ every run and belong in a
  config the caller supplies.

Result: one `schedule.py` taking a JSON config + worker counts, with a smoke test
— invoked with new data instead of rewritten from scratch each session.

See `examples/` for three worked outputs of this skill — `schedule.py` (the
critical-path scheduler), `mrr_calc.py` (a recurring CSV proration transform),
and `ci_suite_rollup.py` (a log parse + rollup). Each is stdlib-only, reads its
data as input, and ships a built-in smoke test — the shape to aim for.
