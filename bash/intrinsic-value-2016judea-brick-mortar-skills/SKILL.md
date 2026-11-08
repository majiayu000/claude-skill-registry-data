---
name: intrinsic-value
description: >-
  Compute what a business is worth as a business — owner earnings, return on
  tangible capital, a reverse DCF, and a margin-of-safety ladder — then rank a set
  of names against each other. Use for "what's it actually worth", "value this
  like Buffett", "is it cheap", "intrinsic value", "margin of safety", "screen
  these names", or when a position needs a floor under it because the trade thesis
  might fail. This is the arithmetic half of `buffett-checklist`, which owns the
  qualitative filters and the temperament rules.
---

# Intrinsic value — the arithmetic

> **Setup.** The scripts sit beside this file. Run them from a working folder that
> holds your `.env` (E*TRADE consumer key/secret) and a `data/` directory; install
> deps with `pip install -r requirements.txt` where one is included. Part of a set:
> `etrade-pull`, `order-check`, `portfolio-review`, `realized-pnl`, `rebalance-plan`,
> `price-history`, `trade-journal`, `intrinsic-value`, `sec-financials`, `buffett-checklist`.

**The theology is: simplify everything.** Buffett has never published a DCF. He
capitalises owner earnings against the long bond and then demands a margin of
safety instead of inventing a risk premium. If the answer needs a nine-tab model
to hold, the answer is *"too hard"* — a legitimate verdict and often the right one.

Deliver **one number and the one relationship that produces it.**

```bash
python3 owner_earnings.py CTVA --price 82.81 --bond 5.19    # one name, full ladder
python3 compare.py --bond 5.19 RMD=232.45 KO=91.99 ...      # rank a set
```

`owner_earnings.py` prints owner earnings by year, return on capital, what the
market is asking, three value anchors, a margin-of-safety ladder, a **reverse
DCF** and a sensitivity grid. `compare.py` ranks a set on the expectations gap.
Both take every input from `sec-financials` — nothing is typed by hand.

## Owner earnings

Buffett, 1986 Berkshire letter, Appendix:

> reported earnings **+** depreciation, depletion, amortisation and other non-cash
> charges **−** the average annual **maintenance** capex (**−** additional working
> capital where the business needs it)

He adds that this is *"the relevant item for valuation purposes"* and *"does not
lend itself to the precision of GAAP"* — approximately right beats precisely wrong.

## The rules — each one earned by a name that broke the model

**1. CALIBRATE BEFORE DELIVERING A VERDICT. Non-negotiable.**
Run the identical model on a business Buffett actually owns before saying a word
about the target. Run on Corteva it returned 92% overvalued — and on **Coca-Cola,
116% overvalued**, against 40.7% ROE and a 72% return on tangible capital. The
verdict was never about Corteva; it was a 10% hurdle applied against a 5.19% long
bond, which calls the entire market overvalued. **An uncalibrated intrinsic-value
model is a permanent bear wearing a spreadsheet.** Never deliver the absolute
number alone.

**2. Never value on EBITDA. Convert it, and state the ratio.**
Munger: *"every time you see the word EBITDA, substitute the words 'bullshit
earnings.'"* Corteva's owner earnings are **44% of its operating EBITDA**, so a
13x EBITDA bid that sounds cheap is **29x owner earnings**. That one ratio has
explained the whole bull/bear gap every time.

**3. The reverse DCF is the deliverable; the DCF is scaffolding.**
Nobody can adjudicate your growth assumption. Invert it: *at an 8% required
return, what growth does today's price require?* Corteva answered **+9.2%/yr for
ten years** from a business whose owner earnings had fallen **8.5%/yr for four**.
That is a fact about the price, not an opinion about the company.

**4. Pick the base by testing the series — this is the easiest way to be badly wrong.**
Averaging five years is right for a **cyclical**, whose good years fund its bad
ones. It is wrong for a **compounder** (it averages in years the company has
permanently outgrown) and wrong for a **spin-off** (it averages in carve-out
losses belonging to the former parent). Un-fixed, this made NVIDIA look like it
needed 25% growth and Constellation 28% — both artefacts. `choose_base()` tests
monotonicity and *says which basis it used*; read that line every time.

**5. Owner earnings must track the cash. If they don't, refuse.**
A large positive owner-earnings figure against weak or negative free cash flow
means the D&A add-back is carrying a **goodwill impairment**, not depreciation —
and adding back a write-off of money already lost values a melting business at a
premium. FMC screened at a **57% owner-earnings yield on a −108% ROE**; Kraft
Heinz at 7.3% on −14%. Both were impairments. The guard is
`owner earnings ÷ free cash flow > 1.6 → REFUSE`.

**6. "Too hard" is a valid output — Munger keeps three baskets: in, out, and too hard.**
Fewer than three positive owner-earnings years in five is not a cheap stock, it
is an absence of the thing being valued; averaging the winners is data-mining.
Loss-making in the latest year is an automatic refusal. So is a business the
formula does not fit: **banks, insurers and GSEs have no meaningful capex or D&A**
— value those on book value and ROE, not here.

**7. Never extrapolate a delivered CAGR above ~30%,** and check it against
**forward guidance**, not just history. The expectations gap compares the growth
a price requires to the growth a business *has* delivered — which silently
assumes the past is the right comparator. It is not, once a business inflects.
Lululemon screened as the cheapest name on the board (implied −3.2% vs delivered
+14.7%) **while management guided EPS down 16% and gross margin fell 550bps.**
Cheapness does not save a declining business. **Before acting on any negative gap,
read the latest guidance and the gross-margin direction.** That is where filter 2
lives.

**8. Split D&A before adding it back.** Depreciation ≈ maintenance capex and is a
**real** cost. Amortisation of *acquired* intangibles is a non-cash residue of a
past purchase price. Add it back **only when the company separately expenses the
R&D that renews the asset** — Corteva expenses $1.47B/yr of R&D while amortising
$644M of 2017-vintage intangibles, so the add-back is correct, not generous.
Where the asset is *not* separately funded, adding it back is how you talk
yourself into a melting asset.

**9. "One-time" charged every year is opex.** Corteva booked restructuring in
four consecutive years. Adjusted figures excluding a recurring charge are not
adjusted, they are wrong.

**10. Return on TANGIBLE capital is Munger's first question, and the spread is
the story.** Corteva earns **31.7% on tangible capital and 4.5% on accounting
equity.** That gap is not noise — it *is* the price a previous buyer paid, parked
in goodwill and intangibles. Excellent business, bought dearly by someone else.
Watch for a near-zero tangible denominator making the ratio meaningless.

**11. Capex ≫ D&A means owner earnings are understated,** because the excess is
growth capex, which belongs to the owner. Capex ≪ D&A on a capital-intensive
business means the opposite — it is under-investing and the bill is deferred.

**12. Holding is not buying.** Buffett's Coca-Cola basis is ~$3.25; he is not
buying at $92. "Buffett owns it" is never evidence a price is sensible. State
which question is on the table: *initiate*, *add*, or *hold*.

**13. A verdict here does not govern a trade with a date on it.** This framework
has nothing to say about a three-week holding period. Do not let an
intrinsic-value number override a pre-committed dated plan — see
`trade-journal`, whose gates were written before conviction was tested.
What this framework uniquely supplies is **the price of the fallback**: "if the
trade fails I'll hold it long term" is only available when intrinsic value is
*near* the price. When it is half the price, that exit does not exist and the
written stop is the only floor. Say so — it is the most useful sentence this
skill produces.

**14. A stale valuation gate must be RE-BASED, not obeyed or ignored.** A ceiling
written as "19.5x forward = $227" is a *multiple* gate wearing a price tag. When
the fiscal year rolls and new guidance lands, recompute it — 19.5x FY2027
guidance of $12.00–12.25 is $234.00–$236.44, so a $232.45 price that looks like a
breach is actually inside the gate. Show the arithmetic; never silently drop a
gate you wrote.

## Output shape

Four filters (stop at the first fail, see `buffett-checklist`) → owner
earnings and how they were built → return on capital → **what the market is
asking, in owner-earnings terms** → reverse DCF → calibration against a Buffett
holding → one-line verdict naming *initiate / add / hold*, with the fallback
price stated. Lead with the number; keep the chain loaded for "why".

## Related

`sec-financials` supplies every figure. `buffett-checklist` owns the
qualitative filters, management read and temperament rules — run it alongside,
not instead. `price-history` locates a name in its own cycle.
`trade-journal` holds the written invalidation this must be checked against.
