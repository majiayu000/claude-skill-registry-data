---
name: comp-quota-plan
description: Turn "what should we pay reps and what number do we give them" into a defensible comp and quota plan. Reconciles a top-down number against a bottom-up build, sets the OTE mix, lays out accelerators, and names the behaviors the plan will drive and the ones it will break. Built for B2B sales leaders, customizable to your motion and your segments. Trigger on "design the comp plan", "set quotas", "what OTE should I pay", "reconcile top-down and bottom-up", "what will this plan actually incentivize", or any comp or quota build.
---

# Comp and Quota Planner

## What this does
Takes your revenue target and turns it into a comp and quota plan a rep can trust and a CFO can sign. It builds the number two ways, top-down from the goal and bottom-up from rep capacity, then reconciles the gap. It sets base-to-variable mix, designs the accelerator curve, and flags the behaviors the plan will actually drive, including the ones you did not intend.

## What you'll need
You do not need to connect anything to get value today. Bring your target and your headcount and the skill runs now. Connect the tools below and it pulls the history that makes every assumption real instead of guessed.

- Works today with: your revenue target for the period, current or planned rep count, average deal size, and a rough win rate. Paste it or upload a sheet.
- More powerful connected to a CRM: it reads real win rates, deal sizes, and cycle lengths per segment instead of a single blended guess.
- Sharper with a comp or payroll system: it checks your proposed OTE against what you already pay and where the plan drifts.
- Sharper with a data warehouse: it splits productivity by segment and tenure so the quota is not one flat line.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the numbers you give it today and gets more powerful as you connect tools. It never invents a rate it cannot see. A missing input is a prompt, not a guess.

- **Bring your data**: paste your target, headcount, deal size, and win rate. The skill runs the full build today on your real numbers. No connection required.
- **Connect your tools**: the same skill pulls historical productivity, deal sizes, and pay data automatically, so the assumptions are measured, not assumed.
- **Just exploring**: no data yet? Get the framework, the exact inputs it reads, and a worked example on sample numbers, so you can see the shape before you feed it.

Every run ends with the one input that would make the next build sharper, a segment split to add or a system to connect.

## Customize this for yourself
This was built for a B2B SaaS org with a quota-carrying sales team. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| SEGMENTS | how you split the team | SMB, Mid-Market, Enterprise |
| TARGET | the number the plan has to fund | new ARR for the period |
| OTE | on-target earnings per role | role and segment specific |
| MIX | base-to-variable split | 50/50 field, 60/40 for shorter cycles |
| QUOTA_MULTIPLE | quota over OTE coverage ratio | 4x to 6x of variable |
| RAMP | months to full productivity | 3 to 9 by segment |
| ACCELERATOR | rate above 100 percent attainment | 1.5x to 2x on the marginal dollar |
| COVERAGE | total quota over target | 1.15 to 1.25 for overassignment |

Run any philosophy you like. The skill reconciles the number and shows the behavior it drives, so point it at your motion, not anyone else's.

## The method

### The quota build (top-down vs bottom-up, reconciled)
Build the number twice. Top-down: take TARGET, apply COVERAGE, divide across SEGMENTS and heads. Bottom-up: take ramped productivity per rep, multiply by heads, subtract ramp drag for new hires. Then show the gap between the two. If bottom-up capacity falls short of the top-down ask, the plan is already broken and the fix is heads, ramp, or target, not a bigger quota on the same people.

### The OTE mix
Set base-to-variable by how much of the outcome the rep controls. Shorter cycles and higher volume lean more variable. Longer, committee-driven enterprise deals lean more base. Show OTE against MIX per role, and check total comp cost as a percent of the target it funds.

### The accelerators
Design the curve above 100 percent. A flat rate past target pays for luck the same as effort. An accelerator on the marginal dollar past quota pays for the overperformance you actually want. Show the decelerator or cliff too, if any, and where a rep stops being paid to keep selling.

### Behaviors it drives (and breaks)
Every plan is a set of instructions. Name them. A rate that pays the same on a discounted deal tells reps to discount. A quota with no new-logo split tells them to farm the base. A cliff at quota tells them to sandbag into next period. For each lever, state the behavior it rewards and the one it quietly punishes.

## Quality gates
- No plan ships without the top-down and bottom-up numbers shown side by side and the gap named.
- Comp cost is stated as a percent of the target it funds, never a raw OTE in isolation.
- Every accelerator is paired with the behavior it drives, in plain words.
- Ramp drag is subtracted from new-hire capacity, never counted as a full head.

## Output (example)
```
COMP AND QUOTA PLAN · Mid-Market · illustrative
Build            Number       Note
Top-down ask     $12.0M       target $10M x 1.2 coverage
Bottom-up cap    $10.4M       8 ramped + 4 ramping reps
Gap              -$1.6M       coverage unfunded by ~1.5 heads

OTE / mix        $160K @ 50/50     quota $800K (5x variable)
Accelerator      1.8x past 100%    no cliff, decel at 150%

Behavior watch:
  1. Flat rate on discounts. Add a margin gate or reps will trade price for speed.
  2. No new-logo split. Quota is met by expansion alone. Add a logo floor.
  3. Coverage exceeds capacity by 1.5 heads. Hire, cut coverage, or reset target.
```

## Where the numbers come from
QUOTA_MULTIPLE (4x to 6x), COVERAGE (1.15 to 1.25), and the accelerator (1.5x to 2x) are defaults, not laws. They suited a mid-market SaaS motion. If your deals run longer or your win rate is higher, move them. The reconciliation logic does not change. The thresholds are yours.

## Example chat
Here is the skill running on a real mid-market plan build.

**You:** We need $10M in new ARR from mid-market next year, 8 ramped reps plus 4 new hires. Build the comp and quota plan.

**Claude:** Built both ways, and they don't agree.
```
Top-down ask     $12.0M   target $10M x 1.2 coverage
Bottom-up cap    $10.4M   8 ramped + 4 ramping reps
Gap              -$1.6M   coverage unfunded by ~1.5 heads
```
The plan as scoped is already short by about a head and a half of capacity, that gap shows up before you've even set OTE. Shipping the top-down number as-is would mean asking existing reps to cover work that isn't theirs to cover. One sharpener: connect your CRM so productivity per rep is measured from real deal history instead of a blended team-wide guess.

**You:** Given the gap, what should the accelerator curve look like so we don't quietly reward the wrong thing?

**Claude:** Set at 1.8x on the marginal dollar past 100%, no cliff, decelerating at 150%.
```
Behavior watch:
1. Flat rate on discounts. Add a margin gate or reps trade price for speed.
2. No new-logo split. Quota met by expansion alone. Add a logo floor.
```
The accelerator itself is fine, the real risk is the flat rate on discounted deals, which quietly tells reps to win on price instead of holding it. One sharpener: pull real discount data from closed-won deals so the margin gate threshold is set from what actually happened, not a guess.

## Go further
The read is step one. Here's where an operator takes it once the manual version proves out.

- **Reconcile the plan every planning cycle, not once a year.** Point a scheduled Claude task at Salesforce quarterly and re-run the top-down vs bottom-up check as headcount and productivity shift.
- **Wire the accelerator into payroll directly.** Connect your comp or payroll system so attainment tiers calculate and flow through without a manual spreadsheet reconciliation.
- **Watch for the behavior the plan is quietly rewarding.** Feed closed-won discount data into Snowflake monthly and alert if margin erosion tracks with a specific rep or segment.

You built the read once; now it runs itself.


## Make it yours
Fork it. Change the segments, the mix, the curve. The point is not to run someone else's comp philosophy. It is to build yours, with the top-down and bottom-up actually reconciled. Built by an operator. Customize it, break it, make it better.
