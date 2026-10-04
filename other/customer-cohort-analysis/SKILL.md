---
name: Customer Cohort Analysis
description: Produces a cohort retention memo -- vintage-level NRR, gross revenue retention, and curve shape rebuilt from raw billings -- when you need to test whether blended churn is masking a deteriorating recent cohort before it carries the seller's forecast.
---

# Customer Cohort Analysis

## When to use

Use this skill in the commercial workstream alongside commercial analysis, on any business with recurring or repeat revenue. Commercial analysis sizes the market and stress-tests the growth drivers; this skill tests whether the installed base behaves the way the model assumes. Run it before the returns model is locked: two points of terminal NRR compound straight into the exit EBITDA.

## What it does

Produces a cohort memo: a vintage triangle rebuilt from raw billings, retention split into logo, gross and net revenue components by vintage, an assessment of curve shape and terminal retention, and a reconciliation of that evidence to the revenue line in the seller's model.

## Method

### Step 1 -- Rebuild the triangle, do not accept it

Work from the billings extract, not the seller's cohort slide. Assign every customer to the cohort of its first invoice and plot cohort revenue against months since. Churned customers stay in at zero -- a triangle that drops them is survivorship bias. Reconcile the cohorts to reported revenue before reading anything from them.

### Step 2 -- Decompose retention into three separate numbers

Report gross logo retention, gross revenue retention (churn plus contraction, capped at 100%) and net revenue retention for each vintage. NRR above 100% with GRR in the low 80s is not a retention story -- it is a few accounts expanding fast enough to conceal a leaking base, and expansion is the first thing to stop in a downturn.

### Step 3 -- Read the shape, not the average

Plot each vintage by cohort age: does the curve flatten, and at what level? A curve still declining at month 24 has no terminal value: it is a decaying book and should not be capitalised as an annuity in the exit multiple. State the terminal retention you are prepared to underwrite and the cohort age at which it is observed.

### Step 4 -- Isolate the newest vintage

Compare vintages at equal cohort age -- month 12 against month 12 -- never at the same calendar date. Blended NRR is weighted by the oldest, largest cohorts, so a deteriorating recent vintage stays invisible for two or three years. Where the newest is worse, find the cause before pricing it: discount-led acquisition, a downmarket segment, or a channel shift.

### Step 5 -- Reconcile the cohorts to the model

Roll the base forward on vintage-specific NRR rather than the blend, and solve for the gross new bookings the seller's revenue line requires. Test it against historical bookings and sales capacity, then price the gap: incremental margin on the shortfall, entry multiple on the EBITDA. Where vintages disagree, underwrite the newest one -- it is the cohort that carries the forecast, and the blend is the artefact.

## Inputs

- Billings extract by customer and month (36 months minimum)
- Customer start dates, churn dates, and contract values
- Seller's stated retention metrics and their definitions
- Revenue build from the model or CIM, with the new-bookings assumption
- Incremental margin and entry multiple from the returns model

## Output format

A cohort memo with five sections:
1. Triangle construction and reconciliation to reported revenue
2. Logo, gross and net retention by vintage (prose, never a table)
3. Curve shape and the terminal retention underwritten
4. Vintage comparison at equal cohort age, and the cause of any drift
5. Reconciliation to the model: implied bookings and EBITDA impact

Total length: 900-1,200 words. Every number traceable to the billings extract.

## Example

**Vintage reconciliation (excerpt -- Meridian Fieldworks, fictional):**
LTM revenue $60.0m, EBITDA $15.0m, offered at 12.0x for an EV of $180.0m. Blended NRR is reported at 107%. Rebuilt by vintage, the opening base splits $36.0m pre-2023 at 112%, $15.0m 2023 vintage at 104% and $9.0m 2024 vintage at 94%, closing at $64.38m -- 107.3% blended. The blend is accurate and useless: by year three the post-2023 cohorts are most of the base. Held at 107%, revenue reaches $73.5m in year three; at 102% it reaches $63.7m. That $9.8m gap is $5.9m of EBITDA at a 60% incremental margin, and $71m of exit EV at an unchanged 12.0x. Recommend the base case adopt the 2024 curve, not the blend.
