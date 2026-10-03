---
name: strategy-review
description: Spawn the architect agent in state+refine mode. Surfaces current render quality, project state, and asks one short open question about direction.
invocation: /strategy-review
---

# /strategy-review

Spawn the `architect` agent in **state+refine mode**.

Pass the agent:
- Mode: `state+refine`
- Instruction: pre-gather context silently (git log, closed PRs, render
  outputs, convergence plots). Surface state with visuals + one short
  open question. Update ROADMAP.md if direction changes. Open a doc PR.

## What the architect will do

1. Read git log + PRs since the last strategy review.
2. Read the latest showcase HTML and any convergence/parity PNGs in
   `test_results/` and `benchmarks/`.
3. Surface state in 3–5 lines + embedded renders.
4. Ask ONE short open question.
5. After the user responds, update ROADMAP.md if needed and open a PR.

## When to use

- Manually at any time for a direction check
- Automatically after `/close-round` every round (light pass)
- After every 3rd round (full pass with render comparison)
