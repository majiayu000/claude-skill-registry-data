---
name: precedent-transaction-screener
description: Build a screened, cycle-adjusted set of M&A precedents that actually inform pricing. Use when building the precedent page of a valuation deck, pressure-testing a control-premium thesis, or framing a buy-side bid against historical comparables. Built around screening discipline, cycle and structure adjustments, and synergy calibration.
---

# Precedent Transaction Screener

## Purpose

Identify the M&A transactions that genuinely inform what a control buyer would pay for this target — and discard the ones that look comparable but were priced under conditions that no longer apply.

The output is not a long list of "transactions in the sector." It is a tight set of true comparables, calibrated for cycle, deal structure, and buyer type, with the multiples that should actually anchor the valuation conversation.

## Governing Principle

**A precedent is only useful if you would re-do the deal at the same multiple today. If not, adjust or discard.**

Bad precedent work pads the page with deal count. Good precedent work cuts the list down to the five to fifteen transactions that an experienced buyer or seller would actually negotiate against.

## The Five Filters Every Precedent Set Must Pass

Every precedent in the final set must clear all five filters, with explicit justification on the borderline cases.

1. **Business comparability** — same business model, customer profile, and economic shape
2. **Scale comparability** — close enough in size that scale economics and buyer universe overlap
3. **Geography and regulatory comparability** — same regime, or explicitly adjusted
4. **Deal structure comparability** — control transaction with similar consideration mix and process type
5. **Cycle comparability** — same credit and sector regime, or cycle-adjusted

A precedent missing one of these is a footnote. A precedent missing two is noise. Cut it.

## Workflow

### Step 1 — Define the screen, in writing, before pulling the list

A common mistake is pulling 200 deals and then arguing about which to keep. Define the screen first:

- **Sector / sub-sector:** SIC, GICS, or a custom taxonomy that matches the target's business model
- **Geography:** target HQ, or revenue concentration
- **Size band:** transaction value range, typically 0.5x to 3x the expected deal size
- **Deal type:** majority/control transactions only (>50% economic stake)
- **Timeframe:** typically 3–5 years for stable sectors, 12–24 months for cyclical or rapidly repricing sectors
- **Consideration:** all-cash, stock, mixed — flag but include all; treatment depends on what the buyer profile teaches
- **Exclusions:** related-party transactions, distressed sales, court-approved sales, recap-style minority sales mislabeled as M&A

Document the screen at the top of the precedent page. The screen is the audit trail.

### Step 2 — Pull the raw list from multiple sources and reconcile

Use at least two databases (LSEG SDC, Mergermarket, Capital IQ, Bloomberg M&A, PitchBook, Dealogic). They will not agree on:

- Transaction value (enterprise value treatment of assumed debt varies)
- Announce vs. close dates
- LTM metrics (databases often pull from filings of different dates)
- Earnout treatment (included or excluded in headline)
- Minority stakes (sometimes mislabeled as control)

For each deal that makes the short list, go back to the primary source: 8-K, proxy, scheme document, press release, target's last 10-Q before announcement. The database is a starting point, not a citation.

### Step 3 — Calibrate metrics to announcement-date economics

Every multiple must use the same metric convention:

- **EV at announcement:** offer price × diluted shares (pre-deal share count, treasury method on options/RSUs) + assumed debt − cash, on the announcement date
- **LTM EBITDA / EBIT / revenue:** trailing 12 months ending at the most recent filing before announcement. Calendarize if needed.
- **NTM (optional):** forward consensus or company guidance at announcement, only if available across the set
- **Adjustments:** apply the same adjustments (one-time items, stock-comp treatment, lease accounting) consistently across the set

If a database shows a multiple and you cannot rebuild it from primary sources, do not use the multiple. Bankers get burned more often by an unreproducible multiple than by a missing one.

### Step 4 — Tag each precedent on the dimensions that move the multiple

Build a working file with the following tags. These are what makes the difference between a "median multiple" and an actionable range.

| Tag | Why it matters |
|---|---|
| Buyer type (strategic / sponsor / consortium) | Strategics typically pay more for synergy; sponsors are returns-constrained |
| Process type (broad auction / limited / targeted / unsolicited) | Auction premiums vs. negotiated deals run 5–15% differently |
| Consideration mix (cash / stock / mixed) | Stock deals tend to print higher headline multiples; cash deals are cleaner |
| Strategic rationale (consolidation / capability / scale / vertical / defensive) | Different rationales support different premiums |
| Sector cycle position at announcement | Top-of-cycle deals print high; trough deals print low |
| Credit conditions at announcement (HY index, leverage availability) | LBO activity and strategic financing capacity flex with credit |
| Target situation (forced seller / dual-track / opportunistic / unsolicited target) | Distress depresses multiples; opportunistic processes lift them |
| Synergy disclosure (announced run-rate, % of target revenue) | Synergy assumption magnitude is a direct premium driver |
| Earnout / contingent consideration | Headline price overstates real economics if contingent value is meaningful |

### Step 5 — Cycle-adjust the multiples

A 2021 software deal at 12x revenue is not a useful precedent for a 2025 deal. Two adjustment methods:

- **Index method:** divide the precedent multiple by the sector trading multiple at announcement; multiply by the current sector trading multiple. Crude but defensible.
- **Cohort method:** group precedents by cycle regime (e.g., pre-pandemic / pandemic / post-pandemic / current cycle) and present medians by cohort

Show both the unadjusted and adjusted multiples. The MD will want to see both.

Flag any precedent where the credit market at announcement is materially different from today. A deal financed at 7.0x leverage when the market is now offering 5.0x will not re-print at the same multiple.

### Step 6 — Separate the precedent set into tiers

Not every precedent deserves equal weight. Force a tiering:

- **Tier 1 — Direct precedents:** same sub-sector, similar size, similar structure, within the last 24 months. Carries most weight.
- **Tier 2 — Analog precedents:** adjacent sub-sector or different scale, but same economic shape and recent. Triangulation use.
- **Tier 3 — Reference precedents:** older, distant, or smaller — useful for showing the historical range, not for pricing

Present Tier 1 separately. The median and 25th–75th percentile of Tier 1 is the working range. Tiers 2 and 3 are context.

### Step 7 — Read the premium and synergy logic separately

For public-target precedents, report two related but distinct numbers:

- **Multiple paid** (EV / LTM EBITDA, etc.)
- **Control premium** (offer price vs. unaffected share price, typically 1-day, 30-day, 90-day)

These often disagree. A deal at a "high multiple" can have a "low premium" if the stock was already running. Both numbers matter for different audiences:

- **Boards / proxy advisors:** care about premium
- **Buyer underwriting / fairness reasoning:** cares about multiple
- **Target shareholders:** care about absolute per-share

For strategic precedents, also pull **synergy disclosure**: announced run-rate cost synergies, expressed as a % of target revenue or target operating cost. The premium offered is often roughly equal to the present value of disclosed synergies — when this holds, the strategic was paying away the synergies to get the deal done. When the premium exceeds the synergy PV, the buyer was paying for strategic scarcity, not value creation.

### Step 8 — Write the precedent page with a view

The precedent page is not a list. It is a recommendation. End with:

- The median and 25th–75th percentile of Tier 1
- A written sentence on where this target should fall within that range and why (growth, margin, scale, scarcity, buyer profile)
- An explicit note on which precedents would re-print today at the same multiple and which would not
- The implied valuation range applied to the target's metric

## Hypotheses to Pressure-Test

1. **"The median precedent multiple includes deals that would not re-print today."** Which precedents are from a different credit cycle, a different sector regime, or a different consolidation phase?
2. **"The precedent set is biased by survivorship of announced deals."** Walked deals, busted processes, and at-the-altar terminations are missing — what do they tell us about the real walk-away multiple?
3. **"Strategic premiums in the set are paying away synergies."** Is the headline premium consistent with the disclosed synergy run-rate, or is it pricing in scarcity / strategic urgency?
4. **"The 'control premium' on our precedents was inflated by leak-driven run-up."** Was the unaffected price actually unaffected, or was the market already pricing the deal?
5. **"The sub-sector definition is too broad."** Are we lumping in business models with different unit economics under a single SIC code?

## Quality Checks Before Sharing

- [ ] Screen criteria documented in writing at the top of the working file
- [ ] Every multiple is reproducible from primary sources, not just from a database pull
- [ ] EBITDA / EBIT / revenue treatment is consistent across the set (same adjustments, same period)
- [ ] Each precedent is tagged on buyer type, process type, consideration, strategic rationale, and cycle
- [ ] Cycle adjustment is applied or explicitly waived with reasoning
- [ ] Tier 1 / Tier 2 / Tier 3 split is explicit and the working range is taken from Tier 1
- [ ] Control premium and multiple paid are reported separately for public targets
- [ ] Synergy disclosure pulled and compared to premium for strategic precedents
- [ ] The page ends with a recommended range and a sentence on where the target sits within it
- [ ] Outliers either kept with a written reason or excluded with a written reason — never silently dropped

## Common Failure Modes

- **Median multiple as the answer.** Showing a list of 25 deals and applying the median. The median is the start of the conversation, not the end.
- **Stale cycle.** Pulling deals from a different credit regime without adjustment. The multiple is real; the conditions that produced it are not.
- **Buyer-blind set.** Mixing strategic and sponsor deals into one number without acknowledging that they price differently.
- **Synergy-blind precedents.** Showing premiums without the synergy disclosures that explain them. The premium is the output; the synergy logic is the input.
- **Optical comparables.** Including deals because the target name sounded similar, not because the business model and economics are the same.
- **Earnout illusion.** Reporting headline transaction value with full earnout achievement when the contingent portion was the buyer's discipline against an overstated case.
- **Distressed inclusion.** Letting court-approved sales, forced divestitures, or recap-style transactions sit in the set without flag. They depress the median and mislead the range.

## Deliverable

A documented screen, a tiered precedent table with multiples, control premiums, buyer type, consideration, strategic rationale, and cycle tags, a cycle-adjusted view alongside the raw view, a Tier 1 median and 25th–75th percentile, and a written recommendation on where the target should be priced within the precedent range and why.
