---
name: startup-metrics
description: >
  Core startup metrics framework by business model and stage-specific benchmarks for SaaS, Marketplace, Consumer, and B2B.
  Triggers on "startup metrics", "key metrics", "KPI", "metrics", "benchmark", "investor reporting",
  "스타트업 지표", "핵심 지표", "KPI", "메트릭스", "벤치마크", "투자자 보고" requests.
---

# Startup Metrics

> For unfamiliar placeholders or to check connected tools, see [CONNECTORS.md](../../CONNECTORS.md).

Provides core startup metrics framework by business model and stage-specific benchmarks. Delivers metric sets optimized for SaaS, Marketplace, Consumer, and B2B models, with target numbers by funding stage (Pre-seed through Series B).

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    STARTUP METRICS FRAMEWORK                    │
├─────────────────────────────────────────────────────────────────┤
│  Core Features (Standalone)                                      │
│  ✓ Auto-detect business model (SaaS/Marketplace/Consumer/B2B)   │
│  ✓ Model-specific metric sets (North Star + supporting metrics)  │
│  ✓ Stage benchmarks by round (Pre-seed ~ Series B)               │
│  ✓ Investor-ready metrics dashboard generation                  │
├─────────────────────────────────────────────────────────────────┤
│  Enhanced Mode (With Connectors)                                 │
│  + ~~analytics: Auto-collect real-time metric data               │
│  + ~~spreadsheet: Cohort analysis and trend charts               │
│  + ~~knowledge base: Extract benchmarks from past reports        │
└─────────────────────────────────────────────────────────────────┘
```

## Getting Started

1. **Identify business model**: "What are the key metrics for our SaaS product?"
2. **Compare benchmarks**: "How do we compare to Pre-seed SaaS benchmarks?"
3. **Investor reporting**: "Create a monthly metrics dashboard for investors"
4. **Improve metrics**: "Which metrics should we focus on to improve NRR?"

## Core Metrics by Business Model

### 1. SaaS (Software as a Service)

#### North Star Metric
- **ARR/MRR** (Annual/Monthly Recurring Revenue)

#### Core Metrics (8)
| Metric | Definition | Target | Calculation |
|--------|-----------|--------|-------------|
| **MRR Growth** | Monthly recurring revenue growth rate | 10-20%/mo (early) | (MRR_this_month - MRR_last_month) / MRR_last_month |
| **NRR** | Net Revenue Retention | >100% (strong: >120%) | (Start ARR + Expansion - Contraction - Churn) / Start ARR |
| **CAC** | Customer Acquisition Cost | < LTV/3 | Total Marketing+Sales / New Customers |
| **LTV** | Lifetime Value | > CAC × 3 | ARPA × Gross Margin % / Churn Rate |
| **CAC Payback** | Payback period | < 12mo (strong: < 6mo) | CAC / (ARPA × Gross Margin %) |
| **Burn Multiple** | Burn vs revenue growth | < 1.5x (strong: < 1.0x) | Net Burn / Net New ARR |
| **Rule of 40** | Growth + profitability | > 40% | ARR Growth % + EBITDA Margin % |
| **Magic Number** | S&M efficiency | > 0.75 (strong: > 1.0) | Net New ARR / Prior Quarter S&M Spend |

#### Supporting Metrics
- **Quick Ratio**: (New MRR + Expansion MRR) / (Contraction MRR + Churn MRR) — Target > 4x
- **Gross Margin**: Target > 70% (mature SaaS > 80%)
- **Churn Rate**: <2%/mo (<20%/yr), Logo Churn < Revenue Churn
- **Expansion MRR %**: Expansion revenue as % of total MRR — Target > 10%

### 2. Marketplace

#### North Star Metric
- **GMV** (Gross Merchandise Value) or **Net Revenue**

#### Core Metrics (7)
| Metric | Definition | Target | Calculation |
|--------|-----------|--------|-------------|
| **GMV Growth** | Total transaction volume growth rate | 15-30%/mo (early) | (GMV_this_month - GMV_last_month) / GMV_last_month |
| **Take Rate** | Commission rate | 10-30% (varies by category) | Net Revenue / GMV |
| **Liquidity** | Supply-demand balance | > 80% match rate | Completed Transactions / Total Requests |
| **Buyer Retention** | Buyer repeat purchase rate | >30%/mo, >60%/yr | Repeat Buyers This Month / Total Buyers |
| **Seller Retention** | Seller retention rate | >70%/mo, >50%/yr | Active Sellers This Month / Prior Month |
| **Repeat Tx %** | Repeat transaction share | > 40% (mature > 60%) | Repeat GMV / Total GMV |
| **Supply Utilization** | Supply utilization | > 60% | Sellers with Transactions / Total Sellers |

#### Supporting Metrics
- **Average Order Value (AOV)**: Avg amount per transaction
- **Frequency**: Avg monthly transactions per customer
- **Contribution Margin**: (Net Revenue - Variable Costs) / Net Revenue — Target > 20%
- **Time to Liquidity**: Time for new category to reach 80% match rate

### 3. Consumer / Social

#### North Star Metric
- **DAU** (Daily Active Users) or **Engagement**

#### Core Metrics (6)
| Metric | Definition | Target | Calculation |
|--------|-----------|--------|-------------|
| **DAU / MAU** | Daily / Monthly active user ratio | > 20% (strong: > 50%) | DAU / MAU |
| **L7/L28** | Weekly/monthly engagement | > 50% | Active Last 7 Days / Active Last 28 Days |
| **D1/D7/D30 Retention** | Post-signup return rate | D1 > 40%, D7 > 20%, D30 > 10% | Day N Active / Day 0 Signups |
| **K-factor** | Viral coefficient | > 1.0 (explosive growth) | (Invites × Conversion Rate) × Repeat |
| **Session Length** | Avg session duration | Category-dependent | Total Session Time / Session Count |
| **Frequency** | Weekly visit frequency | > 3x/week (habit formation) | Total Sessions / Weekly Active Users |

#### Supporting Metrics
- **Activation Rate**: % reaching "Aha moment" post-signup — Target > 30%
- **Retention Curves**: Long-term cohort retention (identify plateau point)
- **Resurrection Rate**: Reactivated churned user %
- **Stickiness**: DAU / MAU × 100 (higher = stronger habit)

### 4. B2B (Enterprise / SMB)

#### North Star Metric
- **ARR** (Annual Recurring Revenue) or **Bookings**

#### Core Metrics (8)
| Metric | Definition | Target | Calculation |
|--------|-----------|--------|-------------|
| **Win Rate** | Sales close rate | 20-40% (Ent), 10-20% (SMB) | Won Deals / Total Opportunities |
| **Sales Cycle** | Avg sales duration | SMB 30-60d, Mid 60-120d, Ent 120-270d | Avg (Close Date - Opp Create Date) |
| **ACV** | Average Contract Value | Ent >$100K, SMB $10K-50K | Total Contract Value / Contract Years |
| **Pipeline Coverage** | Pipeline coverage ratio | 3-5x quota | Total Pipeline Value / Quarterly Quota |
| **Lead Velocity Rate** | Qualified lead growth | 10-20%/month | (This Month Leads - Prior Month) / Prior |
| **Conversion Rates** | Stage conversion | Lead→Opp 10-20%, Demo→Prop 30-50% | Next Stage / Current Stage |
| **Customer Concentration** | Customer concentration | Top 5 < 50% ARR | Top 5 ARR / Total ARR |
| **Expansion ARR** | Existing customer expansion | > 30% of New ARR | Upsell + Cross-sell / Total New ARR |

#### Supporting Metrics
- **Sales Productivity**: ARR per sales rep — Target > $500K (mature > $1M)
- **NPS** (Net Promoter Score): Target > 30 (strong: > 50)
- **Time to Value**: Time from contract to first value — Target < 30 days
- **Implementation Time**: Onboarding completion timeline

## Metrics by Funding Stage

### Pre-seed / Seed
**Primary Goal**: Validate Product-Market Fit

| Stage | Core Metrics | Benchmarks |
|-------|-------------|-----------|
| **Pre-seed** | • Activation Rate<br>• D7/D30 Retention<br>• Qualitative Feedback | • First value realization > 30%<br>• D7 Retention > 20%<br>• "Would be very disappointed" > 40% |
| **Seed** | • MRR/GMV Growth<br>• Unit Economics (CAC/LTV)<br>• Retention Curves | • 10-15%/mo growth<br>• LTV:CAC > 1:1 (early acceptable)<br>• Flattening curve |

### Series A
**Primary Goal**: Scalable Growth Engine

| Core Metric | Benchmark |
|-----------|----------|
| MRR/GMV Growth | 8-12%/mo (2.5-3.5x/yr) |
| CAC Payback | < 18 months |
| LTV:CAC | > 3:1 |
| NRR (SaaS) | > 100% |
| Burn Multiple | < 2.0x |

### Series B
**Primary Goal**: Efficient Growth + Path to Profitability

| Core Metric | Benchmark |
|-----------|----------|
| ARR/GMV Growth | 5-8%/mo (1.8-2.5x/yr) |
| Rule of 40 | > 30% (target > 40%) |
| CAC Payback | < 12 months |
| Gross Margin | > 70% (SaaS), > 30% (Marketplace) |
| Magic Number | > 0.75 |
| Burn Multiple | < 1.5x |

**Detailed Benchmarks**: See [references/benchmarks-by-stage.md](references/benchmarks-by-stage.md)

## Output Format

### Metrics Dashboard (Investor-ready)

```markdown
# [Company Name] Monthly Metrics Dashboard
**Reporting Period**: [YYYY-MM] | **Business Model**: [SaaS/Marketplace/Consumer/B2B]

## 📊 North Star Metric
- **[ARR/MRR/GMV/DAU]**: $X.XM (+Y% vs prior month)
- **Goal Achievement**: Z% (monthly target $X.XM)

## 🎯 Core Metrics (MoM)

| Metric | Current | Prior Month | Change | Benchmark | Status |
|--------|---------|-------------|--------|-----------|--------|
| MRR Growth | 12% | 10% | +2%p | 10-15% | 🟢 |
| NRR | 108% | 105% | +3%p | >100% | 🟢 |
| CAC Payback | 14mo | 16mo | -2mo | <18mo | 🟡 |
| Burn Multiple | 1.8x | 2.1x | -0.3x | <2.0x | 🟢 |

🟢 = Target met/exceeded  |  🟡 = Caution  |  🔴 = Needs improvement

## 📈 Cohort Analysis (Retention)
[Monthly cohort table or chart]

## 💡 Insights
- **Positive**: [2-3 key wins]
- **Concerns**: [1-2 areas needing improvement]
- **Next Month Focus**: [Key metrics and targets]
```

## Execution Flow

1. **Detect Model**: Auto-classify as SaaS/Marketplace/Consumer/B2B from description
2. **Identify Stage**: Determine Pre-seed/Seed/Series A/B (explicit or traction-based)
3. **Select Metrics**: Choose 5-8 metrics optimized for model + stage
4. **Collect Data**:
   - Basic: User input or file upload
   - Enhanced: Auto-collect from ~~analytics tools
5. **Compare to Benchmarks**: Assess current metrics vs stage targets
6. **Generate Dashboard**: Investor-ready format or internal monitoring
7. **Provide Insights**: Prioritized improvements and action recommendations

## Metrics-Specific Improvement Strategies

### Improve NRR (SaaS)
1. **Strengthen Expansion**: Build upsell/cross-sell motions
2. **Reduce Churn**: Early identify at-risk customers (Health Score)
3. **Prevent Downsells**: Transition from usage-based to feature-based pricing

### Improve Liquidity (Marketplace)
1. **Acquire Supply**: Seller onboarding incentives, exclusive inventory
2. **Activate Demand**: Buyer acquisition campaigns, repeat loops
3. **Optimize Matching**: Search/recommendation algorithms, category refinement

### Improve Retention (Consumer)
1. **Strengthen Activation**: Shorten time to "Aha moment", optimize onboarding
2. **Build Habit**: Push notifications, email reminders, streak systems
3. **Enable Network Effects**: Social features, viral loops, community

### Improve Win Rate (B2B)
1. **Refine ICP**: Focus on highest-win-rate segments
2. **Enable Sales**: Battlecards, demo environments, ROI calculators
3. **Handle Objections**: Standardized responses to common concerns

## Connectable Tools

| Tool Category | Placeholder | Purpose | Example Tools |
|---------------|-------------|---------|----------------|
| Analytics Platform | `~~analytics` | Auto-collect real-time metric data | Mixpanel, Amplitude, Segment |
| Spreadsheet | `~~spreadsheet` | Cohort analysis, trend charts | Google Sheets, Excel |
| Knowledge Base | `~~knowledge base` | Extract benchmarks from past reports | Notion, Confluence |
| BI Tool | (~~analytics) | Dashboard visualization | Looker, Tableau, Metabase |

## Related Skills

- **financial-modeling** — Integrate metrics into financial models
- **fundraise-comms** — Include metrics in investor updates
- **market-sizing** — Reverse-engineer metrics for TAM/SAM achievement
- **gtm-strategy** — Select key metrics by GTM motion

## Tips

- **Less is More**: Focus on 5-8 core metrics. Tracking 30 kills execution
- **Stage-specific Focus**: Pre-seed emphasizes Retention, Seed emphasizes Unit Economics, Series A+ emphasizes efficiency
- **Cohort Analysis Required**: Averages mislead. Cohort analysis reveals true trends
- **Benchmarks as Reference Only**: Vary by industry/region/model. Compare vs your own history first
- **Leading vs Lagging**: CAC/LTV are lagging; Pipeline Coverage/Lead Velocity are leading
- **Investor Perspective**: Rule of 40, Burn Multiple, CAC Payback are most VC-watched
- **Consistency Matters**: Definition of same metric varies by company. Once defined, maintain consistently
