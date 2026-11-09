---
name: indian-market-structure
description: |
  Reference for how Indian stock markets work: NSE/BSE sessions and timings (pre-open, closing VWAP,
  post-close, block windows, Muhurat), T+1 settlement, optional T+0, product types (CNC, MIS, NRML,
  MTF), order types (limit, SL, SL-M, GTT, AMO), circuit limits and market-wide circuit breakers,
  surveillance frameworks (ASM, GSM, ESM, trade-for-trade), F&O ban and MWPL, margins and the 50%
  cash rule, DDPI/eDIS, corporate actions, and the 2026 trading-holiday calendar.

  Use when the user asks about market timings, holidays, why an order was rejected, circuits, T+1,
  BTST, auto square-off, GTT vs stop-loss orders, ASM/GSM stocks, F&O ban, margin rules, record and
  ex-dates, or any "how does the Indian market work" question. Other skills consult it for
  time-of-day and holiday checks.
---

# Indian Market Structure

Facts verified on 31 Oct 2026. Exchanges change rules by circular. When a detail matters for money,
confirm it on nseindia.com, bseindia.com, or the broker's help pages.

## Exchanges and regulator

- **NSE** (National Stock Exchange) has most cash-market volume and nearly all index-options volume (NIFTY).
- **BSE** (Bombay Stock Exchange) runs SENSEX derivatives, and many small companies list only here.
- **SEBI** is the regulator. **NSDL/CDSL** are the depositories holding your demat shares.
- **NSE IX** in GIFT City lists GIFT Nifty, a USD-denominated NIFTY future traded for nearly 21 hours.
  Indian traders use it as the overnight indicator for the next open.
- **MCX** handles commodities, which are out of scope here.

## Daily timeline (equity cash and F&O, IST)

| Time | Session | Notes |
|---|---|---|
| 08:45–09:00 | Morning block-deal window | Large negotiated trades |
| 09:00–09:08 | Pre-open order entry | Random close in the last minute. Orders can be modified or cancelled |
| 09:08–09:12 | Pre-open matching | Equilibrium (opening) price discovered by call auction |
| 09:12–09:15 | Buffer | Unmatched pre-open orders move to the normal market |
| 09:15–15:30 | Normal market | Continuous trading |
| 14:05–14:20 | Afternoon block-deal window | — |
| 15:00–15:30 | Closing-price window | NSE cash **closing price = VWAP of the last 30 minutes**, not the last trade |
| 15:40–16:00 | Post-close session | Trades only at the closing price |
| After hours | AMO | After-market orders queue for the next pre-open/open |

- F&O trades 09:15–15:30. Since 8 Dec 2025 current-month index and stock **futures** also have a 09:00–09:08 pre-open.
- **IPO listing day / relisted stocks:** special pre-open 09:00–10:00 (call auction), then normal trading from 10:00.
- **MIS auto square-off:** brokers close intraday positions around 15:15–15:25. Many charge ₹50 + GST per auto-squared order.
- **Muhurat trading:** a short evening session on Diwali (Sunday 8 Nov 2026; timings come by circular).
- **Special sessions** happen: for example, Sunday 1 Feb 2026 (Union Budget) ran 09:15–15:00.

## Holidays

The full 2026 list is in `references/holidays-2026.md`. The remaining 2026 weekday holidays are
**Tue 10 Nov** (Diwali Balipratipada), **Tue 24 Nov** (Guru Nanak Jayanti), and **Fri 25 Dec**
(Christmas). Exchanges can add holidays at short notice: 15 Jan 2026 (Maharashtra civic polls) was
announced three days ahead, and that day's expiries moved a day earlier. When an expiry falls on a
holiday, it moves to the **previous** trading day.

## Settlement

- **T+1 rolling** for all equity. Buy on Monday and shares reach your demat on Tuesday. Sell proceeds are
  usable for trading immediately (with limits), and withdrawable after T+1.
- **Optional T+0** (same-day settlement) exists for a list of up to 500 large stocks, but broker
  support is limited. Check with the broker before assuming it.
- **Selling from demat** needs authorisation: either a one-time **DDPI** or per-sale **eDIS/TPIN**
  through CDSL/NSDL. Without one, sell orders from holdings are rejected. The Groww MCP also requires
  DDPI for sells.
- **BTST** (buy today, sell tomorrow before delivery) works but carries **short-delivery risk**. If the
  original seller fails to deliver, the shares go to auction and the close-out price can be punitive.
- **Ex-date = record date** under T+1. To receive a dividend, bonus or rights entitlement, you must
  hold the shares at the end of the day **before** the record date.

## Product types

| Code | Meaning | Key rules |
|---|---|---|
| CNC | Delivery (cash and carry) | Full payment. Shares go to demat |
| MIS | Intraday | Margin at least 20% (max 5x leverage). Auto squared off before close |
| NRML | F&O carry-forward | SPAN + exposure margin. Position carries to the next day |
| MTF | Margin Trading Facility | Broker funds part of a delivery buy. Shares are pledged. Daily interest (≈12–18% a year) |

- **Upfront margins.** SEBI peak-margin rules require full margin upfront. Shortfalls attract penalties.
- **50:50 rule.** At least half of F&O margin must be cash or cash-equivalents (liquid funds and G-secs
  count). Pledged shares, after a haircut, can make up the rest.
- **Option buyers pay the full premium upfront.** Option sellers post SPAN + exposure. A naked
  NIFTY short needs far more margin than a hedged spread, so check the broker's basket margin
  calculator.

## Order types

| Type | Behaviour | Use / caveat |
|---|---|---|
| Limit | Executes at your price or better | Default choice, especially for options and small caps |
| Market | Executes at the best available price | Brokers add price protection. Dangerous in illiquid strikes and small caps |
| SL (stop-loss limit) | Becomes a limit order when the trigger is hit | Set a limit beyond the trigger (buffer) so it fills in fast moves |
| SL-M (stop-loss market) | Becomes a market order at the trigger | Many brokers block it for options and illiquid contracts |
| GTT | Good-till-triggered (often up to 1 year), stored at the broker | **The only way to keep a stop alive across days for CNC holdings.** On trigger it places a limit order, which may not fill on a gap |
| AMO | Placed after hours | Enters the next pre-open/open |
| Iceberg | Splits a large order into legs | Large F&O orders above the exchange **freeze quantity** must be split |

**Day validity.** Regular SL/SL-M orders are DAY orders. They expire at close, and a delivery stop
must be re-placed daily or converted to GTT.

## Price bands and circuits

- **Stocks outside F&O** have fixed daily price bands of **2%, 5%, 10% or 20%**, revised periodically by
  the exchanges. At an upper circuit there are only buyers; at a lower circuit only sellers. **You may
  be unable to exit**, and stop orders will not fill.
- **F&O stocks** have no fixed band. They have dynamic operating ranges (≈10%) that exchanges relax in
  steps when hit.
- **Market-wide circuit breakers** apply on NIFTY or SENSEX, whichever breaches first. Trigger levels
  are computed daily from the previous close:

| Move | Before 13:00 | 13:00–14:30 | After 14:30 |
|---|---|---|---|
| 10% | 45-min halt | 15-min halt | No halt |
| 15% | 1 h 45 min halt | 45 min (13:00–14:00), rest of day after 14:00 | Rest of day |
| 20% | Rest of day | Rest of day | Rest of day |

Trading resumes with a 15-minute pre-open call auction after a halt.

## Surveillance and special series

Details are in `references/surveillance-and-series.md`. In short:
- **ASM** (Additional Surveillance Measure, long-term and short-term) brings higher margins (up to
  100%) and is triggered by abnormal price/volume.
- **GSM** (Graded Surveillance Measure, stages 0–IV) is for fundamentally weak, low-price stocks.
  Effects include trade-for-trade settlement, deposits, and trading allowed only weekly at higher stages.
- **ESM** (Enhanced Surveillance Measure) targets small companies (market cap below ₹500 crore). Stage
  I brings a 5% band and trade-for-trade; stage II brings a 2% band and periodic call auctions.
- **Series:** `EQ` is normal; `BE`/`BZ` are trade-for-trade (no intraday netting, every trade settles
  by delivery); `SM`/`ST` are SME-platform stocks with large lots. BSE uses groups (A, B, T, X, XT, Z, M/MT).

A stock entering ASM/GSM/ESM is a governance and liquidity red flag, not a buying opportunity.

## F&O mechanics that affect traders

- **One weekly index expiry per exchange:** NIFTY weekly expires **Tuesday** (NSE) and SENSEX weekly
  **Thursday** (BSE), in force since 1 Sep 2025. BANKNIFTY, FINNIFTY, MIDCPNIFTY and NIFTYNXT50 are
  monthly only, on the last Tuesday. BSE monthlies (SENSEX, BANKEX) expire on the last Thursday.
  Stock F&O is monthly, on the last Tuesday.
- **Lot sizes** (verified Oct 2026): NIFTY 65, BANKNIFTY 30, FINNIFTY 60, MIDCPNIFTY 120,
  NIFTYNXT50 25, SENSEX 20, BANKEX 30. Contracts are sized to about ₹15 lakh or more, and lot sizes
  are revised periodically.
- **Stock F&O is physically settled.** In-the-money stock options and futures held into expiry become
  delivery obligations. Brokers raise margins sharply in expiry week and may square off.
- **F&O ban:** when a stock's open interest crosses 95% of its market-wide position limit (MWPL), no
  new positions are allowed until it falls below 80%. OI has been measured on a **delta-based
  (future-equivalent)** basis since Dec 2025. Exchanges publish the ban list daily.
- **Expiry-day rules:** an extra 2% extreme-loss margin on short options, and no calendar-spread margin
  benefit on expiry day.
- **SEBI retail algo framework** (fully in force from 1 Apr 2026): API orders must come from a
  registered app with a whitelisted static IP, and algos above exchange thresholds must be registered.

## Corporate actions

- **Bonus and split:** price adjusts on the ex-date. Check that charts and indicator history are adjusted.
- **Dividend:** price drops by roughly the dividend on the ex-date. It is taxed at your slab rate, with
  TDS of 10% above ₹10,000 per company per year.
- **Demerger:** a new symbol lists later, and the parent's price drops on the ex-date. Cost-of-acquisition
  split ratios come from the company.
- **Buyback (tender):** taxed as capital gains for shareholders from 1 Apr 2026, replacing the
  deemed-dividend treatment used from Oct 2024 to Mar 2026.
- **Rights issue:** entitlements (REs) trade separately for a few days.

## Answering style

When asked "can I do X now?", check the IST time and holiday calendar first. Then state the rule,
the reason, and what the user should do instead (for example: "Your SL order expired at 15:30.
Place a GTT so the stop survives overnight.").
