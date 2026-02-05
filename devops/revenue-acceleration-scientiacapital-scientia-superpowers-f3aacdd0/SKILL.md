---
name: revenue-acceleration
description: GTM workflows for revenue acceleration across Scientia projects. Use for demo preparation, sales outreach, battle cards, pricing strategy, and revenue tracking. Triggers on "revenue focus", "prepare demo", "sales outreach", "battle card", "GTM strategy", "pricing", "tier-1 projects".
---

# Revenue Acceleration for Scientia Stack

Workflows for accelerating revenue across the top 7 projects.

## Tier-1 Projects (Highest Revenue Potential)

| Project | Score | ACV Target | Timeline |
|---------|-------|------------|----------|
| sales-agent | 91/100 | $36-60k/year | 4-6 weeks |
| dealer-scraper | 83/100 | $10-40k deals | 2-4 weeks |
| thetaroom | 81/100 | Track record | 6-12 weeks |
| ai-cost-optimizer | 81/100 | Case study | 8-12 weeks |

## Tier-2 Projects (Active Development)

| Project | Status | Revenue Model |
|---------|--------|---------------|
| signal-siphon | Production | Freemium SaaS |
| fieldvault-ai | Production | Per-seat SaaS |
| gemma-payroll | Development | Enterprise SaaS |

## Demo Preparation Workflow

### 1. Pre-Demo Checklist

```markdown
## Demo Prep for [PROJECT_NAME]

### Environment
- [ ] Production URL working
- [ ] Test accounts created
- [ ] Sample data loaded
- [ ] API keys valid
- [ ] No console errors

### Content
- [ ] Key features identified (3-5)
- [ ] Pain points to address
- [ ] Competitor comparison ready
- [ ] Pricing tiers defined
- [ ] ROI calculator prepared

### Technical
- [ ] Screen recording backup
- [ ] Fallback slides ready
- [ ] Mobile view tested
- [ ] Load time < 3s
```

### 2. Demo Script Template

```markdown
# [PROJECT] Demo Script (15 minutes)

## Opening (2 min)
- Introduce yourself
- Confirm their pain point
- Preview what you'll show

## Problem Statement (2 min)
- Current workflow issues
- Cost of status quo
- Industry context

## Solution Demo (8 min)
1. **Feature 1**: [Core value prop]
2. **Feature 2**: [Differentiation]
3. **Feature 3**: [Scalability]

## ROI & Pricing (2 min)
- Time savings calculation
- Cost comparison
- Tier recommendation

## Next Steps (1 min)
- Trial offer
- Implementation timeline
- Follow-up schedule
```

## Battle Card Template

```markdown
# [PROJECT] Battle Card

## One-Liner
[10-word value proposition]

## Target Customer
- Industry: [specific]
- Size: [employee count]
- Pain: [primary problem]

## Key Differentiators
1. [Unique feature 1]
2. [Unique feature 2]
3. [Unique feature 3]

## Competitors
| Competitor | Their Weakness | Our Strength |
|------------|----------------|--------------|
| [Name] | [Gap] | [Advantage] |

## Objection Handling
| Objection | Response |
|-----------|----------|
| "Too expensive" | [Value justification] |
| "We use X already" | [Migration ease] |
| "Security concerns" | [Compliance points] |

## Pricing
| Tier | Price | Includes |
|------|-------|----------|
| Starter | $X/mo | [Features] |
| Pro | $Y/mo | [Features] |
| Enterprise | Custom | [Features] |

## Proof Points
- [Customer quote/metric]
- [Case study reference]
- [Third-party validation]
```

## Sales Outreach Templates

### Cold Email (First Touch)

```markdown
Subject: [Pain point] at [Company]?

Hi [Name],

I noticed [Company] is [relevant observation].

We've helped [similar company type] [specific result] with [product].

Would you have 15 minutes this week to see if it could work for you?

[Your name]
```

### Follow-Up (No Response)

```markdown
Subject: Re: [Original subject]

Hi [Name],

Just floating this back up - [one-liner value prop].

If timing isn't right, no worries. But if [pain point] is still a priority, happy to share how we've helped others.

[Your name]
```

### LinkedIn Message

```markdown
Hi [Name] - saw you're leading [role/initiative] at [Company].

We just helped [similar role] at [similar company] [specific result].

Worth a quick chat?
```

## Revenue Tracking

### Weekly Revenue Standup Template

```markdown
# Revenue Standup - Week of [DATE]

## Pipeline Status
| Project | Stage | Deal Size | Next Step | Owner |
|---------|-------|-----------|-----------|-------|
| sales-agent | Demo scheduled | $48k | Run demo Tue | TK |
| dealer-scraper | Proposal sent | $15k | Follow up | TK |

## Won This Week
- [Deal details]

## Lost/Stalled
- [Reason + learning]

## Blockers
- [What's blocking progress]

## Focus Next Week
1. [Priority 1]
2. [Priority 2]
```

### Revenue Command Quick Access

To open all revenue projects:

```bash
# Opens terminals for tier-1 + tier-2 projects
cd /Users/tmkipper/Desktop/tk_projects
for p in sales-agent dealer-scraper thetaroom ai-cost-optimizer signal-siphon fieldvault-ai gemma-payroll; do
  if [ -d "$p" ]; then
    open -a "Terminal" "$p"
  fi
done
```

## Pricing Strategy Framework

### Cost-Plus Pricing

```
Monthly Cost = (Infrastructure + AI + Support) * 1.3 margin
Price = Monthly Cost * 3x multiplier
```

### Value-Based Pricing

```
Annual Value = (Hours Saved * Hourly Rate) + (Revenue Increase)
Price = Annual Value * 0.1-0.2 (10-20% of value)
```

### Tier Structure

```markdown
| Tier | Target | Price Point | Margin |
|------|--------|-------------|--------|
| Starter | SMB | $29-99/mo | 60% |
| Pro | Mid-market | $199-499/mo | 70% |
| Enterprise | Enterprise | $1k+/mo | 80% |
```

## Metrics to Track

### Leading Indicators
- Demo requests / week
- Trial signups / week
- Pipeline value
- Email open rates

### Lagging Indicators
- MRR / ARR
- Churn rate
- CAC / LTV ratio
- NPS score

## Quick Reference Commands

```bash
# Open revenue dashboard
/revenue-focus

# Prepare demo for specific project
/demo-prep sales-agent

# Generate battle card
/battle-card fieldvault-ai

# Track costs across projects
/cost-check
```
