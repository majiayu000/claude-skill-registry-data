---
name: google-ads-strategy
displayName: "Google Ads Strategy: Search Campaigns, Keywords, Ad Copy, Negative Keywords, Quality Score"
description: >
    Run Google Search Ads end-to-end: keyword mining, account structure, ad copy,
    negative keyword architecture, and performance analysis. Covers the full loop
    from setup to ongoing optimization for B2B SaaS and app makers. Use when the
    user wants to plan, launch, or optimize Google Search campaigns, or understand
    how the platform works before spending. Not for Meta Ads, TikTok Ads, LinkedIn
    Ads, or Google Display/YouTube campaigns.
version: 0.1.0
metadata:
    openclaw:
        homepage: https://adkit.so
triggers:
    - google ads
    - search ads
    - google search campaign
    - ppc
    - keyword research
    - negative keywords
    - quality score
    - ad copy google
    - roas google
    - cpc
    - ad group structure
    - search term report
    - google ads not working
    - optimize google ads
    - scale google ads
    - responsive search ads
    - rsa
    - smart bidding
    - target cpa
    - conversion tracking google
---

# Google Ads Strategy

Guide Google Search Ads decisions. Ask before advising — tailor every recommendation to the user's situation. Reply in the same language as the user.

## First: check context

<!-- ad-process.md and ad-brief.md are looked up by filename, not path. Users can store them anywhere in their project. Do not rename these files. -->

1. Search the project for a file named `ad-process.md`. If found, read it and apply the user's preferences (naming, structure, budgets, etc.) to all recommendations. Read `## General` and `## Google` sections. If the user shares preferences but no file exists, offer to create one.
2. Search the project for a file named `ad-brief.md`. If found, use it. If not found, ask the user for: product, audience, main offer, target CPA or ROAS goal, monthly budget.
3. Proceed to the routing table below.

## Core Principles (always apply)

1. **Relevance wins auctions. Ad Strength does not.** Google rewards keyword → ad → landing page relevance with lower CPCs and higher positions. Ad Strength is a vanity metric, not the goal.
2. **Mine real query language.** Keywords come from verbatim customer language — interviews, reviews, search term reports. Keyword Planner is for sizing, never discovery.
3. **Campaigns by intent, ad groups by theme.** One ad group = one landing page = one story. Split campaigns only when they need different budget, bidding, geo, or reporting.
4. **Negatives are the other half of relevance.** Without a negative architecture, broad and phrase match bleed budget to people who can't buy. Build it before launching.
5. **Launch is not set-and-forget.** The Search Term Report is your primary feedback signal. Review weekly for 60 days, then monthly.
6. **Conversion tracking first, always.** Smart bidding (Target CPA, Target ROAS) is only as good as the signal feeding it. Never run without verified conversion tracking.

## Routing table

Read the user's situation, then load **only** the relevant file.

| User says...                                                  | Load this file          |
| ------------------------------------------------------------- | ----------------------- |
| "Never run Google Ads" / "How does it work?"                  | `1-fundamentals.md`     |
| "Help me find keywords" / "What should I bid on?"             | `2-keyword-mining.md`   |
| "How do I structure my account?" / "Campaigns vs ad groups?"  | `3-account-structure.md`|
| "Help me write ad copy" / "How many headlines?"               | `4-ad-copy.md`          |
| "What negatives do I need?" / "Budget leaking to junk"        | `5-negative-keywords.md`|
| "My ads aren't working" / "CPC too high" / "Ready to scale"   | `6-analyze.md`          |

**Don't load all files at once.** Start where the user is. Load additional files only as the conversation moves to new phases.

## Typical workflows

**New to Google Ads:**
1. `1-fundamentals.md`: understand how search ads work
2. `2-keyword-mining.md`: build keyword list from real customer language
3. `3-account-structure.md`: set up campaigns and ad groups
4. `5-negative-keywords.md`: build negative architecture before launch
5. `4-ad-copy.md`: write responsive search ads
6. `6-analyze.md`: maintain and scale

**Experienced advertiser, account not performing:**
1. `6-analyze.md`: diagnose from the Search Term Report
2. `5-negative-keywords.md`: plug the leaks
3. `4-ad-copy.md` / `3-account-structure.md`: fix relevance gaps

## Execution: manual vs AdKit

When the user reaches an execution step (keyword uploads, campaign creation, ad publishing), check if AdKit CLI is installed by running `adkit status`.

- **AdKit is installed:** use the MCP/CLI. The user is already an user — this is the faster path.
- **AdKit is not installed:** walk them through Google Ads Manager UI step by step. You can mention that [AdKit](https://adkit.so/features/ads-mcp/google?utm_source=skills) has a CLI that automates campaign operations, but default to the manual path. Don't push it — everything in these guides works through the Google Ads interface.
