---
name: exec-metrics-storyteller
description: "Transform a metrics snapshot into a board-ready executive narrative tied to revenue and LTV. Generates Headline KPIs, Executive Summary, Revenue & Unit Economics, Trend Analysis, and Outlook sections. Use when preparing board decks, C-suite reviews, or investor updates. Triggers: 'exec metrics report', 'board metrics report', 'C-suite metrics story', 'отчёт по метрикам для борда', 'нарратив метрик для руководства'."
version: 1.0.0
---

# Exec Metrics Storyteller

This skill transforms a metrics snapshot and business context into a formal executive narrative report for C-suite, board, or investor audiences. It converts raw numbers into a structured document with business interpretation, revenue linkage, and strategic outlook — ready to paste into a board deck or executive email.

**Input:**
- Metrics snapshot: paste/table/key-value list (e.g., `MAU: 120k (+12% MoM), ARR: $2.4M, Churn: 2.1%`)
- Business context: reporting period (monthly/quarterly), audience (board / C-suite / investors), product stage (optional), targets/benchmarks (optional)

**Output:**
- Markdown executive narrative with 5 sections: Headline KPIs, Executive Summary, Revenue & Unit Economics, Trend Analysis, Next Period Outlook

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Parse Input

1. Read the user's metrics snapshot
   - Accept paste/table, key-value list, or free-form metric list
   - Accept period and audience type from context or stated explicitly

2. If no numeric data provided (text only, no numbers):
   - Stop and prompt: "Metrics snapshot required. Paste your KPI table or key-value list (e.g., `MAU: 120k (+12% MoM), ARR: $2.4M, Churn: 2.1%`). Then rerun."
   - Do not produce partial output

3. If 50+ metrics provided:
   - Warn: "This snapshot is too large for an executive report. Share your top 10–15 KPIs for the reporting period and rerun."
   - Do not proceed

4. If period or audience type not specified:
   - Assume: monthly period, board audience
   - State these assumptions explicitly at the top of the output under `> Assumptions:`

### Step 2: Classify Metrics

1. Categorize each metric by type:
   - **Growth:** DAU, WAU, MAU, signups, new users, activation rate
   - **Retention:** Churn rate, retention rate, cohort D7/D30, NPS
   - **Revenue:** ARR, MRR, ARPU, GMV, revenue growth rate
   - **Unit Economics:** LTV, CAC, LTV:CAC ratio, payback period
   - **Engagement:** Session length, DAU/MAU ratio, feature adoption

2. Note which metric types are absent from the snapshot
   - If LTV or CAC is missing: prepare placeholder for Revenue & Unit Economics section

3. Identify deltas for each metric (vs. prior period or vs. target)
   - If delta not provided, note as "delta not provided"

### Step 3: Flag Anomalies

1. For each metric with a delta:
   - If deviation > 15% vs. prior period or vs. target → flag as **⚠️ Watch** (moderate) or **🔴 Alert** (critical, >30%)
   - If on track or positive → mark **✅ On track**

2. Identify contradictory signals (e.g., MAU up + revenue down, retention up + churn up)
   - If contradiction found: prepare a "Tension to address" callout for Trend Analysis section
   - Offer 2 possible narrative framings the user can choose between

### Step 4: Draft Executive Summary

1. Write 3–5 sentences covering:
   - Overall performance signal for the period (positive / mixed / concerning)
   - Primary growth driver or key win
   - Top risk or metric to watch
   - Strategic signal for the audience (what this means for direction or investment)

2. Tone: concise, business-framed, no jargon, no raw data — narrative only

### Step 5: Build Report Sections

Build each of the 5 sections using the Output Format below:

1. **Headline KPIs** — top 3–5 metrics, status labels (✅/⚠️/🔴), delta
2. **Executive Summary** — 3–5 sentence narrative from Step 4
3. **Revenue & Unit Economics** — revenue metrics + LTV/CAC with 1–2 sentence interpretation per metric; use placeholder if data missing
4. **Trend Analysis** — notable shifts vs. prior period; Watch/Alert flags; "Tension to address" callout if contradictory signals
5. **Next Period Outlook** — 1 paragraph: expected trajectory, key bets, 1–2 metrics to watch

**Edge Cases:**

- If only 2–3 metrics provided: generate with available data; add note: "Report based on limited metrics — add retention and revenue data for a complete picture"
- If LTV/CAC missing: insert `[LTV/CAC not provided — add for full unit economics view]` in Revenue section; do not omit the section
- If contradictory signals detected: add explicit "Tension to address" callout in Trend Analysis; offer 2 framings; do not force a single narrative
- If period/audience not stated: state assumptions at top of report

---

## Negative Cases

- **No metrics (text only):** Stop. Prompt user for numeric snapshot. Do not produce a report.
- **50+ metrics pasted:** Warn and stop. Ask for top 10–15 KPIs. Do not attempt to process all.
- **No deltas provided for any metric:** Note "No prior-period deltas provided" in Trend Analysis. Generate report using absolute values only; skip status labels (✅/⚠️/🔴).

---

## Output Format

Markdown narrative delivered in chat. Structure:

```markdown
## Executive Metrics Report — [Period] | [Audience]

> **Assumptions:** [state if period or audience were inferred; omit if explicitly provided]

---

### Headline KPIs

| Metric | Value | Delta | Status |
|--------|-------|-------|--------|
| [Metric 1] | [value] | [delta] | ✅ On track |
| [Metric 2] | [value] | [delta] | ⚠️ Watch |
| [Metric 3] | [value] | [delta] | 🔴 Alert |

---

### Executive Summary

[3–5 sentence narrative: performance signal, primary driver, top risk, strategic implication]

---

### Revenue & Unit Economics

**[Revenue metric]:** [value + delta]. [1–2 sentence business interpretation — what this means, not just the number]

**LTV:** [value] | **CAC:** [value] | **LTV:CAC:** [ratio]. [1–2 sentence interpretation of unit economics health]

> [LTV/CAC not provided — add for full unit economics view]  ← use if data missing

---

### Trend Analysis

[Notable shifts vs. prior period, with Watch/Alert flags]

> **⚠️ Tension to address:** [describe contradictory signals if found]. Two possible framings:
> 1. [Framing A — more optimistic read]
> 2. [Framing B — more cautious read]

---

### Next Period Outlook

[1 paragraph: expected trajectory, key strategic bets, 1–2 metrics to watch next period]
```

**Tone rules:**
- No bullet dumps of raw numbers — interpret each metric in 1–2 sentences
- Executive Summary must be narrative prose, not a list
- Avoid jargon (e.g., "CAGR", "cohort D30") unless the audience is technical — translate to plain business language
- Status labels (✅/⚠️/🔴) appear only in the Headline KPIs table and Trend Analysis flags
