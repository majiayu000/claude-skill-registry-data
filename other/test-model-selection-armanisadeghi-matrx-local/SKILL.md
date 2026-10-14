---
name: test-model-selection
type: Skill
title: "test-model-selection — which model a coding agent tests with"
description: "Picks the model a coding agent uses when a test or browser check sends an AI call. Use when choosing a model for any test, UI check, bench, or agent run, or when a test names Opus, Sonnet, Fable, Astra, or any model by habit."
tags: [testing, models, spend, agents]
timestamp: 2026-10-10T00:00:00Z
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/test-model-selection/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# test-model-selection — which model a coding agent tests with

Arman, 2026-10-10: "The point is to know what is being tested and adjust accordingly." Never pick a
test model from memory. Ask what the test is for, then ask the catalog.

## 1. What are you testing?

| The test is about | Purpose | Gets you |
|---|---|---|
| Plumbing: UI, persistence, wiring, tools, streaming. The answer's content does not matter. | `plumbing` | The cheapest unrestricted priced chat model that supports tool calls. Cheaper than Haiku. |
| Something that depends on the provider: its API, its streaming shape, its errors. | `provider` + name | The cheapest unrestricted model of THAT provider (Haiku for Anthropic). |
| The actual intelligence: answer quality, reasoning, an eval. | `intelligence` | The recommended default (Sonnet 5.5 today) plus the list of restricted models. |

## 2. Ask (one call)

```
agent_catalog action=test_model purpose=plumbing
agent_catalog action=test_model purpose=provider provider=Anthropic
agent_catalog action=test_model purpose=intelligence
```

No MCP? From `aidream/`: `uv run python scripts/test_model.py plumbing`, or `provider Anthropic`,
or `intelligence`. Both return the model id, name, price per 1M tokens in and out, and why. Use that
model name as given.

## 3. Never a restricted model

Max-tier, Fable, Astra, Mythos, and anything at or above the cost rating the answer reports
(`restricted_min_cost_rating`, 6 today) are off limits for testing. An `intelligence` answer lists
them in `restricted_models`. The top-tier gate refuses them for anyone not approved, and a test
account that asks for one raises a spend alarm to the super admins (one per account per day). The
guard warns; it does not block, so the refusal is not your signal. This skill is.

## 4. Keep the test small

Fresh short context, as few calls as prove the point, and no premium pipeline re-run to check a code
fix that does not depend on the model's reasoning. Rules:
[ai-model-and-spend-rules §5](/policies/ai-model-and-spend-rules.md).

## 5. Where the answer comes from

One function, `ai.test_model_choice(purpose, provider)`, computed from the live catalog (active,
priced offerings only). Knobs under `ai.test_models` override it: `plumbing_model`,
`provider_models`, `intelligence_model`, `restricted_min_cost_rating`, `restricted_name_pattern`.
Reviewed monthly; the catalog changes, so never hard-code the answer in a test.
