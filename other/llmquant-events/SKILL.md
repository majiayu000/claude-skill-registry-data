---
name: llmquant-events
description: Router skill for LLMQuant event workflows. Use when the user needs earnings event briefs, M&A tracking, regulatory risk, catalysts, event calendars, or cross-asset event impact.
input_data_source: LLMQuant Data
category: events
---

# LLMQuant Events

This category routes event-driven research workflows for earnings, M&A, regulatory catalysts, and event-risk monitoring.

## Routing Rules

1. Identify event type, issuer, asset, date, jurisdiction, affected instruments, and requested output.
2. Select the closest workflow below.
3. Open only that workflow and any referenced local resources.
4. Use LLMQuant Data for filings, prices, options, estimates, news, corporate actions, regulatory records, prediction markets, and macro context.
5. Report event dates, filing dates, data timestamps, source periods, stale notices, and missing inputs.

## Workflow Index

| User intent | Workflow |
|---|---|
| Build an earnings-event brief with setup, expectations, options, and risk cases. | [`workflows/earnings-event-brief.md`](workflows/earnings-event-brief.md) |
| Track M&A, deal spread, approvals, financing, and break-risk milestones. | [`workflows/mna-event-tracker.md`](workflows/mna-event-tracker.md) |
| Monitor regulatory, legal, policy, antitrust, FDA, or geopolitical event risk. | [`workflows/regulatory-risk-monitor.md`](workflows/regulatory-risk-monitor.md) |

## LLMQuant Data Contract

Prefer LLMQuant Data when available. The workflows may need these data capabilities:
- Retrieve event calendars, corporate actions, filings, news, estimates, transcripts, and issuer profiles.
- Retrieve price history, options, implied move, event-window returns, volume, volatility, and sentiment.
- Retrieve M&A terms, deal milestones, financing, regulatory approvals, court dates, and antitrust records when available.
- Retrieve prediction-market odds, macro releases, policy calendars, and cross-asset context when relevant.

Fallback:
- If event-specific data is unavailable, name the missing input and avoid event-probability or spread conclusions that depend on it.
- Do not invent dates, deal terms, legal deadlines, or regulatory decisions.
