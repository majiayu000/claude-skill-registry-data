---
name: accretion-dilution-tester
description: Run a defensible accretion/dilution analysis with the financing, synergy, and tax mechanics that actually move EPS. Use when pricing an M&A transaction with a public-company acquirer, framing a stock-vs-cash consideration mix, or stress-testing IC and board materials. Built around purchase-price mechanics, financing mix, synergy timing, tax shield, intangible amortization, and disciplined sensitivity.
---

# Accretion / Dilution Tester

## Purpose

Produce an accretion/dilution analysis that holds up under board, sell-side analyst, and rating-agency scrutiny — built from a defensible sources-and-uses, the right financing mix at market rates, realistic synergy timing, and a tax model that reflects actual deal mechanics.

The output is not a single accretion number. It is a sensitivity table that shows the path from "what we believe" to "what would have to be true" — and a written paragraph on where the deal lives within that sensitivity.

## Governing Principle

**Synergies decide the deal. Financing decides the day-one math. Neither is what's in the IC deck — the IC deck shows the punchline.**

A weak accretion analysis lets the headline accretion number do the work and hides the synergies, the financing assumptions, and the share count mechanics that produced it. A strong analysis shows all three transparently and lets the reader see what the deal really requires.

## The Five Mechanics That Move Accretion

Every accretion model is the interaction of five mechanics. Get any one of them wrong and the answer is wrong.

1. **Purchase price and structure** — equity value paid, consideration mix (cash / stock / mixed)
2. **Financing mix** — new debt, cash on hand, stock issuance — each with its own after-tax cost
3. **Synergies and dis-synergies** — type, magnitude, timing, phasing
4. **Tax** — cash tax rate, NOL utilization, tax shield from new debt, deductibility of intangibles
5. **Share count and intangible amortization** — new shares issued, intangible step-up, amortization drag

## Workflow

### Step 1 — Lock the transaction structure and sources and uses

Before any EPS line is built, fix the transaction architecture:

- **Purchase price:** equity value at offer, with the bridge from offer price per share × diluted shares to total equity consideration
- **Total enterprise value:** equity + assumed debt − cash − other adjustments (preferred, minority interest)
- **Consideration mix:** % cash, % stock, % other (CVR, rollover equity, earnout)
- **Stock-component mechanics:** exchange ratio (fixed or floating), collar terms, walk-away rights
- **Sources of cash:** acquirer cash on balance sheet, new term loan, new bond issuance, revolver draw
- **Uses of cash:** purchase price (cash portion), refinanced target debt, transaction fees, change-of-control payments, financing fees

The sources and uses table is the spine of the model. Build it once, label every line, and tie it to financial statements.

### Step 2 — Apply realistic cost-of-financing assumptions

The single most common error in accretion analysis is using outdated or wishful financing costs. Use the marginal cost of new issuance, not the weighted-average cost of existing debt.

- **New term loan / senior secured:** spread over SOFR / EURIBOR at current credit rating implied by pro forma leverage; check recent comparable issuances
- **New senior unsecured / high yield:** secondary trading levels for comparable issuers, with a primary new-issue premium
- **Bridge financing:** include the cost if the financing is bridge-then-take-out
- **Foregone interest on cash used:** the after-tax interest rate the acquirer was earning on the cash balance (real, not hypothetical — many corporates earn well below money-market rates on operating cash)
- **Cost of equity:** for stock-funded deals, the dilution cost shows up via share count; no explicit interest, but the EPS impact must reflect the new share base

Apply the after-tax cost: pre-tax interest × (1 − marginal tax rate). The tax shield is real but only to the extent the acquirer has taxable income to absorb it.

### Step 3 — Build the synergy schedule

Synergies are the deal economics. Build them with discipline:

- **Cost synergies — type:** SG&A overlap (corporate functions, public company costs), procurement, manufacturing footprint, technology, real estate
- **Cost synergies — magnitude:** run-rate $ amount and as % of target operating cost; sanity-check against precedent synergy disclosures in this sub-sector (cost synergy as % of target revenue typically clusters 3–8% for in-sector deals)
- **Cost synergies — phasing:** the standard phasing is 25% / 50% / 100% by Year 1 / Year 2 / Year 3. Aggressive deals show full-year-one; conservative deals push to Year 3. The IC should see the phasing assumption explicitly.
- **Revenue synergies:** include only if you can name the specific mechanism (cross-sell into target customers, geographic extension of acquirer product, channel access). Revenue synergies should be presented separately and excluded from base-case EPS.
- **Dis-synergies:** customer overlap loss, talent attrition, integration disruption, capex catch-up. Often understated or omitted.
- **Cost to achieve:** integration costs (severance, system migration, real estate consolidation) — typically 1.0–1.5x run-rate synergies, expensed over Years 1–2

A synergy schedule that shows only the run-rate is incomplete. Show year-by-year phasing, cost to achieve, and net synergy contribution to EPS for at least three years.

### Step 4 — Model the tax mechanics

Tax is where accretion math gets quietly wrong:

- **Acquirer cash tax rate:** the rate actually paid, not statutory; reflect NOL utilization and book-vs-cash differences
- **Target cash tax rate:** same — and if it differs materially from acquirer, model the convergence path post-deal
- **Tax shield on new debt:** interest expense × marginal tax rate, applied only to the deductible portion (subject to interest deductibility limits — Section 163(j) in the US, similar caps in other jurisdictions)
- **Goodwill / intangible amortization:** for stock deals, goodwill is generally not tax-deductible (US); for asset deals or 338(h)(10) elections, goodwill amortizes for tax over 15 years. The deal structure determines this.
- **Step-up benefits:** in asset deals, the tax basis step-up creates a depreciation tax shield. Quantify.
- **NOL transfer and limitation:** target NOLs may be transferable but subject to Section 382 limits in the US

For cross-border deals, the picture is more complex: withholding, repatriation, transfer pricing, controlled-foreign-corporation rules. Engage tax counsel early; do not assume.

### Step 5 — Build the GAAP / IFRS amortization drag

For purchase accounting:

- **Intangible asset identification:** customer relationships, trade names, technology, non-competes
- **Amortization life by intangible type:** customer relationships typically 8–15 years, technology 5–10, trade names indefinite or 10–20
- **Annual amortization charge:** the sum of the above, hitting reported EBIT and net income (but not cash EBITDA)
- **Pro forma EBITDA vs. pro forma net income:** the intangible amortization is the wedge — pro forma EBITDA may show accretion while pro forma EPS shows dilution

Sophisticated audiences look at both EPS (GAAP) and "cash EPS" (EPS before amortization of acquired intangibles). Present both; flag the gap. Strategic acquirers will often guide to cash EPS post-deal — anticipate this.

### Step 6 — Compute the share count carefully

In stock-funded deals, share count mechanics drive the answer:

- **Exchange ratio:** fixed or floating; if fixed, what is the value at the announcement price vs. the deal-close price?
- **Treasury method on target options/RSUs/converts:** rolled into the deal at the deal price, with the cash-out economics
- **Acquirer treasury method:** account for the acquirer's own option pool dilution
- **Issuance for financing:** if any equity is being raised alongside the deal, model the dilution
- **Buyback / cash discipline:** in cash deals, no new shares issued, but the cash deployed reduces interest income or increases debt — both affect EPS

The denominator is as important as the numerator. A model that uses pre-deal share count for accretion math will be wrong by the issuance fraction.

### Step 7 — Run the accretion / dilution math year by year

Build the pro forma P&L for at least three years post-close:

```
Pro Forma EPS Year N
  = (Acquirer Net Income standalone
     + Target Net Income standalone
     + After-tax synergies (phased)
     − After-tax incremental interest from new debt
     − After-tax foregone interest on cash used
     − After-tax incremental D&A from PPA step-up
     − After-tax amortization of acquired intangibles
     − After-tax integration costs (Years 1–2))
    ÷ Pro Forma Share Count
```

Compare to standalone Acquirer EPS. The difference is the accretion / (dilution) per share, expressed both as $/share and as %.

A deal is "accretive in Year 1" if Year 1 pro forma EPS > standalone EPS. Conventional standards expect accretion by Year 2 on cash deals; Year 3 on stock-financed strategic deals. Anything beyond that should be defended explicitly.

### Step 8 — Sensitize the inputs that actually move the answer

A single-point accretion answer is not analysis. Sensitize:

- **Purchase price** ±10% — the bid range the board will consider
- **Cost synergy run-rate** ±25% — the realistic range the IC will challenge
- **Synergy phasing** (slow / base / fast) — the timing risk
- **Interest rate** ±100bps — the financing cost reality
- **Cash / stock mix** at three points — to see what the consideration choice costs
- **Cash tax rate** — particularly for cross-border

Present the two most important sensitivities as a 2D table (e.g., purchase price × synergy run-rate). The honest answer often is: the deal is accretive in the base case but dilutive in 30% of the sensitivity space — show this, don't bury it.

### Step 9 — Translate to credit and capital allocation implications

A complete analysis covers the second-order effects:

- **Pro forma leverage:** net debt / EBITDA at close, and the deleveraging path
- **Interest coverage:** EBITDA / interest expense, with cushion to covenant or rating threshold
- **Rating impact:** likely change in credit rating from S&P / Moody's / Fitch (use their stated leverage thresholds)
- **Buyback / dividend capacity:** how the deal constrains shareholder return for how long
- **Strategic optionality:** what the post-deal balance sheet permits or precludes (next M&A capacity, organic investment, etc.)

A deal that is mildly accretive but burns three years of buyback capacity and triggers a rating downgrade may not be a good deal — even if the EPS line is positive.

## Hypotheses to Pressure-Test

1. **"The headline accretion depends entirely on the synergy assumption."** Strip out synergies. Is the deal still accretive on hard mechanics (cost of financing × debt issued vs. target earnings)? If not, the deal is a synergy bet dressed as an EPS-accretive transaction.
2. **"The cost of financing assumed is below market."** Is the modeled interest rate consistent with where a comparable issuer would price today, or with the acquirer's prior issuance from a different rate environment?
3. **"Synergy phasing is aggressive."** Does the model show 75%+ of synergies in Year 1, when integration realities typically deliver 25–40% in Year 1?
4. **"Tax assumptions are optimistic."** Is the model assuming full tax shield on debt that may be limited by Section 163(j)? Is goodwill amortization being treated as tax-deductible in a stock deal?
5. **"The pro forma share count is wrong."** Is the exchange ratio mechanic correct? Are target options being properly rolled at deal price? Is acquirer dilution from concurrent equity issuance reflected?
6. **"The dis-synergies are missing."** Customer overlap loss, talent attrition, integration disruption, capex catch-up — present in every deal, often omitted from the model.

## Quality Checks Before Sharing

- [ ] Sources and uses tied to balance sheet, with every line labeled
- [ ] Cost of new debt reflects current market for comparable issuer credit and tenor
- [ ] After-tax interest used (not pre-tax), with the marginal tax rate documented
- [ ] Synergies broken into cost / revenue, with magnitude and phasing both disclosed
- [ ] Revenue synergies presented separately and not in the base case unless specifically defended
- [ ] Cost to achieve and dis-synergies included
- [ ] Intangible amortization modeled with named life assumptions by intangible type
- [ ] Both GAAP EPS and cash EPS (ex-amortization) presented
- [ ] Share count rebuilt for stock deals using exchange-ratio mechanics; target option treatment explicit
- [ ] Year 1 / Year 2 / Year 3 accretion shown, not just steady-state
- [ ] Sensitivity on purchase price × synergies, financing cost, and tax presented as 2D tables
- [ ] Pro forma leverage and rating-agency implications stated
- [ ] Written paragraph explains where in the sensitivity range the deal lives and what would have to be true for it to fail the IC test

## Common Failure Modes

- **Headline accretion as the answer.** Showing a single accretion % without the sensitivity around it. Hides the synergy or financing assumption that produces the answer.
- **Stale cost of debt.** Using a 2-year-old marginal cost of new debt. The financing market is the most volatile input in the model.
- **Synergy fairy tale.** Run-rate synergies that exceed precedent ranges, phased into Year 1, with no cost to achieve. These deals don't show up on the EPS line as forecast — they show up in the integration costs line.
- **Revenue synergies in the base case.** Revenue synergies are rarely realized; they should never carry the EPS thesis.
- **Tax shield on non-deductible debt.** Modeling full tax shield without testing 163(j) limits or jurisdiction-specific caps.
- **Goodwill amortizing for tax in a stock deal.** A US stock deal generally produces non-deductible goodwill. Modeling tax shield on it is wrong.
- **Wrong share count.** Pre-deal share count in the denominator for a stock-funded deal. Forgetting to roll target options. Ignoring concurrent equity issuance.
- **Hiding pro forma leverage.** Showing accretion without showing the rating-agency consequence.
- **No "what would have to be true."** Failing to write the paragraph on where the deal lives in the sensitivity space. Numerically defensible, commercially indefensible.

## Deliverable

A pro forma model with sources and uses tied to balance sheet, year-by-year accretion / dilution math (Years 1–3+), GAAP and cash EPS both presented, 2D sensitivity tables on the inputs that actually move the answer (purchase price × synergies, interest cost, tax), pro forma leverage and rating-agency analysis, and a written paragraph stating where in the sensitivity space the deal sits and what would have to be true for the thesis to fail.
