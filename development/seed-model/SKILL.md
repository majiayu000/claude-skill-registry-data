---
name: seed-model
description: >-
  Financial Modeler. Builds the 36-month financial model behind your raise:
  customers, orders, GMV, revenue (GMV x your take rate), contribution,
  payroll, marketing (new customers x CAC), opex, net and cash, month by
  month, then the numbers investors ask for: runway, the breakeven month,
  peak burn, revenue for years 1 to 3, and the unit economics (contribution
  per order, CAC payback, LTV:CAC). Checks that the use of funds adds up to
  the raise and exports a CSV. Reads seed/assumptions.json, writes
  seed/model.json for the business plan, the deck and the pitch coach. Use
  when the user says "build my financial model", "how long will the money
  last", "what's my runway", "when do we break even", "3-year projections",
  "use of funds", "how much should I raise", "unit economics", "burn rate",
  or before /seed-plan and /seed-deck.
argument-hint: "[run | funds | csv] [--write]"
---

# seed-model

The Financial Modeler turns a handful of assumptions into the 36 months an
investor will ask about. You say what a walk (or an order, or a seat) costs,
how much of it you keep, how many customers you win and lose, who you hire
and when, and how much you are raising. It does the arithmetic, every month,
to the cent, and tells you when the money runs out, when the business pays
for itself and what each customer is worth. Every number traces back to an
assumption you can change and defend. It is a plan, not a forecast: the
model is only as honest as its inputs.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/model.py" init                # seed/assumptions.json from the example
python3 "${CLAUDE_SKILL_DIR}/model.py" run                 # the summary, nothing written
python3 "${CLAUDE_SKILL_DIR}/model.py" run --write         # also writes seed/model.json
python3 "${CLAUDE_SKILL_DIR}/model.py" run --months        # every month in a table
python3 "${CLAUDE_SKILL_DIR}/model.py" funds               # the use of funds against the raise
python3 "${CLAUDE_SKILL_DIR}/model.py" csv                 # seed/model.csv for a spreadsheet
```

Other flags: `--dir PATH` (default `./seed`), `--assumptions PATH`, `--json`,
`csv --out -` to print the CSV.

## What it reads and writes

| file | what |
| --- | --- |
| `assumptions.example.json` (this folder) | the Leashly example `init` copies: every field filled in |
| `seed/assumptions.json` | your assumptions: price, take rate, cost per order, customers, CAC, churn, payroll, opex, one-off costs, the raise, the use of funds |
| `seed/model.json` | with `run --write`: the assumptions, 36 monthly rows, the summary and the unit economics. seed-plan, seed-deck and seed-coach read it |
| `seed/model.csv` | with `csv`: the 36 rows, one column per line item |

## The assumptions

| field | what it means |
| --- | --- |
| `price` | what a customer pays for one unit (a $25 walk) |
| `take_rate_pct` | the share of that price you keep (15 means 15%) |
| `cost_per_order` | what one unit costs you: `pct_of_price` and/or `fixed`, like card fees (2.9% + $0.30) |
| `customers` | `starting`, `new_month_1`, `new_growth_pct` (one monthly rate a year), `churn_monthly_pct`, `orders_per_customer_month` |
| `cac` | what it costs to win one new customer; marketing = new customers x CAC |
| `payroll`, `payroll_overhead_pct` | each role's monthly pay and start month; overhead covers payroll taxes and benefits |
| `opex`, `one_off` | monthly costs (software, insurance) and one-time costs in a given month (a city launch) |
| `raise`, `raise_month`, `cash_at_start` | the round, the month it lands, cash before it |
| `use_of_funds` | `{what: amount}`, adding up to the raise |

## The method

Each month: customers = last month's minus churn plus the new ones. Orders =
customers x orders a month. GMV = orders x price. Revenue = GMV x take rate.
Gross profit (the contribution) = revenue minus the per-order costs. Opex =
payroll with overhead + marketing + monthly opex + any one-off cost. Net =
gross profit minus opex. Cash = last month's cash + net (+ the raise when it
lands). Customers and orders round half up to whole numbers; money is exact
to the cent.

- **Breakeven month**: the first month with net at or above $0 that every
  later month keeps. A single good month does not count.
- **Peak burn**: the biggest monthly loss, and the month it happens.
- **Runway**: the months the cash covers before it first goes below $0. If
  it never does in 36 months, the summary says the cash lasts all 36.
- **Unit economics**: revenue per order = price x take rate. Contribution
  per order = that minus the costs of one order. CAC payback = CAC /
  (contribution per order x orders a month). LTV = monthly contribution per
  customer / monthly churn. LTV:CAC = LTV / CAC.
- **Use of funds**: must add up to the raise to the cent, or `funds` exits 1
  and says by how much it is short or over.

## Steps

1. If `seed/assumptions.json` does not exist, run `model.py init` and walk
   the founder through every field in plain words. Replace the Leashly
   numbers; never keep an example number the founder did not confirm.
2. Ask where each number comes from (a pilot, a quote, a competitor's public
   price). Note the source next to it in the chat. Guesses are fine if they
   are called guesses.
3. Run `model.py run`. Read back the yearly table, the unit economics,
   breakeven, peak burn and runway.
4. If the cash runs out before breakeven, say so plainly and show the two
   levers: raise more, or cut the plan (slower hiring, lower CAC). Never
   tweak an assumption on your own to make the picture prettier.
5. Run `model.py funds` until the use of funds adds up to the raise.
6. Run `model.py run --write`, then `model.py csv` if they want a
   spreadsheet.
7. Hand off to `/seed-plan` (it pulls these numbers into the business plan),
   then `/seed-deck`. `/seed-coach` will ask about every number here.

## Example: the reel

Leashly (fictional): $25 flat walks, a 15% take rate, card processing 2.9% +
$0.30 and a $0.50 backup-walker standby fee per walk, 210 pilot owners, 150
new owners in month 1 growing 10% a month in year 1, 7% monthly churn, 8
walks per owner a month, a $60 CAC, a $1.5M seed landing in month 1 (Jan
2027). `model.py run`:

```
Leashly: 36-month model, Jan 2027 to Dec 2029 (USD)
                             Year 1         Year 2         Year 3
  Walks                     124,640        423,104        798,272
  GMV                    $3,116,000    $10,577,600    $19,956,800
  Revenue                  $467,400     $1,586,640     $2,993,520
  Gross profit             $277,324       $941,406     $1,776,155
  Opex                     $957,800     $1,467,120     $1,679,880
  Net                     -$680,476      -$525,714        $96,275
  Cash at year end         $819,524       $293,810       $390,086
  Customers (end)             2,490          6,200          9,999

  Per walk           price $25.00, you keep $3.75 (15%), costs $1.53, contribution $2.23
  Per customer       LTV $254.29 on a $60.00 CAC: LTV:CAC 4.24x, CAC paid back in 3.37 months
  Breakeven          month 29 (May 2029), and every month after it
  Peak burn          $82,801 in month 5 (May 2027)
  Runway             the cash lasts all 36 months (low point $252,553 in month 28)
  Use of funds       adds up to the $1,500,000 raise
```

Peak burn lands in month 5 because the second city's $25,000 launch cost
hits that month. The use of funds: product and engineering $600,000 (40%),
city launches $450,000 (30%), marketing $300,000 (20%), operations and
insurance $150,000 (10%).

## Rules

- Every number comes from `seed/assumptions.json`. Nothing is looked up or
  invented by the tool.
- Projections from your own assumptions, not a forecast and not a promise of
  funding. Not investment advice.
- Show the bad months as clearly as the good ones: burn, the low point, a
  runway that ends.
- Never change an assumption to hit a target without saying so and getting
  the founder's yes.
