---
name: sequence-analyzer
description: >
  Analyzes email sequence performance metrics. Evaluates open rates,
  click rates, reply rates, and conversion by step. Identifies drop-off
  points, benchmarks against industry averages, and recommends optimizations.
tags: [email, analytics, sequences, optimization, performance]
---

# Sequence Analyzer

Evaluates the performance of email outreach and nurture sequences. Ingests per-email metrics (opens, clicks, replies, conversions, unsubscribes), identifies drop-off points and underperforming steps, benchmarks against industry averages for B2B services, and outputs actionable optimization recommendations.

## Prerequisites

- `agency.config.json` populated (sequences, benchmarks)
- Sequence performance data: per-email metrics for at least one complete sequence run
- Data source: CRM export, email tool analytics, or manual input
- Optional: previous analyzer reports for trend comparison

## Capabilities Used

1. `crm-writer` -- pull sequence engagement data from CRM
2. `reply-analyzer` -- analyze reply quality and sentiment
3. `ab-test-analyzer` -- evaluate A/B test results within sequences
4. `email-copywriter` -- rewrite underperforming emails

## Phase 0: Intake

Read `agency.config.json`:
- `sequences[]` -- defined sequences with expected benchmarks
- `outreach.daily_caps` -- volume context
- `benchmarks` -- agency-specific benchmark targets if defined:
  ```json
  {
    "benchmarks": {
      "cold_outreach": {
        "open_rate": 55,
        "click_rate": 5,
        "reply_rate": 8,
        "positive_reply_rate": 3,
        "meeting_rate": 2,
        "unsubscribe_rate": 0.5
      },
      "nurture": {
        "open_rate": 40,
        "click_rate": 4,
        "reply_rate": 5,
        "conversion_rate": 12,
        "unsubscribe_rate": 0.3
      }
    }
  }
  ```

Accept parameters:
- `sequence_name` -- (required) name of the sequence to analyze
- `data_source` -- `crm` | `csv` | `manual`. Default: `crm`
- `date_range` -- start and end dates for analysis period
- `comparison_period` -- previous period for trend analysis. Default: `previous_equivalent`
- `include_rewrites` -- boolean, generate improved copy for underperformers. Default: `true`
- `granularity` -- `per_email` | `per_step` | `aggregate`. Default: `per_email`

## Phase 1: Data Collection

### From CRM
Query CRM for sequence performance data:
```
For each email in the sequence:
  - Sent count
  - Delivered count (sent - bounced)
  - Open count (unique opens)
  - Click count (unique clicks)
  - Reply count (unique replies)
  - Positive reply count (interested / meeting booked)
  - Negative reply count (not interested / unsubscribe request)
  - Neutral reply count (OOO, wrong person, info request)
  - Unsubscribe count
  - Bounce count (hard + soft)
  - Conversion count (meeting booked / demo scheduled / proposal requested)
```

### From CSV
Accept a CSV with columns:
```
step, subject, sent, delivered, opened, clicked, replied, positive_replies, negative_replies, unsubscribed, bounced, converted
```

### Manual Input
Prompt for per-step data:
```
For sequence "[name]", provide metrics for each step:
Step 1: [subject line]
  Sent: ___  Opens: ___  Clicks: ___  Replies: ___  Meetings: ___  Unsubs: ___
Step 2: ...
```

## Phase 2: Per-Email Analysis

For each email in the sequence, calculate:

### Core Metrics
```
Step [N]: "[Subject Line]"
---
Sent: [count]
Delivered: [count] ([delivery_rate]%)
Opened: [count] ([open_rate]%)
Clicked: [count] ([click_rate]%)
Replied: [count] ([reply_rate]%)
  - Positive: [count] ([positive_rate]%)
  - Negative: [count] ([negative_rate]%)
  - Neutral: [count] ([neutral_rate]%)
Converted: [count] ([conversion_rate]%)
Unsubscribed: [count] ([unsubscribe_rate]%)
Bounced: [count] ([bounce_rate]%)
```

### Step-Over-Step Decay
Calculate the drop-off between each step:
```
Step 1 -> Step 2: [X]% drop in opens, [Y]% drop in clicks
Step 2 -> Step 3: [X]% drop in opens, [Y]% drop in clicks
...
```

### Benchmark Comparison
Compare each email against industry benchmarks:
```
Step [N] vs Benchmark:
  Open rate: [actual]% vs [benchmark]% -- [ABOVE/BELOW/AT benchmark]
  Click rate: [actual]% vs [benchmark]% -- [ABOVE/BELOW/AT benchmark]
  Reply rate: [actual]% vs [benchmark]% -- [ABOVE/BELOW/AT benchmark]
```

Flag emails performing >20% below benchmark as "underperforming."
Flag emails performing >20% above benchmark as "outperforming."

## Phase 3: Funnel Analysis

### Sequence Funnel
```
SEQUENCE FUNNEL: [name]
===
             Sent: [count] (100%)
        Delivered: [count] ([rate]%)
           Opened: [count] ([rate]%)  -- at least one email opened
          Clicked: [count] ([rate]%)
          Replied: [count] ([rate]%)
Positive replies: [count] ([rate]%)
       Converted: [count] ([rate]%)
```

### Drop-Off Identification
Identify the biggest drop-off points:
```
CRITICAL DROP-OFFS:
1. Step [N] -> Step [N+1]: [X]% drop -- [diagnosis]
2. Step [N] -> Step [N+1]: [X]% drop -- [diagnosis]
```

Drop-off diagnoses:
- Large open drop: subject line fatigue, send timing, list quality degradation
- Large click drop: CTA weak, content not compelling, link placement poor
- Large reply drop: ask too big, value prop unclear, timing wrong
- Spike in unsubs: content mismatch, frequency too high, tone wrong

### Cumulative Performance
```
Total across all steps:
  Unique contacts reached: [count]
  Total emails sent: [count]
  Total opens: [count] (avg [rate]% per email)
  Total clicks: [count] (avg [rate]% per email)
  Total replies: [count] (total reply rate: [rate]%)
  Total conversions: [count] (sequence conversion rate: [rate]%)
  Total unsubscribes: [count] (sequence unsub rate: [rate]%)
  Cost per conversion: [if spend data available]
```

## Phase 4: Content Analysis

### Subject Line Performance
Rank all subject lines by open rate:
```
SUBJECT LINE RANKING:
1. "[subject]" -- [open_rate]% -- Style: [question/number/curiosity/direct]
2. "[subject]" -- [open_rate]% -- Style: [type]
3. "[subject]" -- [open_rate]% -- Style: [type]
...
```

Identify patterns:
- Which subject line styles perform best?
- What length performs best?
- Does personalization (first name, company) improve opens?

### CTA Performance
Rank CTAs by click and reply rate:
```
CTA RANKING:
1. "[CTA text]" in Step [N] -- [click_rate]% clicks, [reply_rate]% replies
2. "[CTA text]" in Step [N] -- [click_rate]% clicks, [reply_rate]% replies
...
```

Identify patterns:
- Direct CTAs ("Book a call") vs soft CTAs ("Reply with thoughts")
- Link-based CTAs vs reply-based CTAs
- CTA placement (end of email vs inline vs PS)

### Reply Quality
If `reply-analyzer` data available:
```
REPLY ANALYSIS:
  Total replies: [count]
  Positive (interested): [count] ([rate]%)
  Negative (not interested): [count] ([rate]%)
  Neutral (OOO, wrong person): [count] ([rate]%)
  Common positive signals: [list]
  Common objections in negative replies: [list]
  Steps generating most positive replies: [step numbers]
```

## Phase 5: Trend Analysis

If comparison period data is available:

```
PERIOD-OVER-PERIOD COMPARISON
===
Metric          | Current | Previous | Change | Trend
Open rate       | [%]     | [%]      | [+/-]  | [up/down/flat]
Click rate      | [%]     | [%]      | [+/-]  | [up/down/flat]
Reply rate      | [%]     | [%]      | [+/-]  | [up/down/flat]
Conversion rate | [%]     | [%]      | [+/-]  | [up/down/flat]
Unsub rate      | [%]     | [%]      | [+/-]  | [up/down/flat]
```

Flag significant changes (>10% shift in either direction).

## Phase 6: Optimization Recommendations

Based on analysis, generate specific, actionable recommendations:

### Underperforming Emails
For each email flagged as underperforming:

```
STEP [N] OPTIMIZATION
---
Issue: [specific metric below benchmark]
Diagnosis: [likely cause based on patterns]
Recommendation: [specific change to make]
Priority: [HIGH/MEDIUM/LOW]

Rewrite (if include_rewrites = true):
  Original subject: "[old subject]"
  Recommended subject: "[new subject]" -- [reasoning]

  Original CTA: "[old CTA]"
  Recommended CTA: "[new CTA]" -- [reasoning]

  Body changes: [specific suggestions]
```

### Sequence-Level Recommendations
```
SEQUENCE OPTIMIZATIONS
===

1. TIMING:
   - [Recommendation about send days/times based on open patterns]
   - [Recommendation about spacing between emails]

2. CONTENT:
   - [Recommendation about content types that work best]
   - [Recommendation about email length based on performance]
   - [Recommendation about personalization approach]

3. STRUCTURE:
   - [Should emails be added/removed?]
   - [Should the sequence be shortened/extended?]
   - [Should the CTA progression change?]

4. TARGETING:
   - [Are certain segments performing differently?]
   - [Should the sequence be split by segment?]

5. A/B TEST SUGGESTIONS:
   - Test 1: [subject line variant] -- Expected impact: [%]
   - Test 2: [CTA variant] -- Expected impact: [%]
   - Test 3: [timing variant] -- Expected impact: [%]
```

## Phase 7: Output

Return structured JSON:

```json
{
  "sequence_name": "cold_outreach_d2c_india",
  "analysis_date": "2026-03-07",
  "date_range": {"start": "2026-02-01", "end": "2026-02-28"},
  "summary": {
    "total_contacts": 200,
    "total_emails_sent": 950,
    "sequence_open_rate": 52.3,
    "sequence_click_rate": 4.8,
    "sequence_reply_rate": 7.2,
    "sequence_conversion_rate": 2.5,
    "sequence_unsub_rate": 0.4,
    "total_conversions": 5,
    "health": "GOOD",
    "vs_benchmark": "ABOVE_AVERAGE"
  },
  "per_email": [
    {
      "step": 1,
      "subject": "Quick question about your Shopify store",
      "sent": 200,
      "open_rate": 58.5,
      "click_rate": 6.2,
      "reply_rate": 4.5,
      "conversion_rate": 1.0,
      "unsub_rate": 0.5,
      "vs_benchmark": "ABOVE",
      "status": "OUTPERFORMING"
    }
  ],
  "drop_offs": [
    {
      "from_step": 3,
      "to_step": 4,
      "open_rate_drop": 18.5,
      "diagnosis": "Subject line fatigue -- Step 4 uses similar style to Step 3",
      "recommendation": "Change Step 4 subject line style from question to curiosity gap"
    }
  ],
  "top_performers": [
    {"step": 1, "metric": "open_rate", "value": 58.5, "reason": "Strong curiosity-based subject line"}
  ],
  "underperformers": [
    {"step": 4, "metric": "open_rate", "value": 38.2, "reason": "Subject line fatigue, poor timing"}
  ],
  "recommendations": [
    {
      "type": "rewrite",
      "step": 4,
      "priority": "HIGH",
      "change": "Replace subject line and lead with fresh angle",
      "expected_impact": "+8-12% open rate",
      "rewrite": {
        "original_subject": "Following up on my last email",
        "new_subject": "This cost [industry] brands 23% in lost revenue last quarter",
        "reasoning": "Pattern interrupt instead of follow-up framing"
      }
    }
  ],
  "ab_test_suggestions": [
    {
      "test": "Step 1 subject line: question vs statement",
      "hypothesis": "Direct statement may outperform question for enterprise segment",
      "sample_size_needed": 100,
      "duration": "2 weeks"
    }
  ],
  "trend": {
    "vs_previous_period": {
      "open_rate_change": "+3.2%",
      "reply_rate_change": "+1.1%",
      "conversion_change": "+0.5%"
    }
  },
  "generated_at": "2026-03-07T10:00:00Z"
}
```

## Phase 8: Review

Present the analysis report.

**APPROVAL GATE**: "Sequence analysis complete. [N] optimization recommendations. Apply the rewrites?"

If approved:
- Update sequence emails via `crm-writer`
- Set up A/B tests for recommended variants
- Schedule next analysis for 2-4 weeks out
- Log baseline metrics for comparison

## Example Usage

Trigger phrases:
- "Analyze the cold outreach sequence performance"
- "How is our nurture sequence doing?"
- "Sequence analytics for [sequence name]"
- "Which emails in the sequence are underperforming?"
- "Optimize our outreach sequence based on the numbers"
- "Run sequence analysis for February"
- "Compare this month's sequence performance to last month"
