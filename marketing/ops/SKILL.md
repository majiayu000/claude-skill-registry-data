---
name: marketing-ops
description: 'Use when > Complete AI-powered marketing & sales operating system for
  solo founders. Covers the full revenue lifecycle: customer research, content creation,
  SEO/GEO/SMO optimization, paid ads, email sequences, sales enablement, CRO, pricing,
  retention, analytics, automation, and global expansion. Includes stage-based playbooks
  ($0→$100K MRR), AI agent orchestration, PLG frameworks, Indonesia e-commerce, and
  decision-making infrastructure.'
domain: marketing
author: oyi77
license: Apache-2.0
subdomain: marketing
tags:
- ai-agent
- email
- growth
- marketing
- ops
- seo
- money
- automation
- sales
version: 1.0.0
category: marketing
---


# Marketing Ops

One AI-powered system that runs your entire marketing & sales operation
so you can focus on building product. 4-layer architecture with shared
context, auto-chaining orchestrator, and feedback loops that learn.

---

## Overview

Marketing Ops is a complete AI-powered marketing & sales operating system for solo founders. It covers the full revenue lifecycle: customer research, content creation, SEO/GEO/SMO optimization, paid ads, email sequences, sales enablement, CRO, pricing, retention, analytics, automation, and global expansion. Includes stage-based playbooks ($0 → $100K MRR), AI agent orchestration, PLG frameworks, Indonesia e-commerce, and decision-making infrastructure.

## When Not to Use

- **Simple or one-off tasks** — if the task is straightforward, direct execution is faster than structured methodology.
- **Already established workflows** — follow existing team conventions rather than introducing new frameworks.
- **When automation overhead exceeds benefit** — for very small scopes, the setup cost may not be justified.


## Dependencies

- Python 3.8+ or Node.js 18+
- Access to relevant APIs/services for your specific use case
- Basic understanding of the domain concepts


## Commands

```bash
# Refer to the skill's usage section for specific commands
# Adapt these to your workflow
```
## Money-Making Overview

| Service | Client Price | Your Time | Monthly Recurring |
|---------|-------------|-----------|------------------|
| Marketing audit + setup (1x) | $1,500–$3,000 | 8–15 hrs | No |
| Marketing ops retainer (weekly) | $1,000–$2,500/mo | 4–8 hrs/wk | Yes |
| Full-stack marketing automation | $3,000–$5,000/mo | 10–20 hrs/wk | Yes |
| Growth consulting + execution | $5,000–$10,000/mo | 20–30 hrs/wk | Yes |

**Target clients:** Solo founders, pre-seed/seed startups, e-commerce brands, and agencies who need a full marketing operation without hiring a CMO + team.

**Buyer persona:** Founder generating $5K–$100K/mo who knows they need marketing but doesn't have time to execute. They have a product, some revenue, but zero marketing infrastructure — no tracking, no funnel, no content system.

**First dollar timeline:** Week 1 — audit + quick wins (fix tracking, set up one channel). Month 1 — first campaign live + leads coming in. Month 3 — full flywheel running.

---

## Full Stack: What You're Selling

```
┌─────────────────────────────────────────────────────────────┐
│                   MARKETING OPERATING SYSTEM                  │
├──────────────┬──────────────┬──────────────┬────────────────┤
│  CUSTOMER    │  CONTENT     │  CHANNEL     │  ANALYTICS &   │
│  RESEARCH    │  FACTORY     │  ORCHESTRATOR│  OPTIMIZATION  │
├──────────────┼──────────────┼──────────────┼────────────────┤
│ ICP Profiling│ Blog/SEO     │ Email (5x/wk)│ UTM tracking   │
│ Competitor   │ Social posts  │ Paid ads     │ Funnel           │
│   Intel      │ Video/Shorts │ Organic SMO  │   analytics    │
│ Keyword Gap  │ Lead magnets │ DM outreach  │ CAC/LTV/ROAS   │
│ Customer     │ Case studies │ Partnerships│ Attribution    │
│   Interviews │ Newsletters  │ Affiliates   │ Cohort reports │
└──────────────┴──────────────┴──────────────┴────────────────┘
```

---

## Core Architecture

4-layer system that runs on auto-pilot:

**Layer 1 — Shared Context Layer**
- Customer profiles, ICP, brand voice, competitor file, keyword map
- Single source of truth every campaign reads from
- Updated weekly from performance data

**Layer 2 — Orchestrator (Auto-Chaining)**
- Week planning → daily execution → performance review
- Each completed task triggers the next (research → create → publish → analyze)
- No manual handoffs between stages

**Layer 3 — Execution Layer**
- Content creation (blog, social, video, email)
- Channel distribution (scheduling, posting, DMs)
- Ad buying & optimization
- Email sequences (nurture, sales, retention)

**Layer 4 — Feedback Layer**
- Daily: engagement metrics, ad spend, email stats
- Weekly: pipeline review, CAC by channel, content performance
- Monthly: full funnel audit, strategy pivot recommendations

---

## Stage-Based Playbooks ($0 → $100K MRR)

### Stage 1: Foundation ($0–$5K MRR)
**Goal:** 10 customers, repeatable acquisition channel, basic tracking
- [ ] Set up UTM tracking + analytics dashboard
- [ ] Define ICP and write 10 customer profiles
- [ ] Pick ONE channel — optimize before expanding
- [ ] Create 5 pieces of pillar content
- [ ] Set up email welcome sequence
- [ ] Manual outreach: 20 DMs/day to ICP
- **Key metric:** 1 signup/day from organic + outreach

### Stage 2: Scale Channel ($5K–$20K MRR)
**Goal:** 50 customers, content machine running, paid ads tested
- [ ] Content calendar: 3x blog + 5x social + 2x email per week
- [ ] SEO: 10 keyword-targeting articles, backlink outreach
- [ ] Paid ads: $1K/mo test budget, find winning creative
- [ ] Referral program with tracking
- [ ] Affiliate/partnership pipeline started
- **Key metric:** < $50 CAC, 10%+ conversion rate to paid

### Stage 3: Systematize ($20K–$50K MRR)
**Goal:** 200 customers, multi-channel, automated nurture
- [ ] 3+ channels active (organic + paid + partnerships)
- [ ] Automated lead scoring + routing
- [ ] Email automation: behavior-triggered sequences
- [ ] Content repurposing pipeline (1 blog → 10 pieces)
- [ ] Customer health scoring + retention playbook
- **Key metric:** 20%+ MoM growth, < 5% churn

### Stage 4: Flywheel ($50K–$100K MRR)
**Goal:** 500+ customers, predictable revenue engine
- [ ] Full funnel automation (awareness → purchase → advocacy)
- [ ] Customer-led growth: UGC, referrals, case studies
- [ ] International expansion playbook (Indonesia, SEA)
- [ ] Retargeting + win-back automation
- [ ] CRO program: A/B test pricing, landing pages, emails
- **Key metric:** > 3x LTV/CAC, > 80% paid retention

---

## First Action in 60 Minutes

```bash
#!/usr/bin/env bash
# marketing-ops: 60-min setup — tracking + first campaign
set -euo pipefail

PROJECT="${1:-my-startup}"
echo "=== Marketing Ops Quick Start: $PROJECT ==="
echo ""

# Step 1: Create project structure
mkdir -p "$PROJECT"/{tracking,content,ads,email,analytics}
echo "[OK] Project structure created"

# Step 2: Set up UTM tracking spreadsheet
cat > "$PROJECT/tracking/utm-builder.sh" << 'SCRIPT'
#!/usr/bin/env bash
# Usage: ./utm-builder.sh "campaign-name" "source" "medium"
# Generates trackable URLs for every channel
CAMPAIGN="$1"
SOURCE="$2"
MEDIUM="${3:-web}"
BASE_URL="${4:-https://example.com}"

echo "=== UTM Links for: $CAMPAIGN ==="
echo ""
for content in "homepage" "pricing" "blog-post" "landing-page"; do
    URL="${BASE_URL}/${content}?utm_source=${SOURCE}&utm_medium=${MEDIUM}&utm_campaign=${CAMPAIGN}&utm_content=${content}"
    echo "$URL"
done
echo ""
echo "Add these URLs to: Google Analytics → Acquisition → Campaigns"
SCRIPT
chmod +x "$PROJECT/tracking/utm-builder.sh"
echo "[OK] UTM builder script ready"

# Step 3: Create analytics dashboard query (GA4 placeholder)
cat > "$PROJECT/analytics/ga4-queries.sql" << 'SQL'
-- Google Analytics 4 — Key Queries for Solo Founders
-- Run these in GA4 Explorations

-- Query 1: Top acquisition channels by revenue
SELECT
  session_source,
  session_medium,
  COUNT(DISTINCT user_pseudo_id) AS users,
  SUM(purchase_revenue) AS revenue
FROM `project.dataset.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20250101' AND '20251231'
GROUP BY 1, 2
ORDER BY revenue DESC;

-- Query 2: Funnel drop-off (landing → signup → purchase)
SELECT
  event_name,
  COUNT(DISTINCT user_pseudo_id) AS users,
  RATIO_TO_REPORT(COUNT(DISTINCT user_pseudo_id)) OVER() AS percent
FROM `project.dataset.events_*`
WHERE event_name IN ('page_view', 'signup_start', 'signup_complete', 'purchase')
GROUP BY 1;
SQL
echo "[OK] GA4 analytics queries created"

# Step 4: Create first email sequence template
cat > "$PROJECT/email/welcome-sequence.md" << 'EMAIL'
# Welcome Email Sequence — 3 Emails

## Email 1: Welcome + Value (Day 0)
**Subject:** Welcome to {{PROJECT}} — here's your first win
**Body:** Quick intro, deliver the freebie/onboarding step, set expectations

## Email 2: Social Proof + Case Study (Day 2)
**Subject:** How {{customer-type}} used {{PROJECT}} to {{result}}
**Body:** Real story with numbers, bullet points of key takeaways

## Email 3: Offer + CTA (Day 5)
**Subject:** Ready to {{desired-outcome}}?
**Body:** Direct pitch, limited-time incentive, clear CTA
EMAIL
echo "[OK] Email sequence template created"

# Step 5: Launch first campaign checklist
cat > "$PROJECT/first-campaign.md" << 'CHECKLIST'
# First Campaign Launch Checklist

## Pre-Launch (done before start)
- [ ] UTM tracking working (test click → GA)
- [ ] Landing page live with tracking pixel
- [ ] Email capture form active
- [ ] Welcome sequence active

## Launch Day
- [ ] Post on 2 platforms (LinkedIn + Twitter/IG)
- [ ] Send to existing email list (min 50 people)
- [ ] DM 10 potential customers with link
- [ ] Post in 3 relevant communities

## Day 3 Check
- [ ] Check UTM data in GA4
- [ ] Check email open rates (> 30% target)
- [ ] Check landing page conversion (> 2% target)
- [ ] Document what's working and double down
CHECKLIST
echo "[OK] First campaign checklist created"

echo ""
echo "=== DONE ==="
echo "Next: cd $PROJECT && ./tracking/utm-builder.sh 'launch' 'linkedin' 'social'"
echo "Then: open first-campaign.md and start checking boxes"
```

---

## Deliverable Format

```markdown
# Marketing Operations Audit & Proposal

## Client: [Name]
## Prepared: [Date]
## Engagement: [One-time / Retainer / Full-Stack]

---

## 1. Executive Summary
- Current state: channels active, revenue, traffic, conversion rate
- Key gaps: missing tracking, low conversion, no content system, no retention
- Opportunity: estimated lift from fixing gaps (X% increase)
- Recommendation: three-phase plan (quick wins → system → scale)

## 2. Audit Findings

| Area | Current State | Gap | Priority |
|------|--------------|-----|----------|
| Tracking | [e.g., No UTM] | [e.g., Can't attribute] | Critical |
| Content | [e.g., 1 blog/mo] | [e.g., No content engine] | High |
| Email | [e.g., No list] | [e.g., No nurture] | High |
| Paid Ads | [e.g., Untested] | [e.g., No data] | Medium |
| SEO | [e.g., 5 articles] | [e.g., No keyword strategy] | Medium |
| Retention | [e.g., No follow-up] | [e.g., High churn] | Critical |

## 3. Quick Wins (Week 1)
1. Fix tracking — UTM parameters + analytics dashboard
2. Email capture — popup + welcome sequence
3. One channel — pick highest ROI channel, optimize
4. Content — repurpose best content into 5 pieces

## 4. System Build (Month 1-2)
- Content calendar: weekly blog + social + email
- SEO: 10 articles targeting high-intent keywords
- Email nurture: 5-email automated sequence
- Paid ads: $500-1000 test budget, 5 creative variants
- Analytics: weekly reporting dashboard

## 5. Scale (Month 3+)
- Expand to 3+ channels
- Affiliate/partnership program
- CRO: A/B test landing pages, pricing, emails
- Retention: customer health scoring, win-back flows

## 6. Investment

| Phase | Deliverables | Price | Timeline |
|-------|-------------|-------|----------|
| Audit + Setup | Tracking, analytics, quick wins | $1,500–$3,000 | Week 1 |
| Monthly Retainer | Content, ads, email, optimization | $2,000–$5,000/mo | Ongoing |
| Full-Stack | Everything above + partnerships, CRO | $5,000–$10,000/mo | Ongoing |

## 7. KPIs We'll Track
- Traffic (by channel)
- Leads (by source)
- Conversion rate (visit → lead → customer)
- CAC (by channel)
- LTV (cohort-based)
- ROAS (paid ads)
- Email metrics (open, click, unsubscribe)
- Monthly recurring revenue growth
```

---

## When to Use

**Trigger phrases:**
- "marketing ops"
- "Help me with marketing ops"
- "set up marketing automation"
- "build a marketing system"
- "I need marketing for my startup"

**Use cases:**
- Solo founders who need a marketing system but can't hire a team
- Pre-seed/seed startups needing first 100 customers
- E-commerce brands needing multi-channel marketing
- Agencies who want to outsource marketing execution
- Indonesia/SEA businesses needing localized marketing

**When NOT to use:**
- When the audience is too small to justify the effort (< 100 potential customers)
- For regulated industries without compliance review (healthcare, finance)
- When the campaign budget does not support the channel (< $500/mo ad budget)
- For tasks that need deep vertical expertise (enterprise sales, biotech)
- When the client needs a CMO strategist, not an executor

---

## Workflow

```python
# Example: SEO keyword analysis
def analyze_keywords(keywords: list[str]) -> list[dict]:
    results = []
    for kw in keywords:
        volume = get_search_volume(kw)
        difficulty = get_difficulty(kw)
        results.append({
            "keyword": kw,
            "volume": volume,
            "difficulty": difficulty,
            "opportunity": volume / max(difficulty, 1),
        })
    return sorted(results, key=lambda x: x["opportunity"], reverse=True)
```

1. **Research** — Analyze market, competitors, and audience
2. **Strategy** — Define goals, channels, and messaging
3. **Create** — Develop content and creative assets
4. **Launch** — Deploy campaigns across channels
5. **Optimize** — A/B test and iterate based on data
6. **Report** — Track KPIs and ROI

---

## Key Metrics

- Reach and impressions
- Engagement rate (likes, shares, comments)
- Conversion rate (clicks → leads → customers)
- Customer acquisition cost (CAC)
- Return on ad spend (ROAS)
- Lead velocity (leads/week growth)
- Pipeline velocity (days from lead to close)
- Net revenue retention / churn

---

## Best Practices

- Test everything — headlines, images, CTAs, timing
- Focus on one channel at a time, then expand
- Build organic before scaling paid
- Track attribution across the full funnel
- Document every campaign — what worked, what didn't, why
- Automate everything that doesn't need human judgment
- Refresh content on a 90-day cycle
- Price by value delivered, not hours worked

---

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll set up tracking later" | Without tracking, every dollar is a guess. Day 1 or never. |
| "I can't afford marketing yet" | You can't afford NOT to market. One paying customer funds your system. |
| "I need a perfect strategy first" | Speed beats perfection. Launch, measure, iterate. A bad campaign teaches more than no campaign. |
| "My product sells itself" | No product sells itself. Marketing is how people find out you exist. |
| "SEO takes too long" | SEO is a 6-month exponential curve. Day 1 is the cheapest it will ever be. |
| "I don't have time to manage marketing" | That's what a retainer is for. You focus on product; I run the system. |
| "Paid ads are too expensive" | Wrong creative is expensive. Right creative with proper tracking prints money at $5/day. |

---

## Process

1. **Research** — Analyze target audience, competitors, and trending topics
2. **Create** — Generate content following brand guidelines and best practices
3. **Publish & Optimize** — Distribute to target platforms, track performance, iterate

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings
- [ ] Client deliverables exported in report format
- [ ] Tracking verified (click → GA → conversion)
- [ ] Email sequence tested end-to-end
