---
name: meta-ads-optimizer
description: Meta Ads automation with global market optimization
author: "@namanwtf"
version: 3.0.0
requires: brand-context, copywriting, analytics-dashboard
category: paid-ads
---

# 🎯 Meta Ads Optimizer

**Purpose:** Automate Meta Ads campaigns with market-specific optimizations, seasonal calendar targeting, and performance scaling.

---

## When to Use

```bash
@meta-ads-optimizer create campaign "Summer Sale"
@meta-ads-optimizer optimize --roas-target 2.5
@meta-ads-optimizer scale --budget-increase 20%
```

Use this skill when:
- Launching new Meta Ads campaigns
- Optimizing existing campaigns for ROAS
- Scaling winning ad sets
- Creating seasonal campaigns
- A/B testing ad creatives

---

## Quick Commands

```bash
@meta-ads-optimizer create campaign "Product X Launch"
@meta-ads-optimizer optimize --roas-target 2.5
@meta-ads-optimizer creative-rotate --fatigue-threshold 1.5
@meta-ads-optimizer scale --budget-increase 20% --if-roas-above 2.0
```

---

## Market Optimizations

### Audience Targeting
- **Lookalike audiences:** 1%, 3%, 5% from converters
- **Interest targeting:** Based on brand context
- **Behavioral:** Engaged shoppers, recent travelers
- **Custom audiences:** Website visitors, email lists

### Seasonal Calendar
```yaml
Campaigns:
  - Holiday Season: Nov-Dec (highest CPM, highest conversion)
  - Spring Sale: Mar-Apr (new product launches)
  - Back to School: Aug-Sep (education/tech focus)
  - Summer: Jun-Jul (travel, lifestyle products)
  - Black Friday: Nov (biggest discount event)
```

### Creative Best Practices
- **Format:** 9:16 vertical video (Stories/Reels)
- **Length:** 15-30 seconds
- **Hook:** First 3 seconds critical
- **Audio:** Trending music or brand-appropriate sounds
- **CTA:** "Shop Now" or "Learn More"

---

## Auto-Optimization Rules

```javascript
// Budget Scaling
if (ROAS > 2.5 && Spend > 100) {
  IncreaseBudget(20%)
}

// Creative Fatigue
if (CTR < 1.0 && Frequency > 3) {
  PauseAd()
  Notify("Creative fatigue detected")
}

// Audience Overlap
if (Overlap > 30%) {
  MergeAdSets()
}
```

---

## Configuration

Add to your `brand-context.md`:

```yaml
meta-ads-optimizer:
  target-roas: 2.5
  target-cpa: 25
  daily-budget: 100
  
  audiences:
    lookalike:
      - source: "purchasers"
        percentage: 1
      - source: "website-visitors"
        percentage: 3
    
    interests:
      - "technology"
      - "online shopping"
      
  optimization:
    auto-scale: true
    fatigue-threshold: 1.5
    overlap-merge: true
```

---

## Usage Examples

### Create Campaign
```
User: @meta-ads-optimizer create campaign "Spring Launch"

Agent: 🎯 CAMPAIGN CREATED

Campaign: Spring Launch
Objective: Conversions
Budget: $100/day

Ad Sets:
1. Lookalike 1% (Purchasers)
   - Audience size: 2.1M
   - Placements: Feed, Stories, Reels
   
2. Website Visitors (30 days)
   - Audience size: 45K
   - Placements: Feed, Stories

Creative Strategy:
- 3 video ads (15-30 sec)
- 2 carousel ads
- A/B test hooks in first 3 seconds

Launch scheduled for tomorrow 9 AM.
```

### Optimize Performance
```
User: @meta-ads-optimizer optimize

Agent: 📊 OPTIMIZATION REPORT

Current Performance:
• ROAS: 2.8 ✅ (above target 2.5)
• CPA: $22 ✅ (below target $25)
• CTR: 1.2%

Actions Taken:
✅ Scaled "Lookalike 1%" budget by 20%
✅ Paused "Interest: Gaming" (CTR 0.6%)
✅ Duplicated winning creative with new hook

Recommendations:
→ Test new audience: Lookalike 3%
→ Refresh creative (frequency 2.8)
```

---

## Related Skills

- **copywriting**: Ad copy creation
- **analytics-dashboard**: Performance tracking
- **competitive-intel**: Competitor ad monitoring

---

*Part of the Brand Marketing Team framework.*
*Author: @namanwtf | Version 3.0.0 | MIT License*
