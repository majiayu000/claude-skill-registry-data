---
name: ad-analyzer
description: Analyze competitor ads from Meta Ad Library or descriptions, extract creative patterns, hooks, and offers, and generate variants. No API keys required.
---

# Ad Analyzer

Analyze competitor advertising creative - hooks, offers, emotional patterns, and CTAs - and generate new variants based on what works.

## What this does

Three phases:

1. **Ad Collection** - Pull ads from Meta Ad Library (public, no login) or analyze provided screenshots/descriptions
2. **Pattern Extraction** - Identify hooks, offers, emotional triggers, and CTA patterns
3. **Variant Generation** - Create new ad variations based on extracted patterns

## How to use

Pass a competitor brand name or Meta Ad Library URL:

```
/ad-analyzer Competidor SA
```

Or with a direct library URL:
```
/ad-analyzer https://www.facebook.com/ads/library/?search_terms=empresa&country=ES
```

Or with screenshots or ad copy pasted directly:
```
/ad-analyzer [paste ad copy or describe the ads you want analyzed]
```

## Phase 1 - Ad Collection

### Option A: Meta Ad Library (public, no login)

The Meta Ad Library is public. Access pattern:
```
https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ES&search_terms=[brand]&media_type=all
```

```python
from scripts.ad_library import scrape_meta_ads

ads = scrape_meta_ads(brand_name=brand, country="ES", limit=20)
# Returns: list of ads with body text, CTA button, media type, start date
```

Focus on:
- Active ads (currently running = currently working or being tested)
- Ads running over 30 days (survived, likely performing)
- Ads with social proof signals in the copy

### Option B: User-provided ad copy

If the user pastes ad copy or describes ads, skip collection and go directly to Phase 2.

Accept:
- Pasted ad copy (text)
- Description of ads seen ("they show a video of X with text saying Y")
- Screenshot descriptions

## Phase 2 - Pattern Extraction

For each ad or batch of ads, extract:

### Hook analysis

The hook is the first 1-2 sentences or the headline. It determines whether someone stops scrolling.

Hook types:
- **Question hook** - "Are you still using X?"
- **Statistic hook** - "83% of [target] struggle with X"
- **Negative hook** - "Stop doing X" / "The real reason your X isn't working"
- **Story hook** - "I used to spend 5 hours a week on X until I found..."
- **Curiosity hook** - "The one thing most [target] get wrong about X"
- **Social proof hook** - "10,000 [target] switched to X because..."
- **Problem statement hook** - "[Specific pain] is costing you [specific cost]"
- **Before/after hook** - "From [before state] to [after state] in [timeframe]"

Identify which hook type is used and whether it is specific or generic.

### Offer analysis

What is the ad actually selling or offering?

- Hard offer: direct purchase, specific price, specific product
- Soft offer: free trial, lead magnet, demo, consultation
- Brand offer: awareness, no explicit CTA
- Content offer: video, guide, article

What is the value proposition in the offer?
- Time saved (quantified or vague)
- Money saved or earned (quantified or vague)
- Pain eliminated (specific or generic)
- Social proof element (specific number or vague)

### Emotional trigger analysis

What feeling is the ad trying to create?

- Fear of missing out
- Frustration with current situation
- Desire for status / recognition
- Desire for simplicity / relief
- Trust / safety
- Exclusivity / insider knowledge

### CTA analysis

- Button text used
- Urgency present? (limited time, spots, offer)
- Landing page type (if detectable from URL)

### Output format

```
## Ad Analysis: [Brand/Campaign]

Ads analyzed: [n]
Active ads running: [n]
Oldest ad in set: [days running]

### Pattern Summary

Most common hook type: [type]
Most common offer type: [type]
Primary emotional trigger: [trigger]
CTA buttons used: [list]

### Individual Ads

**Ad 1:**
Hook: "[first line]"
Hook type: [type]
Offer: [what they're selling/giving]
Emotional trigger: [trigger]
CTA: [button text]
Days running: [n] (longer = more likely performing)
Why it works / why it does not: [1-2 sentences]

**Ad 2:**
[same structure]
```

## Phase 3 - Variant Generation

Based on the patterns found, generate new ad variants.

Rules for variant generation:
- Keep what is working (hook type, offer structure, emotional trigger)
- Change one element at a time
- Generate at least one variant per working pattern
- Each variant needs a hypothesis: "If we change X, we expect Y because Z"

### Variant types

**Hook swap** - Same offer, different hook type
```
Original: "Are you still doing X manually?"
Variant A (statistic): "Teams using X spend 8 hours/week on [task]. Here's how to cut that to 30 minutes."
Variant B (story): "I tracked every hour I spent on X for a month. The number shocked me."
```

**Offer reframe** - Same product, different angle
```
Original: "Try [Product] free for 14 days"
Variant: "See [specific result] in your first session - or your money back"
```

**ICP shift** - Same message, different target audience signal
```
Original: "Perfect for marketing teams"
Variant A: "Built for solo founders who hate spreadsheets"
Variant B: "The tool 500+ CMOs switched to last year"
```

**Urgency variant** - Add or test urgency
```
Original: "Start your free trial"
Variant: "Spots filling up - [n] teams joined this week"
```

### Variant output format

```
## Variants to Test

**Variant 1: [Variant type]**
Hypothesis: Changing [X] to [Y] will increase [click-through / sign-ups] because [reason]

Ad copy:
[full ad copy variant]

CTA: [button text]
Landing page: [type of page this should go to]
Test duration: [minimum days before deciding]
```

## References

- `references/hook-patterns.md` - 15 hook formulas with examples
- `references/creative-formulas.md` - ad frameworks (PAS, AIDA, BAB, 4Ps)

## Output principles

1. Patterns must come from actual ads analyzed - not invented
2. Variants must change one element at a time (for testability)
3. Every variant needs a hypothesis - no "try this" without a reason
4. Hook analysis must identify type + rate specificity (specific beats generic)
5. Never recommend copying a competitor ad - derive the pattern, not the words
