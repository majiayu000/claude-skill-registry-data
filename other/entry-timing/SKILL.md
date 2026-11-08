---
name: entry-timing
description: >-
  Analyze a stock for entry timing — "when should I buy X", "is now a good time",
  "what's actually driving X", "analyze X for entry/a position". Pulls live price and
  financials, separates the fundamental thesis from technical/supply factors (M&A share
  overhangs, lock-up expiries, secondary offerings, PE-sponsor distribution, index flows,
  rate/rotation pressure), maps the catalyst, earnings and seasonality calendar, locates
  the name in its 52-week cycle and on the recognized-vs-unrecognized spectrum,
  underwrites the financials and the people, and returns a concrete, tranched,
  date-stamped buy plan sized as a percent of the book. For a self-directed active
  sleeve, not a diversified retirement core.
---

# Entry-timing teardown

Goal: say **whether and when to buy a name**, grounded in live data and the underlying
financials, delivered as an honest broker — not a cheerleader. Lead with the financials
and the *driver of price action* before any buy call. Be willing to say "don't buy" or
"not yet".

Before starting, read the investor's own rules if they exist (a journal with a firewall,
position caps, whether they use stops, their edge). The edge this method is built for is
being *early* on structural theses: size at entry, don't chase once it's consensus.

## The 6 passes

1. **Live snapshot.** Current price; position in the 52-week range; % moves (1w / 1m /
   YTD / vs all-time high); valuation (forward P/E, EV/EBITDA, FCF yield) vs its own
   history and peers. Don't work from memory; pull it live.

2. **Diagnose what's *actually* driving the recent move.** Separate two things that look
   identical on a chart:
   - **Fundamental thesis** — demand, contracts, guidance, margins.
   - **Technical / mechanical** — what distorts price independent of the business:
     **M&A stock issued to sellers** (e.g. a utility's acquisition paid partly in ~50M
     shares on a staged 18-month lock-up, with sponsors distributing via block sales that
     cap the stock), **lock-up expiries**, **secondary offerings**, **PE-sponsor
     distribution schedules**, **index add/drop flows**, **rate sensitivity**, **sector
     rotation**.
   - The tell that it's *technical*: the stock falls on good news. A **clean float with
     no overhang** (e.g. a clean spin-off with no lock-up) means the price is "real" — no
     mechanical entry to wait for.
   - **The absence of an overhang is a finding, not a non-finding — and it argues for
     SMALLER size.** Always search for one explicitly and state which case you're in:
     - **Overhang present** -> the gap closes on a *date*, whether or not anyone changes
       their mind (e.g. a second lock-up tranche releasing on a known date, a secondary
       already cleared above the current price). A beat nobody rewarded is then holdable,
       because "why won't it move" has a mechanical answer.
     - **No overhang** -> the de-rate is *narrative*, so the re-rate needs the market to
       genuinely revise a belief. Slower, less certain, no forcing date. A company that is
       a net *buyer* of its own stock with a shrinking share count can still be a
       good business at a real discount — but **size it as a starter and say so.**
     - Check the buyback/share-count direction while you're here: a shrinking share count
       means the mechanical flow is a bid, not an offer.

3. **Map the catalyst calendar.** Earnings date (binary for rich momentum names — never
   initiate the day before at a high multiple); regulatory decisions; policy/legislative
   events; **seasonality tested with actual data, not eyeballs** (`price_history.py`) —
   flag small samples and data-mining, and check whether a "seasonal" is really a
   recurring *catalyst* (e.g. a sector's "August" that is policy-news clustering, not a
   calendar law). Identify the dated trigger the entry hangs on.

4. **Locate on the recognition spectrum — FOUR ORDERED TESTS, all must clear.** Usually
   the crux of the buy/no-buy call. Run `recognition.py` first; it measures R1-R3.

   | # | test | fails when | example kill |
   |---|---|---|---|
   | **R1 — is there a crowd?** | **>= 4 covering SELL-SIDE brokers** with live targets. **Quant/model services (Zacks, Weiss, CO FORECST, CFRA) are excluded from every count.** | < 4 -> **UNCOVERED**: no crowd whose mind can change | a name with 2 brokers whose last opinions were 20 and 37 months old |
   | **R2 — is the crowd falsifiable?** | **>= 1 sell-side SELL.** | 0 sells -> **CONSENSUS**: no bear to convert | names rated 20/4/0 and 21/3/0 |
   | **R3 — has the crowd ALREADY turned?** | consensus target **<= ~10% off its own trough**, OR **>= 20% upside** left | already re-rated -> **MID-FLIGHT** | a target +42% off its trough with only +6.7% upside left |
   | **R4 — is the crowd WRONG?** | **forward EPS must EXCEED trailing, AND forward P/E must be BELOW trailing P/E** | the multiple *rises* going forward -> "cheap" was a trailing artifact | fwd P/E 17.6 vs trailing 11.6 with EPS guided -36% |

   **R4 is the load-bearing test and it is deliberately NOT automated.** R1-R3 describe the
   *shape of opinion*; **only R4 asks whether the opinion is RIGHT.** Without it the
   framework walks into a falling knife: the one name in 86 where the crowd had not
   turned (0 Buy / 7 Hold / 2 Sell, target still falling) was a kill. **The crowd had not
   turned because the crowd was right** — a value screen with no wrong belief to arbitrage.

   **R4 needs a second feed and a guidance check.** Take forward EPS from a second source
   (e.g. your broker's quote API — E*TRADE `/v1/market/quote/<SYM>?detailFlag=ALL` ->
   `estEarnings`), then **verify it against CURRENT company guidance**: a consensus figure
   that predates a guidance cut inverts the test.

5. **Underwrite the financials before advising.** Revenue growth and quality (organic vs
   acquisition vs cannibalization), gross/operating margins, **FCF and GAAP net income**
   (is "adjusted EBITDA" masking a net loss?), balance sheet (net debt, cash),
   **share-count trend** (serial dilution?). Real business vs story stock. Pull figures
   with `sec-financials`.

5b. **Underwrite the PEOPLE — run `leadership-teardown`.** Who runs this, what have they
   said in public, how did they leave their last job, and — if the company is splitting,
   merging or reorganising — **where did the operating talent go?** **This pass can
   downgrade or explain, but it can NEVER promote a name that failed pass 1 or pass 4**:
   a great new CEO does not fix 80x forward with zero sell ratings.

6. **The buy plan — concrete and honest.**
   - A specific answer: **buy now / wait for <dated trigger> / don't add.** Pick real dates
     (overhang-clear estimate, earnings date, catalyst window).
   - **Scale in** in 2-3 tranches. If no stops are used, size is the only risk control. A
     starter answers FOMO; the reserve respects buying ahead of a catalyst.
   - **Write every tranche as a PERCENT OF BOOK plus a dollar figure — never as a share
     count.** A share count silently inflates the position if the price rises between plan
     and fill (a plan written as "37 shares = 5% of book" at $216 is 5.23% at a $226.74
     fill, overrunning the next tranche's earmark). State the target percent and recompute
     shares at the price on the day the order is placed.
   - **Give every tranche a gate that is a condition, not a date alone** — a price ceiling
     with its valuation logic ("<= $227 = 19.5x fwd; above that you're paying a premium
     multiple for a *de-rating* story, which is self-contradictory"), or a named print. A
     gate whose *why* is written down survives being tested; a bare number gets
     rationalized around.
   - **Sizing inside a firewall** — speculative single-name bets live in the active sleeve
     only, sized like money you can watch go to zero; the retirement core stays diversified.
   - **Honest-broker delivery** — distinguish thesis from price; push back plainly if it's
     FOMO/chasing; recommend against low-value adds. Make a framework point **once**, then
     advise forward; don't turn past losses into a recurring scold.

## Tooling (bundled)

- **Live quotes / news / analyst targets / deal terms:** web search. Verify suspicious
  prints (a "crash" with no news is usually bad data).
- **Price history & seasonality:** `python price_history.py <TICKER>` — ~10y of daily bars
  from `api.nasdaq.com`, no key, browser User-Agent; prints trailing windows and
  month-by-month seasonality. **Dead sources, don't retry:** the Yahoo chart API hard-429s,
  Stooq sits behind a JavaScript proof-of-work wall. Fallback for live quotes only:
  `quote.cnbc.com/quote-html-webservice/restQuote/...`.
- **Recognition distribution AND its derivative:** `recognition.py` — R1-R3 automated.
  ```bash
  pip install requests
  python recognition.py DKS --series --brokers      # one name, full history
  python recognition.py @tickers.txt --csv out.csv  # a list
  ```
  Source: `api.nasdaq.com/api/analyst/<T>/targetprice`, which returns
  **`historicalConsensus`, a ~13-month MONTHLY series of {buy, hold, sell, consensus
  target}.** The 0-sells test is a SNAPSHOT; the series gives the **derivative** — whether
  the crowd has ALREADY changed its mind. **`y` in that series is the consensus TARGET, not
  the stock price**; the tool re-proves this at runtime and refuses to score if it fails.
- **Market-implied macro:** `python kalshi_macro.py fed cpi` — Kalshi's public contracts
  give a *distribution* for the Fed path, CPI, payrolls, unemployment and recession
  timing, so "the market says a cut" becomes "73% hold, 25% hike." **Read it, never trade
  it**: the fee is 7%·p·(1-p), and benchmarks of LLMs trading real order books mostly lose
  money. Where it disagrees with CME fed funds futures, the gap itself is worth explaining.
- **Seasonality is ~10 observations per month.** Report `n`, mean, median AND win-rate, and
  say plainly that small-n is data-mining. Check whether a lopsided month is just the
  name's beta to a market-wide seasonal. Never let a seasonal override a thesis; at most
  it is a pre-commitment device ("red in this month is expected, not information").
- **Sector context first:** `sector-acceleration`. **Positions:** `etrade-pull`.

## Output shape

Snapshot -> what's driving the move (thesis vs technical) -> catalyst/earnings/seasonality
calendar -> recognized-or-not -> financials -> people -> **dated, tranched buy plan with a
clear recommendation.** End with the single most important date or trigger to watch.

Not investment advice; a research method.
