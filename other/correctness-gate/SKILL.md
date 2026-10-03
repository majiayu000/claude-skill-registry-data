---
name: correctness-gate
description: How to run and interpret this repo's correctness gate (format/lint/typecheck/build/test) before calling any change done. Use whenever finishing a coding task, before reporting success, or when deciding whether a change is ready to checkpoint/commit.
---

# Correctness gate

`scripts/run-checks.sh` is this repo's single source of truth for "is this change
correct." It reads `.claude/stack-cache.json` (regenerating it via
`scripts/detect-stack.sh` if missing) and runs, in order: format-check, lint,
typecheck, build, test — skipping any step the detected stack doesn't define.

The same script runs in CI (`.github/workflows/ci.yml`), the `Stop` hook runs it
before checkpointing, and a `PostToolUse` hook formats individual files as you go.
There should never be a separate "what CI checks" vs "what Claude checks" — if you
find yourself writing a check that only runs in one place, put it in this script
instead.

## When to run it

- Whenever you believe a task is complete, before saying so.
- Before triggering (or letting the `Stop` hook trigger) a checkpoint commit.
- After merging/rebasing, since the working tree changed underneath you.

## How to handle failures

- **Caused by your change:** fix it. Don't report done with a known-failing gate.
- **Pre-existing / unrelated to your change:** say so explicitly, name the failing
  step, and don't claim success. Don't silently skip the gate to avoid an
  inconvenient truth.
- **Flaky test:** re-run once to confirm flakiness before concluding that; if
  confirmed flaky, say so and don't treat it as a blocker, but don't quietly assume
  flakiness on the first failure either.

## Beyond the automated gate

The scripted gate catches mechanical issues. It does not replace judgment on logic
errors, security issues, or over-engineering — for anything non-trivial, pair it
with the review swarm (see `.claude/skills/swarm/SKILL.md`, pattern 2) or
`/code-review` / `/code-review ultra` before calling a change ready to ship.
