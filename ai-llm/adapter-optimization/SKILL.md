---
name: adapter-optimization
description: "Act as the LLM variant proposer inside the Step-12 optimize-adapter loop: given the current adapter and the behaviour tests it is failing, propose edited adapter variants that should score higher, for the deterministic driver to score and gate. Use only within optimize_adapter.py's propose step — the driver owns all scoring, gating, and keep-winner selection."
---

# Skill: adapter-optimization

**Purpose:** Be the LLM **variant proposer** inside the Step-12 optimize-adapter loop — given the
current adapter and the behaviour-tests it is failing, propose edited adapter variants that should
score higher, for the deterministic driver to score and gate. This is the *propose* step only; the
driver (`tools/subagent_factory/optimize_adapter.py`) does all scoring, gating, and keep-winner
selection. See `docs/enhancement-steps/step-12-optimize-adapter.md`.

---

## Where this runs

After build (Steps 1–9) and after a Step-11 behaviour-test suite exists. The driver calls you once
per round with the current best adapter + its failing tests; you return candidate adapter texts. The
driver screens (minibatch), confirms (full suite), and merges a candidate **iff** it flips ≥1
fail→pass with **zero** pass→fail (assess-before-merge) **and** passes the hard pre-merge gate
(faithfulness + quote + adapter-policy). You never decide what merges.

---

## Input (per round)

- `best_adapter` — the current best adapter text (the system prompt under optimization).
- `failing` — list of `{test, grade}`: the behaviour-tests scoring below the pass bar, each with its
  test record (prompt, `expected_route`, `minimum_output`, `must_ask_for`, `must_not_do`) and the
  grader's component breakdown (`route` / `minimum` / `ask` / `mustnot`) and, when an LLM grader is
  used, the `reason` (why it failed — the cheapest quality lever, finding #4).
- `round_index`.

## What to edit (and what NOT to)

- **Edit:** the adapter's *induced-guidance* rules and *worked examples* (jointly — MIPRO blueprint,
  finding #7). Tighten a vague rule, add a worked example that demonstrates the failing behaviour,
  sharpen routing language so out-of-scope prompts are declined.
- **Never edit:** the `## Operating invariants (must hold)` layer (A3/A5 — frozen), the front-matter
  tool grants, or anything that would widen authority.
- **Never** invent a claim the source does not support to make a test pass. A variant that out-claims
  its evidence is rejected by the pre-merge faithfulness gate no matter its score — wasted budget.

## Steps

1. Read each failing test's `reason` / component breakdown. Group failures by cause (wrong route,
   thin coverage of `minimum_output`, didn't ask for missing context, did a `must_not_do`).
2. Propose **N small, diverse, human-readable variants** (default N≈3), each a *full adapter text*
   with a targeted edit. Diversity beats greedy at equal budget (finding #6) — vary the fix, don't
   submit three near-identical edits.
3. Keep each variant minimal: change what the failures point to, leave passing behaviour untouched
   (a broad rewrite risks a pass→fail regression that the gate will reject).
4. Return the variants. Do **not** self-score — the driver scores them. If a later round shows a
   variant regressed, the scored history tells you; propose a different direction.

## Output

A list of candidate adapter texts (strings). Nothing else.

## Guardrails (the driver enforces; respect them so budget isn't wasted)

- Behaviour-tests are the merge gate; the LLM grader is only critique + relative ranking, never the
  reward (finding #2).
- Faithfulness / quote / adapter-policy is a hard pre-merge gate (anti-reward-hacking).
- Human-readable edits only — no gibberish/white-box token tricks (finding #10).
