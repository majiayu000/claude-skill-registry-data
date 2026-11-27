---
name: product-roadmap-prioritizer
description: "Runs candidate features through Reach-Impact-Confidence-Effort (RICE), Kano, Must-Should-Could-Won't (MoSCoW), and Cost-of-Delay scoring, surfaces convergence and divergence across frameworks, and produces a defensible quarterly priority list with explicit trade-offs. Use when building a quarterly or annual roadmap; resolving conflicting stakeholder input; justifying a deprioritization to a stakeholder; or normalizing requests from multiple sources (sales, customer success, leadership) into one queue."
---

# Product Roadmap Prioritizer

> Multi-framework feature ranking that withstands stakeholder pushback.

## What this skill is

A workflow that scores candidate features across four complementary prioritization frameworks - Reach-Impact-Confidence-Effort (RICE), Kano, Must-Should-Could-Won't (MoSCoW), and Cost of Delay - surfaces where they agree and disagree, and turns that into a ranked quarterly roadmap with explicit reasoning. Designed so that every "no" can be defended with the same rigor as every "yes."

## What it solves

- Highest-Paid-Person's-Opinion (HiPPO) driven prioritization
- Feature ranking that ignores effort or confidence
- Single-framework analysis that misses the trade-off (RICE without Kano misses delighters; Kano without RICE misses scale)
- Sales, customer success, and executive requests that bypass any structured queue
- Inability to explain to a stakeholder why their request didn't make the cut

## When to invoke

- Quarterly or annual roadmap planning
- Resolving conflicting input from sales, customer success, and leadership
- Justifying a deprioritization in writing
- Normalizing a backlog of 50+ requests into a ranked queue
- Pre-Objectives and Key Results (pre-OKR) planning to align roadmap with stated objectives

## Phase 1: Inventory candidates

Collect every candidate from every source:
- Sales requests (deal-driven asks)
- Customer success and support themes (volume, severity)
- Leadership, board, or strategy directives
- Customer interview opportunity tree
- Technical debt and platform investments
- Engineering quality and reliability work

For each, capture: title, sponsor, source link, hypothesized outcome, hypothesized customer.

Reject anything missing sponsor or outcome.

## Phase 2: Score with RICE

For each candidate:

```
Reach-Impact-Confidence-Effort (RICE) = (Reach × Impact × Confidence) / Effort
```

- **Reach** - number of users affected per time period
- **Impact** - 0.25 (minimal) / 0.5 / 1 (medium) / 2 / 3 (massive)
- **Confidence** - 50% / 80% / 100% - based on quality of evidence
- **Effort** - person-months

Document the data source behind each number. A RICE score with no evidence is a feeling.

## Phase 3: Classify with Kano

For each candidate, classify the **customer perception**:

| Kano category | Definition | Investment posture |
|---------------|------------|---------------------|
| Must-have | Expected baseline; absence → dissatisfaction | Reach parity, then stop |
| Performance | More is better; linear satisfaction | Invest while Return on Investment (ROI) holds |
| Delighter | Unexpected; non-linear satisfaction | Invest selectively for differentiation |
| Indifferent | No effect on satisfaction | Defer or kill |
| Reverse | More → less satisfaction | Avoid |

Classification source: survey, interview, behavioral data, or analyst hypothesis (flag the confidence).

A roadmap of all must-haves is a defensive crouch. A roadmap of all delighters is fragile. Balance.

## Phase 4: Categorize with MoSCoW (per release)

For each candidate **within a release window**, apply the Must-Should-Could-Won't (MoSCoW) categorization:
- **Must** - non-negotiable; release fails without it
- **Should** - important; release weaker without it
- **Could** - nice to have; first to cut
- **Won't (this time)** - explicitly out of scope

Rule of thumb: Must ≤ 60% of release capacity. Anything higher means everything is "must," which means nothing is.

## Phase 5: Weight with Cost of Delay

For time-sensitive items, compute Cost of Delay Divided by Duration (CD3):

```
CD3 = Cost of Delay / Duration
```

Cost of delay components:
- Revenue at risk (deal blockers, churn risk)
- Competitive timing (feature parity windows)
- Compliance or regulatory deadlines
- Dependency unblocking (other teams gated)
- Brand or public-relations opportunity

CD3 sorts the queue for sequencing within a release.

## Phase 6: Convergence analysis

Build the convergence table:

| Candidate | RICE rank | Kano | MoSCoW | CD3 rank | Convergence |
|-----------|----------:|------|--------|---------:|-------------|
| A | 1 | Performance | Must | 1 | Strong yes |
| B | 5 | Delighter | Should | 3 | Mixed - investigate |
| C | 12 | Must-have | Must | 8 | Table stakes - do |
| D | 2 | Indifferent | Could | 15 | RICE alone is misleading |

Where frameworks agree → high confidence to commit. Where they disagree → the disagreement IS the strategy conversation. Don't average; investigate.

## Phase 7: Quarterly roadmap

For the chosen quarter:
- 60% capacity → must-haves and high-converging items
- 25% capacity → performance and delighter bets
- 10% capacity → technical debt and platform investment
- 5% capacity → discovery experiments (no committed output)

Stakeholder reply template for declined requests:
> Thanks for the request. We scored [X] using RICE / Kano / MoSCoW. It scored [Y], which puts it behind [Z]. We'd reconsider if [explicit trigger]. Here's what we're doing instead: [items A, B, C] and the outcome we expect.

## Output

- Scored candidate table across all four frameworks
- Convergence and divergence analysis with reasoning
- Ranked quarterly roadmap with capacity allocation
- Explicit "won't do this quarter" list with reasoning
- Stakeholder decline templates per declined request
- Re-evaluation triggers for next quarter

## Operating rules

**Always**
- Source every RICE input from evidence
- Apply at least two frameworks before committing
- Investigate divergence - don't average it away
- Cap "Must" at 60% of release capacity
- Document why each declined item was declined

**Never**
- Score with confidence above what the evidence supports
- Use one framework alone
- Promote a request because the sponsor is senior
- Treat technical debt as automatically deferrable
- Confuse a feature with an outcome
