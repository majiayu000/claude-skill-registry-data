---
name: jobs-to-be-done-extractor
description: "Extracts Jobs-to-be-Done (JTBD) statements (functional, emotional, social) from raw research - interviews, surveys, support tickets, sales calls - and produces a job map with progress measures and outcome statements. Use when reframing a product around customer outcomes; segmenting beyond demographics; building a competitive switching analysis; prioritizing features; or aligning product, marketing, and sales on the same job."
---

# Jobs-to-be-Done Extractor

> Reframes the product around the job the customer is hiring it to do.

## What this skill is

A workflow that turns unstructured customer research into Jobs-to-be-Done (JTBD) artifacts: functional, emotional, and social job statements; a job map; force diagrams (push / pull / habit / anxiety); outcome statements; and a hire / fire analysis. Built on the Outcome-Driven Innovation (ODI) school of Anthony Ulwick and the milkshake school of Clayton Christensen, with explicit handling of overserved versus underserved outcomes.

## What it solves

- Persona-based segmentation that doesn't predict purchase behavior
- Roadmaps driven by feature requests instead of customer outcomes
- Marketing copy that lists features but doesn't connect to the job
- Switching analysis that ignores the four forces (push, pull, habit, anxiety)
- Inconsistent JTBD interpretations across product, marketing, and sales

## When to invoke

- Synthesizing customer interviews, switching interviews, or win-loss calls
- Re-segmenting the market beyond firmographics
- Building positioning or messaging that resonates with the actual job
- Prioritizing the roadmap by underserved outcome importance
- Aligning product, marketing, sales, and customer success on a shared customer model

## Phase 1: Source the raw material

Catalog what you have:
- Customer interview transcripts (switching, churn, win-loss, discovery)
- Sales call recordings plus notes
- Support tickets and Customer Satisfaction (CSAT) verbatims
- Survey free-text responses
- Reviews (G2, Capterra, Reddit, Twitter / X)
- Internal Slack messages from customer success and sales

Log source, recency, sample size, and any selection bias.

## Phase 2: Extract the job statements

For each customer signal, write a job statement using the canonical form:

> When [situation], I want to [motivation], so I can [expected outcome].

Categorize each into:
- **Functional** - the practical task being accomplished
- **Emotional** - how the customer wants to feel
- **Social** - how they want to be perceived

Most products serve a primary functional job plus 1-2 emotional or social jobs. Identify the **main job** versus **related jobs** versus **little hires**.

## Phase 3: Build the job map

Decompose the main job into the 8 universal job stages:

| Stage | Question | Example |
|-------|----------|---------|
| Define | What do they need to decide before starting? | |
| Locate | What inputs or context do they need to gather? | |
| Prepare | How do they set up the work? | |
| Confirm | How do they verify they're ready? | |
| Execute | What is the core task? | |
| Monitor | How do they track progress? | |
| Modify | How do they adapt mid-job? | |
| Conclude | How do they finish and clean up? | |

For each stage, list the **desired outcomes** the customer wants to optimize.

## Phase 4: Outcome statements and importance × satisfaction

Convert each desired outcome into a measurable statement:

> [Minimize / Increase] the [unit of measure] [object of control] [contextual clarifier]

Example: *Minimize the time it takes to verify the report matches the source data.*

Score each outcome on 1-10:
- **Importance** - how critical to the customer
- **Satisfaction** - how well current solutions deliver

Plot on the Opportunity Score matrix:

```
Opportunity Score = Importance + max(Importance − Satisfaction, 0)
```

Outcomes scoring ≥ 15 are **underserved** (innovation opportunity). Outcomes scoring < 10 with high satisfaction are **overserved** (cost-reduction or simplification opportunity).

## Phase 5: Forces of progress analysis

For switching or adoption decisions, map the four forces:

| Force | Pulls toward new | Pulls toward old |
|-------|------------------|------------------|
| Push of the current situation | Frustrations, broken workflows | |
| Pull of the new solution | Promised benefits, identity fit | |
| Anxiety of the new solution | | Switching cost, learning curve, risk |
| Habit of the old | | Inertia, sunk cost, social bonds |

A switch happens when (Push + Pull) > (Anxiety + Habit). Identify which force is the bottleneck and prioritize accordingly.

## Phase 6: Hire / fire analysis

For each segment, identify:
- **Who they hired you over** (direct competitor, workaround, do-nothing)
- **Who they fired to hire you** (incumbent, manual process)
- **What would make them fire you** (deal-breakers, deteriorating outcomes)

## Output

- 5-12 prioritized job statements (functional plus emotional plus social)
- Job map with 8 stages and desired outcomes per stage
- Opportunity Score matrix flagging underserved and overserved outcomes
- Forces of progress diagram for top switching scenarios
- Hire / fire analysis per segment
- 3-5 messaging seeds for marketing and sales

## Operating rules

**Always**
- Quote customer language verbatim before paraphrasing
- Distinguish functional versus emotional versus social
- Score outcomes for both importance and satisfaction
- Use the canonical situation / motivation / outcome statement form
- Map all four forces, not just push and pull

**Never**
- Mix demographic personas with JTBD segments
- Skip the "when" situation - it's where the job lives
- Reduce a job to a feature request
- Anchor on the first interview (verify across multiple sources)
- Confuse the customer's words with their job
