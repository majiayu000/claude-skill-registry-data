---
name: jev-second-perspective
description: "Use TypeSafe's Jev as a fast, typed second opinion inside a research or optimization lane. Rank candidate levers by composite score, or check a write-up's claims against a lab log. Pair it with TypeSafe's own typesafe-ai skill, which owns the API and its docs."
---

# Schiedsrichterli (jev-second-perspective)

*Jev as a second-perspective judge*

Jev returns typed judgments (Choice, Score, Noul) with probabilities; it does not reason or generate text. Code owns
retrieval, arithmetic and policy; Jev supplies one narrow judgment per question. Read the typesafe-ai skill and the
live docs (https://docs.typesafe.ai/llms.txt) before changing request shapes.

## Client
`python3 scripts/jev.py REQUEST.json [OUT.json]` (POST /v1/systemone, model defaults to jev-latest) and
`python3 scripts/jev.py --models`. The key comes from $TYPESAFE_API_KEY or ~/.config/typesafe/api-key (mode 600);
never put it in a request file, artifact, skill or command line. Billing is per input token; output is free.

## Pattern 1: lever triage (composite scoring)
State = the task, the rules (gates, time guard, editable files, cost weights) and the candidates with their
ledgers. Per candidate ask two independent Scores (feasibility under the rules; share of the required gap) and one
Choice over all candidates for "the next hour of work". Multiply in code.
Treat it as a tie-breaker and a blind-spot detector: a candidate it rates plausible but unmeasured is the next
thing to measure, cheaply. Do not trust the rating itself.

## Pattern 2: citation check of a public draft
Code splits the draft into claim blocks (those with job ids or large numbers), retrieves the log entries that share
the most ids/numbers, and asks one Choice per (claim, entry): supports / contradicts / says_nothing. Only
confidence >= 0.8 stands on its own; route every "contradicts" to a human check. In practice most contradictions
came from retrieving a neighbouring job's entry; retrieve by the claim's own id first. It still caught an actual
overclaim ("twelve records" when the board's twelve include another participant's starting record).

## Limits
Jev judges only the state you give it; it cannot verify soundness, run code, or invent constructions. Never let a
Jev answer authorize a submission, a post, or spend: those stay with the measured gates and the user.
