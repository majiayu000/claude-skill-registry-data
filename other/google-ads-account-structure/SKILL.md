---
name: google-ads-account-structure
description: Structure a Google Ads account the right way. Use when the user asks about Google Ads account structure, the account hierarchy (account, campaign, ad group, ad and keyword or asset), MCC or manager accounts, how to organize campaigns and ad groups, ad group structure, the shared library (shared budgets, negative keyword lists, audience lists, placement exclusions), labels, or why structure still matters with Smart Bidding and Performance Max.
---

# Google Ads account structure

Decide how to map a marketing plan onto the Google Ads hierarchy: how many accounts, how
campaigns split, how tightly to theme ad groups, and how to wire the shared library and labels
so bidding, budgets, and reporting hold up. Structure is the biggest lever on whether Smart
Bidding gets clean signal and whether reporting answers the questions you will actually ask.
Bad structure is cheap to create and expensive to unwind once spend and conversion history
accrue.

Google Ads is Google's self-service auction platform. It buys Search, YouTube, the Display
Network, Discover, Gmail, and Maps through its own auction, organized by campaign type. It is
a different platform from DV360. Do not carry DV360's insertion-order or line-item model over.
For KPI definitions and shared math (CPA, ROAS, CPM, CPC), see the `programmatic-foundations`
skill. For which campaign type to run, see the `google-ads-campaign-types` skill.

## When to use this skill

- "How should I structure my Google Ads account?"
- "Do I need a manager account / MCC?" / "How do MCC accounts work?"
- "How do I organize campaigns and ad groups?" / "How should I theme my ad groups?"
- "What goes in the shared library?" / "Shared budgets, negative keyword lists, audience lists?"
- "Should I use labels? How?"
- "Does account structure still matter with Smart Bidding and Performance Max?"

Boundaries with sibling skills:
- Which campaign type to choose for a goal: hand off to `google-ads-campaign-types`.
- Bid strategy choice and Smart Bidding configuration: hand off to `google-ads-bidding`.
- Performance Max asset groups, listing groups, and structure: hand off to
  `google-ads-performance-max`.
- Keyword selection and match types inside an ad group: hand off to
  `google-ads-keywords-and-match-types`.
- Audience list construction and targeting: hand off to `google-ads-audiences-and-targeting`.
- Budget pacing and daily-budget mechanics: hand off to `google-ads-budgets-and-pacing`.
- Bulk edits and API-driven structure changes: hand off to `google-ads-api-and-bulk-operations`.
- Reading results by goal: hand off to `reporting-by-campaign-goal` and `google-ads-reporting`.

## Quick reference

The hierarchy, top to bottom:

```
Manager account (MCC)   optional; links and manages multiple Google Ads accounts centrally
  Account               one advertiser; one billing setup, time zone, and currency
    Campaign            one campaign type, budget, bid strategy, networks, geo and language
      Ad group          one tight theme; holds keywords (Search) or asset groups (PMax)
        Ad / Keyword    Search: keywords trigger ads. Display/Video: targeting and assets
        Asset           headlines, descriptions, images, video, sitelinks and other assets
```

What each level decides:

| Level | Owns | You change it when |
| --- | --- | --- |
| Account | Billing, time zone, currency, account-level conversions and exclusions | A separate legal entity, currency, or billing relationship is involved |
| Campaign | Campaign type, budget, bid strategy, networks, geo, language, schedule, devices | The budget, goal, campaign type, geo, or bidding differs |
| Ad group | One theme: its keywords or asset group, plus bids and the ads that serve | The theme, audience, or creative set differs enough to read or bid apart |

Key constraints to remember:
- Time zone and currency are set at account creation and cannot be changed afterward. Decide
  them deliberately.
- Budget and bid strategy live on the campaign, not the ad group. Anything that needs its own
  budget or its own optimization goal needs its own campaign.
- A keyword belongs to exactly one ad group. Theme is what keeps the ad relevant to the query.

## Core process

1. Decide the account boundary first. One advertiser, one billing relationship, one currency,
   and one time zone is one account. Use a manager account (MCC) to manage several accounts
   (clients, brands, or regions with separate billing or currency) from one login, with
   consolidated billing and cross-account shared resources where supported.
2. Split campaigns by the things only a campaign can hold: campaign type, budget, bid strategy,
   networks, geo, language, and schedule. Each distinct budget-and-goal cell is a candidate
   campaign, because budget and bid strategy do not exist below the campaign level. See the
   campaign-split rules below.
3. Inside each campaign, build tightly themed ad groups. For Search, one ad group is one
   coherent set of closely related keywords with ads written to match that theme, so Quality
   Score and relevance hold. For Display and Video, an ad group is a targeting-plus-creative
   unit. For Performance Max, the equivalent is the asset group (hand off to
   `google-ads-performance-max`).
4. Wire the shared library before you scale: shared budgets where campaigns should pool spend,
   negative keyword lists applied across Search campaigns, audience lists for reuse, and
   placement exclusion lists for Display and Video brand safety. Building these once and
   applying them broadly beats editing every campaign by hand.
5. Apply a consistent label scheme (and a naming convention) so you can filter and report on
   slices that cut across the hierarchy (test cells, promotions, priority products, regions).
6. Hand off campaign-type choice to `google-ads-campaign-types`, bidding to
   `google-ads-bidding`, and keyword build-out to `google-ads-keywords-and-match-types`.

## Decision rules and thresholds

### Use a MANAGER ACCOUNT (MCC) when

- You manage more than one Google Ads account (multiple clients, brands, or markets) and want
  one login, consolidated billing, and central user access management.
- Billing or currency differs across the businesses you run, so they cannot share one account
  but should still roll up to one place.
- You want to apply manager-level negative keyword lists or placement exclusions across client
  accounts from a single library.

A single advertiser with one budget and one currency does not need an MCC. Add one only when
the count of accounts or the billing split justifies the extra layer.

### Split CAMPAIGNS by

Each of these forces its own budget, bid strategy, network, or targeting scope, which only a
campaign can hold.

- Campaign type. Search, Performance Max, Demand Gen, Display, Video, Shopping, and App are
  distinct campaign types with their own inventory and controls. One campaign is one type.
- Budget. Anything that must own its daily budget is its own campaign. Campaigns do not share
  a budget unless you explicitly put them on a shared budget.
- Bid strategy and goal. A campaign carries one bid strategy. Separate campaigns when one
  group should optimize to a different target (for example, a prospecting Target CPA versus a
  retention Target ROAS). See `google-ads-bidding`.
- Geo and language. Split when budgets, performance, or messaging differ enough by market that
  you want to pace and read them independently.
- Networks. Keep Search and Display intent separate. Do not enable Display Network on a Search
  campaign as an afterthought, because the two behave differently on intent, benchmarks, and
  creative, and blended reporting hides what is working.
- Priority or product line. Separate campaigns when a product line, promotion, or seasonal push
  needs its own budget control and its own clean reporting line for finance or the client.
- Device or schedule, only when it must drive a budget split. Prefer bid adjustments and
  schedules within a campaign first; split to a separate campaign only when the slice needs its
  own budget.

### Theme AD GROUPS tightly

- One ad group is one theme. Group closely related keywords together and write ads that speak
  to exactly that theme, because tight relevance lifts Quality Score and click-through and keeps
  reporting legible.
- Aim for a small set of closely related keywords per ad group rather than a large grab bag.
  If a keyword would pull a different ad message, it belongs in its own ad group.
- Mirror the structure of the site or catalog. An ad group per product category or landing
  page keeps the query, the ad, and the landing page aligned.
- Do not over-split. Every extra ad group and campaign fragments conversion volume, and Smart
  Bidding needs enough conversions per bidding unit to learn (see `google-ads-bidding` on
  learning). Split only where you will act on the distinction or must read it apart.

### Shared library

Build these once and apply them across campaigns instead of editing each campaign by hand.

- Shared budgets. A single average daily budget shared by multiple campaigns, so underused
  budget reallocates to budget-limited campaigns. Available on Search, Shopping, Display, and
  Video campaigns; not available on App or Performance Max campaigns. Use shared budgets when
  campaigns share a goal and you want the system to balance spend across them; keep budgets
  separate when you need a hard per-campaign cap or a clean finance line.
- Negative keyword lists. Maintain blocklists (competitor terms, irrelevant intent, brand-safety
  terms) once and apply them to many Search campaigns. Limits: up to 20 negative keyword lists
  per account and up to 5,000 negative keywords per list; account-level negative keywords are
  capped at 1,000. See `google-ads-keywords-and-match-types` for how negatives interact with
  match types.
- Audience lists (audience segments). Build remarketing and data segments once and reuse them
  across campaigns for targeting or observation. See `google-ads-audiences-and-targeting`.
- Placement exclusion lists. Maintain brand-safety placement blocklists for Display and Video
  and apply them at account or campaign level, so unsuitable sites, apps, and videos are
  excluded consistently. See `google-ads-audiences-and-targeting` for placement targeting.

### Labels

Use labels to tag campaigns, ad groups, ads, and keywords with custom categories (for example
`promo-bf`, `test-cell-A`, `priority-sku`, `region-west`) so you can filter and report on slices
that cut across the hierarchy. Labels are not inherited down the hierarchy, so apply a label at
each level you want to report on. Pair labels with a consistent naming convention; labels slice,
names describe.

### Account and campaign limits

Google Ads enforces ceilings on the number of campaigns, ad groups, keywords, and assets per
account, and these numbers change over time, so confirm the current caps in the live Help center
or product UI before you design a very large account rather than relying on a remembered number.
The limits verified here are the shared-library ones above (20 negative keyword lists per
account, 5,000 negative keywords per list, 1,000 account-level negatives). In practice you hit a
manageability and Smart Bidding signal wall long before a hard limit, so structure for clean
signal and clean reporting, not for the maximum object count.

## Why structure still matters with Smart Bidding and Performance Max

Automation did not remove the need for deliberate structure. It changed what structure is for.

- Signal. Smart Bidding optimizes per campaign and per bid strategy. Conversion volume that is
  fragmented across too many tiny campaigns starves each strategy of the data it needs to hit a
  target. Consolidate where the cells share a goal so each bidding unit gets enough conversions.
- Budgets. Budget is still a campaign-level lever. How you split campaigns determines where
  money can and cannot flow, and a single mega-campaign gives up the ability to fund a priority
  line independently. Shared budgets are a tool, not a default.
- Reporting and control. The campaign and ad group boundaries are the lines your reports break
  on and the levers you pull to control geo, schedule, networks, and exclusions. Performance Max
  hands creative and placement decisions to Google, but you still control it through the
  boundary you draw around it: its own campaign, its own budget and goal, its asset groups, and
  its negative and brand-safety exclusions. Structure is how you keep control of an automated
  campaign type.

## Templates and examples

A direct-response advertiser, single account, US only, running brand plus non-brand Search and
a Performance Max campaign for the catalog:

```
Account: ACME (USD, America/Los_Angeles, one billing setup)
  Campaign: ACME_Search_Brand        (own budget; Target impression share or tCPA; brand terms)
    Ad group: Brand-Core             (acme, acme.com variants)
    Ad group: Brand+Category         (acme running shoes, acme trail shoes)
  Campaign: ACME_Search_NonBrand     (own budget; Target CPA; category demand)
    Ad group: Running-Shoes          (tightly themed running-shoe keywords)
    Ad group: Trail-Shoes            (tightly themed trail-shoe keywords)
  Campaign: ACME_PMax_Catalog        (own budget; Target ROAS; Merchant Center feed)
    Asset group: Running             (assets + listing group for running products)
    Asset group: Trail               (assets + listing group for trail products)

Shared library:
  Negative keyword list "brand-terms-block"  -> applied to ACME_Search_NonBrand
  Negative keyword list "junk-intent"        -> applied to both Search campaigns
  Audience list "site-visitors-30d"          -> reused for observation and PMax signal
Labels: priority-sku, promo-bf (applied at ad group and campaign level for reporting)
```

Why it splits this way: brand and non-brand are separate campaigns because they carry different
budgets, bid targets, and intent, and you must read them apart. Performance Max is its own
campaign with its own budget and Target ROAS so it neither borrows from nor starves Search.
Negatives and audiences live in the shared library so one edit applies everywhere.

## Common pitfalls

- One mega-campaign for everything. You lose independent budget control and you blend goals that
  Smart Bidding cannot serve with a single target. Split by budget and goal first.
- Over-splitting into many tiny campaigns or ad groups. Each bidding unit starves for
  conversions and the account becomes unmanageable. Consolidate cells that share a goal.
- Loose ad groups. A grab bag of unrelated keywords drags Quality Score and forces a generic ad.
  Keep each ad group to one theme with ads written for it.
- Enabling the Display Network on a Search campaign for "extra reach." Display intent and
  benchmarks differ from Search, and the blended numbers hide performance. Run Display as its own
  campaign.
- Treating Performance Max as set-and-forget. It still needs its own campaign boundary, budget,
  goal, asset groups, and brand-safety and negative exclusions to stay under control. See
  `google-ads-performance-max`.
- Setting the wrong time zone or currency at account creation. Both are permanent. Confirm
  before you create the account.
- Editing negatives or exclusions campaign by campaign. Use shared library lists so one change
  propagates.

## Reference material

- For the Google Ads hierarchy and account creation basics, see the Sources below; the
  "Organize your account with ad groups" and "How ad groups work" pages are the canonical
  account-structure references.

## Sources

- [Create a campaign](https://support.google.com/google-ads/answer/6324971) (as of June 2026)
- [Create a Google Ads manager account](https://support.google.com/google-ads/answer/7459399) (as of June 2026)
- [How ad groups work](https://support.google.com/google-ads/answer/2375404) (as of June 2026)
- [Organize your account with ad groups](https://support.google.com/google-ads/answer/6372655) (as of June 2026)
- [About ads labels](https://support.google.com/google-ads/answer/2475865) (as of June 2026)
- [About shared budgets](https://support.google.com/google-ads/answer/10487241) (as of June 2026)
- [About negative keyword lists](https://support.google.com/google-ads/answer/2453983) (as of June 2026)
- [Exclude specific webpages and videos](https://support.google.com/google-ads/answer/2454012) (as of June 2026)
- [Google Network](https://support.google.com/google-ads/answer/1752334) (as of June 2026)
- [About Performance Max campaigns](https://support.google.com/google-ads/answer/10724817) (as of June 2026)
