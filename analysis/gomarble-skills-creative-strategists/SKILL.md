---
name: gomarble-skills-creative-strategists
description: "Use for creative strategy frameworks across platforms: ad fatigue detection, hook and hold analysis, creative performance ranking, design and copy audits, A/B test interpretation, audience-to-creative mapping, creative lift forecasts, messaging theme classification, and a weekly creative brief. Pairs with analyse-creative and brief-creative for live GoMarble data."
---

# GoMarble Skills for Creative Strategists

**9 Core Skills + Weekly Brief** for analyzing and optimizing creative performance across platforms.

> **Read-and-recommend only.** These skills never change your ad accounts. The model reads data and produces recommendations in plain language; you apply them manually.

---

## The 9 Skills

### 1. Ad Fatigue Detector
**What it does:** Catches frequency creep and CTR decay before your cost per conversion spikes.

**How it works:**
- Tracks CTR trend over 7-14 days per creative
- Flags when CTR drops >15% from week 1 baseline
- Correlates with frequency increase (>2.0 average reach per user)
- Predicts conversion lift opportunity from refreshing

**Minimum data needed:** Ad-level metrics for last 14 days (CPM, impressions, CTR, frequency)

---

### 2. Hook & Hold Analyzer
**What it does:** Pinpoints which moments lose viewers and what hooks work across platforms.

**How it works:**
- Calculates Hook Rate (% who watch first 3 seconds of video)
- Calculates Hold Rate (% who finish middle section)
- Compares against account average
- Identifies common hook patterns in top 20% performers

**Minimum data needed:** Video plays, 3-second video plays, ThruPlay count per ad

---

### 3. Creative Performance Ranker
**What it does:** Ranks by CTR, CPC, and conversion rate. Shows which creative angles win.

**How it works:**
- Pareto analysis — top 20% of creatives drive 80%+ of value
- Calculates efficiency ratio (CTR ÷ CPC) per creative
- Groups by angle (problem-first, social proof, urgency, scarcity)
- Flags which angles outperform category average

**Minimum data needed:** Ad-level CTR, CPC, conversion count, campaign objective

---

### 4. Design & Copy Auditor
**What it does:** Evaluates ad copy, CTA clarity, and visual hierarchy against best practices.

**How it works:**
- Scores headline length (optimal 3-8 words)
- Checks CTA presence and specificity (vs vague CTAs like "Learn More")
- Rates image/video visual hierarchy (primary focal point clear?)
- Flags copy-to-visual mismatch

**Minimum data needed:** Ad creative (image/video + copy text), CTR, conversion rate

---

### 5. A/B Test Interpreter
**What it does:** Translates CTR and conversion gaps into actionable creative insights.

**How it works:**
- Calculates statistical significance (need 100+ conversions each arm minimum)
- Identifies winning variable (is it the hook? the CTA? the visual?)
- Quantifies lift per variable
- Recommends which elements to keep vs iterate

**Minimum data needed:** Two ad variants with CTR, impressions, conversions, spend each

---

### 6. Audience-to-Creative Mapper
**What it does:** Shows which creative resonates with which audience segment and why.

**How it works:**
- Segments performance by age, geography, device (if available)
- Identifies angle preferences per segment (e.g., younger audiences prefer urgency; older prefer authority)
- Flags creative mismatches (creative designed for one demo, performing poorly there)
- Recommends audience-specific creative rotation

**Minimum data needed:** Ad performance segmented by demographic (age/gender/location)

---

### 7. Creative Lift Forecaster
**What it does:** Estimates how a new creative angle could move ROAS based on peer benchmarks.

**How it works:**
- Compares current account's top angle ROAS vs second-best
- Checks peer benchmark for that angle (via industry data)
- Models revenue impact of replacing bottom 20% with new angle
- Accounts for learning phase loss

**Minimum data needed:** Current ad ROAS, spend, conversions; benchmark data for angle type

---

### 8. Messaging Theme Classifier
**What it does:** Breaks down ad copy themes (urgency, social proof, scarcity) and ranks by conversion.

**How it works:**
- Categorizes ad copy by primary emotional trigger
- Ranks themes by conversion rate and CPA
- Identifies over-reliance on one theme (fatigue risk)
- Recommends theme rotation schedule

**Minimum data needed:** Ad copy text, conversion count, spend per ad

---

### 9. Weekly Creative Brief
**What it does:** Top performers, fatigue alerts, test recommendations. One report, all platforms.

**Includes:**
- Top 3 creatives by ROAS this week
- Ads showing fatigue (CTR down >15%)
- Hook rate / Hold rate averages
- Theme distribution (are you over-reliant on one message?)
- A/B test recommendations for next week
- Platform comparison (which format + audience wins where)

**Minimum data needed:** Full ad account export for last 7 days

---

## How to Use These Skills

1. **Identify what you need** — fatigue check? design audit? angle testing?
2. **Gather the data** — ad-level metrics + creative content
3. **Run the relevant skill** — get diagnosis + recommendations
4. **Apply manually** — pause underperformers, test new angles, rotate themes

---

## Data Requirements by Source

| Skill | MCP (GoMarble/Meta) | CSV Export | Manual |
|---|---|---|---|
| Ad Fatigue Detector | ✅ | ✅ | ⚠️ spot-check only |
| Hook & Hold Analyzer | ✅ | ✅ (if video metrics enabled) | ❌ |
| Creative Performance Ranker | ✅ | ✅ | ✅ |
| Design & Copy Auditor | ✅ (via creative endpoint) | ❌ (content not in CSV) | ✅ (upload image/video) |
| A/B Test Interpreter | ✅ | ✅ | ⚠️ |
| Audience-to-Creative Mapper | ✅ | ⚠️ (needs breakdown export) | ⚠️ |
| Creative Lift Forecaster | ✅ | ✅ | ⚠️ |
| Messaging Theme Classifier | ✅ | ✅ | ✅ |
| Weekly Creative Brief | ✅ | ✅ (7-day export) | ❌ |

✅ = works perfectly | ⚠️ = requires manual input or separate export | ❌ = not possible from this source

---

## Key Metrics Reference

| Metric | Definition | Good Benchmark |
|---|---|---|
| Hook Rate (video) | % of viewers who watch first 3 seconds | ≥40% |
| Hold Rate (video) | % of viewers who finish the middle section | Account average + 5% |
| CTR | Click-through rate | ≥ 1.25% (depends on platform) |
| Frequency | Avg times same user sees ad | 1.5–2.0 (above = fatigue risk) |
| ROAS | Revenue per dollar spent | ≥3.0 for profitable |
| CPA | Cost per acquisition | ≤ 40% of customer LTV |

---

## Output Format for Recommendations

```
### [Skill Name]: [Creative Name]

Finding:
[1–2 sentences describing the issue or opportunity]

Data:
| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| [Metric] | X | Y | [Good/Poor] |

Recommendation:
1. [Specific action with rationale]
2. [Specific action with rationale]
```

---

## When to Run Each Skill

| Situation | Use Skill | Timeline |
|---|---|---|
| CTR dropping on top ad | Ad Fatigue Detector | Weekly |
| Video not performing | Hook & Hold Analyzer | After 5K plays minimum |
| Too many similar ads | Creative Performance Ranker + Messaging Theme Classifier | Biweekly |
| Testing new angle | A/B Test Interpreter | After 100 conversions per arm |
| Expanding to new region | Audience-to-Creative Mapper | After change |
| Planning sprint | Weekly Creative Brief | Every Monday |

---

## Common Guardrails

**Before recommending a pause or rotation:**
- ✅ Confirm fatigue signal is real (CTR down >15%, frequency >2.0)
- ✅ Confirm replacement creative is ready to launch (don't create gap)
- ✅ Keep top 20% performers running while testing new angles
- ✅ Never pause an ad mid-learning phase (<50 conversions)

**Before recommending a new angle:**
- ✅ Confirm current angle is mature (30+ days data)
- ✅ Ensure spend budget for testing (usually 10–20% of total)
- ✅ Have the creative ready before recommending (not hypothetical)

---

## Questions to Ask Yourself

- Am I testing one variable at a time? (angle, audience, placement, format)
- Do I have 100+ conversions per variant for statistical significance?
- Is my top performer still running while I test? (don't stop the winner)
- Am I rotating themes or stuck on urgency?
- What does my Hold Rate tell me vs my CTR?

---

## Next Steps

1. Pull your ad data (last 7–30 days)
2. Choose 2–3 skills to run this week
3. Apply recommendations to 10–20% of spend first
4. Measure results, iterate

