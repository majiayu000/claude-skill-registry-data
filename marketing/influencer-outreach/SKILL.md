---
name: influencer-outreach
description: Discover, vet, and manage influencer partnerships at scale
author: "@namanwtf"
version: 3.0.0
requires: brand-context, social-content
category: partnerships
---

# 👥 Influencer Outreach Agent

**Purpose:** Find perfect influencers, automate outreach, and manage partnerships—all while tracking ROI.

---

## When to Use

```bash
# Find influencers in your niche
@influencer-outreach find --niche gaming --followers 10k-100k

# Analyze influencer quality
@influencer-outreach vet @username

# Automate outreach campaign
@influencer-outreach campaign "Product X Launch"

# Track campaign performance
@influencer-outreach track --campaign "Spring 2025"

# Manage partnerships
@influencer-outreach manage
```

---

## Capabilities

### 1. Influencer Discovery
- Search by niche, follower count, engagement rate
- Filter by location, language, platform
- AI-powered audience quality scoring
- Fake follower detection
- Brand alignment analysis

### 2. Vetting & Analysis
- Engagement rate calculation
- Audience demographics breakdown
- Content quality assessment
- Previous brand partnership history
- Authenticity scoring

### 3. Outreach Automation
- Personalized email templates
- DM automation (Instagram, TikTok, Twitter)
- Follow-up sequences
- Contract template generation
- Rate negotiation assistance

### 4. Campaign Management
- Brief creation
- Content approval workflow
- Post scheduling coordination
- Performance tracking
- ROI calculation

---

## Usage Examples

### Find Influencers
```
User: @influencer-outreach find --niche gaming --followers 50k-500k --platform youtube

Agent: 🎯 TOP 10 GAMING INFLUENCERS

1. @GamerPro_X
   • Followers: 245K
   • Engagement: 4.2% (Excellent)
   • Avg Views: 180K
   • Audience: 78% Male, 18-34
   • Est. Rate: $2,500/post
   • Brand Fit Score: 92/100

2. @MobileGamingDaily
   • Followers: 189K
   • Engagement: 5.8% (Exceptional)
   • Avg Views: 95K
   • Audience: 65% Mobile gamers
   • Est. Rate: $1,800/post
   • Brand Fit Score: 88/100

[8 more results...]

Recommendation: Prioritize @MobileGamingDaily
→ Highest engagement
→ Mobile-focused audience
→ Better value per dollar
```

### Vet Influencer
```
User: @influencer-outreach vet @TechReviewer99

Agent: 🔍 INFLUENCER ANALYSIS

@TechReviewer99
━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Metrics:
• Followers: 127K
• Engagement Rate: 3.2%
• Avg Likes: 4,064
• Avg Comments: 203

⚠️ Red Flags:
• Follower growth: +450% in 30 days (suspicious)
• Comment quality: Generic/spam detected
• Previous brands: 15 promos in 30 days (oversaturated)

✅ Positives:
• Consistent posting schedule
• High video quality
• Genuine audience interactions

🎯 Verdict: PROCEED WITH CAUTION
→ Negotiate lower rate
→ Request story posts + feed
→ Track performance closely
```

### Outreach Campaign
```
User: @influencer-outreach campaign "Product X Launch"

Agent: 📧 OUTREACH CAMPAIGN CREATED

Campaign: Product X Launch
Budget: $15,000
Target: 10 tech influencers

Outreach Sequence:

EMAIL 1 (Day 1):
Subject: Partnership Opportunity - Product X Launch 🚀

Hi [Name],

Love your recent review on [specific video]. Your take on [topic] was spot-on.

We're launching Product X (flagship feature, under $250) and think your audience would love it.

Interested in an exclusive first look?

Best,
[Your Name]

EMAIL 2 (Day 4, if no reply):
Subject: Re: Product X - Still interested?

[Follow-up template]

DM TEMPLATE (Instagram):
Hey [Name]! Big fan of your content. Have a partnership opportunity for Product X launch. Worth $X. Interested? 📱

10 influencers contacted ✓
Tracking responses... ✓
```

---

## Configuration

```yaml
influencer-outreach:
  platforms: ["instagram", "youtube", "tiktok", "twitter"]
  
  criteria:
    min-followers: 10000
    min-engagement: 2.0
    max-fake-ratio: 20
    
  outreach:
    email-template: "partnership"
    follow-up-days: [3, 7, 14]
    
  budget:
    nano: [100, 500]      # 1K-10K
    micro: [500, 2000]    # 10K-100K
    macro: [2000, 10000]  # 100K-1M
```

---

*Part of the Brand Marketing Team framework.*
*Author: @namanwtf | Version 3.0.0 | MIT License*
