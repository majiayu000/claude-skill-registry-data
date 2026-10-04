---
name: bmc-channel-economics-check
description: "Puts a real cost-to-acquire against every Channel on the canvas and checks it against the company's actual budget, payback period, and cash runway — so channels get chosen on economics, not just descriptive fit or trend appeal."
---

# BMC Channel Economics Check

## Purpose

Channels are usually listed on a BMC the way they'd be listed in a
marketing plan — "outbound sales, content marketing, referrals" — with
no cost attached to any of them. This skill forces a number onto every
channel before it's accepted onto the canvas: what does it actually cost
to acquire a customer through this channel, and can the business afford
that cost at the volume it needs? Use once Channels has a first draft
and `bmc-economic-prototyping` has established a price and margin to
check the cost against.

## Anchored in research

Standard SaaS/growth-marketing unit-economics discipline — customer
acquisition cost (CAC), lifetime value (LTV), and CAC payback period are
widely practiced, general-purpose metrics, not tied to a single named
source. Commonly cited practitioner ranges (e.g., an early-stage
company generally wanting CAC payback under roughly 12-18 months) are
treated here as an order-of-magnitude guide, not a verified universal
benchmark — the real threshold in Step 4 below always comes from the
specific company's own budget and runway, not a rule of thumb.

## Method

1. **List every channel on the canvas separately** — outbound sales,
   inbound/content, paid acquisition, partnerships/referral,
   marketplace/platform, direct. Don't group them; each has its own
   economics.
2. **For each channel, estimate the CAC components honestly:**
   - Direct cost per lead or impression (ad spend, event cost, tooling).
   - Conversion rate from lead to paying customer, at each stage if the
     funnel has more than one.
   - Time cost — sales cycle length, and the fully-loaded cost of the
     people involved (a channel that "costs nothing" in ad spend but
     eats three weeks of a founder's time is not free).
   - Any channel-specific tooling or platform fees.
3. **Compute a blended CAC per channel** and compare it to two things at
   once: the price/margin `bmc-economic-prototyping` already
   established, and the actual budget realistically available for that
   channel (not an aspirational number).
4. **Run the payback period check.** `CAC ÷ (revenue per customer per
   period × margin) = months to payback`. Compare this against the
   company's own cash runway and patience threshold — a company with 8
   months of runway cannot tolerate a 24-month CAC payback the way a
   well-funded one can, regardless of what "normal" looks like in a
   generic benchmark. The threshold is set by THIS company's actual
   cash position, not a rule of thumb from a different kind of company.
5. **Check volume feasibility, not just unit cost.** A channel can have
   attractive per-unit CAC and still fail if it can't produce the volume
   needed to hit the revenue target established in
   `bmc-economic-prototyping`'s "big enough" question — a channel that's
   cheap per customer but can only ever deliver ten customers a year is
   not a scalable channel, it's a nice-to-have.
6. **Watch for channel novelty bias.** A common trap: a channel gets
   added to the canvas because it's currently fashionable ("we should do
   TikTok," "let's try a Product Hunt launch") without anyone costing it
   first. Every channel on the canvas should have survived steps 2-5
   before it's treated as part of the plan, not just brainstormed onto
   a sticky note.
7. **Decision rule.** If CAC payback exceeds the company's own
   runway-adjusted threshold, OR the channel can't sustain the volume
   needed at any affordable spend level, either redesign the channel
   (different targeting, different offer, different price point feeding
   back into `bmc-economic-prototyping`) or drop it — don't keep an
   unaffordable channel on the canvas "for completeness."

## What this skill does NOT do

- Doesn't build a full customer lifetime value model — for a rigorous
  LTV calculation feeding a business case, hand off to
  `business-case-and-analysis/roi-npv-sensitivity-model`.
- Doesn't design the channel's actual marketing execution (ad creative,
  content calendar, sales scripts) — it only tests whether the channel's
  economics justify pursuing it at all.
- Doesn't apply a fixed, universal CAC payback benchmark as a pass/fail
  gate — the real threshold always comes from the specific company's
  cash runway, not a generic number.

## Refinement notes

- What's your own real CAC payback threshold when advising early-stage
  clients — how much does it actually flex by runway and stage in
  practice?
- Which channel do clients most often overestimate the economics of
  before this check, and which do they underestimate?
- Have you seen "channel novelty bias" (Step 6) derail a client's
  channel strategy? What did the correction look like?

## Continue from here

- Uses: `bmc-economic-prototyping/SKILL.md` — the price/margin and
  revenue target this skill checks channels against.
- Feeds into: `business-case-and-analysis/roi-npv-sensitivity-model` for
  a full LTV/CAC model once the channel mix is set.
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/bmc-source-material-notes.md` — source material background
- `../../references/bmc-resilience-heuristics-research.md` — selection and grounding notes for this skill and its siblings
- `../../CLAUDE.md` — this pack's shared guardrails
