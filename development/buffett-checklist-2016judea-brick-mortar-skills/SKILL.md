---
name: buffett-checklist
description: >-
  Apply Warren Buffett's investment framework as a discipline lens when weighing
  a buy, hold, or sell decision — circle of competence, economic moat, owner
  earnings & intrinsic value, margin of safety, management/capital-allocation
  quality, and market psychology (Mr. Market, fear vs greed, temperament). Use
  when asked to "run this through Buffett", "what would Buffett say", "does this
  pass the moat test", "is this cheap enough", or for a second, more skeptical
  read on a name being evaluated or already held. This is a discipline overlay,
  not a replacement for a strategy — it applies the Buffett lens to how someone
  actually invests, rather than issuing generic advice.
---

# Buffett checklist

A checklist for running a name through Warren Buffett's actual methodology — not
the internet-meme version ("buy what you know," "hold forever"), but how he and
Munger really filtered, valued, and sized positions, per the shareholder letters
and interviews. The canonical primary source for anything cited here is the
shareholder-letter archive at `berkshirehathaway.com`; verify against the actual
letter before quoting Buffett anywhere it matters.

**The honest tension to hold onto:** if the book you're checking is concentrated,
early-cycle and thematic — a structural macro thesis that hasn't been recognized
yet — Buffett's strike zone is close to the opposite: simple, already-proven,
wide-moat cash generators he can hold forever (Coke, Amex, See's). **Don't force
an early-thesis book to pass a strict circle-of-competence and
10-year-predictability test. Most of it won't, and that isn't automatically a
verdict.** Use the parts of Buffett's discipline that transfer regardless of
style: not overpaying, judging whether management is a good steward of capital,
and the temperament rules around not selling into fear. Flag the parts that don't
transfer rather than pretending they do.

## The filter, in order

1. **Circle of competence.** Can you explain in one paragraph, without jargon,
   exactly how this company makes money and why it'll still be making money the
   same way in 10 years? If not, it's in the "too hard" pile — that's a real
   answer, not a cop-out. Buffett's own circle expanded slowly and only with deep
   study (Apple wasn't evaluated as "tech," it was evaluated as a
   consumer-loyalty business).

2. **Economic moat.** What specifically stops a competitor from taking this
   company's margin? Buffett's four moat types: **pricing power/brand** (raise
   price, keep customers — See's Candies), **low-cost production** (Costco,
   GEICO), **switching costs** (enterprise software, banking rails), **network
   effects** (Amex). Quantitative tell: **ROIC consistently >15% over 10 years**
   and **gross margins >40%** without competitors eroding them. A moat you can't
   point to a mechanism for is a story, not a moat.

3. **Owner earnings & intrinsic value.** Buffett doesn't use EBITDA or consensus
   FCF. His formula: `Owner Earnings = Net Income + D&A − maintenance capex`
   (capex to *sustain* the current competitive position, not growth capex).
   Discount future owner earnings back at a conservative rate — historically the
   10-yr Treasury yield, bumped to a 7–10% hurdle when rates are artificially
   low, precisely so you don't fool yourself into overpaying because money is
   cheap. No CAPM, no beta — Buffett's explicit view is volatility ≠ risk.

4. **Margin of safety.** Buy meaningfully below your intrinsic-value estimate —
   historically Buffett has looked for 30–40% discounts, not 5%. *"You build a
   bridge that can carry 30,000 pounds and drive 10,000-pound trucks across it."*
   This is the check against your own projection error, not a pricing nicety —
   apply it hardest to names whose growth assumptions are most aggressive.

## Management & capital allocation

- **Integrity, intelligence, energy — in that order.** *"If they don't have the
  first, the other two will kill you."* Look for candor: do they admit mistakes
  on earnings calls, or is it always the weather / the macro / one-time items?
  Heavy reliance on adjusted-EBITDA or non-GAAP framing to paper over a GAAP loss
  is a red flag, not a nuance.
- **The $1 test.** Over a 5–10yr window, has $1 of retained earnings produced at
  least $1 of market-cap growth? Management reinvesting at mediocre returns
  instead of returning cash is value destruction dressed up as "growth."
- **Buybacks vs. dividends.** Buybacks are only value-accretive **below**
  intrinsic value — buybacks at a stretched multiple mostly offset options
  dilution and flatter EPS, and Buffett is on record hating that pattern.
  Dividends are a management's admission it has run out of high-return uses for
  cash — not inherently bad, just a tell about the growth runway.
- **Institutional imperative.** Munger and Buffett's term for management that
  imitates peers, chases acquisitions to "use up" cash, or resists changing
  course out of inertia rather than analysis. Watch for a CEO who can articulate
  *why not* as clearly as *why*.

## Red flags / the "too hard" pile

High leverage without a matching float-like funding source; convoluted financial
structure or a business model you can't explain simply; frequent management/CFO
turnover; heavy stock-based comp excluded from "adjusted" earnings; commodity
economics without being the low-cost producer; capital-intensive businesses where
profit gets plowed right back into equipment just to stay in place (steel, and —
Buffett's own cautionary tale — textiles, which is literally the original
Berkshire Hathaway). Airlines are his favorite personal example of breaking his
own rule (bought 2016, sold at a loss in the 2020 panic) — evidence that even
Buffett's framework doesn't override a genuinely bad structural business.

## Temperament

For most people running a concentrated book, this is the highest-value section,
because the documented leak is usually **exits, not picks** — cutting losers near
local bottoms. If a backtest of your own closed losing lots (see
`backtest_holding.py` in this repo) shows you'd have done better holding, that's
this section, quantified.

- **Mr. Market allegory:** the market is a manic-depressive business partner who
  quotes you a price every day. You're never obligated to trade at his price —
  his mood swings are information about *him*, not about the business, unless
  something about the business actually changed.
- **Fear vs. greed:** *"Be fearful when others are greedy, greedy when others are
  fearful."* A drawdown with no thesis-breaking news is Mr. Market having a bad
  day — the hamburger analogy: if you're still buying, falling prices should make
  you happy, not scared.
- **Temperament over IQ:** *"Investing is not a game where the guy with the 160
  IQ beats the guy with the 130 IQ... what you need is the temperament to control
  the urges that get other people into trouble."* The skill isn't spotting the
  moat — plenty of people can do that. It's sitting through a 40% drawdown on a
  name you underwrote correctly without flinching.
- **When Buffett actually does sell** (the counter-check against "hold forever"
  becoming an excuse): the moat is structurally broken (not just the stock is
  down), he concludes the original thesis was wrong (the 2020 airline exit — a
  real mistake, admitted plainly, not rationalized), or a dramatically better
  opportunity needs the capital. This maps directly onto a written
  thesis-invalidation rule per position — the Buffett version and the journal
  version are the same rule stated two ways.

## Concentration & sizing

Buffett's *"diversification is protection against ignorance — it makes little
sense if you know what you're doing"* is a defense of concentration, not of
diversification, for anyone doing real underwriting. Berkshire holds ~40 names but
the top 5 are ~70% of the equity book. The "punch card" framing (20 lifetime
swings, so make them count) and the Ted Williams happy-zone analogy (only swing at
pitches in your sweet spot) both argue for concentration around conviction.

Where Buffett's sizing discipline differs from most concentrated retail books: he
sizes only *after* the margin-of-safety test clears. If you run without stop-losses,
position size is your only risk control, which puts far more weight on the sizing
decision than his process does. Name that difference plainly rather than blurring it.

## How to actually run it

When invoked on a specific name (held or candidate):

1. State the circle-of-competence answer in plain language — or say explicitly
   "this doesn't pass, it's a thematic bet, evaluate it as one."
2. Name the moat mechanism, or say there isn't one yet. Early-cycle names often
   don't have a moat *yet* — that's the bet, be honest about it.
3. Owner-earnings / valuation check — **run `intrinsic-value`, don't estimate
   it here.** That skill owns the arithmetic (owner earnings, return on tangible
   capital, the reverse DCF, the margin-of-safety ladder) and the refusal rules
   that stop a goodwill impairment or a carve-out year from being valued as
   earnings. It also carries the calibration rule: **never deliver an absolute
   "fair value" without running the same model on a business Buffett actually
   owns** — un-calibrated, this model called Coca-Cola more overvalued than the
   name being screened. For pre-moat or early-cycle names it will refuse outright
   ("too hard"); substitute "what has to be true" and say so plainly.
4. Margin-of-safety read: is the current price already assuming the thesis plays
   out, or is there room for the thesis to be right *and* the stock to re-rate?
5. Management / capital-allocation quick read if public filings support one.
6. Temperament check — if this is a "should I sell" question during a drawdown,
   lead with Mr. Market and fear-vs-greed and the written invalidation rule
   before anything else.
7. Say plainly where Buffett's framework and the actual strategy diverge on this
   name, rather than forcing a fit.

## Tooling

Refresh or verify any specific Buffett quote, letter, or recent Berkshire move
before citing it — positions and public statements change, and this file is a
framework snapshot, not a live feed.

- The valuation arithmetic, and the data behind it: `intrinsic-value` and
  `sec-financials`. This file is the lens; those two are the numbers.
- Current positions and weights: `etrade-pull`.
- The temperament section, quantified against trades actually made:
  `realized-pnl` — its counterfactual is what turns "you cut losers too
  early" from an accusation into a number.
- Where a name sits in its own cycle, for the margin-of-safety read:
  `price-history`.
- A written invalidation to check the "when Buffett actually sells" test against:
  `trade-journal`.

Invoked as one step of `portfolio-review`, which decides when a skeptical
read is the thing that's needed.
