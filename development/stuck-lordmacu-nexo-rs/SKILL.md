---
name: Stuck
description: Bounded auto-debug loop for failing build/test commands with evidence-first diagnosis.
requires:
  bins: []
  env: []
---

# Stuck

Run a bounded diagnostic loop when a build or test is failing repeatedly.
This skill is for "reproduce -> inspect -> isolate -> propose fix", not for
open-ended retries.

## Use when

- User reports a failing `cargo build` or `cargo test`.
- The failure can be reproduced from a concrete command or recent log.
- You need structured diagnosis before applying code changes.

## Do not use when

- There is no runnable command and no usable failure output.
- The issue is infrastructure-only (network outage, registry down, host disk full)
  and not actionable from the repo.
- The task is a one-off explanation without debugging.

## Input contract

- `failing_command` (required): command to reproduce the failure.
- `max_rounds` (optional): default `3`, clamp to `[1, 5]`.
- `focus_pattern` (optional): regex/error token to prioritize while scanning output.
- `failure_context` (optional): pasted stderr/stdout snippet for first-pass triage.

## Parsing rules (priority order)

1. If structured args are provided, use them directly.
2. Else infer from user text:
   - first explicit command-like phrase -> `failing_command`
   - "2 rounds", "max 4 attempts", "repeat 3x" -> `max_rounds`
   - "focus on E0425", "grep unresolved import" -> `focus_pattern`
3. Defaults:
   - `max_rounds = 3`
4. If `failing_command` is still missing, ask for one concrete reproducible command.

## Canonical workflow

1. **Reproduce baseline**
   - Run `failing_command` as-is.
   - Capture exit code + shortest error excerpt that identifies the failure.
2. **Increase observability**
   - Build-style command: add verbosity (`-vv`) when safe.
   - Test-style command: add `-- --nocapture` when safe.
3. **Isolate blast radius**
   - Prefer targeted reruns (`-p <crate>`, single test path, or narrowed filter)
     once the failing unit is known.
4. **Classify likely root cause**
   - compile/type/import mismatch
   - feature-flag/config mismatch
   - flaky test/runtime ordering
   - environment/toolchain mismatch
5. **Propose one fix candidate per round**
   - Keep the fix minimal and directly tied to captured evidence.
6. **Verify**
   - Re-run the narrow check first, then the original `failing_command`.
7. Stop when:
   - failure is fixed (`status=fixed`), or
   - root cause is clear but fix needs user decision (`status=diagnosed`), or
   - rounds exhausted (`status=max_rounds_reached`).

## Guardrails

- Never run unbounded loops.
- Never execute destructive commands (`git reset --hard`, `rm -rf`, force-push).
- Do not broaden task scope while debugging; stay on the current failure.
- Keep evidence concise (error-focused snippets, not full logs).
- If command hangs, use bounded execution and report timeout explicitly.

## Output format

Always return:

- `status`: `fixed` | `diagnosed` | `max_rounds_reached` | `needs_user_input`
- `rounds_run`: number of rounds executed
- `failing_command`: normalized command used for reproduction
- `focus_pattern`: normalized pattern or `none`
- `root_cause_hypothesis`: strongest current diagnosis
- `evidence`: per-round bullets (command, exit code, key error line)
- `fix_candidate`: concrete minimal patch idea (or applied change summary)
- `verification`: narrow check result + full command result
- `next_action`: required unless `status=fixed`

## Examples

- `failing_command="cargo build -p nexo-core" max_rounds=3 focus_pattern="E0[0-9]{3}"`
- `failing_command="cargo test -p nexo-core agent::skills::tests" max_rounds=4`
- `failing_command="cargo test" failure_context="thread 'x' panicked at ..."`
