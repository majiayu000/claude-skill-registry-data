---
name: affiliate-manager
description: Build and manage affiliate programs with automated recruitment, tracking, and payouts
author: "@namanwtf"
version: 3.0.0
requires: brand-context, analytics-dashboard
category: partnerships
---

# 🤝 Affiliate Manager Agent

**Purpose:** Turn customers and creators into revenue-generating affiliates with zero manual work.

---

## When to Use

```bash
# Set up affiliate program
@affiliate-manager setup --commission 15%

# Recruit affiliates
@affiliate-manager recruit --niche tech-reviewers

# Track performance
@affiliate-manager track --month current

# Process payouts
@affiliate-manager payout --month last

# Optimize program
@affiliate-manager optimize
```

---

## Capabilities

### 1. Program Setup
- Commission structure design
- Cookie duration settings
- Payout threshold configuration
- Terms & conditions generation
- Affiliate portal creation

### 2. Affiliate Recruitment
- Identify potential affiliates
- Automated outreach sequences
- Application vetting
- Onboarding automation
- Welcome kit generation

### 3. Performance Tracking
- Real-time click tracking
- Conversion attribution
- Revenue per affiliate
- Fraud detection
- Top performer identification

### 4. Automated Payouts
- Monthly/quarterly calculations
- Tax form collection (W-9, W-8)
- Payment processing (PayPal, bank transfer)
- Commission adjustments
- Refund handling

---

## Usage Examples

### Program Setup
```
User: @affiliate-manager setup

Agent: 🎯 AFFILIATE PROGRAM CONFIGURED

Program Name: Brand Marketing Team Partners
Commission: 20% recurring
Cookie Duration: 60 days
Payout Threshold: $50
Payment Schedule: Monthly (Net-30)

Structure:
• Tier 1: 0-10 sales = 20%
• Tier 2: 11-50 sales = 25%
• Tier 3: 50+ sales = 30%

Affiliate Portal:
✅ Custom dashboard created
✅ Unique tracking links auto-generated
✅ Marketing assets library
✅ Real-time stats
✅ Payout history

Terms Generated:
✅ Commission rules
✅ Payment terms
✅ Prohibited activities
✅ Termination clauses

Ready to recruit! 🚀
```

### Recruit Affiliates
```
User: @affiliate-manager recruit --niche "tech-youtubers" --count 50

Agent: 📧 RECRUITMENT CAMPAIGN LAUNCHED

Target: 50 tech YouTubers
Channels: Email + Twitter DM

Outreach Message:
"Hey [Name],

Love your recent video on [specific topic]. Your audience clearly trusts your tech recommendations.

Want to earn 20% recurring commission promoting Brand Marketing Team?

Your audience gets 10% off, you get paid monthly.

Interested? [Apply Link]

Best,
Affiliate Team"

Sent: 50 personalized emails
Expected response rate: 15-20%
Expected signups: 7-10 affiliates

Tracking applications in real-time... ✓
```

### Performance Dashboard
```
User: @affiliate-manager track --month current

Agent: 📊 AFFILIATE PERFORMANCE - MARCH 2025

OVERVIEW:
• Active Affiliates: 127 (+23 this month)
• Total Clicks: 45,230
• Conversions: 312
• Conversion Rate: 0.69%
• Revenue: $18,450
• Commissions Paid: $3,690

TOP PERFORMERS:
🥇 @TechReviewer_Pro
   • Sales: 47
   • Revenue: $2,350
   • Commission: $470
   • EPC: $2.10

🥈 @MarketingGuru
   • Sales: 38
   • Revenue: $1,900
   • Commission: $380
   • EPC: $1.85

🥉 @StartupDaily
   • Sales: 29
   • Revenue: $1,450
   • Commission: $290
   • EPC: $1.62

INSIGHTS:
• YouTube affiliates converting 3x better
• Blog affiliates highest EPC ($2.40)
• Twitter affiliates lowest but highest volume

RECOMMENDATION:
→ Recruit more YouTube tech reviewers
→ Create exclusive YouTube discount code
```

---

## Configuration

```yaml
affiliate-manager:
  commission:
    type: "percentage"  # or "fixed"
    rate: 20
    recurring: true
    tiers:
      - sales: 0, rate: 20
      - sales: 10, rate: 25
      - sales: 50, rate: 30
      
  cookie:
    duration: 60  # days
    attribution: "last-click"
    
  payout:
    threshold: 50
    schedule: "monthly"
    methods: ["paypal", "bank-transfer"]
    
  fraud-protection:
    self-referral: false
    coupon-stacking: false
    ip-tracking: true
```

---

*Part of the Brand Marketing Team framework.*
*Author: @namanwtf | Version 3.0.0 | MIT License*
