---
name: data-storytelling
description: "Transform data into compelling narratives using visualization, context, and persuasive structure. Use when presenting analytics to stakeholders, creating data reports, or building executive presentations."
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Create a data story for: $ARGUMENTS

---

# Data Storytelling

Transform raw data into compelling narratives that drive decisions and inspire action.

## When to Use

- Presenting analytics to executives
- Creating quarterly business reviews
- Building investor presentations
- Writing data-driven reports
- Communicating insights to non-technical audiences
- Making recommendations based on data

## Core Concepts

### Story Structure

```
Setup → Conflict → Resolution

Setup: Context and baseline
Conflict: The problem or opportunity
Resolution: Insights and recommendations
```

### Narrative Arc

```
1. Hook: Grab attention with surprising insight
2. Context: Establish the baseline
3. Rising Action: Build through data points
4. Climax: The key insight
5. Resolution: Recommendations
6. Call to Action: Next steps
```

### Three Pillars

| Pillar        | Purpose  | Components                       |
| ------------- | -------- | -------------------------------- |
| **Data**      | Evidence | Numbers, trends, comparisons     |
| **Narrative** | Meaning  | Context, causation, implications |
| **Visuals**   | Clarity  | Charts, diagrams, highlights     |

## Story Frameworks

### Framework 1: Problem-Solution

```markdown
## The Hook
"We're losing $2.4M annually to preventable churn."

## The Context
- Current churn rate: 8.5% (industry average: 5%)
- Average customer lifetime value: $4,800
- 500 customers churned last quarter

## The Problem
73% churned within first 90 days. Common factor: < 3 support interactions.

## The Insight
Customers who don't engage in the first 14 days are 4x more likely to churn.

## The Solution
1. Implement 14-day onboarding sequence
2. Proactive outreach at day 7
3. Feature adoption tracking

## Expected Impact
- Reduce early churn by 40%
- Save $960K annually
- Payback period: 3 months

## Call to Action
Approve $50K budget for onboarding automation.
```

### Framework 2: Trend Story

```markdown
## Where We Started
Q3 ended with $1.2M MRR, 15% below target.

## What Changed
- Oct: Launched self-serve pricing
- Nov: Reduced friction in signup
- Dec: Added customer success calls

## The Transformation
| Metric         | Q3     | Q4     | Change |
|----------------|--------|--------|--------|
| Trial to Paid  | 8%     | 15%    | +87%   |
| Time to Value  | 14 days| 5 days | -64%   |
| Expansion Rate | 2%     | 8%     | +300%  |

## Key Insight
Self-serve + high-touch creates compound growth.

## Going Forward
Double down on hybrid model. Target: $1.8M MRR by Q2.
```

### Framework 3: Comparison

```markdown
## The Question
Should we expand into EMEA or APAC first?

## The Comparison
| Factor      | Weight | EMEA Score | APAC Score |
| ----------- | ------ | ---------- | ---------- |
| Market Size | 25%    | 5          | 4          |
| Growth      | 30%    | 3          | 5          |
| Competition | 20%    | 2          | 4          |
| Ease        | 25%    | 2          | 3          |
| **Total**   |        | **2.9**    | **4.1**    |

## The Recommendation
APAC first. Higher growth, less competition.
Start with Singapore hub (English, business-friendly).
Enter EMEA in Year 2 with localization ready.
```

## Visualization Techniques

### Progressive Reveal
```
Slide 1: "Revenue is growing" [single line chart]
Slide 2: "But growth is slowing" [add growth rate overlay]
Slide 3: "Driven by one segment" [add segment breakdown]
Slide 4: "Which is saturating" [add market share]
Slide 5: "We need new segments" [add opportunity zones]
```

### Contrast and Compare
```
Before/After:
┌─────────────────┬─────────────────┐
│ BEFORE          │ AFTER           │
│ Process: 5 days │ Process: 1 day  │
│ Errors: 15%     │ Errors: 2%      │
│ Cost: $50/unit  │ Cost: $20/unit  │
└─────────────────┴─────────────────┘
```

## Presentation Templates

### Executive Summary Slide
```
┌─────────────────────────────────────────────────────────────┐
│  KEY INSIGHT                                                │
│  "Customers who complete onboarding in week 1               │
│   have 3x higher lifetime value"                            │
├──────────────────────┬──────────────────────────────────────┤
│  THE DATA            │  THE IMPLICATION                     │
│  Week 1 completers:  │  - Prioritize onboarding UX          │
│  • LTV: $4,500       │  - Add day-1 success milestones      │
│  • Retention: 85%    │  - Proactive week-1 outreach         │
│  Others:             │  Investment: $75K                    │
│  • LTV: $1,500       │  Expected ROI: 8x                    │
│  • Retention: 45%    │                                      │
└──────────────────────┴──────────────────────────────────────┘
```

### Data Story Flow
```
Slide 1: THE HEADLINE — "We can grow 40% faster by fixing onboarding"
Slide 2: THE CONTEXT — Current metrics, benchmarks, gap analysis
Slide 3: THE DISCOVERY — What the data revealed
Slide 4: THE DEEP DIVE — Root cause, segments, statistical significance
Slide 5: THE RECOMMENDATION — Actions, resources, timeline
Slide 6: THE IMPACT — Expected outcomes, ROI, risk assessment
Slide 7: THE ASK — Specific request, decision needed, next steps
```

## Writing Techniques

### Headlines That Work
```
BAD: "Q4 Sales Analysis"
GOOD: "Q4 Sales Beat Target by 23% - Here's Why"

BAD: "Customer Churn Report"
GOOD: "We're Losing $2.4M to Preventable Churn"

Formula: [Specific Number] + [Business Impact] + [Actionable Context]
```

### Handling Uncertainty
```
• "With 95% confidence, we can say..."
• "The sample size of 500 shows..."
• "While correlation is strong, causation requires..."
• "Impact estimate: $400K-$600K"
• "Best case: X, Conservative: Y"
```

## Best Practices

### Do's
- **Start with the "so what"** — Lead with insight
- **Use the rule of three** — Three points, three comparisons
- **Show, don't tell** — Let data speak
- **Make it personal** — Connect to audience goals
- **End with action** — Clear next steps

### Don'ts
- **Don't data dump** — Curate ruthlessly
- **Don't bury the insight** — Front-load key findings
- **Don't use jargon** — Match audience vocabulary
- **Don't show methodology first** — Context, then method
- **Don't forget the narrative** — Numbers need meaning
