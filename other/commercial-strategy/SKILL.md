---
name: commercial-strategy
description: Defines the message, hook, structure, call to action and claims for an ad. Use when writing the treatment and script and checking platform fit.
version: 0.1.0
owner: Digikon
---

# commercial-strategy

## Inputs
Brief, audience, platform, approved brand facts (the most relevant ones when the fact sheet is large) and ad playbooks (retrieved).

## Procedure
1. State one objective and one audience. If the brief has several, ask which comes first.
2. Choose a structure suited to the product (see references/structures.md) and say why.
3. Write the hook so the first scene shows something concrete. Do not open on a logo.
4. Write the beats with approximate seconds that add up to the target duration.
5. Write **one** call to action in plain words.
6. Build the claims register (references/claims-register.md): every factual statement gets a claim_id and either a brand_fact_id from the facts you were given, or null (unsupported).

## Never
- Put an unsupported claim in a beat, a caption or the call to action.
- Invent prices, ingredients, awards, results, health effects or statistics.
- Copy a competitor's slogan or a known campaign line.

## Output
A treatment: logline, hook, tone, beats, cta, claims, conflicts_log.

## Failure conditions
No approved facts available for a claim the brief demands: mark it unsupported and tell the user which fact is needed.

## Evals
See evals/cases.md.
