---
name: Loop
description: Bounded auto-iteration for a prompt with explicit stop predicates.
requires:
  bins: []
  env: []
---

# Loop

Run a prompt repeatedly with hard bounds and explicit stop criteria. This is
for finite "try-fix-verify" loops, not background scheduling.

## Use when

- User asks to "retry until it passes", "iterate N times", "keep refining
  until X".
- Task has a measurable stopping condition (exit code, regex match, or clear
  quality criterion).
- A bounded deterministic loop is safer than open-ended autonomous retries.

## Do not use when

- User wants periodic or cron-like recurring tasks.
- Stop condition is ambiguous and cannot be expressed explicitly.
- Task is one-shot and does not benefit from iterative refinement.

## Input contract

- `prompt` (required): instruction/command to run each attempt.
- `max_iters` (optional): default `3`, clamp to `[1, 10]`.
- `until_predicate` (optional): one of:
  - `regex:<pattern>`
  - `exit:<code>`
  - `judge:<criterion>`
  - default when omitted: `judge:task completed`

## Parsing rules (priority order)

1. If user provides explicit structured args, use them directly.
2. Else infer from natural language:
   - `max_iters`: phrases like "3 attempts", "max 5", "try 4 times".
   - `until_predicate`:
     - contains "until exit 0" or "until tests pass" -> `exit:0`
     - contains "until matches ..." -> `regex:<...>`
     - otherwise -> `judge:<user criterion>`
3. If still missing:
   - `max_iters = 3`
   - `until_predicate = judge:task completed`

If `prompt` is empty after parsing, stop and ask for a concrete prompt.

## Canonical workflow

1. Normalize and validate inputs.
2. Initialize an iteration ledger.
3. For `i = 1..max_iters`:
   - Execute `prompt`.
   - Capture evidence:
     - short result summary
     - key output snippet
     - exit code when available
   - Evaluate predicate against current evidence.
   - If predicate satisfied: stop with `status=success`.
   - Else derive a focused refinement for the next attempt.
4. If `max_iters` reached without success:
   - stop with `status=max_iters_reached`
   - return best-attempt summary + concrete next action.

## Guardrails

- Never run unbounded loops.
- Never recurse into `loop` from inside `loop`.
- Keep per-iteration evidence concise to avoid context bloat.
- Do not silently broaden scope between iterations; only refine.
- If a step is destructive/high-risk, require explicit user confirmation
  before the next attempt.

## Output format

Always return:

- `status`: `success` or `max_iters_reached`
- `iterations_run`: attempts executed
- `max_iters`: normalized cap actually used
- `predicate`: normalized predicate
- `final_result`: concise outcome
- `evidence`: per-iteration bullets (delta-focused)
- `next_action`: required when `status=max_iters_reached`

## Examples

- `prompt="cargo test -p core" max_iters=5 until_predicate="exit:0"`
- `prompt="reduce p95 latency by tuning query" max_iters=4 until_predicate="regex:p95 < 200ms"`
- `prompt="rewrite explanation for clarity" max_iters=3 until_predicate="judge:clear, concise, no ambiguity"`
