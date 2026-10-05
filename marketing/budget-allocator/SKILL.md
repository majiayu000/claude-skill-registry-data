---
name: budget-allocator
description: 'Launch budget optimization using portfolio theory and scenario analysis with experimentation reserves. Use when: budget allocation, marketing budget, launch budget, how much to spend, budget planning, channel budget.'
---

# Budget Allocator (APEX Allocation Model)

A rigorous budget optimization engine that applies portfolio theory principles to marketing spend allocation, producing scenario-modeled investment plans with built-in experimentation reserves and continuous rebalancing triggers. APEX ensures every dollar is allocated to its highest-impact use while maintaining optionality for emerging opportunities.

## When to Use
- Planning marketing budget for a product launch
- Allocating spend across channels and timeframes
- Building ROI projections for budget approval
- Designing structured marketing experiments with kill criteria
- Stress-testing budget assumptions through sensitivity analysis
- Rebalancing mid-campaign when channels over- or underperform
- Justifying budget requests to finance or leadership

## What You'll Need

**Critical inputs (ask if not provided):**
- Total available budget and time horizon
- Target metrics (pipeline, revenue, CAC targets, ROI floor)
- Channel performance data or benchmarks (from demand-engine WAVE scores)
- Product and launch context (launch type, audience, market)
- Financial constraints or guardrails (max spend per channel, minimum ROI)

**Nice-to-have:**
- Historical channel performance data (CAC, conversion rates, LTV by channel)
- Competitive spend intelligence (from battle-scanner)
- Seasonal or market timing data (from signal-radar)
- Customer journey stage mapping (from journey-architect)
- Previous launch budgets and actuals for calibration

## Process

### Step 1: Allocate -- Define the Five Spend Buckets

Every launch budget is divided into five strategic buckets. The percentages flex based on launch type and maturity.

| Bucket | Range | Purpose | Examples |
|--------|-------|---------|----------|
| Foundation | 15-20% | Infrastructure that enables all other spend | Website, landing pages, tracking, tooling, creative assets |
| Awareness | 25-30% | Top-of-funnel reach and brand visibility | Content marketing, PR, social media, display, sponsorships |
| Acquisition | 30-35% | Direct pipeline and demand generation | Paid search, paid social, email campaigns, events, webinars |
| Enablement | 10-15% | Sales and partner activation | Sales tools, partner co-marketing, demo environments, training |
| Experiment Reserve | 10-15% | Structured tests on unproven channels | New channels, messaging tests, audience tests, creative tests |

**Bucket Allocation by Launch Type:**

| Launch Type | Foundation | Awareness | Acquisition | Enablement | Experiment |
|-------------|-----------|-----------|-------------|------------|------------|
| New Product (GA) | 20% | 30% | 25% | 15% | 10% |
| Major Feature | 15% | 25% | 35% | 15% | 10% |
| Market Expansion | 15% | 30% | 30% | 10% | 15% |
| PLG/Self-Serve | 20% | 20% | 30% | 10% | 20% |
| Enterprise Upmarket | 15% | 20% | 30% | 25% | 10% |

### Step 2: Allocate -- Channel-Level Distribution Using WAVE Scores

Within each bucket, distribute budget across channels using WAVE scores from demand-engine (or estimate if not available).

**Channel Scoring Matrix:**

| Channel | WAVE Score (1-10) | Historical CAC | Est. Pipeline | Confidence | Budget Share |
|---------|-------------------|---------------|---------------|------------|-------------|
| Paid Search | | | | | |
| Paid Social (LinkedIn) | | | | | |
| Paid Social (Meta) | | | | | |
| Content/SEO | | | | | |
| Email Marketing | | | | | |
| Events/Webinars | | | | | |
| Partner Co-marketing | | | | | |
| PR/Analyst Relations | | | | | |
| Community/PLG | | | | | |
| Direct Outbound | | | | | |

**Budget Share Formula:**

```
Channel_Budget_Share = (WAVE_Score_i / SUM(all WAVE_Scores)) x Bucket_Budget
```

Apply minimum allocation floor of 5% per active channel to avoid spreading too thin.

### Step 3: Predict -- Three Scenarios Per Channel

For each channel, model three outcomes to build a range of expected returns.

| Channel | Scenario | Budget | Est. CAC | Est. Leads | Est. Pipeline | Est. ROI | Probability |
|---------|----------|--------|----------|------------|---------------|----------|-------------|
| Paid Search | Conservative | | | | | | 25% |
| Paid Search | Expected | | | | | | 50% |
| Paid Search | Optimistic | | | | | | 25% |
| Paid Social | Conservative | | | | | | 25% |
| Paid Social | Expected | | | | | | 50% |
| Paid Social | Optimistic | | | | | | 25% |

**Scenario Definitions:**

| Scenario | Conversion Assumption | CAC Assumption | Lead Volume | Probability Weight |
|----------|----------------------|----------------|-------------|-------------------|
| Conservative | 70% of benchmark | 130% of benchmark | 70% of target | 25% |
| Expected | 100% of benchmark | 100% of benchmark | 100% of target | 50% |
| Optimistic | 140% of benchmark | 75% of benchmark | 130% of target | 25% |

**Expected Value Calculation:**

```
Expected_Pipeline = (Conservative x 0.25) + (Expected x 0.50) + (Optimistic x 0.25)
Expected_ROI = Expected_Pipeline / Channel_Budget
```

### Step 4: Predict -- Aggregate Budget Scenarios

Roll up channel-level scenarios into three overall budget scenarios.

| Dimension | Conservative (-20%) | Base Case | Aggressive (+30%) |
|-----------|---------------------|-----------|-------------------|
| Total Budget | | | |
| Expected Leads | | | |
| Expected Pipeline | | | |
| Expected Revenue | | | |
| Blended CAC | | | |
| Overall ROI | | | |
| Payback Period | | | |
| Risk Level | Low | Medium | High |
| Confidence | 85% | 70% | 55% |

### Step 5: Experiment -- Design Structured Tests

The experiment reserve (10-15% of budget) is allocated to structured tests with clear hypotheses and kill criteria.

**Experiment Portfolio Template:**

| # | Experiment Name | Hypothesis | Budget Cap | Duration | Success Metric | Kill Criteria | Status |
|---|----------------|-----------|------------|----------|----------------|---------------|--------|
| 1 | | If we [action], then [outcome] because [reason] | | | | Stop if [metric] < [threshold] after [time] | Planned |
| 2 | | | | | | | |
| 3 | | | | | | | |
| 4 | | | | | | | |
| 5 | | | | | | | |

**Experiment Evaluation Criteria:**

| Criterion | Weight | Scoring (1-5) |
|-----------|--------|---------------|
| Learning value (even if fails) | 25% | 1=Low, 5=Transformative insight |
| Scalability if successful | 25% | 1=Niche, 5=10x scalable |
| Speed to signal | 20% | 1=>90 days, 5=<14 days |
| Budget efficiency | 15% | 1=>10% reserve, 5=<2% reserve |
| Strategic alignment | 15% | 1=Tangential, 5=Core strategy |

**Experiment Priority Score** = SUM(Criterion_Score x Weight)

Run top 3-5 experiments. Graduate winners into main budget; kill losers at criteria thresholds.

### Step 6: X-ray -- Sensitivity Analysis

Identify the top 3 assumptions that most impact ROI and stress-test each.

**Sensitivity Analysis Framework:**

| Assumption | Base Value | -30% | -15% | Base | +15% | +30% | Impact on ROI |
|-----------|-----------|------|------|------|------|------|---------------|
| Conversion rate | | | | | | | |
| Average deal size | | | | | | | |
| Sales cycle length | | | | | | | |
| CAC by channel | | | | | | | |
| Retention rate | | | | | | | |

**Tornado Chart Data (rank by ROI swing):**

| Rank | Assumption | Downside ROI | Base ROI | Upside ROI | Swing |
|------|-----------|-------------|----------|-----------|-------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

For each high-sensitivity assumption, define:
- **Monitoring metric:** How will you track this assumption in real time?
- **Rebalancing trigger:** At what threshold do you adjust spend?
- **Response protocol:** What specific action do you take?

### Step 7: Monthly Rebalancing Protocol

Budget is not static. Apply these rebalancing rules monthly.

**Rebalancing Decision Matrix:**

| Channel Performance | Duration | Action | Budget Change |
|-------------------|----------|--------|---------------|
| Underperform target by >25% | 1 month | Monitor, optimize creative/targeting | No change |
| Underperform target by >25% | 2 months | Reduce allocation | -30% from channel |
| Underperform target by >25% | 3 months | Pause channel | Reallocate 100% |
| At target (+/- 10%) | Any | Maintain | No change |
| Outperform target by >25% | 1 month | Validate signal is real | No change |
| Outperform target by >25% | 2+ months | Increase allocation | +20% to channel |

**Rebalancing Source/Destination Rules:**
- Freed budget goes first to experiment reserve (up to 20% of total)
- Then to highest-ROI performing channel (up to 150% of original allocation)
- Never concentrate >40% of total budget in a single channel

## Output

Save to `outputs/budget-allocator/`

### Deliverables:
1. **Budget Allocation Model** -- Five-bucket allocation with channel-level distribution, WAVE-score-weighted, with minimum floors and maximum caps per channel
2. **ROI Projection Matrix** -- Three scenarios (conservative/base/aggressive) per channel and aggregate, with expected values, CAC, pipeline, and payback calculations
3. **Experiment Portfolio** -- 3-5 structured experiments with hypotheses, budget caps, success metrics, kill criteria, and priority scores
4. **Sensitivity Analysis** -- Tornado chart of top assumptions, stress-test results, monitoring metrics, and rebalancing triggers with response protocols

## Chain Connections
- **Receives from:** demand-engine (WAVE scores, channel strategy), financial-analyst (unit economics, ROI thresholds), battle-scanner (competitive spend intel), signal-radar (market timing)
- **Feeds into:** launch-command (budget as input to launch readiness), demand-engine (rebalancing feedback)
- **Enhanced by:** launch-pulse (actual performance data for rebalancing), launch-debrief (historical calibration data)
