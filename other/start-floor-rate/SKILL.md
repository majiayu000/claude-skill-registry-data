---
name: start-floor-rate
description: Calculates your floor rate from your own records, with the fully loaded monthly cost, your real billable days after selling and admin time, the floor per day and per hour, and what moves the floor most, marked internal. Use for "run start-floor-rate", "what is my minimum day rate", "what should my day rate be", "what do I charge", "turn my old salary into a day rate", "lowest price I can quote", "work out my break-even rate", part of the Claude Guide for New Founders Pack by Polar Bear.
---

# Floor Rate Calculator

## When To Use
Your only reference for a price is your old salary, and the first person has asked what you charge. Dividing a salary by working days gives a number that ignores every day you will now spend selling, invoicing and waiting. Use this before you quote anything, so the price sits on a floor worked out from your own costs and your own calendar.

## When Not To Use
If you do not know your monthly costs yet, run First-Year Runway Plan first; this takes its burn figure. If you want the price of one offer, this floor is an input to Productized Service Offer, not the price itself.

## Inputs
- Your monthly costs from the runway plan or your statements, the pay you need to take, and the set-asides you named
- Your working days per month, and your honest guess at non-billable days: selling, admin, learning, leave
- The billable hours in a delivery day, as you set them
If you have none of this, I start from your statement exports and your own estimates, and mark the output as a first draft.

## Approach
This is break-even analysis as the US Small Business Administration sets it out: fixed costs divided by price minus variable cost per unit gives the units you must sell. Here the unit is one delivery day, and the floor is the day price at which the days you need equal the days you can really bill. The judgement sits in the non-billable time, and a new founder has no history to read it from. In the first months, selling takes a large part of the week, so that line is your estimate, said out loud and revisited. The failure it prevents: a rate that looked generous against the salary and loses money a few months in.

## Workflow
1. Ask at most three questions: what monthly pay you need to take, how many days a week you expect to spend finding work in the first six months, and whether your set-asides are inside the costs you gave.
2. Build the fully loaded monthly cost: every business cost, plus the pay you need, plus set-asides. Each line carries its source or the word "estimate".
3. Work out real billable days per month: working days you set, minus selling, admin, learning and leave. With no calendar history, this is your estimate; I say plainly that the floor is only as true as this line.
4. Calculate with the arithmetic shown. Floor per day = fully loaded monthly cost / real billable days. Floor per hour = floor per day / billable hours per day. Break-even check: at the floor, the days you need each month equal the days you can bill.
5. Show what moves the floor most: change each input by an amount you set (one more billable day, one cost removed, a different pay figure) and show the new floor beside the old.
6. Mark the floor internal. It is the number you do not go below, never the number you quote, and it never appears on a proposal. If you ask what the market charges, I say I do not know and bring you back to this sheet.
7. Produce the sheet as a table or a spreadsheet through file creation. With memory on, the floor can sit under a Topic so later skills start from it.

## Output Format
```markdown
# Floor Rate Sheet
Prepared: [date] | INTERNAL, never shown to a client | Review after: [date, once real weeks exist]
## Fully loaded monthly cost
| Cost line | Monthly amount | Source | Estimate? |
|---|---|---|---|
| [cost line] | [amount] | [statement, runway plan] | [yes / no] |
| Pay I need and set-asides | [amount] | set by me | no |
| **Total** | [amount] | | |
## Real billable days and floor
| Working days | Selling, admin, leave | Real billable days | Floor per day | Hours per day | Floor per hour |
|---|---|---|---|---|---|
| [days] | [days, estimate] | [days] | [amount] | [hours] | [amount] |
## What moves the floor most
| Input changed | Change I set | New floor per day |
|---|---|---|
| [input] | [change] | [amount] |
## Decision
[Your name] confirms the floor per day of [amount] by [date] and sets the date to redo the sheet with real weeks.
```

## Done When
- Every figure has a source from your records or is marked "estimate".
- Non-billable days are stated, not hidden inside "working days".
- The sensitivity table shows at least three inputs changed by amounts you set.
- The sheet is marked internal and has a review date.

## Quality Bar
- The old salary is never divided by working days and called a rate.
- No multiplier, market rate or "typical" day rate appears anywhere.
- No example figures, not even marked as examples; empty means a bracket.
- A tax set-aside is your figure: check with a qualified adviser.
- Every figure is yours; Claude does the arithmetic and never suggests what to charge.

## Next
Run start-productized-offer (Productized Service Offer) to put a scope and a price on one piece of work.

## About the makers

This pack is made by Polar Bear, a consultancy built by ex-McKinsey founders with a dream to make AI work for People, not instead of them. We help our clients build people systems and AI-first ways of working, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
