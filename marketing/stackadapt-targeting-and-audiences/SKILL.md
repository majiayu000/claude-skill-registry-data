---
name: stackadapt-targeting-and-audiences
description: Build and layer targeting and audiences on a StackAdapt ad group. Use for StackAdapt targeting, StackAdapt audiences, StackAdapt retargeting, building a lookalike on StackAdapt, contextual targeting on StackAdapt, or when the user asks how to combine pixel retargeting, lookalike, third-party data, custom segments, contextual or Page Context AI, geo, device, OS, language, dayparting, and inventory or domain targeting and exclusions.
---

# StackAdapt targeting and audiences

Decide which targeting layers an ad group runs and the order to stack them so it reaches the
right users without starving delivery. StackAdapt is a self-serve multi-channel demand-side
platform, strongest in native and also running display, video, connected TV, audio, in-app,
and digital out-of-home. Contextual is a particular strength: Page Context AI reads the page
itself rather than the user, so it works without third-party cookies.

This skill owns the targeting decision. For where targeting sits in the build order, see the
`stackadapt-campaign-setup` skill. For inventory lists and brand-safety controls, hand off to
`stackadapt-inventory-and-brand-safety`. For KPI definitions and audience-size math, see the
`programmatic-foundations` skill. To read whether an audience is delivering against the goal, the
`reporting-by-campaign-goal` skill has the by-objective report recipes.

## When to use this skill

- "Set up targeting for my StackAdapt ad group." / "What targeting should I use on StackAdapt?"
- "Build a retargeting audience from the StackAdapt pixel."
- "Create a lookalike on StackAdapt." / "Expand my audience."
- "Use third-party data / a custom segment on StackAdapt."
- "Set up contextual targeting on StackAdapt." / "How does Page Context AI work?"
- "Target by geo, device, OS, language, or daypart." / "Exclude these domains."
- "How do I layer all of these together without killing delivery?"

Boundaries. Targeting is set on the ad group (the line item on StackAdapt), so everything here
is per ad group. Inventory selection, exchanges, and brand-safety lists belong to
`stackadapt-inventory-and-brand-safety`, though domain include and exclude lists are covered
here because they are a targeting decision. Bid and budget sizing belong to
`stackadapt-bidding-and-budgets`.

## Quick reference

Pick the audience spine first (one per ad group), then add refinement and constraint layers:

| Layer | Type | What it does | Typical use |
| --- | --- | --- | --- |
| Retargeting | Audience spine | Re-reach users the pixel saw on your site | Lower funnel, win-back, cart abandon |
| Lookalike / Lookalike Expansion | Audience spine | Find users who behave like a seed audience | Prospecting at scale off 1P or a segment |
| First-party (CRM) segment | Audience spine | Target or suppress your own customer list | Cross-sell, suppression, ABM |
| Third-party data | Audience spine | Buy curated demographic, behavioral, intent segments | Top-funnel prospecting |
| Custom / Browsing segments | Audience spine or refine | StackAdapt-built segments, including browsing-based | Niche intent not in 3P |
| Contextual (Page Context AI) | Audience spine or refine | Match the page topic, not the user, cookie-free | Native prospecting, cookieless reach |
| Keyword Rule Targeting | Refine | Include or exclude exact keywords on the page | Tighten or brand-safe a contextual buy |
| Geo | Constraint | Country, state, DMA, city, postal or ZIP, radius | Every campaign |
| Device / OS / browser | Constraint | Desktop, mobile web, in-app, CTV, OS, browser | Match creative and goal |
| Language | Constraint | User or content language | Multi-language markets |
| Dayparting | Constraint | Hour of day and day of week | Business hours, time-sensitive offers |
| Domain / inventory include or exclude | Constraint | Allow or block specific publishers | Brand safety, focus, exclusions |

Spine drives reach. Refinements narrow it toward intent. Constraints clip it to who is eligible.
Add them in that order so you always know which layer is the one limiting delivery.

## Core process

1. Choose the audience spine for the ad group. Pick exactly one primary axis: retargeting,
   lookalike, first-party, third-party, custom or browsing, or contextual. One spine per ad
   group keeps reporting and optimization legible, and it is why prospecting and retargeting are
   separate ad groups (see `stackadapt-campaign-setup`).
2. If the spine is retargeting, build the audience from the pixel. The StackAdapt universal pixel
   on every page cookies site visitors so you can re-reach them. Segment visitors by behavior
   (viewed product, abandoned cart, started but did not finish a form) and set a lookback window
   that matches the purchase cycle. Dynamic retargeting can serve the exact product the user
   viewed. Always pair retargeting with a converter-suppression exclusion so you stop paying to
   reach people who already bought.
3. If the spine is prospecting, choose lookalike, third-party, custom, or contextual.
   - Lookalike Expansion grows reach from a seed of first-party data or a Custom Segment and
     needs at least about 1,000 unique users in the seed, with no pixel implementation required.
     The pixel-based Lookalike Audiences product instead needs the pixel firing first (plan for
     roughly 4,000 pixel fires before a lookalike can build).
   - Third-party data is curated segments aggregated by data providers (demographic, behavioral,
     intent). Map buyer personas to segments and expect a data CPM on top of media for most
     third-party segments.
   - Custom and Browsing segments are StackAdapt-built. Browsing segments are a contextual-plus-
     behavioral hybrid that captures users seen on pages matching a context, closer to contextual
     retargeting than to pure prospecting.
   - Contextual (Page Context AI) targets the page, not the person. It reads page meaning with
     natural language processing and does not rely on cookies, so it is the default cookieless
     prospecting play and a native strength.
4. Refine the spine if it is too broad or off-intent. Add Keyword Rule Targeting to a contextual
   buy to include or exclude exact keywords and control placement and frequency. Stack a custom
   or browsing segment onto a broad spine to bias toward intent. Each refinement narrows reach,
   so add one at a time and watch delivery.
5. Apply the constraint layers every ad group needs. Set geo (country down to postal or ZIP, DMA,
   city, or radius), device and OS (and CTV where the channel is CTV), language, and dayparting.
   These do not find users; they decide who is eligible, so set them to the plan and no tighter.
6. Set domain and inventory include or exclude lists. Use an inclusion list to focus on known-good
   publishers, or an exclusion list to block specific domains. Hand the broader supply, exchange,
   and brand-safety decision to `stackadapt-inventory-and-brand-safety`; keep only the targeted
   allow or block of named domains here.
7. Check deliverability before launch. Each layer shrinks the addressable pool multiplicatively.
   Confirm the stacked combination can still spend the ad group budget across the flight. If it
   cannot, loosen the tightest constraint first (usually geo, daypart, or a narrow segment), not
   the spine. Then hand bid and budget to `stackadapt-bidding-and-budgets`.

## Decision rules and thresholds

- One audience spine per ad group. Mixing retargeting and prospecting in one ad group makes it
  impossible to read or optimize either. Split them into separate ad groups.
- Retargeting always carries a suppression exclusion. Exclude past converters (and often current
  customers) so spend is not wasted re-reaching people who already acted.
- Match the retargeting window to the buy cycle. Short window for impulse or cart abandon, longer
  for considered purchases. A 30-day window is a reasonable default for most ecommerce.
- Use Lookalike Expansion when you have a seed but no pixel history. It needs about 1,000 unique
  seed users and runs off first-party data or a Custom Segment. Use pixel-based Lookalike
  Audiences only once the pixel has accrued enough fires (plan for roughly 4,000).
- Lead native prospecting with contextual. Page Context AI is cookieless and reads page meaning,
  so it is durable and on-strategy for native. Add third-party or custom segments when you need a
  specific persona contextual cannot express.
- Budget a data CPM for third-party segments. Third-party data is curated and priced, so it adds
  cost on top of media. Confirm the segment earns its premium versus contextual or first-party.
- Constraints clip, they do not target. Geo, device, OS, language, daypart, and domain lists
  decide eligibility. Set them to the brief and no tighter, because each one compounds with the
  others to shrink reach.
- Add layers one at a time and name the binding constraint. When delivery stalls, you want to
  know which single layer is the bottleneck. Stacking five at once hides it.
- Loosen the constraint, not the spine, to fix under-delivery. Widen geo, open the daypart, or
  drop a narrow segment before you abandon the audience strategy. If it persists, hand off to
  `stackadapt-optimization-and-troubleshooting`.

## Templates and examples

A layered native prospecting ad group and a separate retargeting ad group, filled in:

```
Ad group: ACME_Native_Prospecting_Contextual_2026Q3
  Spine:        Contextual (Page Context AI) on "home fitness, strength training"
  Refine:       Keyword Rule Targeting, exclude "injury, lawsuit, recall"
  Geo:          United States, exclude AK and HI
  Device/OS:    Desktop + mobile web, all OS
  Language:     English
  Dayparting:   06:00-23:00 local, all days
  Domains:      Inclusion list of 40 vetted fitness and lifestyle publishers
  Why:          Cookieless, page-level prospecting on a native strength; keyword
                exclusions keep it brand-safe; inclusion list focuses on quality supply.

Ad group: ACME_Native_Retargeting_PixelAud_2026Q3
  Spine:        Retargeting, site visitors from the universal pixel, 30-day window
  Segment:      Viewed product or started cart, did not purchase
  Exclude:      Purchasers in last 90 days (suppression)
  Refine:       Dynamic retargeting on the last product viewed
  Geo:          United States
  Device/OS:    All
  Language:     English
  Dayparting:   All hours
  Why:          Lower-funnel re-reach with suppression so spend is not wasted on
                converters; dynamic creative shows the exact product viewed.
```

A first-party prospecting ad group using Lookalike Expansion:

```
Ad group: ACME_Display_Prospecting_Lookalike_2026Q3
  Seed:         First-party CRM list of high-value customers (>= 1,000 matched users)
  Spine:        Lookalike Expansion off that seed (no pixel needed)
  Exclude:      Existing customers (suppression of the seed itself)
  Geo:          United States, top 25 DMAs
  Device/OS:    All
  Why:          Find new users who behave like best customers; suppress current
                customers so the buy is true prospecting, not retargeting.
```

## Common pitfalls

- Running retargeting and prospecting in one ad group, then being unable to tell which worked.
  One spine per ad group.
- Forgetting the converter-suppression exclusion on retargeting, so budget keeps chasing people
  who already bought.
- Reaching for pixel-based Lookalike Audiences before the pixel has fired enough, when Lookalike
  Expansion off a 1,000-user seed would have launched immediately.
- Treating contextual as a fallback. On native it is often the strongest cookieless prospecting
  spine; lead with it.
- Over-stacking constraints (tight geo plus narrow daypart plus a small segment) until the ad
  group cannot spend, then blaming the bid. Loosen the binding constraint first.
- Confusing domain include or exclude lists with the full inventory and brand-safety setup. Named
  domain allow or block lives here; supply, exchanges, and safety lists live in
  `stackadapt-inventory-and-brand-safety`.
- Buying a third-party segment for a persona that contextual or first-party already covers, paying
  a data CPM for no incremental reach.

## Sources

- [StackAdapt Developer Documentation (REST, GraphQL, Pixel API, Data Taxonomy, MCP Server)](https://docs.stackadapt.com) (as of June 2026)
- [3 Essential Audiences for Conversion Campaigns | StackAdapt](https://www.stackadapt.com/resources/blog/audience-targeting) (as of June 2026)
- [How to Build an Effective Retargeting Strategy | StackAdapt](https://www.stackadapt.com/resources/blog/retargeting-strategy) (as of June 2026)
- [Expand Your Targeting With Audience Lookalike Expansion | StackAdapt](https://www.stackadapt.com/resources/blog/audience-lookalike-expansion-targeting) (as of June 2026)
- [What to Know About 3rd-Party Audiences and How to Use Them | StackAdapt](https://www.stackadapt.com/resources/blog/third-party-audiences) (as of June 2026)
- [The Future of Contextual Advertising: Page Context AI | StackAdapt](https://www.stackadapt.com/resources/blog/contextual-advertising) (as of June 2026)
- [How to Use Keyword Rule Targeting | StackAdapt](https://www.stackadapt.com/resources/blog/keyword-rule-targeting) (as of June 2026)

The exact in-product targeting screens, the full geo and device option lists, language and
dayparting controls, and the postal-level radius mechanics are documented in the StackAdapt help
center. Some help center articles require a logged-in account, so they are not cited here; where
a specific in-product control or default is not publicly documented, the guidance above states
the operational best practice rather than a fabricated citation. For account-level help, see the
StackAdapt help center at support.stackadapt.com.
