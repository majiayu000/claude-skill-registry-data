---
name: Verify
description: Bounded acceptance verification that runs concrete checks and an explicit LLM judge over evidence.
requires:
  bins: []
  env: []
---

# Verify

Verify that a change actually satisfies an acceptance criterion using runnable
checks plus an explicit judgment over outputs. This is for "prove it works",
not for implementing new features.

## Use when

- User asks to validate a change against acceptance criteria.
- You need evidence from test/lint/type-check/build outputs.
- A plain "looks good" answer is insufficient without execution proof.

## Do not use when

- No acceptance criterion is provided and cannot be inferred.
- The task is to implement/fix code (use implementation/debug skills first).
- Required checks cannot run in the current environment and no fallback exists.

## Input contract

- `acceptance_criterion` (required): plain-English success condition.
- `candidate_commands` (optional): preferred checks in priority order.
- `max_rounds` (optional): default `2`, clamp to `[1, 4]`.
- `judge_mode` (optional): `strict` (default) or `balanced`.
- `fail_fast` (optional): default `true` (stop on decisive failure).

## Parsing rules (priority order)

1. If structured args exist, use them directly.
2. Else infer from user text:
   - requirement sentence -> `acceptance_criterion`
   - explicit commands -> `candidate_commands`
   - "run twice/max 3 rounds" -> `max_rounds`
3. Command selection fallback:
   - explicit commands first
   - then acceptance-based inference (`test`, `lint`, `type-check`, `build`)
   - then repo defaults (Phase 75-style autodetect: e.g., `cargo test`, `cargo check`)
4. If `acceptance_criterion` is still missing, ask for one concrete criterion.

## Canonical workflow

1. **Normalize criterion**
   - Rewrite criterion into objective pass/fail checkpoints.
2. **Build verification plan**
   - Select minimal command set that can falsify the criterion quickly.
3. **Execute bounded rounds (`1..max_rounds`)**
   - Run commands in priority order.
   - Capture per-command: exit code, key output lines, duration.
   - If `fail_fast=true` and decisive failure appears, stop early.
4. **LLM judge over evidence**
   - Evaluate whether collected evidence satisfies each checkpoint.
   - Mark unknowns explicitly instead of guessing.
5. Stop when:
   - criterion satisfied with evidence (`status=pass`), or
   - criterion disproven (`status=fail`), or
   - environment blocks decisive evaluation (`status=inconclusive`), or
   - missing criterion/context (`status=needs_user_input`).

## Guardrails

- Never claim success without command-backed evidence.
- Never run destructive or scope-expanding commands during verification.
- Keep logs concise: only relevant lines proving pass/fail.
- Separate "command passed" from "criterion satisfied" (they are not identical).
- If checks are flaky, report flakiness explicitly and avoid false certainty.

## Output format

Always return:

- `status`: `pass` | `fail` | `inconclusive` | `needs_user_input`
- `rounds_run`: rounds executed
- `acceptance_criterion`: normalized criterion used
- `commands_run`: ordered list with exit codes
- `evidence`: criterion checkpoints mapped to concrete outputs
- `judge_decision`: explicit rationale for pass/fail/inconclusive
- `gaps`: what could not be proven
- `next_action`: required unless `status=pass`

## Examples

- `acceptance_criterion="all core tests pass and no clippy warnings" candidate_commands=["cargo test -p nexo-core","cargo clippy -p nexo-core -- -D warnings"]`
- `acceptance_criterion="feature builds and type-checks"` (autodetect may pick `cargo check`/`cargo test`)
- `acceptance_criterion="endpoint returns 200 and response includes health=ok" candidate_commands=["cargo test -p api health_check"]`
