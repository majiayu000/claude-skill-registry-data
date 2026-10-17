---
name: ttd-targeting-and-audiences
description: How audiences, data, and targeting work on The Trade Desk at a conceptual level. Use when the user asks about Trade Desk targeting, TTD audiences, the TTD data marketplace, first-party data on TTD, third-party data, contextual targeting, seeds, lookalikes, retail data, or UID2 audiences. Covers the publicly documented model of onboarding first-party data, layering marketplace and retail data, and building audiences on Unified ID 2.0, and flags which exact targeting controls live in the partner platform.
---

# The Trade Desk targeting and audiences

How The Trade Desk decides who to reach: you onboard first-party data, enrich and extend it
with third-party and retail data from the data marketplace, add contextual signals, and tie it
all together with a durable identity built on Unified ID 2.0. This skill explains the publicly
documented approach so an agent can reason about a TTD audience strategy. The exact targeting
menus, segment pickers, and audience-builder fields live in the partner platform behind a
login, so this skill states the concept and flags where the operator confirms specifics in the
product.

This skill assumes you know audience, segment, reach, frequency, first- vs third-party data,
and contextual vs audience targeting. For those definitions, see the `programmatic-foundations`
skill. For how an audience feeds the bid as a seed and how the AI scores impressions, see the
`ttd-bidding-and-optimization` skill (sibling). For the identity layer in depth, see the
`ttd-identity-and-uid2` skill (sibling).

## When to use this skill

- "How does targeting work on The Trade Desk?" / "How do TTD audiences work?"
- "How do I get my first-party data onto TTD?" / "CRM onboarding on The Trade Desk."
- "What is the TTD data marketplace?" / "How do I buy third-party data on TTD?"
- "Contextual targeting on The Trade Desk."
- "How do I build a lookalike / a seed audience?"
- "Can I use retail data?" / "UID2 audiences."

Boundaries with sibling skills:
- Unified ID 2.0 and EUID mechanics (hashing, tokens, opt-out, integration):
  `ttd-identity-and-uid2`. This skill uses UID2 as an audience signal and links there for how
  it works.
- How an audience becomes a seed and how the AI scores impressions and sets bids:
  `ttd-bidding-and-optimization`.
- Campaign and ad group structure where targeting is attached: `ttd-campaign-structure`.
- Inventory, deals, and supply paths: `ttd-inventory-and-deals`.
- Programming audiences through the API: `ttd-api-and-automation`.
- Measuring audience performance and attribution: `ttd-measurement-and-reporting`.

## Quick reference

| The user wants | Concept that answers it | Where the specifics live |
| --- | --- | --- |
| To use their own customer data | Onboard first-party data (CRM, clean rooms, CDPs, cloud storage) | Partner platform |
| To extend or enrich an audience | Layer third-party and retail data from the data marketplace | Partner platform |
| To target by content, not user | Contextual targeting | Partner platform |
| To find more like their best customers | Build a seed, then a lookalike from it | Partner platform |
| To reach shoppers by purchase | Retail data via retail media partnerships | Partner platform plus partner terms |
| Durable addressability | Audiences resolved on Unified ID 2.0 and EUID | See `ttd-identity-and-uid2` |

The recurring pattern: start from first-party data, build the largest accurate seed across the
ID types you have, then enrich and extend with marketplace, retail, and contextual signals, all
resolved through a durable identity. The exact segment names and builder fields are in the
product, so confirm labels there rather than guessing.

## Core process

Use this to reason about or advise on a TTD audience and targeting strategy.

1. Start from the objective. Prospecting, retargeting, and retention need different audiences,
   so name the goal first. The `reporting-by-campaign-goal` skill maps objective to KPI, which
   tells you what the audience has to deliver.
2. Onboard first-party data as the foundation. The Trade Desk supports importing first-party
   data from sources such as CRM onboarding, clean rooms, CDPs, and cloud storage, so the most
   valuable known-customer data drives targeting. Resolve it across devices before you use it.
3. Build the largest accurate seed. The public guidance is to assemble the largest seed
   audience for reach across the ID types you hold, from traditional IDs through to UID2, so
   the audience and any lookalike from it have scale. This seed is also the input the AI uses
   on the bidding side; hand that to `ttd-bidding-and-optimization`.
4. Enrich and extend with the data marketplace. Layer third-party data to expand and refine
   targeting by demographic, behavior, and context. The marketplace includes retail data and
   segments that carry multiple ID types, including UID2.
5. Add retail data where it fits the goal. Through retail media partnerships, brands can target
   shoppers based on real purchase signals and connect media to sales. Availability and terms
   depend on the specific retail partner, so confirm both the segments and the contractual
   access in the platform and with the partner.
6. Use contextual targeting when the goal is the content, not the user. Contextual targets the
   environment rather than a profile, which is useful for suitability and for privacy-conscious
   reach. Confirm the exact contextual categories in the platform.
7. Resolve everything through a durable identity. Audiences built on Unified ID 2.0 and EUID
   keep addressability on the open internet beyond third-party cookies. For how UID2 works and
   its opt-out model, hand off to `ttd-identity-and-uid2`.
8. Verify the audience delivers against the KPI. Scale, match rate, and performance only matter
   relative to the goal, so confirm with `ttd-measurement-and-reporting` and adjust.

## Decision rules and thresholds

The Trade Desk does not publish fixed match-rate or audience-size thresholds on its public
pages, and the live targeting controls sit in the partner platform. Apply these public,
concept-level rules and confirm the exact settings in the product.

- First-party data is the anchor for known-customer targeting and the strongest seed input.
  Lead with it, then extend, rather than starting from broad third-party segments.
- Build the seed as large and accurate as the available IDs allow. A bigger, cleaner seed gives
  reach and a better lookalike; a thin seed limits both.
- Prefer durable identifiers for longevity. UID2 and EUID keep audiences addressable on the
  open web as third-party cookies decline, so favor them where coverage allows. See
  `ttd-identity-and-uid2`.
- Use contextual when you cannot or should not rely on a user profile, for suitability,
  privacy-conscious reach, or where audience signal is thin.
- Treat retail data as goal-specific and access-gated. It shines for purchase-based targeting
  and closed-loop sales measurement, but the available segments and the right to use them
  depend on the specific retail partner. Confirm both in the platform.
- Match the audience to the funnel stage. Retargeting and retention lean on first-party
  audiences; prospecting leans on lookalikes plus marketplace and contextual reach.

When a recommendation depends on an exact segment name, marketplace provider, match rate,
minimum audience size, or builder field, say so plainly: that specific detail is set in the
partner platform (and, for retail and third-party data, under the provider's terms), and the
operator should confirm it there.

## How the pieces fit together

A plain-language model of the publicly described components, so an agent can explain them.

- First-party data onboarding. You import your own customer data through CRM onboarding and
  related paths from collection points such as clean rooms, CDPs, and cloud storage, then
  resolve it across devices for activation.
- Seed. The largest accurate audience you can build across your ID types. It serves both as a
  targeting audience and as the input that teaches the AI what a valuable customer looks like
  on the bidding side.
- Data marketplace. A marketplace to layer, enrich, and expand targeting by demographic,
  behavior, and context, populated by many data providers (including retail) with segments that
  carry multiple ID types, including UID2.
- Third-party data. Provider segments from the marketplace used to extend reach and refine
  targeting beyond your first-party data.
- Retail data. Purchase-based segments available through retail media partnerships that let
  brands reach shoppers by real purchase signals and connect media to sales.
- Contextual targeting. Targeting the content and environment rather than a user profile.
- Identity. Unified ID 2.0 and EUID provide durable, privacy-conscious addressability that the
  audiences resolve through. Mechanics live in `ttd-identity-and-uid2`.

Specific product features such as Galileo and the live segment catalog are configured in the
partner platform and evolve over time; confirm current names and availability there.

## Templates and examples

Advice framing, conceptual (confirm exact controls in the platform):

> "Anchor on your first-party converter list. Onboard it (CRM onboarding, or from your clean
> room or CDP), resolve it across devices, and build the largest accurate seed across the IDs
> you have, including UID2. For prospecting, extend that seed with a lookalike plus relevant
> third-party segments from the data marketplace; if purchase intent matters, add retail data
> where your retail partner allows it. Use contextual where you want the environment rather than
> a profile. The exact segment names and builder fields are in the platform, so confirm them
> there, and see the identity skill for how UID2 resolves the audience."

Triage framing when an audience underdelivers:

> "Check the seed first: is it large and accurate, or thin? A small seed caps reach and weakens
> the lookalike. Confirm first-party data onboarded and resolved correctly. If reach is the
> gap, extend with marketplace and contextual; if relevance is the gap, tighten the seed and
> the third-party layer. Match-rate and segment-size specifics are in the partner platform, so
> verify them there."

## Common pitfalls

- Starting from broad third-party segments instead of anchoring on first-party data, which
  weakens both targeting and the seed.
- Building too small a seed, then expecting strong reach or a good lookalike from it.
- Assuming retail data is freely usable. Availability and rights depend on the specific retail
  partner; confirm segments and terms.
- Reaching for an audience profile when contextual would serve the goal better, for suitability
  or privacy-conscious reach.
- Ignoring identity durability and leaning on signals that fade as third-party cookies decline.
  Favor UID2 and EUID where coverage allows; see `ttd-identity-and-uid2`.
- Inventing segment names, provider names, or match-rate numbers. When the detail is
  platform-specific or provider-gated, say it is set in the partner platform and have the
  operator verify it.

## Sources

- The Trade Desk, Our Demand Side Platform (DSP) overview (first- and third-party data, the marketplace of the world's biggest retailers, Unified ID 2.0 and EUID): https://www.thetradedesk.com/our-demand-side-platform (as of June 2026)
- The Trade Desk, Get more from first-party data on The Trade Desk (onboarding from CDPs and clean rooms, building the largest seed across ID types including UID2): https://www.thetradedesk.com/resources/get-more-from-first-party-data-on-the-trade-desk (as of June 2026)
- Unified ID 2.0, official site (definition of UID2, open-source identity, universal opt-out): https://unifiedid.com (as of June 2026)

Note on sourcing: The Trade Desk's detailed product documentation, the live segment catalog,
and the audience-builder reference sit behind a partner login and are not cited here. The exact
targeting controls, segment names, marketplace providers, and match rates require access to the
partner platform, and retail and third-party data are also governed by the relevant provider's
terms.
