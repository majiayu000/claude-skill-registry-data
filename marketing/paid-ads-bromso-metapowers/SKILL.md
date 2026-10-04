---
description: Plan and optimize paid advertising campaigns
---

# Paid Ads

Plan paid advertising campaigns for "$ARGUMENTS". Design campaign structure, targeting, budget allocation, and optimization strategy.

## Prerequisites

Read `.metapowers/marketing/$ARGUMENTS/00-strategy.md`. If this file does not exist, tell the user:

> Phase 0 (Strategy) has not been completed for "$ARGUMENTS". Run `/marketing:customer-research $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check and log to `.metapowers/marketing/$ARGUMENTS/skip-log.md`.

## Process

1. **Read context:**
   - Read `.metapowers/marketing/$ARGUMENTS/00-strategy.md` for audience, positioning, and competitors
   - Read `.metapowers/marketing/$ARGUMENTS/02-act.md` if it exists (for landing page and copy context)
   - Read `plugins/marketing/shared/campaign-plan-template.md` for structure

2. **Platform selection:**
   - Which platforms? Google Ads, Meta (Facebook/Instagram), LinkedIn, X, TikTok, Reddit
   - Match platform to audience and intent (search intent vs. interruption marketing)
   - Budget allocation per platform

3. **Campaign structure:**
   - Campaign hierarchy: campaigns → ad groups → ads
   - Targeting strategy per campaign: keywords, audiences, demographics, interests
   - Match types (for search): broad, phrase, exact
   - Negative keyword strategy
   - Retargeting setup: website visitors, cart abandoners, engaged users

4. **Budget and bidding:**
   - Recommended daily/monthly budget
   - Bidding strategy: manual CPC, target CPA, maximize conversions
   - Budget pacing and scaling plan
   - Expected CPC and CPA ranges for the category

5. **Optimization plan:**
   - Key metrics to monitor: CTR, CPC, CPA, ROAS, quality score
   - Optimization cadence (daily, weekly, monthly actions)
   - When to scale, pause, or restructure campaigns
   - Testing plan: ad copy, audiences, landing pages

6. **Write the artifact** — append to `.metapowers/marketing/$ARGUMENTS/03-convert.md` under a `## Paid Ads` section:
   - **Platform Strategy** — selected platforms with rationale
   - **Campaign Structure** — hierarchy, targeting, match types
   - **Budget Plan** — allocation, bidding, pacing
   - **Ad Copy Direction** — messaging angles per campaign
   - **Optimization Playbook** — metrics, cadence, scaling rules

## Output

Paid ads strategy written to `.metapowers/marketing/$ARGUMENTS/03-convert.md`. Present a summary highlighting:
- Recommended platforms and budget split
- Campaign structure overview
- Expected CPA range
