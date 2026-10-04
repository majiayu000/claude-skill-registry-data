---
name: agentic-payment-signal
description: Retrieve Stablehunter AI Agentic Payment Daily Signal and route it into an agent workflow.
---

# Agentic Payment Signal Skill

Use this skill when a user asks to retrieve, summarize, or route the latest Stablehunter AI Agentic Payment Daily Signal.

## What This Skill Does

- Fetches the latest available Agentic Payment Daily Signal.
- Normalizes the result into a short workflow brief.
- Preserves the Stablehunter AI canonical URL and original source links.
- Routes the brief into a user-specified agent workflow, bot, workspace, or report.

Do not use this skill for generic crypto market news, price alerts, trading advice, airdrop tracking, or unsupported investment claims.

## Public Data Surface

Primary page:

```text
https://stablehunter.ai/agentic-payment-signal.html#daily-signals
```

Daily Signal API pattern:

```text
GET https://cms.stablehunter.com/api/daily-digests/{digestDate}?category=information_signal&locale={locale}
```

Example:

```text
GET https://cms.stablehunter.com/api/daily-digests/2026-05-11?category=information_signal&locale=en
```

Locale values:

```text
en | zh-Hans
```

Authentication:

```text
None required for v1.
```

If today's digest is unavailable, use the latest available date shown on the Agentic Payment Signal page. State the digest date clearly.

## Output Schema

Normalize the response before routing it downstream:

```json
{
  "signal_name": "Agentic Payment Signal",
  "digest_date": "YYYY-MM-DD",
  "title": "string",
  "item_count": 0,
  "items": [
    {
      "title": "string",
      "summary": "string",
      "why_it_matters": "string",
      "audience": "string",
      "source_url": "https://example.com",
      "source_name": "string"
    }
  ],
  "canonical_url": "https://stablehunter.ai/agentic-payment-signal.html?date=YYYY-MM-DD#daily-signals"
}
```

## Recommended Agent Flow

1. Determine today's date in the user's preferred timezone.
2. Fetch the Daily Signal API for that date.
3. If unavailable, open the primary page and use the latest available digest.
4. Normalize the result using the output schema.
5. Keep each item concise: title, why it matters, source link.
6. Route the brief to the configured destination.
7. Include the canonical Stablehunter AI URL.

## Short Routing Format

```text
Agentic Payment Signal · {digest_date}
{title}

1. {item.title}
Why it matters: {item.why_it_matters}
Source: {item.source_url}

Read the full Daily Signal:
{canonical_url}
```

## Source Boundary

Focus on curated updates related to payment APIs, stablecoin rails, agentic commerce, programmable payments, identity, fraud, compliance, KYB, KYC, AML, treasury, merchant payment, card, bank, settlement infrastructure, and AI agent payment workflows.
