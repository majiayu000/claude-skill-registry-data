---
name: retention-analyzer
description: Predict churn, identify at-risk customers, and automate retention campaigns
author: "@namanwtf"
version: 3.0.0
requires: brand-context, analytics-dashboard, email-sequence
category: retention
---

# 🔄 Retention Analyzer Agent

**Purpose:** Stop customers from leaving before they do. Predict churn, trigger retention campaigns, and maximize lifetime value.

---

## When to Use

```bash
# Analyze churn risk
@retention-analyzer risk --segment all

# Identify at-risk customers
@retention-analyzer identify --threshold high

# Trigger retention campaign
@retention-analyzer campaign --risk-level medium

# View retention metrics
@retention-analyzer metrics --period 30d

# Predict future churn
@retention-analyzer predict --months 3
```

---

## Capabilities

### 1. Churn Prediction
- Behavioral scoring (login frequency, usage patterns)
- Engagement decline detection
- Support ticket sentiment analysis
- Payment failure tracking
- ML-powered risk scoring

### 2. At-Risk Identification
- Segment customers by churn probability
- Priority ranking (who to save first)
- Revenue impact calculation
- Root cause analysis
- Early warning alerts

### 3. Automated Retention
- Triggered email sequences
- Personalized win-back offers
- Proactive support outreach
- Loyalty reward automation
- Exit interview requests

### 4. Retention Analytics
- Cohort retention curves
- LTV predictions
- Churn rate by segment
- Campaign effectiveness
- ROI of retention efforts

---

## Usage Examples

### Churn Risk Analysis
```
User: @retention-analyzer risk

Agent: ⚠️ CHURN RISK ANALYSIS

Total Customers: 12,450

RISK BREAKDOWN:
🔴 High Risk (Churn >70%): 487 customers (3.9%)
🟡 Medium Risk (Churn 30-70%): 1,243 customers (10.0%)
🟢 Low Risk (Churn <30%): 10,720 customers (86.1%)

HIGH RISK INDICATORS:
• No login in 30+ days: 312 customers
• Failed payment 2+ times: 89 customers
• Support ticket unresolved: 47 customers
• Usage dropped 80%+: 39 customers

REVENUE AT RISK: $48,700/month

TOP 10 CUSTOMERS TO SAVE:
1. Acme Corp ($2,400/mo) - No login 45 days
2. TechStart Inc ($1,800/mo) - Payment failed 3x
3. GrowthLabs ($1,500/mo) - Support escalation
[7 more...]

IMMEDIATE ACTION REQUIRED ⚡
```

### Retention Campaign
```
User: @retention-analyzer campaign --risk-level high

Agent: 🎯 RETENTION CAMPAIGN ACTIVATED

Target: 487 high-risk customers
Strategy: Multi-channel intervention

SEQUENCE 1: Email (Day 0)
Subject: "We miss you - here's 20% off to come back"

Hi [Name],

We noticed you haven't logged in recently. Everything okay?

We've been busy improving Brand Marketing Team:
✨ New feature: AI video scripts
✨ Faster: 2x speed improvements  
✨ Better: 15 new marketing templates

Come back and get 20% off your next 3 months.

[Claim Discount →]

We're here if you need help.

Best,
The Team

SEQUENCE 2: Personal Outreach (Day 3, if no response)
• Account manager phone call
• Calendly link for demo
• "What would bring you back?" survey

SEQUENCE 3: Final Offer (Day 7)
Subject: "Last chance: 30% off + free onboarding"

[More aggressive offer]

Campaign launched ✓
Tracking responses... ✓
Expected save rate: 15-25%
```

---

## Configuration

```yaml
retention-analyzer:
  scoring:
    login-weight: 30
    usage-weight: 25
    support-weight: 20
    payment-weight: 25
    
  thresholds:
    high: 70
    medium: 30
    
  campaigns:
    high-risk: "aggressive-winback"
    medium-risk: "engagement-boost"
    low-risk: "loyalty-rewards"
```

---

*Part of the Brand Marketing Team framework.*
*Author: @namanwtf | Version 3.0.0 | MIT License*
