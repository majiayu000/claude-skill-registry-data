---
name: data-story
description: >
  Communicate data insights to non-technical stakeholders in a structured, persuasive format. Use when
  the user says "present these findings", "explain this analysis to leadership", "make a data presentation",
  "tell the story behind the data", "translate this into a business narrative", "make this insight
  actionable", "stakeholder readout", "executive summary of results", or needs to turn analysis output
  into a decision-ready document or slide deck.
---

## Overview

Based on **"Storytelling with Data"** by Cole Nussbaumer Knaflic. The core principle: data does not speak for itself. Context, audience, and a clear call to action determine whether an insight drives a decision or gets ignored. Every data communication is a story with a protagonist (the audience), a tension (the problem), and a resolution (the recommended action). Remove everything that doesn't serve that arc.

## Workflow

### Step 1: Define the audience and the decision they need to make

Before touching a chart or a sentence, answer:
- Who is in the room? (technical ICs, business leads, C-suite?)
- What decision do they need to make as a result of seeing this?
- What do they already believe? What might they push back on?

Write one sentence: "After seeing this, [audience] should [specific action or decision]."

This sentence controls everything downstream.

### Step 2: Lead with the conclusion, not the methodology

Knaflic's rule: the insight goes first. The supporting evidence follows.

Structure:
1. Situation - what context does the audience need?
2. Complication - what changed or what problem exists?
3. Resolution - what does the data say to do?

Bad order: "We ran a 4-week A/B test. We measured conversion, retention, and revenue. Here are the results. [charts] Based on this, we recommend..."
Good order: "Variant B increased revenue per user by 12%. Here's why it worked and what we should do next."

### Step 3: Choose one chart per insight

Do not show a chart because you have it. Show a chart because it communicates something words cannot.

Chart selection guide:
- Comparison over time: line chart
- Comparison between categories: bar chart (horizontal if > 5 categories)
- Part-to-whole: stacked bar or pie (only if 2-3 slices)
- Distribution: histogram or box plot
- Relationship between two variables: scatter plot

Remove: dual-axis charts, 3D charts, pie charts with > 3 slices, and any chart where the title is a label instead of an insight.

### Step 4: Edit every chart to carry a single message

Each chart should have:
- A title that states the finding ("Conversion dropped 18% after the November release" not "Conversion rate over time")
- A single highlighted data series or data point that draws the eye to the key number
- All non-essential gridlines, legends, and axes labels removed or minimized

Apply Knaflic's preattentive attributes to guide attention: use color sparingly (one accent color for the key insight), use bold or size for emphasis, use position to show ranking.

### Step 5: Write the narrative scaffolding

For a written report or slide deck, each insight needs a three-part structure:

```
Headline (1 line): The finding, stated as a conclusion.
Evidence (2-3 bullets): The numbers that prove the headline.
Implication (1 line): What this means for the decision at hand.
```

Example:
```
Headline: Power users drive 80% of revenue despite being 12% of accounts.
Evidence:
  - Top 12% of accounts by login frequency generated $4.2M of $5.3M total ARR.
  - Median revenue per power user: $1,400/yr vs. $90/yr for casual users.
  - Power users churn at 4% annually vs. 31% for casual users.
Implication: Retention investment should prioritize power user health, not broad activation.
```

### Step 6: Review for clutter and call to action

Before finalizing, cut:
- Any slide or section that does not directly support the audience's decision
- Methodology details that belong in an appendix
- Charts that show "we did a lot of work" rather than proving a point

End every presentation or report with a single, explicit ask:
"We recommend [action]. We need [decision] by [date] to [outcome]."

## Anti-Patterns

**1. The data dump**
Bad: Sharing a 40-chart dashboard and telling the audience to "explore it".
Good: Curating 3-5 charts that build a specific argument and presenting them in order.

**2. Titles that describe instead of conclude**
Bad: Chart title = "Monthly Active Users by Segment, Jan-Dec"
Good: Chart title = "Enterprise segment MAU grew 34%; SMB flat for 6 months"

**3. Using color for decoration**
Bad: Each bar in a bar chart is a different color.
Good: All bars are grey except the one being discussed, which is the accent color.

**4. Burying the recommendation at the end**
Bad: Walking through all the analysis before stating what the audience should do.
Good: State the recommendation in the first 30 seconds or on slide 2. Everything after is evidence.

## Quality Checklist

- [ ] Audience and their required decision identified before any chart is made
- [ ] Opening leads with the conclusion, not the methodology
- [ ] Each insight has one supporting chart - chart type matches the data relationship
- [ ] Every chart title states a finding, not a label
- [ ] Color used only to direct attention to the key data point
- [ ] Each insight section has a headline, evidence bullets, and an implication
- [ ] Final slide or paragraph contains a specific, time-bound recommendation
