---
name: product-announcement
description: 'Product announcement and launch communications generator that creates coordinated multi-channel launch messaging from press releases to social posts to internal comms. Use when: product announcement, launch announcement, product launch comms, press release, launch communications, announce new feature, announce new product.'
---

# Product Announcement (HERALD Protocol)

Generate coordinated, multi-channel product launch communications that tell a consistent story across every audience and platform.

## When to Use
- New product launches
- Major feature announcements
- Platform/pricing changes
- Partnership announcements
- Milestone announcements

## What You'll Need
**Critical inputs (ask if not provided):**
- What is being announced (product, feature, partnership)
- Launch date
- Target audience(s)

**Nice-to-have:**
- Position Lock output (messaging hierarchy)
- Battle Scanner output (competitive context)
- Approved quotes from executives/customers

## Process

### Step 1: HERALD Framework
Structure the announcement across 6 layers:

| Layer | What It Covers | Key Output |
|-------|---------------|-----------|
| **H**eadline | The headline story -- why this matters to the world | 1 sentence that would make someone stop scrolling |
| **E**cho | Persona-specific angles on the same announcement | 3-5 message variants by audience |
| **R**each | All announcement materials across channels | Full asset list below |
| **A**lign | Internal alignment and stakeholder coordination | Stakeholder sign-off checklist |
| **L**aunch | Timed release across channels for maximum impact | Hour-by-hour launch day plan |
| **D**istribute | Success metrics per channel and overall | KPI dashboard |

### Step 2: Big Idea Distillation
Create the announcement hierarchy:
- **Internal headline** (what we're really doing): 1 sentence, no jargon
- **External headline** (what customers care about): 1 sentence, benefit-led
- **Press headline** (what media would write): 1 sentence, newsworthy angle
- **Social hook** (what gets engagement): 1 sentence, provocative or surprising

All 4 must tell the same story from different angles.

### Step 3: Multi-Channel Asset Creation
Generate content for each channel:

| Asset | Length | Tone | Key Element |
|-------|--------|------|-------------|
| **Press release** | 400-600 words | Formal, newsworthy | Quote from CEO + customer |
| **Blog post** | 800-1200 words | Educational, excited | Problem-solution narrative |
| **Email to customers** | 200-300 words | Direct, valuable | What it means for THEM |
| **Email to prospects** | 150-250 words | Compelling, CTA-driven | Why they should care NOW |
| **Social posts (LinkedIn)** | 150-200 words | Professional, insightful | Hot take or data point |
| **Social posts (X/Twitter)** | 280 chars | Punchy, shareable | The one-liner version |
| **Internal announcement** | 300-500 words | Celebratory, informative | What, why, and what's next |
| **Sales enablement brief** | 1 page | Tactical, action-oriented | Talk track + FAQ + CTA |
| **Partner notification** | 200-300 words | Collaborative, opportunity-focused | What it means for them |

### Step 4: Sequencing Plan
Design the launch day timeline:

| Time | Action | Channel | Owner |
|------|--------|---------|-------|
| T-7 days | Embargo briefings to press | Direct outreach | PR |
| T-3 days | Customer advisory board preview | Email | CS |
| T-1 day | Internal all-hands announcement | Slack/Teams | Exec |
| T-0 Hour 0 | Press release goes live | Newswire | PR |
| T-0 Hour 1 | Blog post published | Website | Marketing |
| T-0 Hour 2 | Customer email sent | Email | Marketing |
| T-0 Hour 3 | Social media barrage begins | LinkedIn, X | Marketing |
| T-0 Hour 4 | Sales outreach begins | Email, phone | Sales |
| T+1 day | Partner co-marketing activates | Joint channels | Partnerships |
| T+7 days | Follow-up content wave | Blog, social | Marketing |

### Step 5: Success Metrics
Track per channel:
- Impressions/reach
- Engagement (clicks, shares, replies)
- Traffic to announcement page
- Sign-ups/demo requests attributed to announcement
- Media coverage (number of articles, reach)
- Social share of voice vs. competitors

## Output
Save to `outputs/announcement-[product]-[YYYY-MM-DD].md`

### Deliverables:
1. **HERALD Brief**: Complete announcement strategy with headline story and layered messaging
2. **Content Package**: All 9 channel-specific assets ready for review
3. **Sequencing Timeline**: Hour-by-hour launch day execution plan
4. **Success Metrics Dashboard**: KPIs per channel with targets

## Chain Connections
- **Next skill**: Run `launch-command` to integrate announcement into full launch orchestration
- **Also feeds**: `enablement-forge` (announcement assets become sales tools), `demand-engine` (announcement drives demand)
- **Enhanced by**: Run after `position-lock` (messaging fuels announcement) and `battle-scanner` (competitive context shapes the story)
