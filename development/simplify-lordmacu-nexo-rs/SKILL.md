---
name: Simplify
description: Bounded simplification pass for a file or hunk that preserves behavior while reducing complexity.
requires:
  bins: []
  env: []
---

# Simplify

Simplify code in a bounded, evidence-driven way: smaller, clearer, and easier
to maintain while preserving behavior unless the user explicitly asks otherwise.

## Use when

- User asks for refactor/cleanup without adding new features.
- A file or hunk looks noisy (duplication, dead code, redundant guards).
- You need clearer names and tighter structure with minimal risk.

## Do not use when

- User is requesting new behavior or a product-level redesign.
- You do not have a concrete target file/hunk.
- The change would require broad API/contract breakage without approval.

## Input contract

- `target` (required): file path or hunk identifier to simplify.
- `scope` (optional): `file` or `hunk` (default `file`).
- `max_passes` (optional): default `2`, clamp to `[1, 4]`.
- `preserve_behavior` (optional): default `true`.
- `focus` (optional): subset of
  `reuse`, `dead_code`, `redundant_guards`, `naming`, `duplication`, `efficiency`.

## Parsing rules (priority order)

1. If structured args are provided, use them directly.
2. Else infer from user language:
   - "this file", explicit path, or pasted diff -> `target`
   - "just this block/hunk" -> `scope=hunk`
   - "two passes/max 3 rounds" -> `max_passes`
   - "don't change behavior" -> `preserve_behavior=true`
   - keywords like "remove dead code", "rename", "dedupe" -> `focus`
3. Defaults:
   - `scope=file`, `max_passes=2`, `preserve_behavior=true`
4. If `target` is still missing, ask for one concrete file or hunk.

## Canonical workflow

1. **Understand baseline**
   - Read the target and identify purpose, invariants, and public interfaces.
2. **Run bounded simplify passes (`1..max_passes`)**
   - Apply only high-signal improvements:
     - remove dead code / unreachable branches
     - collapse redundant guards and repeated conditionals
     - deduplicate copy-paste logic into local helpers where appropriate
     - improve naming for intent clarity
     - replace ad-hoc logic with existing utilities when available
3. **Behavior safety check**
   - If `preserve_behavior=true`, avoid interface/semantic changes.
   - If a behavior change seems necessary, stop and ask for confirmation.
4. **Verification**
   - Run targeted checks (lint/test/build scope relevant to changed files).
5. Stop when:
   - no further meaningful simplification remains (`status=already_simple`), or
   - simplification applied safely (`status=simplified`), or
   - blocked by missing context/approval (`status=needs_user_input`), or
   - pass budget reached (`status=max_passes_reached`).

## Guardrails

- Never run unbounded refactor loops.
- Do not introduce speculative abstractions with no local payoff.
- Do not touch unrelated files "while here".
- Prefer small, reviewable edits over sweeping rewrites.
- Keep comments only for non-obvious WHY; remove narrative noise.

## Output format

Always return:

- `status`: `simplified` | `already_simple` | `needs_user_input` | `max_passes_reached`
- `passes_run`: number of simplify passes executed
- `target`: normalized file/hunk target
- `focus_used`: normalized focus dimensions
- `changes`: concise bullet list of concrete simplifications
- `behavior_safety`: why behavior is preserved (or what approval is needed)
- `verification`: checks run + outcomes
- `next_action`: required unless `status=simplified` or `already_simple`

## Examples

- `target="crates/core/src/agent/mod.rs" max_passes=2 focus="dead_code,redundant_guards"`
- `target="src/main.rs#L120" scope="hunk" preserve_behavior=true`
- `target="diff:latest" focus="reuse,duplication,naming" max_passes=3`
