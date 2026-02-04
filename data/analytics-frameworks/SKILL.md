---
name: analytics-frameworks
description: |
  Load when analyzing performance metrics, creating reports, setting up tracking,
  evaluating growth experiments, or any task involving data-driven decision making
  for content and audience growth. Contains KPIs, benchmarks, and reporting frameworks.
---

# Analytics Frameworks Skill

## Core Philosophy

> "What gets measured gets managed. What gets managed poorly gets measured excessively."

Analytics should drive action, not just reporting. Focus on metrics that inform decisions, not vanity metrics that feel good but don't guide strategy.

## Fundamental Principles

### 1. Metrics Hierarchy

```
North Star Metric
└── Primary KPIs (3-5 max)
    └── Secondary Metrics
        └── Diagnostic Metrics
```

**For a publication like tacosdedatos:**
```
North Star: Active Engaged Subscribers
├── Newsletter subscribers
├── Open rate (engagement quality)
├── Click rate (content value)
└── Organic traffic (reach)
```

### 2. Leading vs. Lagging Indicators

| Type | Description | Examples |
|------|-------------|----------|
| Leading | Predict future outcomes | Social engagement, email signups, page views |
| Lagging | Measure past outcomes | Revenue, churn, lifetime value |

Focus on leading indicators for day-to-day decisions.

### 3. Actionable Metrics

A good metric should:
- Be tied to a specific action you can take
- Have a clear threshold for success
- Be comparable over time
- Not be easily gamed

## Newsletter Analytics

### Key Metrics

| Metric | Calculation | Healthy Benchmark |
|--------|-------------|-------------------|
| Open Rate | Opens / Delivered × 100 | 40%+ (industry avg: 43%) |
| Click Rate (CTR) | Clicks / Delivered × 100 | 2-5% |
| Click-to-Open Rate (CTOR) | Clicks / Opens × 100 | 10-15% |
| Unsubscribe Rate | Unsubscribes / Delivered × 100 | <0.5% |
| Bounce Rate | Bounces / Sent × 100 | <2% |
| List Growth Rate | (New - Unsubscribes) / Total × 100 | 2-5%/month |

### Apple Mail Privacy Protection (MPP) Considerations

```
⚠️ Important: Since iOS 15 (2021), Apple MPP pre-loads email content,
artificially inflating open rates.

What this means:
- Open rates are now ~10-20% higher than actual
- Apple Mail is ~46% of email clients
- Focus on click-based metrics instead

Adjusted Strategy:
1. Primary metric: Click rate (not open rate)
2. Secondary: Click-to-open rate
3. Segment Apple Mail users separately
4. Use multiple data points for decisions
```

### Reporting Cadence

**Daily (Quick Check):**
```
- Open rate vs. 7-day average
- Click rate
- Unsubscribes (any spikes?)
- Bounce rate
```

**Weekly (Performance Review):**
```
## Newsletter Performance: Week of [Date]

### Overview
| Metric | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| Emails Sent | X | Y | +/-% |
| Open Rate | X% | Y% | +/-% |
| Click Rate | X% | Y% | +/-% |
| Unsubscribes | X | Y | +/-% |

### Top Performing Links
1. [Link] - X clicks (X% CTR)
2. [Link] - X clicks
3. [Link] - X clicks

### Insights
- [What worked]
- [What didn't]
- [Experiment to try]
```

**Monthly (Strategic Review):**
```
## Monthly Newsletter Report: [Month Year]

### Subscriber Growth
- Starting: X
- Ending: Y
- Net Growth: +/-Z (X%)
- Sources: [Organic: X, Referral: Y, Paid: Z]

### Engagement Trends
[Chart showing open/click rates over time]

### Content Performance
| Edition | Subject Line | Open Rate | Click Rate |
|---------|--------------|-----------|------------|
| [Date] | [Subject] | X% | Y% |

### Referral Program Performance
- Active referrers: X
- New subscribers from referrals: Y
- Top referrers: [List]

### Recommendations
1. [Strategic recommendation]
2. [Content adjustment]
3. [Experiment proposal]
```

## Website/Blog Analytics

### Key Metrics

| Metric | What It Measures | Target |
|--------|------------------|--------|
| Sessions | Site visits | Growth month-over-month |
| Unique Visitors | Individual users | Growth month-over-month |
| Pageviews | Pages viewed | Higher than sessions |
| Avg. Session Duration | Engagement depth | 2+ minutes for articles |
| Bounce Rate | Single-page visits | <70% for blog content |
| Pages/Session | Content discovery | 1.5+ |

### Google Analytics 4 Key Reports

**Acquisition:**
```
Traffic Sources:
- Organic Search: SEO effectiveness
- Direct: Brand recognition
- Referral: Partnership/link value
- Social: Social media ROI
- Email: Newsletter impact
```

**Engagement:**
```
Key Events to Track:
- page_view
- scroll (25%, 50%, 75%, 90%)
- click (external links, CTAs)
- newsletter_signup
- social_share
```

**Content Performance:**
```
## Content Report: [Period]

### Top Content by Pageviews
| Page | Views | Avg. Time | Bounce |
|------|-------|-----------|--------|
| [Page] | X | X:XX | X% |

### Top Entry Pages
[Where users start their journey]

### Top Organic Landing Pages
[SEO performance]

### Underperforming Content
[Pages with high traffic but high bounce or low time]
```

### UTM Tracking

**Standard UTM Structure:**
```
URL: https://tacosdedatos.com/tutorial/pandas-groupby

With UTMs:
?utm_source=[platform]
&utm_medium=[type]
&utm_campaign=[campaign-name]
&utm_content=[specific-link]

Examples:
Newsletter link:
?utm_source=newsletter&utm_medium=email&utm_campaign=weekly-2024-01-15&utm_content=main-article

Twitter bio:
?utm_source=twitter&utm_medium=social&utm_campaign=bio-link

Referral partner:
?utm_source=partner-newsletter&utm_medium=referral&utm_campaign=cross-promo
```

**UTM Naming Convention:**
```
Sources: newsletter, twitter, linkedin, google, partner-name
Mediums: email, social, organic, paid, referral
Campaigns: [type]-[date or name]
Content: [descriptive-slug]
```

## Social Media Analytics

### Platform Metrics

**Twitter/X:**
```
Engagement Rate = (Likes + Retweets + Replies + Clicks) / Impressions × 100

Benchmarks:
- Good: 2%+
- Great: 4%+
- Viral: 10%+

Key Metrics:
- Impressions (reach)
- Profile visits (curiosity)
- Follower growth (sustained interest)
- Link clicks (conversion)
```

**LinkedIn:**
```
Engagement Rate = (Likes + Comments + Shares + Clicks) / Impressions × 100

Benchmarks:
- Good: 2%+
- Great: 5%+
- Excellent: 8%+

Note: First-hour engagement heavily affects reach
```

### Social Media Report Template

```markdown
## Social Media Report: [Period]

### Platform: Twitter/X

#### Overview
| Metric | This Period | Previous | Change |
|--------|-------------|----------|--------|
| Followers | X | Y | +/-Z |
| Impressions | X | Y | +/-% |
| Engagement Rate | X% | Y% | +/-% |
| Profile Visits | X | Y | +/-% |
| Link Clicks | X | Y | +/-% |

#### Top Performing Content
1. [Tweet text snippet]
   - Impressions: X
   - Engagement: X%
   - Why it worked: [Analysis]

2. [Tweet text snippet]
   - Impressions: X
   - Engagement: X%

#### Content Type Performance
| Type | Posts | Avg. Engagement | Best Day |
|------|-------|-----------------|----------|
| Thread | X | X% | [Day] |
| Single Tweet | X | X% | [Day] |
| Quote Tweet | X | X% | [Day] |

#### Recommendations
- [What to do more of]
- [What to stop doing]
- [Experiment to try]
```

## Growth Experiment Framework

### A/B Testing Structure

```markdown
## Experiment: [Name]

### Hypothesis
If we [change X], then [metric Y] will [improve by Z%] because [reasoning].

### Variables
- **Control (A)**: [Current state]
- **Treatment (B)**: [New approach]

### Success Metrics
- **Primary**: [Metric] (minimum detectable effect: X%)
- **Secondary**: [Metric]
- **Guardrail**: [Metric we don't want to hurt]

### Sample Size & Duration
- Traffic/day: X
- Required sample: Y per variant
- Duration: Z days

### Results
| Variant | Sample | [Primary Metric] | [Secondary] |
|---------|--------|------------------|-------------|
| Control | X | Y% | Z% |
| Treatment | X | Y% | Z% |

**Statistical Significance**: X% confidence
**Winner**: [A/B/No clear winner]

### Learnings
- [What we learned]
- [What to test next]

### Decision
☑️ Implement Treatment
☐ Keep Control
☐ Run follow-up test
```

### Common Growth Experiments

```
Newsletter:
- Subject line variations
- Send time optimization
- CTA placement and copy
- Content length
- Personalization

Website:
- Headline variations
- CTA button color/copy
- Form field count
- Social proof placement
- Content layout

Social:
- Posting times
- Content formats
- Hashtag strategies
- Hook variations
- Thread length
```

## Reporting Templates

### Executive Summary (Weekly)

```markdown
# Growth Summary: Week of [Date]

## Headline Metrics
| Metric | This Week | Target | Status |
|--------|-----------|--------|--------|
| Newsletter Subs | X (+Y) | Z/week | 🟢/🟡/🔴 |
| Open Rate | X% | 40%+ | 🟢/🟡/🔴 |
| Organic Traffic | X | +5%/week | 🟢/🟡/🔴 |
| Social Followers | X (+Y) | +2%/week | 🟢/🟡/🔴 |

## Key Wins
1. [Win and why it matters]
2. [Win and why it matters]

## Challenges
1. [Challenge and proposed action]

## Next Week Focus
- [Priority 1]
- [Priority 2]
```

### Monthly Growth Report

```markdown
# Monthly Growth Report: [Month Year]

## Executive Summary
[2-3 sentence overview]

## Key Metrics Dashboard

### Newsletter
| Metric | [Month] | Previous | MoM Change | YoY |
|--------|---------|----------|------------|-----|
| Total Subscribers | X | Y | +Z% | +W% |
| Open Rate | X% | Y% | | |
| Click Rate | X% | Y% | | |
| Unsubscribe Rate | X% | Y% | | |

### Website
| Metric | [Month] | Previous | Change |
|--------|---------|----------|--------|
| Sessions | X | Y | +/-% |
| Unique Visitors | X | Y | +/-% |
| Organic Traffic | X | Y | +/-% |
| Avg. Session Duration | X:XX | Y:YY | |

### Social
| Platform | Followers | Engagement | Top Post |
|----------|-----------|------------|----------|
| Twitter | X (+Y) | Z% | [Link] |
| LinkedIn | X (+Y) | Z% | [Link] |

## Growth Initiatives

### What Worked
1. **[Initiative]**: [Result and learning]
2. **[Initiative]**: [Result and learning]

### What Didn't Work
1. **[Initiative]**: [Learning and adjustment]

### Experiments Run
| Experiment | Result | Decision |
|------------|--------|----------|
| [Name] | [Outcome] | Implement/Discard/Iterate |

## Recommendations for Next Month
1. **Priority**: [Recommendation]
2. **Test**: [Experiment proposal]
3. **Optimize**: [Improvement area]

## Goals for Next Month
| Goal | Target | Baseline |
|------|--------|----------|
| [Goal] | X | Y |
```

## Quality Checklist for Analytics

```markdown
Before making decisions based on data:

### Data Quality
- [ ] Sample size is sufficient
- [ ] Time period is representative
- [ ] No major external factors (holidays, outages)
- [ ] Data source is reliable

### Analysis Quality
- [ ] Compared to appropriate baseline
- [ ] Considered seasonality
- [ ] Checked for statistical significance
- [ ] Looked for confounding variables

### Decision Quality
- [ ] Metric is tied to business outcome
- [ ] Action is clear and feasible
- [ ] Success criteria defined
- [ ] Follow-up plan in place
```

## Resources

- [Google Analytics Academy](https://analytics.google.com/analytics/academy/)
- [GetResponse Benchmarks](https://www.getresponse.com/resources/reports/email-marketing-benchmarks)
- [Mailchimp Benchmarks](https://mailchimp.com/resources/email-marketing-benchmarks/)
- [Buffer Analytics Guides](https://buffer.com/library/)
