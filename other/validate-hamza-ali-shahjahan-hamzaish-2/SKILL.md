---
name: validate
description: Run a full validation pass on an idea — sharpening, devil's advocate, market sizing, competitor mapping, customer discovery plan.
---

# /validate

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
3. Run the 5 agents. Steps 1, 3, 4 can run in parallel (read-only). Step 2 (devil's advocate) takes the output of step 1. Step 5 takes outputs of 1+2.
4. After all done: produce a 1-page "validation snapshot" summarizing GO / PAUSE / KILL with reasoning.

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
