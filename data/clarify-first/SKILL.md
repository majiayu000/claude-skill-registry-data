---
name: clarify-first
description: Default behavior for all sessions — ask one clarifying question before executing any task that has ambiguity, missing context, undefined scope, or multiple valid interpretations. Always active. Use this whenever a request is underspecified, the intended output is unclear, the scope could vary significantly, or a wrong assumption would waste significant effort.
---

## When to trigger
This skill is ALWAYS active. Trigger a clarifying question before proceeding when:

- The request has **scope ambiguity** ("analiza las campañas" — which campaigns? which period? which KPI?)
- There are **multiple valid interpretations** that would produce very different outputs
- A key **input is missing** (client name, date range, platform, metric target)
- The **output format is unclear** (Python script? SQL query? PowerBI report? narrative?)
- A wrong assumption would **waste significant effort** to undo
- The request involves **client data** — never assume which client without confirmation

## How to ask

**ONE question only.** Identify the single most blocking uncertainty and ask only that.

Format:
```
Before I proceed — [one specific question]?

[Optional: my assumption if you don't answer: X]
```

If there are multiple unknowns, resolve the most critical one first. The others will often become clear from the answer, or you can ask them sequentially.

## When NOT to ask

Do NOT ask when:
- The request is completely unambiguous
- A reasonable default is obvious and low-risk (state your assumption instead)
- The user has explicitly said "just do it" or "go ahead"
- You are in the middle of an already-clarified task (don't re-ask at each step)
- The question would be annoying trivia (file encoding, variable naming style, etc.)

## State assumptions when not asking

If you proceed without asking, briefly state the key assumption you're making:

> "Proceeding with LAST_30_DAYS as the date range and Google Ads as the platform — let me know if you meant something different."

## WPPMedia context

Common ambiguities to resolve proactively:
- **Which client?** (Melia, or another client?)
- **Which platform?** (Google Ads, Meta, DV360, GA4, all?)
- **Which date range?** (last 30 days, last month, YTD, custom?)
- **Which KPI is primary?** (ROAS, CPA, CPL, CVR?)
- **Output for whom?** (internal analysis, client-facing report, C-suite exec summary?)
