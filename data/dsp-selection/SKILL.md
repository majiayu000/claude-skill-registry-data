---
name: dsp-selection
description: Pick the right buying platform for a goal among Google Ads, DV360, Amazon DSP, The Trade Desk, and StackAdapt. Use when the user asks "which DSP", "which platform should I use", "DV360 vs The Trade Desk", "best DSP for CTV", "platform selection", "where should I run this", "walled garden vs independent", "which platform for retail / commerce", "which platform for search intent", or is scoping a brief and has not committed to a platform yet. Routes to each platform's overview skill once the choice is made.
---

# DSP and platform selection

Map an objective and its constraints to the platform that serves it best, across five
choices: Google Ads, Display & Video 360 (DV360), Amazon DSP, The Trade Desk (TTD), and
StackAdapt. This skill decides where the spend should run and why. It does not configure
anything. Once the platform is chosen, hand off to that platform's overview or setup skill.

This skill assumes the shared vocabulary. For what a DSP, walled garden, PMP, clean room,
identity graph, or any KPI means, see the `programmatic-foundations` skill. For a deeper
orientation on a specific platform once you have narrowed to it, see the matching overview
skill named in the routing table. Definitions live there; the decision lives here.

A discipline that governs this whole skill: separate what a platform is documented to do
from what it is marketed to be best at. The "what it is" claims below are tied to verified
official pages in Sources. The competitive "who wins" judgments are positioning, including
each vendor's own framing of its strengths, and are labeled as such. Tell the user which is
which so they can pressure-test the recommendation against their own data.

## When to use this skill

- "Which DSP or platform should I use for this?" or "where should I run this campaign?"
- "DV360 vs The Trade Desk," "Amazon DSP vs The Trade Desk," "Google Ads vs DV360," or any
  head-to-head between the five.
- "Best platform for CTV / streaming," "best platform for retail or commerce," "best
  platform for search intent," "best platform for open-web display at scale."
- "Walled garden vs independent DSP," or a question about owned-media conflict of interest.
- The user is scoping a brief (channel, objective, budget, identity needs) and has not yet
  committed to a platform.
- The user is deciding whether to run on one platform or several.

Boundary with sibling skills. This skill selects and routes. It does not build, target, bid,
or troubleshoot. The moment the platform is chosen and the question becomes "how do I set
this up here," hand off to that platform's skill set. Select here, act there.

## Quick reference: goal to platform

Read the dominant objective first, then the hard constraints. The primary recommendation is
documented capability; the rationale clause flags where it leans on positioning.

| Dominant goal or signal | Primary platform | Why (D = documented, P = positioning) |
| --- | --- | --- |
| Capture active search and shopping intent; run Performance Max | Google Ads | D: Search ads reach people actively searching; PMax accesses all Google inventory from one goal-based campaign |
| Google-owned video (YouTube) plus open-web display, video, audio, CTV at scale, full trading control | DV360 | D: executes display, video, audio, CTV, and YouTube buying across five modules with granular controls |
| CTV and streaming tied to retail and commerce signals; clean-room analytics on shopping data | Amazon DSP | D: omnichannel including streaming TV, built on Amazon shopping and streaming signals; AMC is the clean room |
| Independent omnichannel and CTV on the open internet, strongest cross-channel identity story | The Trade Desk | D: independent DSP, no owned media, open-internet omnichannel. P: "objective" inventory prioritization and identity leadership |
| Multi-channel buying (native, display, video, CTV, audio, DOOH) with self-serve plus hands-on managed support | StackAdapt | D: integrated multi-channel platform, native heritage, self-serve and managed client services. P: best fit for lean or mid-market teams |
| Need more than one of the above at once | Run two, plan reach across them | See "Run more than one" below and `reach-and-frequency-planning` |

If two rows fit, the tie-breakers in "Decision rules and thresholds" resolve it. If the user
has not told you the objective, ask for it before recommending; the goal, not the channel
name, drives the choice.

## The five platforms in one paragraph each

Lead with the documented identity, then the honest positioning note.

**Google Ads.** Google's self-serve platform for buying across Google's own surfaces. It is
the default when the objective is to capture demand that already exists: Search ads reach
people while they are actively searching, Shopping ads show product image, price, and store
for commerce intent, and Performance Max is a goal-based campaign that reaches across all
Google channels (YouTube, Display, Search, Discover, Gmail, Maps) from one campaign. Strong
for direct-response and lower-funnel efficiency on Google inventory. It is a walled garden:
you are buying Google's surfaces, and PMax in particular trades granular control for
automation. For granular open-web buying and full trading control, that is DV360, not Google
Ads. See the `google-ads-campaign-types` skill to act.

**Display & Video 360 (DV360).** Google's enterprise demand-side platform for programmatic
buying across the open web and Google inventory. It executes display, video, audio, CTV, and
YouTube campaigns and is organized around five modules (Campaigns, Audiences, Creatives,
Inventory, Insights) with the granular targeting, deals, bidding, and frequency controls a
trading team expects. It is the right call when you want YouTube alongside open-web display
and video at scale with hands-on control. It is part of the Google ecosystem, so weigh how
much of the value depends on Google's owned data and inventory. See the
`programmatic-foundations` routing table for the full DV360 skill set, starting with
`dv360-campaign-architecture`.

**Amazon DSP.** Amazon's omnichannel programmatic platform. Its documented identity is buying
display, video, audio, and streaming TV against Amazon's first-party shopping and streaming
signals, reaching audiences without relying on traditional ad identifiers. It is the natural
choice when commerce and retail signals or Amazon's streaming inventory (including Prime
Video) are central to the buy, and when you want clean-room analysis of how media connects to
shopping behavior through Amazon Marketing Cloud (AMC). It sits next to Amazon's owned media,
which is the walled-garden tradeoff. See the `amazon-dsp-campaign-setup` skill to act and
`amazon-marketing-cloud` for the clean room.

**The Trade Desk (TTD).** The leading independent DSP built for the open internet. Its
documented and defining fact is structural: it does not own or operate media, so it has no
house inventory to favor. It is buy-side only and omnichannel across CTV, display, video,
audio, native, and DOOH. Reach for it when you want independence from any single media
owner's interests, open-internet omnichannel breadth, and a cross-channel identity approach
not tied to one login graph. Treat the "objectively prioritize inventory" and identity
leadership claims as TTD's own positioning, defensible as structural (no owned media, so no
inventory conflict) but not as proven performance superiority. See the
`ttd-platform-overview` skill, which routes to the rest of the TTD set.

**StackAdapt.** An integrated multi-channel marketing platform with a native-advertising
heritage, now spanning native, display, video, CTV, audio, DOOH, and more. It offers both a
self-serve experience and hands-on managed client services (campaign setup, creative build,
analytics review), which makes it flexible for teams that want to run it themselves, lean on
a service layer, or mix both. Reach for it when the plan is multi-channel with native at the
core and the team values managed-or-self-serve flexibility over the deepest enterprise
trading controls. Note: StackAdapt's own pages position it as "enterprise-level solutions for
every agency and brand," not as a mid-market tool; "mid-market" is an industry
characterization, not a vendor claim, so present it as positioning. See the
`stackadapt-campaign-setup` skill to act.

## The tradeoffs that decide it

When two platforms could serve the goal, these axes break the tie. The first is usually
decisive.

- **Walled garden vs independent.** Google Ads, DV360, and Amazon DSP each sit next to owned
  media and inventory (Google surfaces and YouTube; Amazon retail and streaming). The Trade
  Desk owns no media. StackAdapt owns no media but is a managed-or-self-serve buying platform
  rather than positioned on independence the way TTD is. If avoiding any single media owner's
  conflict of interest is a stated requirement, that points to an independent DSP.
- **Owned-media conflict of interest.** A platform that profits from its own inventory has a
  structural incentive to direct spend there. This is the explicit basis of TTD's
  independence positioning. It does not make the walled gardens wrong, their owned inventory
  (YouTube, Amazon streaming, Search) is often exactly what you want, but name the incentive
  when you recommend one.
- **Identity and addressability.** In a signal-loss world, ask what each platform resolves
  identity on. Amazon DSP leans on logged-in shopping and streaming signals and can target
  without traditional identifiers. TTD pushes an open-internet identity approach not bound to
  one login (see `ttd-identity-and-uid2`). Google platforms lean on Google's own signals.
  Match the identity story to where your audience actually is.
- **Measurement and clean-room access.** If the objective requires privacy-safe joins of
  first-party data to media exposure, the clean room matters. Amazon Marketing Cloud is a
  documented, privacy-safe clean room over Amazon signals. Google's equivalent for DV360 is
  Ads Data Hub (see `dv360-advanced-analytics-adh`). Independent platforms integrate
  third-party measurement partners. Pick for the measurement you must produce, not just the
  media you must buy.
- **Supply path.** Walled gardens are largely their own supply. Independent DSPs buy across
  many exchanges and SSPs, which is broader open-web reach but puts supply-path quality and
  transparency on you. More reach is not automatically better reach.
- **Minimum spends and access gating.** Enterprise DSPs (DV360, Amazon DSP, TTD) are commonly
  accessed through a partner, agency, or managed seat and can carry onboarding and minimum
  commitments, whereas Google Ads is openly self-serve and StackAdapt offers a lower-friction
  self-serve plus managed path. Exact minimums are commercial and not publicly fixed, so
  confirm them with the vendor rather than asserting a number. If low barrier to entry or
  pure self-serve is a constraint, weight it.
- **Genuinely strong vs marketed.** Where a platform is documented to operate a channel,
  treat that as fact. Where a vendor claims to be best at it, treat that as positioning and
  validate against your own results. CTV is the clearest example: Amazon DSP and TTD both run
  it and both market themselves as leaders. The documented part is that each offers CTV; the
  "leader" part is positioning. Recommend on the documented fit plus the user's constraints,
  and tell them the superiority claims are theirs to test.

## Core process

1. Get the dominant objective and funnel stage first. Search intent, commerce, open-web
   reach, premium video, or omnichannel breadth each point to a different default. If the
   user gave a channel ("we want CTV") but not a goal, ask what the CTV buy is for; the goal
   changes the answer.
2. Capture the hard constraints: owned-media conflict tolerance, identity needs, required
   measurement and clean-room joins, supply transparency, budget, and whether self-serve or
   managed access is required. Any one of these can override the goal-based default.
3. Read the Quick reference row for the goal, then apply the tradeoff axes to the
   constraints. The first axis that the user has a firm requirement on usually decides it.
4. Separate documented fit from positioning in your recommendation. State the documented
   reason the platform fits, then flag any competitive claim as positioning to validate.
5. Name one primary platform and, when relevant, a secondary. If the brief genuinely spans
   goals that no single platform serves well, recommend running more than one and route to
   "Run more than one" below.
6. Hand off. Route to the chosen platform's overview or setup skill so the user can act. Do
   not start configuring inside this skill.

## Decision rules and thresholds

These are rules of thumb for the common forks, not hard limits. State your assumption when
you apply one.

- **Search or shopping intent is the goal: Google Ads, not a DSP.** Demand capture on Google
  surfaces is what Search, Shopping, and PMax are for. A DSP is for demand generation across
  display and video, not for bidding on query intent.
- **YouTube is required and you also want open-web display and video with full control:
  DV360.** You can reach YouTube from Google Ads too, but DV360 is the choice when YouTube
  sits inside a broader, hands-on open-web video and display plan.
- **Retail or commerce outcome, or Amazon streaming inventory, is central: Amazon DSP.** When
  the buy lives or dies on shopping signals or Prime Video and you need AMC to measure media
  against purchase behavior, this is the default.
- **Independence is a stated requirement, or the buy is open-internet omnichannel with a
  cross-channel identity need: The Trade Desk.** When "no single media owner's conflict" or
  "open-internet identity not tied to one login" is on the brief, TTD is the structural fit.
- **The team wants multi-channel with native at the core and managed-or-self-serve
  flexibility over the deepest trading controls: StackAdapt.** Especially when a lean team
  values a service layer alongside self-serve.
- **CTV with no other constraint: do not pick on the "leader" claim.** Amazon DSP and TTD
  both run CTV and both market leadership. Decide on the surrounding constraints, retail
  signals and AMC point to Amazon, independence and open-internet identity point to TTD, and
  tell the user the leadership claims are positioning.
- **Low barrier to entry or pure self-serve is required: Google Ads or StackAdapt over the
  enterprise seats.** DV360, Amazon DSP, and TTD are commonly accessed through a partner or
  managed seat. Confirm minimums with the vendor rather than quoting a figure.
- **When uncertain between an independent DSP and a walled garden, name the owned-media
  incentive explicitly.** Let the user weigh it against how much they want the owned
  inventory. Do not bury the tradeoff.

## Run more than one

One platform rarely covers every goal. A common, defensible split: Google Ads for search and
shopping demand capture, plus one programmatic DSP (DV360, Amazon DSP, TTD, or StackAdapt)
for upper-funnel display and video. Or Amazon DSP for retail-signal CTV and commerce
measurement alongside TTD or DV360 for the rest of the open-internet buy. Running more than
one is normal, not a failure to choose.

When you do, the cross-platform problem becomes reach and frequency: the same user can be hit
on each platform, so unmanaged overlap inflates frequency and wastes spend. Plan and cap
total exposure across platforms rather than per platform. Hand off to the
`reach-and-frequency-planning` skill for how to plan combined reach, dedupe overlap, and set
a cross-platform frequency budget. For why frequency and reach are computed the way they are,
see `programmatic-foundations`.

## Reference material

This skill has no bundled reference files. For definitions and KPI math, open
`programmatic-foundations`. For a deeper single-platform orientation once you have narrowed
the choice, open the matching overview skill: `ttd-platform-overview` for The Trade Desk, and
the platform entries in the `programmatic-foundations` routing table for DV360. For the
cross-platform reach math when running more than one, open `reach-and-frequency-planning`.

## Common pitfalls

- **Picking on the channel name instead of the goal.** "We want CTV" is not a platform
  decision until you know what the CTV buy is for. The objective, retail outcome vs
  independent open-internet reach, picks the platform.
- **Repeating a vendor's "best at X" as fact.** Documented capability and marketed
  superiority are different. State the documented fit and label competitive claims as
  positioning the user should validate against their own results.
- **Ignoring owned-media conflict of interest, or overstating it.** Name the incentive when
  recommending a walled garden, but remember its owned inventory (YouTube, Amazon streaming,
  Search intent) is frequently the reason to choose it. Independence is a requirement to
  weigh, not an automatic win.
- **Calling StackAdapt a mid-market tool as if the vendor says so.** Its own pages say
  "enterprise-level solutions for every agency and brand." Present the mid-market fit as an
  industry characterization, not a documented claim.
- **Quoting minimum spends as fixed numbers.** Access gating and minimums for the enterprise
  seats are commercial and not publicly pinned. Say they exist and tell the user to confirm
  with the vendor; do not invent a figure.
- **Forcing one platform onto a multi-goal brief.** If the brief spans demand capture and
  open-web reach, recommend running more than one and plan combined frequency through
  `reach-and-frequency-planning` rather than compromising the whole plan onto a single
  platform.
- **Acting inside this skill.** This skill selects and routes. For any build, target, bid, or
  measurement task, hand off to the chosen platform's skill set.

## Sources

- Google Ads Help, About Search campaigns (text ads reaching people while they are searching;
  active-intent targeting): https://support.google.com/google-ads/answer/2567043 (as of June
  2026)
- Google Ads Help, About Shopping ads (display product photo, title, price, store name from
  Merchant Center): https://support.google.com/google-ads/answer/2454022 (as of June 2026)
- Google Ads Help, About Performance Max campaigns (goal-based campaign accessing all Google
  Ads inventory across YouTube, Display, Search, Discover, Gmail, and Maps from one campaign):
  https://support.google.com/google-ads/answer/10724817 (as of June 2026)
- Google Ads Help, campaign types overview (the list of available Google Ads campaign types):
  https://support.google.com/google-ads/answer/6146252 (as of June 2026)
- Display & Video 360 Help, DV360 overview (executes digital advertising campaigns; organized
  around five integrated modules: Campaigns, Audiences, Creatives, Inventory, Insights):
  https://support.google.com/displayvideo/answer/9059464 (as of June 2026)
- Amazon Ads, Amazon DSP (omnichannel marketing solution; display, online video, audio,
  streaming TV, and physical store advertising; built on Amazon shopping and streaming
  signals; reach audiences without traditional ad identifiers):
  https://advertising.amazon.com/solutions/products/amazon-dsp (as of June 2026)
- Amazon Ads, Amazon Marketing Cloud (secure, privacy-safe, cloud-based clean room for
  analytics and audience building across pseudonymized signals):
  https://advertising.amazon.com/solutions/products/amazon-marketing-cloud (as of June 2026)
- The Trade Desk, Our Demand Side Platform (leading independent DSP for the open internet;
  "we don't own media. We just help you buy it better"; "because we don't own or operate
  media, we can help you objectively prioritize inventory"; open and interoperable;
  omnichannel): https://www.thetradedesk.com/us/our-platform/dsp-demand-side-platform (as of
  June 2026)
- StackAdapt, platform overview (integrated multi-channel marketing platform; native,
  display, video, CTV, audio, DOOH and more; activate first-party data; serves agencies and
  brands; self-serve plus client services): https://www.stackadapt.com/platform (as of June
  2026)

Positioning vs documented, stated plainly: that The Trade Desk "objectively" prioritizes
inventory and leads on identity, that Amazon DSP or The Trade Desk is the CTV "leader," and
that StackAdapt is a "mid-market" platform are positioning or industry characterizations, not
claims the official pages above prove. The documented facts are the channels each platform
runs, Google Ads' intent-capture and Performance Max behavior, DV360's five-module scope,
Amazon DSP's commerce-signal base and AMC clean room, and The Trade Desk's structural lack of
owned media. Recommend on the documented fit and the user's constraints; flag the rest as
positioning to validate.
