---
name: llmquant-etfs
description: Router skill for LLMQuant ETFs workflows. Use when the user needs ETF holdings, overlap, concentration, issuer snapshot, or theme exposure analysis.
input_data_source: LLMQuant Data
category: etfs
---

# LLMQuant ETFs

This category routes ETF analysis tasks to holdings and exposure workflows.

## Routing Rules

1. Identify the ETF tickers, comparison universe, as-of date, and required output.
2. Select the closest workflow below.
3. Open only the selected workflow and required local resources.
4. Use LLMQuant Data for holdings, fund metadata, prices, and coverage notices.
5. Report holdings `as_of_date`, source, stale flags, unsupported tickers, and missing fields.

## Workflow Index

| User intent | Workflow |
|---|---|
| Compare ETF holdings, overlap, concentration, and exposure. | [`workflows/etf-overlap-report.md`](workflows/etf-overlap-report.md) |

## LLMQuant Data Contract

Prefer LLMQuant Data when available. The workflows may need these data capabilities:
- Look up ETF identity, issuer, category, expense ratio, market price, NAV, and coverage status.
- Retrieve ETF holdings with weights, identifiers, sectors, countries, source, and holdings as-of date.
- Compare ETF holdings overlap, top-name concentration, and exposure breakdowns.
- Retrieve price history, fund-flow history, and sector exposure history when available.

Fallback:
- If holdings coverage is unsupported, report the unsupported ticker and the ETF identifiers needed.
- If LLMQuant Data or a compatible data MCP is unavailable, ask the user for issuer holdings files or holdings tables.
- Do not approximate holdings from memory.
