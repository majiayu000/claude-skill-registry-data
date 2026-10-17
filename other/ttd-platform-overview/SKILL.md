---
name: ttd-platform-overview
description: Orient on what The Trade Desk is, where it sits in the programmatic stack, and how its platform is generationally organized. Use when the user asks "what is The Trade Desk", "Kokai", "TTD platform overview", "is The Trade Desk an independent DSP", "Koa AI", "what does Koa do", "Koa bid factors", "OpenPath vs OpenPass", "what is Ventura", "TTD omnichannel", "does The Trade Desk own media", "self-service vs managed service on TTD", or "how is The Trade Desk different from Google DV360 or Amazon DSP". This is the entry point for the TTD skill set; it routes to the sibling TTD skills for setup, targeting, bidding, inventory, identity, measurement, and automation.
---

# The Trade Desk platform overview

Establish what The Trade Desk (TTD) is, why its independence is the whole pitch, and how the
platform is organized so the rest of the TTD skill set makes sense. The Trade Desk is the
largest independent demand-side platform (DSP) for the open internet. It is buy-side only and
does not own or operate media, which is the basis for its positioning as an objective partner
that prioritizes inventory on the advertiser's behalf rather than its own. This skill is the
orientation layer. It does not walk through in-platform setup; it points you to the sibling
skill that does.

This skill assumes you already know what a DSP, a CPM, an auction, and a funnel stage are. For
those definitions and the shared KPI math, see the `programmatic-foundations` skill. For
choosing the right report once a campaign is live, see the `reporting-by-campaign-goal` skill.

A sourcing note that governs this entire skill set: The Trade Desk's operational knowledge base
and API reference sit behind a partner login, and the in-platform help is only visible to
logged-in seat holders. Everything here is drawn from public pages. Where an exact menu path,
field name, endpoint, or number would require platform access, this skill states the publicly
known concept and flags that the specifics live in the partner platform. It does not invent
screen names or values.

## When to use this skill

- "What is The Trade Desk?" or "what does TTD do?"
- "Is The Trade Desk an independent DSP?" or "does The Trade Desk own media?"
- "What is Kokai?" or "what platform generation is TTD on now?" or "is Solimar still around?"
- "What is Koa?" or "what does Koa AI actually do?" or "what are Koa bid factors?"
- "What is Ventura?" or "does The Trade Desk have its own TV operating system?"
- "What is OpenPath?" or "how is OpenPath different from OpenPass?"
- "What channels does The Trade Desk run?" or "is The Trade Desk good for connected TV?"
- "Self-service or managed service on The Trade Desk?"
- "How is The Trade Desk different from a walled garden like Google DV360 or Amazon DSP?"
- The user is new to the TTD skill set and needs routing to the right sibling skill.

Boundary with sibling skills. This skill orients and routes. It does not configure anything.
The moment the question becomes "how do I build, target, bid, deal, identify, measure, or
automate," hand off using the routing table below. Define and orient here; act there.

## Quick reference

| The user wants | Answer or route to |
| --- | --- |
| What TTD is and why independence matters | "What The Trade Desk is" below |
| The current platform generation (Kokai) and Koa AI | "Platform generation and Koa" below |
| What Koa's bid factors do and whether Koa runs automatically | "Platform generation and Koa" below |
| Which channels TTD covers | "Channels" below |
| What Ventura is (streaming TV OS direction) | "Channels" below |
| OpenPath vs OpenPass (these are different products) | "Independence and objectivity" below |
| Self-service vs managed-service | "Service models" below |
| How TTD differs from a walled garden | "Independence and objectivity" below |
| The account and campaign hierarchy | `ttd-campaign-structure` |
| Targeting, audiences, data | `ttd-targeting-and-audiences` |
| Bidding, Koa optimization, bid factors | `ttd-bidding-and-optimization` |
| Inventory, PMP and programmatic guaranteed deals | `ttd-inventory-and-deals` |
| Identity, UID2, third-party cookie durability | `ttd-identity-and-uid2` |
| Reporting, attribution, measurement | `ttd-measurement-and-reporting` |
| API and bulk automation | `ttd-api-and-automation` |

## What The Trade Desk is

The Trade Desk is a demand-side platform: software that advertisers and their agencies use to
buy programmatic advertising across the open internet through real-time auctions and deals. The
defining facts, all from public company pages:

- **Independent and the largest of its kind.** It is positioned and widely described as the
  largest independent DSP for the open internet, distinct from platforms owned by the large
  media companies.
- **Buy-side only, no owned media.** In its own words, "we don't own media. We just help you
  buy it better," and "because we don't own or operate media, we can help you objectively
  prioritize inventory." This is the structural difference from a walled garden.
- **Omnichannel.** A single platform to plan, execute, and measure media buying across channels
  rather than one channel in isolation.

Read independence as the product, not a slogan. Because TTD has no inventory to favor, its
auction and optimization can prioritize what performs for the advertiser. That is the lever the
rest of the skill set keeps pulling.

## Platform generation and Koa

**Kokai** is the current generation of The Trade Desk platform and the one a trader logs into
today. The Trade Desk launched Kokai on June 6, 2023, describing it as a new approach that
distributes artificial intelligence across the media buying process, with new measurement tools,
streamlined partner integrations, and a reworked user experience. **Solimar, the prior
generation, has been retired.** The Trade Desk ran a Solimar-to-Kokai migration and moved seats
onto Kokai as the live experience, so treat any Solimar reference as legacy. Treat "Kokai" as the
name of the current platform, not a separate product to buy.

**Koa** is The Trade Desk's AI layer. Per the Kokai announcement, Koa launched in 2018 and
"assisted the marketer in setting up campaigns based on business objectives and optimizing based
on performance"; Kokai then "distributes the power of Koa's AI across various aspects of media
buying on The Trade Desk platform." Koa is also publicly described as an AI forecasting engine.
So at the level this skill supports, Koa is the assistive intelligence that helps with setup
recommendations, optimization, and forecasting inside the platform.

**Koa Optimizations and bid factors.** In Kokai, Koa optimizes across multiple targeting
dimensions rather than a single lever. The Trade Desk's public description says a trader can
"let the AI automatically optimize your bid factors on individual targeting dimensions like
geography, site, ad format, device type, and more." A bid factor is a multiplier: publicly, a
value above one signals "I want more impressions like this" and a value below one signals "I
want fewer." Koa works alongside the trader, not instead of them. Per the same public material,
traders "can choose to work alongside Koa by overriding optimizations at any time by applying
bid factors" of their own, and Koa "will automatically optimize within your defined targeting
dimensions while still respecting any manual inputs you apply." Read Koa as automatic
optimization across many dimensions that a trader can turn on and override, not a black box that
locks out manual control.

What requires platform access: the exact Koa recommendations surfaced in a given seat, the full
list of optimizable dimensions in a current release, whether Koa is pre-enabled for a specific
account or campaign type, and how each control is configured are in-platform behaviors that
change over releases. Name the dimensions the public pages confirm (geography, site, ad format,
device type, and more), describe Koa as setup, optimization, and forecasting assistance, and
route configuration questions to `ttd-bidding-and-optimization`. Do not assert a specific total
dimension count or default-on state for a given seat that you cannot see.

## Channels

The Trade Desk lists these channels on its public platform pages. The channel determines the
available formats, inventory, and measurement, the same way it does on any omnichannel DSP.

- **Connected TV (CTV) and OTT.** Publicly highlighted as a core strength and, in reputable
  recent coverage, the company's fastest-growing channel. Treat CTV as the flagship when the
  goal is premium video reach on the open internet.
- **Ventura (streaming TV operating system direction).** Separate from the buying channels above,
  The Trade Desk announced **Ventura**, its own streaming TV operating system, on November 20,
  2024, positioned to give CTV a cleaner supply chain and better addressability by incorporating
  OpenPath and Unified ID 2.0. In early 2026 the company reframed it as the "Ventura Ecosystem,"
  opening it to outside TV OS and ad-tech partners rather than shipping only TTD-owned hardware.
  Ventura is a device-layer and ecosystem play, not a buying channel you select inside a
  campaign, so keep it distinct from the CTV line item. When someone asks whether TTD "has its
  own TV OS," the answer is yes, Ventura, and it is where TTD is pushing CTV addressability.
- **Display.**
- **Video** (online and in-stream video distinct from CTV).
- **Audio.** Streaming music and podcasts.
- **Native.**
- **Digital out-of-home (DOOH).**
- **Mobile** as a device context across the above.
- **Retail data and retail media.** The platform exposes retail data to target high-value
  audiences and connect omnichannel buys to sales and ROI, and retail media is a publicly
  emphasized growth area alongside CTV.

Because all channels run from one platform, the same audiences and identity graph carry across
them, which is what makes a single omnichannel buy and a unified measurement view possible. Lean
on that when planning: build the audience once, then run it on whichever channels fit the goal.
Channel-level setup is in `ttd-campaign-structure` and the targeting and inventory skills.

## Service models

The Trade Desk supports both self-service and managed-service engagement. The platform is built
as a self-serve experience for traders to plan, execute, and measure directly, and many seats
are run as a managed or hybrid service by the agency or a partner. Which model a given
organization uses is a commercial arrangement, not a product setting. For an agent, the
practical implication is the same playbooks apply; only who clicks the buttons changes.

## Independence and objectivity

This is the positioning that separates TTD from the walled gardens (for example Google DV360 and
Amazon DSP, both of which sit next to owned media and inventory). The argument, in three steps:

1. The Trade Desk does not own or operate media, so it has no house inventory to push.
2. With no inventory to favor, it can objectively prioritize whatever performs for the
   advertiser across the open internet.
3. That objectivity is the reason to use an independent DSP when you want buying decisions
   aligned to your outcomes rather than to a platform's media P&L.

Keep the claim disciplined. The defensible public statement is structural: no owned media,
therefore no inventory conflict of interest. Avoid turning that into unverifiable performance
superiority claims against named competitors. For where this matters operationally, identity is
the clearest case: see `ttd-identity-and-uid2` for how TTD pushes an open-internet identity
approach rather than a single login graph.

**OpenPath and OpenPass are two different products; do not conflate them.** They are named
similarly and often mentioned together, but they solve different problems:

- **OpenPath** is a supply-path product: a direct connection between buyers and sellers that
  shortens the chain between the advertiser and the publisher's inventory. The Trade Desk
  describes it as "a simplified, direct connection between buyers and sellers" that reduces
  intermediaries. Think supply chain and inventory access.
- **OpenPass** is a sign-in and authentication product: a single sign-on that lets publishers
  authenticate their users. Think login and addressability, not supply path.

A quick disambiguation: OpenPath moves the buy closer to the inventory; OpenPass authenticates
the person. Both show up in the Ventura ecosystem, which is part of why they get confused.

## Reference material

This overview has no bundled reference files; it routes to sibling skills. Open the sibling skill
named in the Quick reference table for any task beyond orientation. For DSP-agnostic definitions
and KPI formulas, open `programmatic-foundations`. For goal-to-report selection, open
`reporting-by-campaign-goal`.

## Common pitfalls

- **Calling Kokai a separate product.** Kokai is the current platform generation, the experience
  the trader uses, not an add-on to purchase. Describe it as "the current version of the
  platform."
- **Treating Solimar as current.** Solimar is the retired prior generation. If a user is working
  in Solimar, they are on a legacy path; Kokai is the live platform. Do not describe Solimar as
  an option a new campaign would choose today.
- **Overstating what Koa does from memory.** Koa is setup, optimization, and forecasting
  assistance at the level public sources support, and it optimizes bid factors across multiple
  targeting dimensions (geography, site, ad format, device type, and more) that a trader can
  override. The full dimension list, whether it is pre-enabled for a given seat, and specific
  controls are in-platform and release-dependent. Route specifics to
  `ttd-bidding-and-optimization` instead of inventing toggle names or a fixed dimension count.
- **Confusing OpenPath with OpenPass.** OpenPath is a supply-path product (direct buyer-to-seller
  connection); OpenPass is a sign-in and authentication product (single sign-on for publishers).
  They are different tools that happen to be named alike. Do not use one name to explain the
  other.
- **Repeating a "cookieless countdown."** Do not frame TTD's identity story as a race against
  Chrome deprecating third-party cookies. Google confirmed in April 2025 that it will not
  deprecate third-party cookies in Chrome and will not ship the planned user-choice prompt, so
  third-party cookies remain in Chrome. TTD's UID2 and open-internet identity case stands on its
  own merits (durable, addressable identity beyond cookies), not on an imminent cookie shutoff.
  Route identity specifics to `ttd-identity-and-uid2`.
- **Turning independence into an unprovable performance claim.** The verified point is
  structural: no owned media, so no inventory conflict. Do not extend that into blanket "beats
  competitor X on ROI" statements.
- **Forgetting CTV is the flagship.** When the goal is premium video reach on the open internet,
  CTV is TTD's publicly emphasized strength and fastest-growing channel. Start there for
  upper-funnel video.
- **Answering in-platform setup from this skill.** This skill orients. For any build, target,
  bid, deal, identity, measurement, or automation task, hand off to the named sibling skill.

## Sources

- Our Demand Side Platform (DSP), The Trade Desk (independent DSP, self-serve, omnichannel, "we
  don't own media. We just help you buy it better," "because we don't own or operate media, we
  can help you objectively prioritize inventory," Frost Radar leader):
  https://www.thetradedesk.com/us/our-platform/dsp-demand-side-platform (as of June 2026)
- Our platform, The Trade Desk (channel list: Audio, CTV / OTT, Digital out-of-home, Display,
  Mobile, Native, Video; retail data; self-serve): https://www.thetradedesk.com/us/our-platform
  (as of June 2026)
- About us, The Trade Desk (independent media buying platform for the open internet, objective
  partner): https://www.thetradedesk.com/us/about-us (as of June 2026)
- The Trade Desk Launches Kokai, The Trade Desk press room (Kokai launched June 6, 2023;
  distributed AI; Koa launched 2018 and assisted setup and optimization; CTV and retail
  measurement):
  https://www.thetradedesk.com/press-room/the-trade-desk-launches-kokai-a-new-media-buying-platform-that-brings-the-full-power-of-ai-to-digital-marketing
  (as of June 2026)
- How to boost campaign performance with AI in Kokai, The Trade Desk (Koa can "automatically
  optimize your bid factors on individual targeting dimensions like geography, site, ad format,
  device type, and more"):
  https://www.thetradedesk.com/resources/how-to-boost-campaign-performance-with-ai-in-kokai
  (as of July 2026)
- Real-time optimization with Koa, The Trade Desk (Koa Optimizations; traders "can choose to work
  alongside Koa by overriding optimizations at any time by applying bid factors"; Koa optimizes
  within defined targeting dimensions while respecting manual inputs):
  https://www.thetradedesk.com/resources/kokai-update-koa-optimizations (as of July 2026)
- The Trade Desk Announces Ventura, The Trade Desk press room (Ventura announced November 20,
  2024; "an innovative new streaming TV operating system (OS)"; incorporates OpenPath and Unified
  ID 2.0): https://www.thetradedesk.com/press-room/the-trade-desk-announces-ventura (as of July
  2026)
- The Trade Desk Introduces the Ventura Ecosystem, The Trade Desk press room (early-2026 pivot to
  an open "Ventura Ecosystem"; V and Nexxen as first collaborators; access to OpenPath, UID2/EUID,
  OpenAds, and OpenPass):
  https://www.thetradedesk.com/press-room/the-trade-desk-introduces-the-ventura-ecosystem-to-advance-the-future-of-ctv-advertising-v-and-nexxen-join-as-the-first-collaborators
  (as of July 2026)
- OpenPath, The Trade Desk (OpenPath is "a simplified, direct connection between buyers and
  sellers" that reduces intermediaries in the supply chain):
  https://www.thetradedesk.com/our-demand-side-platform/openpath (as of July 2026)
- What is OpenPath and how can publishers benefit, The Trade Desk (OpenPath as supply-path
  product; distinct from OpenPass sign-in):
  https://www.thetradedesk.com/resources/what-is-openpath (as of July 2026)
- Google isn't launching a user-choice prompt for third-party cookies in Chrome, AdExchanger
  (April 2025: Google will not deprecate third-party cookies in Chrome and will not ship the
  planned choice prompt):
  https://www.adexchanger.com/data-privacy/google-isnt-launching-a-user-choice-prompt-for-third-party-cookies-in-chrome/
  (as of July 2026)
- The Trade Desk, Wikipedia (largest independent demand-side platform in the world; Koa described
  as an AI forecasting engine; Kokai; Unified ID 2.0):
  https://en.wikipedia.org/wiki/The_Trade_Desk (as of June 2026)
- What is Driving Trade Desk's Rapid CTV and Retail Media Growth, Yahoo Finance / Zacks (CTV the
  company's fastest-growing channel in Q3 2025; retail media momentum):
  https://finance.yahoo.com/news/driving-trade-desks-rapid-ctv-163500468.html (as of June 2026)

Operational specifics that require The Trade Desk platform or partner access (not cited above
because the relevant pages sit behind a partner login): the live Koa recommendations and
optimization controls in a seat, the exact in-platform menus and field names, the API reference,
and any rate-card or performance figures specific to an account. For those, use the partner
platform and its in-platform help.
