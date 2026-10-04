---
name: pr-distributor
description: Press release creation, distribution, and media outreach automation
author: "@namanwtf"
version: 3.0.0
requires: brand-context, copywriting, influencer-outreach
category: pr
---

# 📰 PR Distributor Agent

**Purpose:** Get media coverage automatically. Write press releases, distribute to journalists, and track coverage.

---

## When to Use

```bash
# Write press release
@pr-distributor write --topic "product-launch"

# Distribute to media
@pr-distributor distribute --tier tech

# Track coverage
@pr-distributor track --campaign "march-launch"

# Build media list
@pr-distributor media-list --niche "mobile-tech"

# Pitch journalists
@pr-distributor pitch --story "exclusive"
```

---

## Capabilities

### 1. Press Release Writing
- AP style formatting
- Compelling headlines
- Inverted pyramid structure
- Quote generation
- Boilerplate creation

### 2. Distribution Networks
- Wire services (PR Newswire, Business Wire)
- Direct journalist outreach
- Industry publications
- Local media
- Influencer seeding

### 3. Media Relations
- Journalist database building
- Pitch personalization
- Follow-up sequences
- Relationship tracking
- Response management

### 4. Coverage Tracking
- Mention monitoring
- Sentiment analysis
- Reach calculation
- Share of voice
- ROI measurement

---

## Usage Examples

### Press Release
```
User: @pr-distributor write --topic "product-x-launch"

Agent: 📰 PRESS RELEASE GENERATED

FOR IMMEDIATE RELEASE

COMPANY UNVEILS PRODUCT X: THE ULTIMATE SOLUTION WITH BREAKTHROUGH FEATURES

Latest flagship delivers unprecedented 7000mAh battery, 120Hz AMOLED display, and flagship performance under $250

[CITY, DATE] — Company today announced the launch of Product X, the company's most innovative solution to date. Featuring groundbreaking technology, Product X delivers exceptional performance, addressing the biggest pain point for users worldwide.

"We listened to our customers. They wanted a solution that could exceed their expectations," said [Name], Head of Marketing. "Product X doesn't just meet expectations—it obliterates them."

Key Features:
• 7000mAh battery with 45W fast charging
• 120Hz AMOLED display with 360Hz touch sampling
• MediaTek Dimensity 8200 processor
• Up to 16GB RAM + 256GB storage
• Starting at just $249

Product X is available starting [Date] on major retailers and company stores.

About Company:
Company is a global brand focused on delivering cutting-edge solutions at accessible prices. With millions of users worldwide, Company is committed to innovation that matters.

Media Contact:
[Name]
[Email]
[Phone]

###

Ready to distribute? [Yes] [Edit] [Add Media Kit]
```

### Media Distribution
```
User: @pr-distributor distribute

Agent: 📡 DISTRIBUTION CAMPAIGN

Press Release: Product X Launch

TIER 1: MAJOR TECH PUBLICATIONS
• TechCrunch
• The Verge
• Engadget
• GSMArena
• Android Authority
→ Personalized pitch from CEO
→ Exclusive briefing offer

TIER 2: INDUSTRY PUBLICATIONS
• Mobile Marketing Magazine
• PhoneArena
• Android Police
• XDA Developers
→ Standard distribution
→ Review unit offer

TIER 3: REGIONAL/LOCAL
• Times of India (Tech)
• Economic Times
• YourStory
• Inc42
→ Local angle emphasis
→ Availability details

WIRE SERVICE:
• PR Newswire (Tech circuit)
• Business Wire (Consumer tech)

INFLUENCER SEEDING:
• 20 tech YouTubers
• 15 Twitter tech influencers
• 10 Instagram tech reviewers

TIMELINE:
Day 1: Embargo pitches to Tier 1
Day 3: Follow up, expand to Tier 2
Day 5: General release, wire services
Day 7: Influencer seeding

Distribution starting... ✓
```

### Media List Building
```
User: @pr-distributor media-list --niche "mobile-tech"

Agent: 📋 MEDIA LIST BUILT

MOBILE TECH JOURNALISTS (150 contacts)

TIER A (Prioritize):
1. Jon Porter - The Verge (jon@theverge.com)
   • Covers: Android, mid-range phones
   • Recent: Samsung A-series review
   • Pitch angle: "Better than Samsung at half price"

2. Chaim Gartenberg - TechCrunch
   • Covers: Budget tech, emerging markets
   • Recent: Nothing Phone coverage
   • Pitch angle: "Realme/Samsung competitor"

3. Damien Wilde - 9to5Google
   • Covers: Android ecosystem
   • Recent: Pixel alternatives
   • Pitch angle: "Best Pixel alternative under $300"

[147 more contacts...]

FILTERED BY:
✅ Covers mobile phones
✅ Writes about budget/mid-range
✅ Active in last 30 days
✅ Twitter following >10K

All contacts verified within 90 days ✓
Personalized pitch angles generated ✓
```

---

## Configuration

```yaml
pr-distributor:
  wire-services:
    - pr-newswire
    - business-wire
    
  media-database:
    source: "custom"  # or cision, muck-rack
    update-frequency: monthly
    
  pitch-templates:
    exclusive: "exclusive-briefing"
    embargo: "embargo-offer"
    general: "press-release"
```

---

*Part of the Brand Marketing Team framework.*
*Author: @namanwtf | Version 3.0.0 | MIT License*
