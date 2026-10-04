---
name: acp-feed
description: >
  Exports merchant catalog data to an OpenAI Agentic Commerce Protocol
  product feed shape. Use when preparing products for ChatGPT Commerce,
  Instant Checkout readiness, or OpenAI ACP feed/API onboarding after
  catalog data has been mapped from Shopify, CSV, JSON, or UCP catalog JSON.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# OpenAI ACP Feed Export

Prepare a structured product feed for OpenAI Agentic Commerce Protocol (ACP).
ACP onboarding starts with product feeds for approved partners; keep this skill
focused on feed quality and schema-shaped output, not payment or order capture.

## Inputs

- Preferred input: `store/clients/{client_name}/catalog.json` from `ucp-catalog`
- Alternate input: any JSON object with a top-level `products` array
- Optional merchant context: `target_country`, seller name, seller URL

## Workflow

1. Read the catalog JSON and confirm it has product records.
2. Export ACP feed JSON:

```bash
python ${CLAUDE_SKILL_DIR}/scripts/export_acp_feed.py \
  --input store/clients/{client}/catalog.json \
  --output store/clients/{client}/acp-feed.json \
  --target-country US
```

3. Validate that every exported product has:
   - stable product `id`
   - at least one variant
   - every variant has stable `id` and `title`
   - prices, when present, are integers in ISO 4217 minor units
   - URLs are absolute and encoded enough for ingestion

4. Report any omitted optional fields instead of inventing values.

## Output

Save to the client folder:

- `acp-feed.json` - request-shaped feed payload with `target_country` and `products`
- `acp-feed-report.md` - field coverage, warnings, and next steps

## Reference

Read `references/openai-acp.md` when you need protocol boundaries, official
source links, or field mapping notes.

## Hard Rules

- Do not claim a merchant is approved for ChatGPT Commerce unless the user
  provides that approval status.
- Do not include API keys, payment tokens, or customer data in feed output.
- Keep product copy factual and concise.
- If a field is brittle or unavailable, omit it and record the omission.
