---
name: validate
description: Run a full validation pass on an idea — sharpening, devil's advocate, market sizing, competitor mapping, customer discovery plan.
---

# /validate

An opt-in rail, not a gate. Use `/validate` when a bet is expensive, slow, or hard to undo — paid acquisition, a big build, a pivot. For cheap, reversible ideas, just build; the ship is the validation.

Usage: `/validate <idea or product name>`

## What this does
Runs the Idea-stage agents in sequence (or parallel where independent):
1. **`problem-sharpener`** — turn the idea into a testable hypothesis
2. **`devils-advocate`** — build the strongest case against
3. **`market-researcher`** — TAM/SAM/SOM + trends
4. **`competitor-mapper`** — landscape by tier
5. **`customer-discovery`** — interview plan + outreach templates

Outputs go to `products/<slug>/` (creating the folder if new).

## What you do as the assistant when this is invoked
1. Resolve `<idea>` to a product slug (existing or new).
2. If new product: create `products/<slug>/` with minimal structure, log in `decisions/0001-validation-start.md`.
3. Run the 5 agents — **fleet mode when subagent spawning is available** (see `factory/playbooks/mvp-stage/fleet-patterns.md`):
   - **Fan out blind:** problem-sharpener, devils-advocate, market-researcher, competitor-mapper as 4 concurrent subagents, each getting the raw idea + its own SKILL.md only — none sees another's output (independent verdicts are the point; devils-advocate attacks the raw idea, which is the harder, more honest target). Spawn each on its `model_tier`.
   - **Verify adversarially:** before synthesis, spawn one refuter against the kill case ("is this actually fatal, or survivable?") and one against the strongest FOR evidence ("is this signal or founder hope?").
   - **Synthesize:** customer-discovery runs on the (surviving) sharpened hypothesis; then produce the snapshot, reporting where the blind agents *agreed* (high confidence) and *disagreed* (the open questions — never averaged away).
   - **Serial fallback (no spawning):** run in sequence as before — 1, then 2 on 1's output, 3+4, then 5 on 1+2. Same deliverables either way.
4. After all done: produce a 1-page "validation snapshot" summarizing GO / PAUSE / KILL with reasoning — including the agreement/disagreement map when fleet mode ran.

## Output location
- `products/<slug>/validation/snapshot.md` — the summary
- `products/<slug>/validation/hypothesis.md` — sharpened problem
- `products/<slug>/validation/devils-advocate.md` — kill case
- `products/<slug>/validation/market.md` — sizing + trends
- `products/<slug>/validation/competitors.md` — landscape
- `products/<slug>/interviews/discovery-plan.md` — the plan

## When NOT to invoke
- If the idea hasn't been articulated in writing yet — ask user to write 2 sentences first.
- If user just wants a quick gut check — that's `idea-generator` or `devils-advocate` directly, not full validation.
