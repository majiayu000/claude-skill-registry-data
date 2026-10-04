---
name: trading-comps-builder
description: Construct a clean trading comps universe with disciplined peer selection, calendarization, EBITDA adjustments, and outlier treatment. Use when building the comps page of a valuation deck, framing a minority valuation reference, or pressure-testing a public-market reference range. Built around peer comparability, metric normalization, and the difference between a peer and a peer-shaped distractor.
---

# Trading Comps Builder

## Purpose

Build a defensible public trading comparables set that supports a minority-stake valuation reference, frames the public-market view of the target, and survives a sharp counterparty's review.

The output is a small set of true peers — typically 6 to 12 — with clean, calendarized metrics, consistent EBITDA adjustments, and a documented rationale for inclusion or exclusion of every name considered.

## Governing Principle

**A peer is a company whose multiple a sophisticated investor would actually use to price the target. Everything else is a distractor.**

The discipline is in what gets cut, not in what gets added. A comps page with 25 names is usually a comps page with 6 peers and 19 things hiding the analysis.

## The Three Tests of a True Peer

A name belongs in the set only if it passes all three. Borderline names go on a "near-peer" page, not in the main set.

1. **Business model match** — same revenue model, customer profile, and unit economics
2. **Financial profile match** — comparable growth, margins, and capital intensity (or differences priced explicitly into the discussion)
3. **Trading liquidity and disclosure** — sufficient float, sell-side coverage, and disclosure to produce a defensible multiple

Geography is a tag, not a filter. A non-US peer with the same business model can be more useful than a US name with a different one — but the geographic multiple delta must be acknowledged and adjusted.

## Workflow

### Step 1 — Build the long list before the short list

Start broad. Pull candidates from:

- The target's own 10-K / 20-F competitor disclosure
- Sell-side coverage initiations: which peer sets do covering analysts use?
- Proxy peer groups (from compensation disclosures — often more honest than IR-curated lists)
- Sector indices (S&P sub-industry, GICS Level 4, MSCI)
- The target's own self-described peer set in investor presentations
- The peer sets used in recent precedent transactions on the target or its competitors

A typical long list is 25–50 names. The short list will be 6–12. The discipline is in the cut.

### Step 2 — Score each candidate against the target

Build a candidate scoring table:

| Dimension | Target | Candidate | Match (H/M/L) |
|---|---|---|---|
| Revenue model | Subscription / transactional / project / one-time | | |
| Customer mix | Enterprise / SMB / consumer | | |
| Geographic mix | % NA / % EMEA / % APAC | | |
| Product / service overlap | % of revenue in overlapping segments | | |
| Growth profile | Last 2 yrs revenue CAGR, NTM consensus growth | | |
| Margin profile | Gross %, EBITDA % | | |
| Capital intensity | Capex / revenue, working capital / revenue | | |
| Scale | Revenue, market cap | | |
| Capital structure | Net debt / EBITDA, leverage targets | | |

A name needs to be "H" on business model and at least "M" on financial profile to make the short list. Names that score "L" on business model but high on optical familiarity (same sector ETF) are the most dangerous — they look right and price wrong.

### Step 3 — Pull the metrics with consistent conventions

Standardize before pulling:

- **Pricing date:** a single as-of date applied across the entire set, with reference to the unaffected price if there is deal-related movement on any peer
- **Share count:** fully diluted treasury method (in-the-money options, RSUs, convertibles)
- **Net debt:** most recent reported balance sheet, with pro forma adjustments for announced post-period transactions
- **EBITDA / EBIT / revenue:** clearly labeled LTM, calendar year, or fiscal year — never mixed
- **Forward consensus:** the same consensus source (FactSet, Bloomberg, Refinitiv) for the entire set — never mixed
- **Currency:** convert to the target's reporting currency at the spot rate on the pricing date

The most common comp error is a quietly mixed convention — fiscal-year EBITDA on one peer, calendar on another. The multiple distribution looks tighter or wider than it actually is.

### Step 4 — Calendarize every off-cycle peer

If peers have different fiscal year-ends, calendarize forward and trailing metrics to a common basis (typically calendar year-end or the target's fiscal year-end).

```
Calendarized FY1 = (X months of FY current × current FY estimate)
                 + (12 − X months of FY+1 × FY+1 estimate)
                 ─────────────────────────────────────────────
                                    12
```

Show the calendarization mechanics in the appendix. Without them, fiscal-year-end mix differences will show up as multiple spread that has nothing to do with valuation.

### Step 5 — Adjust EBITDA consistently

Apply the same adjustments to the target and every peer. Common adjustments and their treatment:

| Item | Default treatment | Note |
|---|---|---|
| Stock-based compensation | Subtract (treat as cash cost) | The "true" EBITDA debate — pick a side and apply it consistently |
| Restructuring charges | Add back if disclosed as one-time and not recurring quarterly | Recurring "one-time" is recurring |
| M&A transaction costs | Add back if non-recurring | |
| Asset impairments | Add back (non-cash) | |
| Operating lease expense (post-IFRS 16 / ASC 842) | Apply consistent EBITDA pre-rent or EBITDA post-rent across the set | Materially affects comparability between US and non-US peers |
| Earnout adjustments / contingent consideration | Add back FV adjustments (non-cash) | |
| Litigation reserves | Add back if non-recurring and disclosed | |
| FX gains / losses (operating) | Generally leave in | |
| Gain on sale of business | Subtract (not operating) | |

Two adjusted EBITDA columns — "as-reported adjusted" and "your adjusted" — make the differences transparent. Bankers should never silently adopt management's adjustments without showing them.

### Step 6 — Handle outliers explicitly, not silently

Every peer set produces outliers — multiples 50%+ above or below the median. Outliers are not noise; they are signal.

Three legitimate treatments:

- **Keep and explain:** the outlier is real and the reason (higher growth, scarcity, recent deal speculation, distressed) is documented
- **Move to near-peer:** the company is sector-adjacent but not a true peer; show separately
- **Exclude:** the company has a structural reason its multiple is non-comparable (distressed, controlled stub, pending take-out, accounting under review)

Silently dropping the high or low multiple is the worst option — it skews the median and removes the most informative observation.

### Step 7 — Present the right metrics, not all the metrics

A clean comps page shows:

- **Multiples table:** EV/Revenue, EV/EBITDA, EV/EBIT, P/E — for LTM, FY1, FY2 — with median and 25th/75th percentile
- **Operating metrics table:** revenue growth (LTM, FY1, FY2), EBITDA margin (LTM, FY1, FY2), EBIT margin, ROIC if relevant
- **Financial position:** net debt / EBITDA, capital structure, dividend yield if relevant

The visual goal: a senior banker scanning the page should be able to see at a glance which peer is the growth leader, which is the margin leader, and how the multiples track those rankings. If high-growth peers don't trade at premium multiples in your set, something is wrong — either with the set or with the metrics.

### Step 8 — Land the recommendation

A comps page that doesn't say where the target should price is incomplete. End with:

- The peer median and 25th–75th percentile for the most relevant multiple (typically EV/NTM EBITDA for mature businesses, EV/NTM revenue for growth businesses)
- A written sentence: "The target's [growth / margin / scale / capital intensity / risk profile] supports a multiple at [position] within the peer range, implying an equity value per share of [$X – $Y]"
- An explicit note on which peers are most relevant to the target and which are included for breadth — and why the recommendation leans on the former

## Hypotheses to Pressure-Test

1. **"The set is optically similar but economically different."** Are we mixing subscription and transactional revenue models under the same sector label? Different unit economics, different multiples.
2. **"The median is being pulled by one or two unusual situations."** Distressed, take-out speculation, recent IPO scarcity premium — what happens to the median if we move outliers to near-peer?
3. **"The forward consensus is stale on half the set."** Have peers recently reset guidance or printed quarters that consensus hasn't fully digested?
4. **"The peer ranking by growth/margin doesn't track the multiple ranking."** If the highest-margin peer doesn't trade at the highest multiple, what is the market pricing that the multiples table is missing?
5. **"The target deserves a different multiple than its peer median because of [X]."** Write the sentence. If it can't be defended in one line, the multiple chosen is not defensible.

## Quality Checks Before Sharing

- [ ] Long list documented and short-list cuts justified in writing for every borderline name
- [ ] Pricing date, share count convention, and consensus source applied identically across the set
- [ ] Calendarization shown in an appendix for any peer with an off-cycle fiscal year
- [ ] EBITDA adjustments applied consistently to target and every peer, with the rule documented
- [ ] Outliers either kept (with reason), moved to near-peer, or excluded (with reason) — never silently dropped
- [ ] Multiples are presented on forward metrics primarily, trailing as sanity check
- [ ] Operating metrics (growth, margin) shown alongside multiples so the reader can sanity-check the ranking
- [ ] Median and 25th–75th percentile shown — not mean
- [ ] Page ends with a written recommendation on where the target should price within the range and why
- [ ] No multiple is shown that the analyst cannot rebuild from primary sources

## Common Failure Modes

- **Sector ETF as peer set.** Lifting the constituents of an industry index without testing business-model comparability. Most ETF constituents are distractors.
- **Mixing revenue models.** Putting subscription, project, and transactional businesses in one set because they sit in the same vertical. The multiples mean different things.
- **Stock-comp inconsistency.** Subtracting SBC from one peer's EBITDA and not from another. The multiple delta vanishes when consistency is restored.
- **Median as the answer.** Applying the peer median to the target with no written rationale for the position within the range.
- **Bigger set is better.** Stretching to 20 peers because "more is more robust." It isn't. More noise is just more noise.
- **Currency drift.** Mixing reporting currencies without translation, or translating at the wrong rate.
- **Stale fiscal years.** Treating an unreported quarter as "LTM" by pulling the last reported figures. Fix the LTM with the most recent quarter.
- **Forward without source.** Pulling forward estimates from a different source per peer, then comparing the resulting multiples as if they were on the same basis.

## Deliverable

A peer scoring table that justifies inclusion or exclusion of every long-list candidate, a clean trading comps table with multiples and operating metrics on consistent conventions, a calendarization appendix where relevant, an explicit outlier treatment log, a peer median and 25th–75th percentile, and a written recommendation on where the target should price within the peer range and why.
