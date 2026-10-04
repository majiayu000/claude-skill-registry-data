---
name: market-research
description: Automated surveys, competitor analysis, and customer insight generation
author: "@namanwtf"
version: 3.0.0
requires: brand-context, competitive-intel
category: research
---

# 📊 Market Research Agent

**Purpose:** Understand your market, customers, and competitors with automated research, surveys, and insight generation.

---

## When to Use

```bash
# Customer satisfaction survey
@market-research survey satisfaction

# Competitor SWOT analysis
@market-research swot "Competitor X"

# Market sizing
@market-research size --industry "mobile-gaming"

# Customer interviews
@market-research interview --count 20

# Trend analysis
@market-research trends --topic "5g-phones"
```

---

## Capabilities

### 1. Survey Automation
- Questionnaire design
- Distribution (email, in-app, social)
- Response collection
- Statistical analysis
- Insight extraction

### 2. Competitor Analysis
- SWOT analysis
- Feature comparison matrices
- Pricing research
- Positioning maps
- Market share estimates

### 3. Customer Research
- Interview scheduling
- Focus group management
- Sentiment analysis
- Persona development
- Journey mapping

### 4. Market Intelligence
- Industry trend tracking
- Market sizing (TAM/SAM/SOM)
- Growth rate analysis
- Regulatory monitoring
- Technology forecasting

---

## Usage Examples

### Customer Satisfaction Survey
```
User: @market-research survey satisfaction

Agent: 📋 SURVEY CREATED

Survey: Customer Satisfaction Q2 2025
Target: 500 responses

QUESTIONS:
1. NPS: "How likely are you to recommend us?" (0-10)
2. CSAT: "How satisfied are you with our product?" (1-5)
3. Product-Market Fit: "How would you feel if you could no longer use us?"
   • Very disappointed
   • Somewhat disappointed
   • Not disappointed
   • N/A - I don't use it

4. Feature Importance: Rate importance (1-5)
   • Competitive intelligence
   • Pricing optimization
   • Copywriting
   • Meta ads
   • Analytics

5. Open-ended: "What should we build next?"

DISTRIBUTION:
✅ Email to all active users
✅ In-app popup (30% of users)
✅ Social media poll

INCENTIVE: $10 Amazon gift card for completion

Expected completion: 350 responses (70% rate)
```

### Competitor SWOT
```
User: @market-research swot "HubSpot"

Agent: 📊 COMPETITOR SWOT ANALYSIS

Target: HubSpot Marketing Hub

STRENGTHS:
✅ All-in-one platform (CRM + Marketing)
✅ Strong brand recognition
✅ Massive template library
✅ Excellent educational content
✅ Free tier drives adoption

WEAKNESSES:
❌ Expensive ($800+/month for full features)
❌ Steep learning curve
❌ Overwhelming for small businesses
❌ Slow customer support
❌ Feature bloat (too many tools)

OPPORTUNITIES (for us):
💡 Position as "HubSpot for lean teams"
💡 Focus on AI automation (they're manual)
💡 Price disruption (1/10th the cost)
💡 Faster setup (minutes vs weeks)
💡 Specialized for DTC brands

THREATS:
⚠️ HubSpot acquiring AI startups
⚠️ Price wars if they notice us
⚠️ Feature parity pressure

RECOMMENDATION:
Target HubSpot users complaining about price
Message: "Same results, 1/10th the cost"
```

### Market Sizing
```
User: @market-research size --industry "ai-marketing-tools"

Agent: 📈 MARKET SIZE ANALYSIS

Industry: AI Marketing Tools

TAM (Total Addressable Market):
• Global marketing software: $500B
• AI-powered segment: $75B
• Growing at 28% CAGR

SAM (Serviceable Available Market):
• SMB segment: $25B
• Focus: Under 100 employees
• English-speaking markets: $12B

SOM (Serviceable Obtainable Market):
• Year 1 target: $1M ARR
• Market share: 0.008%
• Realistic with current resources

MARKET TRENDS:
• 67% of marketers plan AI adoption
• Budget shifting from agencies to tools
• Demand for "all-in-one" solutions growing
• Privacy changes driving first-party data focus

COMPETITIVE DENSITY:
• Direct competitors: 15-20
• Indirect alternatives: 100+
• Market leader: HubSpot (12% share)
• Fragmented market (opportunity)

CONCLUSION:
Large, growing market with room for disruption.
Focus on underserved SMB segment.
```

---

## Configuration

```yaml
market-research:
  survey:
    platform: "typeform"  # or custom
    min-responses: 100
    incentive: 10  # dollars
    
  analysis:
    confidence-level: 95
    margin-of-error: 5
    
  sources:
    - gartner
    - forrester
    - industry-reports
    - social-listening
```

---

*Part of the Brand Marketing Team framework.*
*Author: @namanwtf | Version 3.0.0 | MIT License*
