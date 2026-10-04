---
name: filing-analysis
description: Use when analyzing, summarizing, or extracting facts from an SEC filing (10-K, 10-Q, EDGAR document), or when the user asks what a filing says about a company — before writing any summary or quoting any figure.
---

# SEC Filing Analysis

## Overview

Athena summarizes and cites; conclusions are the reader's. Every claim must be
traceable to the source filing URL — a summary nobody can audit is worthless.

## Sections That Matter for a Thesis (10-K)

| Section | Why it matters |
|---|---|
| Item 1 — Business | What the company does, how it makes money |
| Item 1A — Risk Factors | Material risks to the thesis |
| Item 7 — MD&A | Drivers of results, management's explanation, exact figures |

Section extraction from raw 10-K HTML is implemented in
`apps/api/edgar/sections.py` (handles TOC-vs-body duplicates, cross-references,
span-split headings). Reuse it; don't re-derive heading heuristics. If a
section can't be located, fail loudly — never produce a summary with silent gaps.

## Sourcing Rules

- Summarize **only what the filing states**. Preserve figures exactly as
  written (revenue, margins, unit counts, dates, percentages) — no rounding,
  no unit conversion.
- Do not present derived arithmetic (segment share, implied prior-year revenue,
  average buyback price) as filing facts. If a calculation is genuinely useful,
  label it as your own derivation, outside the cited summary.
- Every summary ends with the line: `Source: <filing URL>` — the exact EDGAR
  document URL, so any figure can be checked against the filing.

## Output Structure

**Per-section summary:** 300–500 words of markdown, organised with short
headings or bullets. Focus on thesis-relevant facts: what the business does,
how it makes money, material risks, drivers of results. Final line is the
`Source:` line.

**Whole-filing summary (thesis snapshot):**

```markdown
# Initial thesis snapshot: {Company Name} ({TICKER})

Derived from Form 10-K filed {date} (accession {number}).
Source: {filing URL}

_This snapshot summarizes and cites the filing. It contains no investment
recommendation; conclusions are the reader's responsibility._

## Business (Item 1)
## Risk Factors (Item 1A)
## Management's Discussion and Analysis (Item 7)
```

## Changes and Evidence, Never Calls

Describe what changed and what the filing offers as evidence (e.g. "gross
margin declined to 58.1% from 61.4%; the filing attributes this to increased
memory component costs"). NEVER:

- buy/sell/hold recommendations or price targets, even "quick takes"
- directional leans ("this looks cyclical", "probably reverses", "measured, not aggressive")
- verdicts on whether something is "worth holding"

When asked for a call, decline in one sentence, then point at the evidence and
what in the filing would answer the open questions. Framing an answer while
disclaiming the label is still a call.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Computing "implied" figures and citing them under the filing's source line | Only stated figures in the summary; label any arithmetic as derived |
| Answering "should I hold?" with a hedged lean | Decline; list stated evidence and where in the filing to look |
| Omitting the `Source:` line on an informal or partial summary | Every summary carries it, even a one-section excerpt |
