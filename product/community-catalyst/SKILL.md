---
name: community-catalyst
description: 'Product-led growth and community strategy engine that designs viral loops, self-serve onboarding funnels, and user community programs. Use when: PLG strategy, product-led growth, community strategy, viral growth, referral program, developer community, user community, growth loops.'
---

# Community Catalyst (LOOP Engine)

Design the mechanisms that make your product grow itself through product experience, community engagement, and viral mechanics.

## When to Use
- PLG motion design
- Community program launch
- Referral program design
- Developer ecosystem strategy
- Growth loop optimization

## What You'll Need
**Critical inputs (ask if not provided):**
- Product and its core use case
- Current growth motion (sales-led, PLG, hybrid)
- Target user persona

**Nice-to-have:**
- Journey Architect output (Gates 5-7 for post-sale experience)
- Current product metrics (signups, activation, retention)

## Process

### Step 1: PLG Readiness Assessment
Score your product on 8 dimensions (1-5 each):

| Dimension | Question | Score Guide |
|-----------|---------|-------------|
| Self-serve signup | Can users start without talking to sales? | 1=must talk to sales, 5=instant signup |
| Time-to-value | Can users see value in under 5 minutes? | 1=days/weeks, 5=under 5 minutes |
| Freemium viability | Is a free tier sustainable? | 1=no, 5=natural free tier exists |
| Network effects | Does product improve with more users? | 1=no, 5=strong network effects |
| Collaboration | Does usage naturally involve inviting others? | 1=solo use, 5=inherently collaborative |
| Integration distribution | Does product plug into existing workflows? | 1=standalone, 5=deep integrations |
| Data personalization | Can the product self-optimize with usage? | 1=static, 5=gets smarter over time |
| Virality mechanics | Can users share/embed/publish from product? | 1=private only, 5=public artifacts |

**PLG Readiness** = sum / 40 (percentage)
- Below 50%: PLG not primary -- focus on community and assisted growth
- 50-75%: PLG-assisted (hybrid with sales)
- Above 75%: PLG-primary viable

### Step 2: LOOP Design
Four interconnected growth loops:

**L - Leverage Points**: Where in the product do users naturally encounter reasons to share or expand? Map these to journey Gates 5-7.

**O - Onboarding Friction Audit**: Walk through first-time experience step by step:
- Score each step: value delivered (1-5) vs. friction imposed (1-5)
- Remove or simplify every step where friction > value
- Target: 3 clicks or fewer to first value moment

**O - Organic Amplifiers**: Design the growth mechanics:
- Referral program (incentive, mechanics, tracking)
- User-generated content (templates, showcases)
- Community forums (platform, content pillars, moderation)
- Ambassador program (recognition, access, revenue share)

**P - Product-Embedded Growth**: Features that inherently drive expansion:
- Collaboration and team invites
- Public sharing and embedding
- Integration marketplace
- API ecosystem

### Step 3: Community Architecture
Design the community program:

| Element | Decision |
|---------|---------|
| Platform | Discord, Slack, forum, GitHub, or hybrid |
| Content pillars | 3-5 topics that drive engagement |
| Contribution ladder | Lurker -> Contributor -> Champion -> Ambassador |
| Incentive structure | Recognition, early access, swag, revenue share |
| Moderation model | Community-led, staff-led, or hybrid |
| Feedback loop | How community insights flow back to product team |

### Step 4: Viral Coefficient Modeling
- **K-factor** = (invites sent per user) x (conversion rate per invite)
- K > 1 = viral growth (each user brings more than 1 new user)
- K > 0.5 = meaningful organic amplification
- Design experiments to improve each component of K

## Output
Save to `outputs/community-catalyst-[YYYY-MM-DD].md`

### Deliverables:
1. **PLG Readiness Scorecard**: 8-dimension assessment with improvement roadmap
2. **LOOP Growth Blueprint**: Four interconnected growth loops with specific mechanics
3. **Community Architecture Plan**: Complete program design from platform to incentives
4. **Viral Mechanics Playbook**: Features and experiments to increase organic growth

## Chain Connections
- **Next skill**: Run `launch-command` to orchestrate the launch including PLG readiness
- **Also feeds**: `growth-loop` (PLG mechanics drive retention), `demand-engine` (community becomes a channel)
- **Enhanced by**: Run after `journey-architect` (Gates 5-7 define growth loop triggers)
