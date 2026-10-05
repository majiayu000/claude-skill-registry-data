---
name: ai-model-route-evaluator
description: "Compare current AI models, providers, gateways, subscriptions, local routes, and free/paid endpoints for a concrete task. Evaluate exact model identity, modality, Turkish and multilingual quality, coding/reasoning, context, tool support, privacy, limits, price, latency, reliability, and benchmark fit; give task-specific winners and uncertainty. Turkish triggers: hangi model daha iyi, ChatGPT/Claude/OpenCode modeli seç, ücretsiz model, API karşılaştır, yerel mi bulut mu."
---

# AI Model Route Evaluator

Choose a route for the user's task, not a universal leaderboard winner. Model
catalogs, aliases, limits, prices, and product entitlements are time-sensitive;
verify them from current primary sources.

## Workflow

1. **Define the job.** Resolve the actual task, input/output modalities,
   languages, context size, tool/agent needs, latency tolerance, budget, data
   sensitivity, local hardware, and whether a free route is a hard constraint.
   Ask only for a missing fact that could change the winner.
2. **Resolve exact identities.** Record provider, product/plan or gateway, exact
   model ID/version/date, endpoint, region when relevant, and whether a name is
   a floating alias. Never treat a gateway alias as a stable model identity.
3. **Verify capability and access.** Use official catalogs, model cards, pricing,
   rate-limit/usage documentation, privacy/data-use terms, and product help.
   Separate API access from consumer subscription access.
4. **Select task-fit evidence.** Prefer current, version-pinned evaluations that
   match the required language, modality, agent/tool use, and difficulty. Do not
   infer Turkish or multimodal quality from an English text benchmark alone.
5. **Measure locally when practical.** Run the same representative prompt/input,
   record settings, retries, time, tokens/cost, success criteria, and failures.
   Do not compare outputs produced under materially different scaffolds as if
   only the model changed.
6. **Assess privacy and operational risk.** Never route API keys, private code,
   customer data, health/legal/financial records, or personal data through an
   untrusted or vaguely governed free endpoint. State retention/training facts
   only when verified for that exact product and plan.
7. **Score by scenario.** Give one winner per meaningful task class, a fallback,
   and explicit disqualifiers. Use weighted scores only after showing the raw
   facts; do not hide a hard requirement inside an average.
8. **Conclude conditionally.** State what to use now, for which task, under which
   plan/route, why, when to switch, and what remains uncertain.

Read [references/evaluation-scorecard.md](references/evaluation-scorecard.md)
for the comparison schema.

## Output contract

```markdown
## Decision
<task-specific winner, exact route, and one-line reason>

| Route | Exact model/version | Best for | Limits/cost | Privacy | Evidence confidence |
|---|---|---|---|---|---|

## By task
- <task>: <winner> — <reason and disqualifier>

## What to do
<setup or selection steps, fallback, and recheck trigger>

## Uncertainty
<floating aliases, missing Turkish/multimodal evidence, unmeasured latency, or plan ambiguity>
```

Avoid provider fandom, copied leaderboard rank, guaranteed quality, or a single
winner across unrelated tasks.
