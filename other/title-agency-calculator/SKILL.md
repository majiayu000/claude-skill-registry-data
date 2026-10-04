---
name: title-agency-calculator
description: Run a Florida closing-cost and title-agency estimate from first principles — statutory charges, agency rate cards, tax proration, seller net, buyer cash to close, concession modelling, and every cost percentage. Use when quoting or checking what a closing will cost, comparing title agencies on price, sizing a seller concession, or answering "what percentage of the sale price is this". Triggers - "what will closing cost", "estimate the closing", "title fees", "how much is the title agency", "closing costs as a percentage", "seller net", "cash to close", "what if we split closing costs", "compare title quotes on price", "prorate the taxes". For QA of a settlement statement already received, use title-closing-review. For loan documents, use real-estate-closing-check.
---

# Title Agency & Closing Cost Calculator

Computes a closing instead of reading one. Give it a price and it derives every statutory
charge, applies a recorded agency rate card, prorates the taxes, and reports the seller's net
and every cost ratio.

## When to use

- Quoting what a sale will cost before a statement exists.
- Checking a statement someone sent you against what the numbers *should* be.
- Choosing between title agencies on price.
- Sizing or capping a seller concession.
- Answering "what percentage of the sale price is that".

**Not for:** QA of a received settlement statement → `title-closing-review`. Loan documents,
Note/Mortgage/Guaranty → `real-estate-closing-check`.

## The engine

`scripts/closing_calc.py`. **Run the self-test first, every time.**

```bash
python3 scripts/closing_calc.py selftest    # must print ALL PASS
python3 scripts/closing_calc.py cards       # show every recorded rate card
```

The self-test reproduces three real closings to the penny — 8 Pine Track under both agencies
and the closed 31 Juniper file. If it does not print **ALL PASS**, a rate card or a statutory
rate has drifted. Fix that before quoting anything.

```bash
# full estimate
python3 scripts/closing_calc.py estimate \
    --price 279000 --agency marion-lake --loan 270630 --deposit 3000 \
    --close 2026-08-24 --annual-tax 290.11 --commission 4.5 \
    --basis 210474.47 --sf 1400 --notary 175

# concession as a share of the buyer's costs, with a cap
python3 scripts/closing_calc.py estimate --price 279000 --agency marion-lake \
    --loan 270630 --close 2026-08-24 --annual-tax 290.11 \
    --concession-pct 50 --concession-cap 3500

# side-by-side agency comparison, notary forced onto both cards
python3 scripts/closing_calc.py compare --price 279000 --loan 270630 \
    --close 2026-08-24 --annual-tax 290.11 --commission 4.5
```

Useful flags: `--strike-junk` (drop technology / warehousing / ID-verification / escrow-
disbursement fees), `--exact-premium` (price the owner's policy on the exact sale price rather
than rounding coverage up), `--survey`, `--noc-pages`, `--mortgage-pages`.

## The four rules this skill exists to enforce

**1 — Quote the cost ex-commission and ex-concession.** A commission is a brokerage cost and a
concession is a price adjustment; neither is a cost of closing. Folding them in inflates the
percentage and hides the real number. Report **closing costs ex-commission** as the headline,
then show commission and concession separately.

**2 — Only the title-agency bucket is shoppable.** Deed stamps, the owner's premium and
recording are fixed by Florida law or promulgated rate — identical at every agency in the
state. On a typical file ~75% of non-commission closing cost cannot be negotiated by anyone.
Comparing agencies on anything but their own fees compares noise.

**3 — Normalise before comparing.** Agencies leave different things off. One quote omits the
notary, another omits the proration; whichever is missing makes that agency look cheaper.
Force the same line items onto both cards (`--notary`) before drawing a conclusion. This flips
the answer more often than not.

**4 — Distinguish what the agency keeps from what it collects.** A fee payable to the agency
is its revenue. A fee payable to a search vendor, underwriter or Simplifile is a pass-through
you pay anywhere. `keeps` vs `passed through` in the output.

## Reading the output

| Figure | What it means |
|---|---|
| `CLOSING COSTS — EX-COMMISSION, EX-CONCESSION` | **The headline.** Benchmark 1.0%–3.0% of price in FL |
| `TITLE AGENCY TOTAL` | The only shoppable bucket. Typically 0.25%–0.40% of price |
| `the agency keeps` | The agency's actual revenue — what a discount request targets |
| `ALL-IN TITLE` | Agency fees + promulgated premium |
| `% of gross margin` | On a build-to-sell, the number that matters. Closing costs routinely eat 25%+ of margin |

The tool prints `% price`, `% basis`, `% margin` and per-square-foot. On a spec build the
margin ratio is the honest one: 1.6% of price is 6.7% of margin.

## Traps this tool is built around

- **Prepaids and escrow reserves are not modelled.** A financed buyer usually adds $3,000–
  $6,000 in prepaid interest, hazard premium and tax/insurance reserves. If a draft HUD shows
  blank 900 and 1000 series, it is incomplete. **Never agree to a percentage concession before
  seeing the buyer's Loan Estimate** — and a flat concession larger than the buyer's actual
  costs is forfeited, not refunded to the seller.
- **New-construction proration is deceptively small.** Florida assesses as of 1 January, so the
  construction year is taxed on land only. The following year picks up the house and the bill
  multiplies ~10×. Small at this closing, large for the next one.
- **A missing line is not a saving.** An omitted proration or notary will be added before
  funding. Add it yourself before comparing.
- **Cap percentage concessions in the contract.** "50% of buyer's closing costs, not to exceed
  $X" — otherwise an inflated buyer cost sheet expands the seller's exposure without limit.
- **Check the transaction type before reusing a rate card.** A multi-property loan closing
  prices nothing like a one-house sale. The loan cards are marked as such.

## Adding a rate card

Add an entry to `CARDS` in the script: `seller` and `buyer` fee dicts, `keeps` listing the
lines payable to the agency itself, `notary_quoted`, and a `context` string naming the source
document and transaction type. Then add an assertion to `selftest()` against a real statement
from that agency — a card without a self-test assertion is not trustworthy.

## Reference

`references/fl-rates-and-ratecards.md` — statutory formulas and worked examples, the recorded
rate cards with provenance, Florida benchmarks, the full 8 Pine Track closing-cost record, the
closed 31 Juniper comparable, and the open items on the live deal.
