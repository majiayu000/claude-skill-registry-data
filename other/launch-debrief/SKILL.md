---
name: launch-debrief
description: 'Structured post-launch retrospective that produces quantified learnings and improvement playbooks. Use when: launch retrospective, post-launch review, what worked, launch debrief, post-mortem, lessons learned.'
---

# Launch Debrief (MIRROR Protocol)

A structured post-launch retrospective engine that transforms raw launch data into quantified learnings, root-cause analyses, and improvement playbooks. MIRROR ensures every launch makes future launches better by extracting actionable insights from both successes and failures through systematic analysis rather than anecdotal recall.

## When to Use
- Conducting a post-launch retrospective (ideally at T+30 and T+90)
- Analyzing why a launch over- or underperformed expectations
- Building an institutional knowledge base of launch learnings
- Creating improvement playbooks for the next launch cycle
- Presenting launch results to leadership with root-cause analysis
- Comparing actual results against pre-launch projections
- Identifying systemic issues across multiple launches

## What You'll Need

**Critical inputs (ask if not provided):**
- Launch name, date, and type (GA, beta, feature, expansion)
- Pre-launch targets for all VITAL metrics (from launch-pulse)
- Actual performance data for all tracked metrics
- Launch readiness scores from gate reviews (from launch-command)
- Budget allocation and actual spend (from budget-allocator)
- Channel performance data by channel (from demand-engine)

**Nice-to-have:**
- Customer feedback (NPS, surveys, support tickets, social mentions)
- Internal team feedback (retro notes, Slack threads, post-mortems)
- Competitive activity during launch window (from battle-scanner)
- Sales feedback on messaging and enablement effectiveness
- Win/loss analysis data from CRM
- Previous launch debrief reports for trend analysis

## Process

### Step 1: Metrics Review -- Actual vs Target vs Baseline

For each VITAL metric, calculate the Performance Index and classify the result.

**Performance Index Table:**

| VITAL Layer | Metric | Baseline | Target | Actual | Perf. Index | Classification |
|-------------|--------|----------|--------|--------|-------------|---------------|
| Volume | Website Traffic | | | | Actual/Target | |
| Volume | Impressions | | | | | |
| Volume | Social Reach | | | | | |
| Intent | MQLs | | | | | |
| Intent | Demo Requests | | | | | |
| Intent | Trial Signups | | | | | |
| Traction | SQLs | | | | | |
| Traction | Pipeline Created | | | | | |
| Traction | Win Rate | | | | | |
| Adoption | Activation Rate | | | | | |
| Adoption | Time to Value | | | | | |
| Adoption | DAU/WAU | | | | | |
| Loyalty | NPS | | | | | |
| Loyalty | 30-Day Retention | | | | | |
| Loyalty | Referral Rate | | | | | |

**Performance Index Scale:**

| Index | Classification | Color | Meaning |
|-------|---------------|-------|---------|
| >= 1.20 | Significant Overperformance | Blue | Exceeded target by 20%+, investigate why |
| 1.00 - 1.19 | On Target | Green | Met or exceeded target |
| 0.80 - 0.99 | Slight Underperformance | Yellow | Close to target, minor optimization needed |
| 0.60 - 0.79 | Material Underperformance | Orange | Significant gap, root-cause analysis required |
| < 0.60 | Critical Miss | Red | Major failure, deep investigation required |

**Top 3 Overperformances:**

| Rank | Metric | Index | Why It Worked | Replicable? |
|------|--------|-------|--------------|-------------|
| 1 | | | | Yes / Partially / No |
| 2 | | | | |
| 3 | | | | |

**Top 3 Underperformances:**

| Rank | Metric | Index | Initial Hypothesis | Severity |
|------|--------|-------|--------------------|----------|
| 1 | | | | Critical / High / Medium |
| 2 | | | | |
| 3 | | | | |

### Step 2: Insights Extraction

Systematically extract learnings across four dimensions.

**Win Analysis (What Worked):**

| # | Category | Finding | Evidence | Impact Level | Replicable? |
|---|----------|---------|----------|-------------|-------------|
| 1 | Messaging | Which messages resonated strongest? | Data point | High/Med/Low | |
| 2 | Channel | Which channels outperformed? | Data point | | |
| 3 | Content | Which assets drove the most engagement? | Data point | | |
| 4 | Timing | Were there timing advantages? | Data point | | |
| 5 | Audience | Which segments responded best? | Data point | | |

**Loss Analysis (What Did Not Work):**

| # | Category | Finding | Evidence | Impact Level | Preventable? |
|---|----------|---------|----------|-------------|-------------|
| 1 | Messaging | Which messages fell flat? | Data point | High/Med/Low | |
| 2 | Channel | Which channels underperformed? | Data point | | |
| 3 | Competitive | Where did competitors win? | Data point | | |
| 4 | Execution | What execution gaps occurred? | Data point | | |
| 5 | Assumptions | Which assumptions were wrong? | Data point | | |

**Customer Feedback Synthesis:**

| Source | Volume | Top Positive Themes | Top Negative Themes | Surprise Insights |
|--------|--------|-------------------|-------------------|------------------|
| NPS Comments | | | | |
| Support Tickets | | | | |
| Social Mentions | | | | |
| Sales Conversations | | | | |
| User Surveys | | | | |

**Internal Feedback Synthesis:**

| Team | What Went Well | What Was Frustrating | What Would They Change |
|------|---------------|---------------------|----------------------|
| Product | | | |
| Marketing | | | |
| Sales | | | |
| Support | | | |
| Engineering | | | |

### Step 3: Root-Cause Mapping

For each material underperformance (Index < 0.80), perform a structured 5-Whys analysis.

**5-Whys Template:**

| Underperformance | Why 1 | Why 2 | Why 3 | Why 4 | Why 5 (Root Cause) |
|-----------------|-------|-------|-------|-------|-------------------|
| Metric: [name], Index: [value] | | | | | |

**Root-Cause Classification:**

| Root Cause | Error Type | Definition | Example |
|-----------|-----------|------------|---------|
| RC1 | Strategy | Wrong approach chosen | Targeted wrong segment |
| RC2 | Execution | Right approach, poor implementation | Campaign launched late, buggy landing page |
| RC3 | Assumption | Incorrect belief about market/customer | Assumed price sensitivity that did not exist |
| RC4 | External | Outside factors beyond control | Competitor launched same week, economic shift |
| RC5 | Timing | Right approach, wrong time | Feature not ready, market not primed |

**Root-Cause Summary:**

| # | Underperformance | Root Cause | Error Type | Controllable? | Fix Difficulty |
|---|-----------------|-----------|-----------|---------------|---------------|
| 1 | | | Strategy/Execution/Assumption/External/Timing | Yes/Partial/No | Easy/Medium/Hard |
| 2 | | | | | |
| 3 | | | | | |

### Step 4: Improvement Scoring and Prioritization

Score each potential improvement on three dimensions to prioritize the next-launch playbook.

**Improvement Scoring Model:**

| # | Improvement | Impact (1-10) | Ease (1-10, inverse) | Confidence (1-10) | Priority Score |
|---|------------|--------------|---------------------|-------------------|---------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |
| 6 | | | | | |
| 7 | | | | | |
| 8 | | | | | |

**Scoring Definitions:**

| Dimension | Weight | 1 (Low) | 5 (Medium) | 10 (High) |
|-----------|--------|---------|-----------|-----------|
| Impact | 40% | Marginal improvement, <5% lift | Moderate improvement, 10-20% lift | Transformative, >30% lift |
| Ease (inverse) | 30% | Requires org change, 6+ months | Cross-team effort, 1-3 months | Single team, <1 month |
| Confidence | 30% | Hypothesis only, no data | Some supporting data | Strong evidence, proven elsewhere |

**Priority Score Formula:**

```
Priority = (Impact x 0.4) + (Ease x 0.3) + (Confidence x 0.3)
```

**Priority Classification:**

| Score Range | Priority | Action |
|------------|---------|--------|
| 8.0 - 10.0 | P0: Implement immediately | Must-do for next launch, assign owner this week |
| 6.0 - 7.9 | P1: Implement next cycle | Plan for next launch, assign owner within 2 weeks |
| 4.0 - 5.9 | P2: Backlog | Good ideas, queue for future improvement |
| < 4.0 | P3: Monitor | Low confidence or low impact, revisit if new data |

### Step 5: Build the Next-Launch Playbook

Compile all P0 and P1 improvements into an actionable playbook.

**Next-Launch Playbook Template:**

| # | Improvement | Priority | Owner | Deadline | Dependencies | Success Metric | Status |
|---|------------|---------|-------|----------|-------------|---------------|--------|
| 1 | | P0 | | | | | Not Started |
| 2 | | P0 | | | | | |
| 3 | | P1 | | | | | |
| 4 | | P1 | | | | | |
| 5 | | P1 | | | | | |

**Assumptions to Revalidate:**

| # | Assumption from This Launch | Was It Valid? | Updated Assumption | Validation Method |
|---|---------------------------|-------------|-------------------|------------------|
| 1 | | Yes/No/Partial | | |
| 2 | | | | |
| 3 | | | | |

**Benchmarks Updated:**

| Metric | Previous Benchmark | Actual This Launch | New Benchmark | Notes |
|--------|-------------------|-------------------|--------------|-------|
| | | | | |
| | | | | |

### Step 6: Launch Comparison (Multi-Launch Trend)

If prior launch debriefs exist, compare trends across launches.

**Cross-Launch Comparison:**

| Dimension | Launch N-2 | Launch N-1 | This Launch | Trend | Notes |
|-----------|-----------|-----------|------------|-------|-------|
| Overall LRI at gate G4 | | | | | |
| Pipeline created (T+30) | | | | | |
| Activation rate (T+30) | | | | | |
| NPS (T+30) | | | | | |
| Budget efficiency (ROI) | | | | | |
| Debrief improvement adoption | | | | | |

## Output

Save to `outputs/launch-debrief/`

### Deliverables:
1. **Launch Scorecard** -- Performance Index for every VITAL metric with actual vs target vs baseline, top 3 over/underperformances, and overall launch grade (A through F based on weighted Performance Index)
2. **Insights Report** -- Win analysis, loss analysis, customer feedback synthesis, and internal feedback synthesis with evidence-backed findings across messaging, channels, content, timing, and audience
3. **Root-Cause Analysis** -- 5-Whys analysis for each material underperformance, classified by error type (Strategy/Execution/Assumption/External/Timing), with controllability and fix-difficulty assessments
4. **Next-Launch Playbook** -- Prioritized improvement list (P0 through P3) using the Impact x Ease x Confidence scoring model, with owners, deadlines, dependencies, and updated benchmarks

## Chain Connections
- **Receives from:** launch-pulse (actual metrics data), launch-command (gate scores, launch plan), budget-allocator (spend actuals), demand-engine (channel performance), battle-scanner (competitive context)
- **Feeds back into:** All future launch cycles -- updated benchmarks flow to launch-pulse, process improvements flow to launch-command, messaging learnings flow to position-lock, channel learnings flow to demand-engine
- **Enhanced by:** growth-loop (post-launch retention data), signal-radar (market context during launch window)
