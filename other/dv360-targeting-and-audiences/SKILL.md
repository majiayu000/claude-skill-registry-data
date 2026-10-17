---
name: dv360-targeting-and-audiences
description: Decide who to target in Display & Video 360 and assemble the targeting on a line item. Use when the user asks "who should I target", about audience setup, first-party vs Google audiences, PAIR or first-party data onboarding, affinity vs in-market, custom segments, how to combine or exclude audiences, contextual or content targeting, geography or device or environment targeting, viewability or Active View targeting, optimized or expanded targeting, or why layered targeting is choking delivery.
---

# DV360 targeting and audiences

Pick the right audiences and contextual signals, then layer them so the line item reaches the
right people at enough scale to spend. This skill is the targeting brain. For where the
inventory itself comes from (open auction, deals, packages) hand off to `dv360-deals-and-inventory`.
For KPI and reach math definitions, see `programmatic-foundations`.

## When to use this skill

Use this when the task is about WHO and IN WHAT CONTEXT a line item should serve, including:

- Choosing between your first-party data, Google audiences, and custom segments.
- Affinity vs in-market vs demographics vs life events.
- Building combined audiences and deciding include vs exclude, AND vs OR.
- Adding contextual layers: geography, language, device, environment, day and time, content
  categories or keywords, and content exclusions.
- Targeting predicted viewability with Active View.
- Deciding whether to turn on optimized targeting and what it costs you.
- Debugging "my line item barely spends" when the cause is over-layered targeting.

Boundaries with sibling skills:
- Inventory sourcing, deal IDs, and inventory-source targeting live in `dv360-deals-and-inventory`.
- Frequency caps, brand-safety verification vendors, and content-label exclusions as a brand-safety
  program live in `dv360-frequency-and-brand-safety`. This skill covers the targeting controls;
  that skill covers the safety policy and caps.
- Bid pricing against the audience you select lives in `dv360-bid-strategy`.
- If targeting looks correct but the line item still will not deliver, hand off to
  `dv360-troubleshooting`.

## Quick reference

Audience taxonomy and when to reach for each:

| Audience type | What it is | Reach for it when |
| --- | --- | --- |
| Your first-party data | Floodlight or activity-based remarketing lists, customer match lists, and PAIR audiences reconciled with a publisher | You have a site, app, CRM, or pixel signal and want to re-engage or seed, and you want a path that survives without third-party cookies |
| Google audiences: affinity | Broad, durable interest groups | Upper funnel awareness and consideration at scale |
| Google audiences: in-market | Active purchase intent for a category | Lower funnel, capture people about to buy |
| Google audiences: demographics | Age, gender, parental status, household income | Coarse qualification, usually layered not standalone |
| Google audiences: life events | Moving, graduating, marrying, and similar | Time-bound relevance windows |
| Custom segments | You define by search terms or phrases, URLs, and apps | No off-the-shelf list fits the niche you want |
| Combined audiences | Boolean assembly of the above into one persona | You need AND across categories or curated OR groups |
| Optimized targeting | Model finds new converters beyond your manual lists | You want scale and will accept it reallocating spend |

Combination logic in one line: within a category, lists are OR (any match); across categories,
groups are AND (must match all); exclusions remove users regardless of includes; each contextual
layer you add (geo, content, device) is an additional AND that shrinks reach fast.

Targeting dimensions checklist for a line item: audience, geography, language, device and OS and
browser, environment (web vs app, instream vs outstream, CTV), day and time, content (categories,
keywords, and exclusions), inventory source (see `dv360-deals-and-inventory`), and Active View
predicted viewability.

## Core process

1. **Start from the goal, not the lists.** Map the funnel stage to the audience class first.
   Awareness leans on affinity plus broad context. Consideration leans on in-market and custom
   intent. Performance leans on first-party remarketing plus optimized targeting. This keeps you
   from stacking lists that fight each other.
2. **Lay the base audience.** Choose the primary include layer (for example, an in-market list or a
   first-party remarketing list). Within that category you may add several lists; they combine as
   OR, so adding more widens reach. When the durable, privacy-safe activation path matters, put
   first-party data at the base: onboard CRM and site or app signal through Floodlight, customer
   match (directly or via a customer match uploader partner), or PAIR audiences reconciled with a
   publisher inside a data clean room. PAIR is the way to activate first-party data against a
   specific publisher's audience without relying on third-party cookies or a shared user identifier;
   the clean room returns only an aggregate match rate, and no user-level match is exposed to either
   side or to the exchange. Onboard those lists first, then extend outward.
3. **Narrow deliberately with AND, one category at a time.** Add a second category (a demographic
   floor, a custom segment) only when it earns its keep. Each new category is an intersection that
   can cut reach by an order of magnitude, so add, check the reach estimate, then decide.
4. **Add exclusions before more includes.** Exclude converters, existing customers, employees, and
   audiences that overlap or waste spend. Exclusion is the cheapest precision you have and prevents
   serving to people you do not want.
5. **Layer the contextual dimensions.** Set geography, language, device and environment, day and
   time, and content controls. Treat each as an AND against the audience. Watch the cumulative
   effect: audience plus tight geo plus narrow content can starve a line item.
6. **Add Active View viewability prediction.** Set a predicted viewability floor (for example, bid
   only on impressions at least 50 percent likely to be viewable) so you pay for impressions a human
   can actually see. Know this trims inventory, and that CTV is excluded from video viewability
   targeting by default.
7. **Decide on optimized targeting last.** If you need scale, enable it knowing it treats your
   first-party lists as a soft signal and may move budget away from them when it finds equal-ROI
   traffic elsewhere. Keep geo and brand-safety controls on; those stay hard constraints.
8. **Sanity-check scale.** Pull the reach or forecast estimate after layering. If it collapses, peel
   back the most recent AND layer rather than loosening the core audience.

## Decision rules and thresholds

- **First-party first, Google audiences for scale.** Spend your owned signal on the people most
  likely to convert, then extend with Google audiences and optimized targeting. The durable,
  privacy-safe path leans on first-party data and publisher-provided signals: Floodlight, customer
  match, PAIR audiences, and deal-level publisher signals rather than third-party lists. PAIR is the
  primary way to reconcile your first-party data with a publisher's without a third-party cookie or a
  shared user id, so a strategy built on onboarded first-party data plus PAIR survives when
  cookie-based and browser-signal targeting is not available. Onboard the owned data, then reach for
  Google audiences only to scale beyond it.
- **Affinity vs in-market is funnel position.** Affinity equals durable interest for the top of the
  funnel. In-market equals active intent for the bottom. If the KPI is a conversion or a strong
  action, prefer in-market and custom intent. If the KPI is reach or awareness, prefer affinity.
- **AND across categories, OR within a category.** Use OR (multiple lists in one group) to widen.
  Use AND (a new group) to qualify. Never express an intent as five intersected groups when one
  curated combined audience would do; deep intersection shrinks reach and starves learning.
- **Cap intersection depth.** Combined audiences allow many includes but a limited number of
  intersects. Treat 2 to 3 AND groups as the practical ceiling for most line items; beyond that,
  reach and bid-strategy learning both suffer.
- **Recency is a lever, not a default.** For remarketing lists, tighter recency raises intent and
  cuts reach. You can include and exclude the same list at different recency windows to isolate a
  band (for example, include 0 to 30 days, exclude 0 to 7 days to skip very recent visitors).
- **Target predicted viewability when the KPI is viewable.** If you are measured on viewable CPM or
  viewable impressions, set the Active View floor rather than hoping placement quality covers it.
  Expect a smaller, pricier pool.
- **Mind audience size.** Very small audiences (tight first-party lists, deep intersections) cannot
  spend a meaningful budget and starve automated bidding of data. If the audience cannot support the
  budget and flight, widen the audience or move budget to a line item that can.

## Reference material

- See `programmatic-foundations` for definitions of CPM, reach, frequency, viewability, and funnel
  stages. This skill does not redefine them.
- For the structured way to express any targeting on a line item programmatically, the DV360 API
  models every dimension as an assigned targeting option on the line item; see the Sources for the
  API resource and the assign-targeting guide. Read those when automating targeting via the API or
  Structured Data Files; `dv360-api-and-sdf-automation` covers the automation workflow.

## Templates and examples

Performance line item, retail SUV launch:

- Base audience (OR within category): in-market for "SUVs" plus in-market for "Auto financing".
- Narrow (AND, one group): custom segment built from competitor model search terms and review URLs.
- Exclude: Floodlight converters 0 to 90 days, existing-owner customer match list.
- Geography: target sale-region DMAs only. Language: English plus Spanish.
- Environment: web and app display, exclude very small in-app sizes that hurt the creative.
- Viewability: bid only on impressions at least 50 percent likely to be viewable.
- Optimized targeting: on, because the seed lists are tight and the KPI is a configured conversion.
- Reach check: confirm the forecast supports the daily budget before launch; if it does not, drop
  the custom-segment AND first.

Awareness line item, new beverage brand:

- Base audience: affinity "Food and Dining" plus "Health and Wellness" enthusiasts (OR).
- Demographic floor (AND): age 21 and over for an alcohol product.
- Exclude: recent purchasers if a first-party list exists.
- Content: target relevant content categories, exclude sensitive categories per the brand-safety
  policy in `dv360-frequency-and-brand-safety`.
- Viewability: set a viewability floor since the KPI is viewable reach.
- Optimized targeting: off or cautious; awareness wants predictable reach, not conversion-chasing.

## Common pitfalls

- **Stacking too many AND layers.** The single most common cause of a healthy budget barely
  spending. Audience intersected with tight geo intersected with narrow content can cut reach by
  one hundred times. Add layers one at a time and watch the estimate.
- **Forgetting exclusions.** Without converter and customer exclusions you pay to re-serve people
  who already acted, and you let overlapping includes double-count. Exclusions are mandatory hygiene.
- **Treating optimized targeting as free scale.** It can quietly pull spend off your best
  first-party audience when it finds equal-ROI traffic elsewhere. That is fine for performance, bad
  if you needed those exact users reached. Decide intentionally.
- **Ignoring recency.** Targeting a remarketing list with no recency window mixes red-hot and cold
  users and dilutes intent. Set the window.
- **Setting an unreachable viewability floor.** A very high predicted-viewability floor on scarce
  inventory can leave nothing to bid on. Tune it against delivery, and remember CTV video is
  excluded from viewability targeting by default.
- **Building tiny audiences for big budgets.** A deep intersection of first-party lists may be too
  small to spend the plan or to teach the bid strategy. Match audience size to budget and flight.

## Sources

Official Display & Video 360 Help and Display & Video 360 API documentation. PAIR, first-party
onboarding, audiences, optimized targeting, and viewability lines verified as of July 2026; the
remaining lines verified as of June 2026.

- Audiences overview: https://support.google.com/displayvideo/answer/9099427
- PAIR audiences (reconcile first-party data with a publisher via a clean room, target on the line item): https://support.google.com/displayvideo/answer/15478755
- Onboarding first-party data from external DMPs, PAIR data clean rooms, and customer match uploader partners: https://support.google.com/displayvideo/answer/9649053
- Audience list targeting (include, exclude, recency, combining): https://support.google.com/displayvideo/answer/2949947
- Combined audiences (OR to expand, AND to narrow, exclude): https://support.google.com/displayvideo/answer/9001225
- Affinity audiences targeting: https://support.google.com/displayvideo/answer/6021489
- In-market audience targeting: https://support.google.com/displayvideo/answer/6213232
- Custom list targeting (custom affinity and custom intent from search terms, URLs, apps): https://support.google.com/displayvideo/answer/7583366
- Optimized targeting (and its effect on first-party reach): https://support.google.com/displayvideo/answer/12060859
- About targeting in Display & Video 360 (dimension taxonomy): https://support.google.com/displayvideo/answer/2949929
- Viewability targeting (predicted viewability, CTV exclusion): https://support.google.com/displayvideo/answer/6101342
- DV360 API v4, assignedTargetingOptions on line items: https://developers.google.com/display-video/api/reference/rest/v4/advertisers.lineItems.targetingTypes.assignedTargetingOptions
- DV360 API, assign targeting guide: https://developers.google.com/display-video/api/guides/managing-line-items/targeting
