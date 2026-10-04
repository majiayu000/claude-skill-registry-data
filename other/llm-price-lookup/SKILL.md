---
name: llm-price-lookup
description: look up and explain llm api pricing across models.dev, openrouter, and official provider pages. use when the user asks for model prices, input/output token costs, cached-token costs, openrouter aliases such as :free, provider-specific pricing, official versus third-party prices, or wants to verify an api call cost log.
---

# LLM Price Lookup

## Overview

Use this skill to look up, compare, and explain LLM pricing. Always bind a price to its source and provider; the same model family can have many prices depending on the serving provider.

## Core Workflow

1. **Identify the query.** Determine whether the user gave a broad model name such as `glm-5.1`, an exact provider/model id such as `z-ai/glm-5.1`, an OpenRouter id such as `z-ai/glm-4.5-air:free`, or a provider intent such as "Z.AI official".
2. **Query Models.dev for broad coverage.** Prefer the bundled script:
   ```bash
   python scripts/lookup_price.py "<query>"
   ```
   Use its `models_dev` rows to preserve `provider`, `provider_id`, `model_key`, `model_id`, costs, and limits.
3. **Query OpenRouter exactly when relevant.** If the id looks like an OpenRouter id or includes suffixes such as `:free`, `:online`, `:beta`, `:extended`, or `:thinking`, check OpenRouter exact ids before fuzzy matches. Never strip suffixes unless explicitly comparing variants.
4. **Check official provider pages when the user asks for official prices or when aggregator data conflicts.** Treat official pricing pages as source of truth for billing, especially for OpenAI, Anthropic, Google, Z.AI, DeepSeek, Mistral, xAI, and other first-party APIs.
5. **Explain ambiguity.** Missing Models.dev data does not mean a model is free or unavailable. A third-party provider price is not the same thing as the model vendor's official direct-API price.

## Source Priority

Use this order for conclusions:

1. Official provider pricing page or official billing docs.
2. Exact OpenRouter `/api/v1/models` match for OpenRouter ids and aliases.
3. Models.dev provider-specific entry with provider context preserved.
4. LiteLLM or other community price registries as secondary corroboration.

If sources disagree, state the discrepancy and say which source you are using for the final conclusion.

## Required Output Fields

For price lookups, include at least:

- model or query
- source
- provider and provider_id
- model_id or model_key
- input cost per 1M tokens
- output cost per 1M tokens
- cache read and cache write cost per 1M tokens when available
- context window and output limit when available
- notes about free aliases, previews, batch discounts, cache behavior, or tool pricing when relevant

Preferred table:

| source | provider | provider_id | model_id | input $/1M | cache read $/1M | cache write $/1M | output $/1M | context |
|---|---|---|---|---:|---:|---:|---:|---:|

## Important Rules

- Do not answer from a raw recursive `.id` search alone. Recursive search loses the parent provider, which is essential for pricing.
- Do not conflate model vendor and serving provider. For example, GLM-5.1 can appear under Z.AI, Hugging Face, DeepInfra, OpenRouter, 302.AI, and other providers with different prices.
- For OpenRouter aliases, match the full id first. `z-ai/glm-4.5-air:free` and `z-ai/glm-4.5-air` can have different prices.
- Do not default unknown prices to zero. Only say zero when the matched source explicitly lists zero.
- For official prices, prefer rows whose provider_id is the official provider, or verify against the official pricing page. For Z.AI/智谱, look for provider ids such as `zai` or `z-ai` and verify official docs when available.
- For cost logs, recompute using the exact model id, input tokens, output tokens, cache read tokens, and cache write tokens. Mention any fields not priced by the selected source.

## Bundled Resources

- `scripts/lookup_price.py`: deterministic lookup against Models.dev and OpenRouter, preserving provider context.
- `references/source-priority.md`: guidance for interpreting official, aggregator, and routing-platform prices.
- `references/jq-recipes.md`: jq commands for manual inspection of Models.dev without losing provider context.
