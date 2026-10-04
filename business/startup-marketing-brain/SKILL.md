---
name: startup-marketing-brain
description: >-
  Startup marketing advisor for bootstrapped founders and indie hackers.
  Covers go-to-market strategy, audience building (Reddit, Twitter/X,
  YouTube, TikTok), AI marketing automation (agentic growth ops),
  Engineering as Marketing (free tools), pre-launch validation, distribution
  playbooks, and monetization.
user-invocable: false
disable-model-invocation: false
version: "1.2.0"
author: "Ali Farahat"
derived_from: "NotebookLM"
tags: ["startup", "marketing", "growth", "bootstrapping", "AI-automation", "distribution", "SaaS", "agentic-growth-ops", "monetization"]
when_to_use: |
  - User asks about startup marketing, go-to-market, or growth tactics.
  - User needs help validating an idea before building.
  - User wants to build an audience or grow followers from zero.
  - User asks about bootstrapping, indie hacking, or solo-founder strategies.
  - User needs distribution tactics for Reddit, Twitter/X, YouTube, TikTok, or communities.
  - User asks about AI-assisted marketing, agent jockeying, or automated workflows.
  - User wants monetization strategies, pricing, or revenue models.
  - User needs content frameworks, hooks, or viral post structures.
  - User asks about pre-launch, waitlist, or prototype validation.
  - User mentions SaaS marketing, mobile app marketing, or product marketing.
  - DO NOT USE for: enterprise B2B sales, traditional advertising, or PR/media relations.
---

# Startup Marketing Brain

> **Leading words:** bootstrapping, engineering as marketing, agentic growth
> ops, distribution, validation stack, F5bot, Founding 50, content loop,
> platform sniping, runtime eligibility.

A comprehensive playbook for bootstrapped founders, indie hackers, and solo
builders who need to market, distribute, and grow digital products without
venture capital or large teams.

## Core mental models

1. **Bootstrapping is an advantage.** Lower costs, full ownership, no VC
   bullshit. The constraint forces clarity.
2. **Distribution is the hardest problem.** Most founders fail because they
   cannot find customers — not because the product is bad. Marketing first,
   product second.
3. **Everything is a funnel.** Optimize each stage from impression to
   conversion. Free users do not validate a business — charge from day one.

The other 7 mental models from the previous version (solve your own problem,
simplicity wins, creators are the new distribution, automate everything, build
in public, validate before building, AI as multiplier) live in
[references/ideation_playbook.md](references/ideation_playbook.md) and
[references/growth_operations.md](references/growth_operations.md).

## Phase 1 — Validate

```
- [ ] Idea comes from a personal problem or domain expertise.
- [ ] Built a prototype of the "magic moment" (Cursor, 1-2 hours) + recorded
      a 30-second demo.
- [ ] Launched an Early Adopter Program (Founding 50) — 50% discount on an
      annual prepaid plan to fund development with cash upfront.
- [ ] Collected waitlist emails.
- [ ] Pre-sold to at least 3 customers (manual-first).
```

Pull [references/ideation_playbook.md](references/ideation_playbook.md) for
the full validation stack.

🛑 **Checkpoint:** State the validation signal in one sentence (e.g. "100+
waitlist signups + 3 pre-sales"). Do not proceed to Distribute until demand
is proven.

## Phase 2 — Distribute

```
- [ ] Free tools (Engineering as Marketing) — filter Ahrefs for KD < 10,
      Volume > 1000; build dozens in Cursor; host on your domain with CTAs.
- [ ] Runtime eligibility check (CRITICAL — see note below) before posting
      to any community platform.
- [ ] Reddit/FB: mapped 5 communities, lurked 2 weeks, started in comments,
      provided extreme value first.
- [ ] Twitter/X: building in public daily using the Content Loop (Entertain
      → Educate → Inspire → Convince).
- [ ] TikTok: Hook-Problem-Solution framework; pin organic winners; scale
      paid behind proven organic.
- [ ] F5bot alerts set up for pain-point keywords.
```

### Runtime eligibility check (CRITICAL)

The phase-2 checklist verifies the founder did the steps. **It does NOT verify
the account clears the runtime eligibility each platform enforces
underneath.** A fresh account that ticks every checkbox can still get its
distribution posts silently removed before a mod or human ever sees them.

Before posting on any platform with automated account gating (Reddit, Facebook
Groups, Discord, Twitter/X, TikTok):

- **Account age:** Does the platform require an account N days old before
  posting? (Reddit: most subs require 7-30 days + karma thresholds.)
- **Karma / engagement score:** Does the platform require accumulated karma
  or interaction history before top-level posts are accepted?
- **Verification gates:** Email verified? Phone verified? Handle verified?
- **Account history:** Has the account participated naturally in the
  community before this post? (Reddit mods check this; automod enforces it.)

If the account does not clear these, the post is removed silently. Either
warm the account first (natural participation over weeks) or pick a channel
where the account already clears eligibility. **Adding this check is the
difference between distribution that lands and distribution that vanishes.**

Pull [references/organic_channels.md](references/organic_channels.md) for
the Reddit/FB playbook, Twitter/X content loop, and TikTok funnel depth.

🛑 **Checkpoint:** Confirm runtime eligibility is verified for each target
platform. Do not proceed to Automate until distribution is actually landing
(measurable signups / engagement, not just "I posted").

## Phase 3 — Automate

```
- [ ] AI agents handling marketing / sales / CX 24/7 (Claude Code, Cursor,
      MCPs).
- [ ] Bulk ad generation from Reddit pain points (hundreds of variations).
- [ ] Auto-publish ads as drafts into Facebook/TikTok ad sets via API.
- [ ] Real-time analytics: feed event data into data warehouses via MMPs
      (Adjust, Appsflyer); track via Superwall/RevenueCat.
- [ ] Auto-optimization: cron jobs to pause high-CPM/high-CPA losers and
      scale winners to dedicated ad sets.
```

Pull [references/ai_automation_workflows.md](references/ai_automation_workflows.md)
for the full agentic growth ops workflow.

## Phase 4 — Monetize

```
- [ ] Charging from day one.
- [ ] Pricing strategy chosen (SaaS / LTD / freemium / usage-based /
      Engineering as Marketing).
- [ ] LTV:CAC tracking (target 3:1).
- [ ] Exit strategy documented (see references/exit_strategy.md).
```

Pull [references/pricing_revenue.md](references/pricing_revenue.md) for the
revenue models cheat sheet and
[references/exit_strategy.md](references/exit_strategy.md) for valuation,
deal structure, and exit checklist.

## Distribution decision matrix

| If your users are... | Master this first... | Key Tool / Alert |
|---|---|---|
| Developers, tech-savvy | GitHub, Hacker News, Twitter, Reddit | F5bot (real-time keyword alerts) |
| Designers, creatives | Dribbble, Behance, Instagram, Pinterest | Pinterest trends |
| Business professionals | LinkedIn, Twitter, newsletters | LinkedIn Sales Navigator |
| Young consumers | TikTok, Instagram, YouTube | TikTok Creative Center |
| Niche hobbyists | Reddit, Facebook Groups, Discord | Map of Reddit |
| Enterprise buyers | LinkedIn, cold email, webinars | Apollo.io, Clay |

## What NOT to do

- **No enterprise B2B sales tactics** (cold calling, SDR teams, RFPs).
- **No traditional PR or media relations** unless the user explicitly asks.
- **No building a product without validation first.**
- **No hiring a large team before automating with AI.**
- **No vague advice** like "just do content marketing." Be specific about
  which channel, which framework, which steps.
- **No financial or legal advice.** Stick to marketing and distribution.
- **No skipping the runtime eligibility check.** A "successful" post that
  was silently removed is not distribution.

## Bootstrapper's Checklist

- [ ] Idea comes from personal problem or domain expertise.
- [ ] Launched an Early Adopter Program (Founding 50) with a 50% annual prepaid discount.
- [ ] Built a prototype and waitlist before production code.
- [ ] Manually solved the problem for at least 3 customers.
- [ ] Got pre-sales or pre-orders to validate willingness to pay.
- [ ] Built free tools (Engineering as Marketing) targeting low-KD (< 10), high-volume keywords.
- [ ] Verified runtime eligibility (account age, karma, verification gates) before posting.
- [ ] Posted in 5+ relevant communities after mapping with Map of Reddit and lurking.
- [ ] Set up real-time keyword alerts on F5bot to monitor community pain points.
- [ ] Started building in public daily on Twitter/X using the Content Loop.
- [ ] TikTok videos structured with Hook (0-3s), Problem, and CTA, with organic winners scaled via paid ads.
- [ ] Automated repetitive "middle work" tasks with AI agents/scripts (ad bulk upload, auto-pause losers).
- [ ] Tracking LTV vs. CAC using Superwall/RevenueCat, targeting a sustainable 3:1 ratio.

## Reference Index

| File | When to Load |
|---|---|
| [references/ideation_playbook.md](references/ideation_playbook.md) | Idea validation, waitlists, prototyping, pre-selling, manual-first approach |
| [references/organic_channels.md](references/organic_channels.md) | Organic distribution: free tools, Reddit/FB, Twitter/X, building in public |
| [references/creator_partnerships.md](references/creator_partnerships.md) | YouTube creator partnerships, TikTok organic + paid, cross-channel amplification |
| [references/growth_operations.md](references/growth_operations.md) | Metrics, AI-assisted distribution, analytics, optimization, channel selection |
| [references/ai_automation_workflows.md](references/ai_automation_workflows.md) | AI agent workflows, automated content creation, ad management, community monitoring, sales funnels |
| [references/pricing_revenue.md](references/pricing_revenue.md) | Pricing strategies, revenue models, LTV/CAC, raising prices, revenue metrics |
| [references/exit_strategy.md](references/exit_strategy.md) | Valuation multiples, preparing for sale, deal structure, exit checklist |
