---
name: start-runway-plan
description: Builds a First-Year Runway Plan from your own records, with monthly personal and business costs, the money available, months of runway, the income you need by which month, set-aside lines you fill and three scenarios with decision dates you choose. Use for "run start-runway-plan", "how long can I last without a salary", "how much money do I need to go out on my own", "work out my runway", "when do I need my first invoice paid", "first year budget for my practice", "plan my money for year one", part of the Claude Guide for New Founders Pack by Polar Bear.
---

# First-Year Runway Plan

## When To Use
You left a salary and do not know how many months you have before the first invoice has to be paid. Until that number exists, every decision is made under a vague fear: you take the wrong work, or you discount too early. This answers: how long does the money last, and what has to be true by which month?

## When Not To Use
If you know your runway and need a price, run Floor Rate Calculator. If the first income has arrived and you want to see where you stand each month, Monthly Practice Review reads the same numbers as they move.

## Inputs
- Three months of bank or card statements, personal and business, exported by you
- One-time costs of starting (equipment, registration, insurance, adviser fees) and any income already agreed
- The money you are willing to spend on this: savings, a final payment, a partner's income you count on
If you have none of this, I start from your own estimate of monthly spending and money available, and mark every line "estimate" and the output as a first draft.

## Approach
The US Small Business Administration's startup cost guide gives the steps: list your expenses, estimate each, split one-time from monthly, count the months, add it up, then run a break-even analysis. It advises planning for at least a year of monthly expenses. The guide is written for businesses with premises and stock; for one person the largest line is their own living costs, so both sides of your life go on one sheet. The failure it prevents is the six-month plan that quietly assumed the first client would pay in month two.

## Workflow
1. Ask at most three questions: which money counts as available for this, what income is already agreed and when it will be paid, and what date you privately think of as "decision time".
2. List expenses from your statements, one line each with its source, split into one-time and monthly, and into personal and business. A cost you remember but cannot find goes in as "estimate".
3. Add the set-aside lines and leave them for you to fill: tax, pension, insurance, a buffer. I never suggest the amounts; for tax, check with a qualified adviser.
4. Calculate with the arithmetic shown: monthly burn = monthly personal + monthly business + set-asides. Runway in months = (money available minus one-time costs) / monthly burn.
5. Work back the income you need: the month the money runs out, minus the weeks between sending an invoice and being paid (your figure, or "unknown"), gives the month by which work has to be signed.
6. Build three scenarios on a month-by-month table: no income, the income already agreed, and the income you are aiming for. For each, you set a decision date and what you will decide then (cut a cost, take interim work, change the offer).
7. Produce the sheet as a table, or as a spreadsheet through file creation, so you can update it monthly.

## Output Format
```markdown
# First-Year Runway Plan
Prepared: [date] | Records used: [statements, months] | Lines marked estimate: [number]
## Costs
| Line | One-time or monthly | Personal or business | Amount | Source | Estimate? |
|---|---|---|---|---|---|
| [cost] | [type] | [side] | [amount] | [statement, invoice] | [yes / no] |
| Set-asides (tax, pension, insurance, buffer) | monthly | [side] | [amount I set] | [me / my adviser] | no |
## Runway
- Money available: [amount] | One-time costs: [amount] | Monthly burn: [amount]
- Runway: ([available] minus [one-time]) / [burn] = [months], to [month, year]
- Work must be signed by: [month], allowing [weeks] from invoice to payment
## Scenarios
| Scenario | Income assumed | Money runs out | My decision date | What I decide then |
|---|---|---|---|---|
| No income | none | [month] | [date] | [decision] |
| Agreed income | [amount, from whom] | [month] | [date] | [decision] |
| Target income | [amount, by month] | [month] | [date] | [decision] |
## Decision
[Your name] confirms the monthly burn and the three decision dates by [date], and puts each date in the calendar.
```

## Done When
- Every cost line has a source from your records or is marked "estimate".
- The runway arithmetic is visible and adds up.
- Each scenario has a decision date and a decision, both set by you.
- The set-aside lines are filled by you or marked "to ask my adviser".

## Quality Bar
- No figure for what a first year "usually" earns, and no promise of when income arrives.
- Payment delay is your figure or "unknown", never an assumed number of days.
- Tax, pension and insurance amounts are yours: check with a qualified adviser.
- A scenario without a decision date is a worry, not a plan.
- Every number comes from your own records; Claude does the arithmetic and you set the dates.

## Next
Run start-floor-rate (Floor Rate Calculator) to turn the monthly cost into the lowest day price you can accept.

## About the makers

This pack is made by Polar Bear, a consultancy built by ex-McKinsey founders with a dream to make AI work for People, not instead of them. We help our clients build people systems and AI-first ways of working, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
