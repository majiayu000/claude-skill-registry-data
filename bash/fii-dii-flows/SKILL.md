---
name: fii-dii-flows
description: |
  Institutional money flow in Indian equities, from CSVs you download: FII/FPI and DII cash flows
  (₹ crore) with 5/10/20-session and month-to-date sums, streaks, how much FII selling DIIs
  absorbed, largest days and NIFTY correlation; NSE participant-wise F&O open interest (FII
  index-futures long %, day-over-day change, index calls/puts, client positioning, extreme flags);
  quarterly shareholding changes with pledge red flags; bulk/block deals by symbol and client.
  flows.py works offline.

  Use when the user asks: "FII DII data this week", "are FIIs selling", "how long have FIIs been
  selling", "are DIIs absorbing FII selling", "FII long short ratio", "participant wise OI", "FII
  positioning in index futures", "who is buying this stock", "FII holding change", "promoter
  pledge", "bulk deals in X", "block deals", or wants flow context for a market or stock view.
---

# FII/DII Flows (India)

`market-pulse` quotes last evening's FII/DII figures. This skill turns weeks of downloaded data into
streaks, absorption, positioning extremes and holder changes, so a single day's number gets context.

## Commands

```bash
python3 scripts/flows.py cash --csv fii_dii.csv                      # flows, streaks, absorption
python3 scripts/flows.py cash --csv fii_dii.csv --nifty nifty.csv --json   # + NIFTY correlation
python3 scripts/flows.py participants --oi participant_oi/ --days 10  # folder of daily NSE files
python3 scripts/flows.py shareholding --csv shp.csv [--symbol HDFCBANK,ITC]
python3 scripts/flows.py deals --csv bulk.csv --csv block.csv [--symbol XYZ] [--client "fund"]
```
Common flags: `--json` (strict JSON), `--as-of DATE`, `--date-format dmy|mdy`. Tuning: `--lookback 60`,
`--top 5` (cash); `--long-low 20 --long-high 70 --shift-pp 5` (participants); `--min-change 1`,
`--promoter-drop 0.5`, `--pledge-watch 10 --pledge-red 20 --pledge-severe 50` (shareholding);
`--kind bulk|block --from --to` (deals). Errors exit 2 with one `error:` line.

**Dates are never guessed.** ISO, `30-Oct-2026`, `30-OCT-2026`, `Oct 30, 2026` and `30-10-2026` (dashes =
day first, NSE style) parse directly. Slash dates like `05/10/2026` work only if some row in the file
proves the order (a day above 12); otherwise the script stops and asks for `--date-format`.

## Getting the files

nseindia.com blocks scripted requests: download in a browser, or use WebSearch/WebFetch on sites that
republish the figures (cite them). Never invent a missing day.

| Command | Source | Format handled |
|---|---|---|
| `cash` | NSE → Reports → FII/FPI & DII trading activity (provisional, NSE+BSE+MSEI); Moneycontrol FII/DII table; NSDL FPI daily report | Wide `date,fii_buy,fii_sell,fii_net,dii_buy,dii_sell,dii_net`; NSE rows `Category,Date,Buy Value,Sell Value,Net Value` (`FII/FPI`, `DII`); Moneycontrol two-row header (FII/DII × Gross Purchase/Gross Sales/Net); FPI-only files (NSDL: rename to `date,fii_net`). Net is derived from buy − sell if blank. Totals rows are skipped |
| `participants` | NSE → All Reports → Derivatives → "F&O – Participant wise Open Interest" (`fao_participant_oi_DDMMYYYY.csv`, one per day) | Title row ("…as on Oct 30, 2026"), then `Client Type` header with Future Index/Stock Long/Short, Option Index/Stock Call/Put Long/Short, Total Long/Short; rows Client, DII, FII, Pro, TOTAL. Trailing spaces in headers and CRLF are fine. Date from the title, else the file name |
| `shareholding` | NSE/BSE shareholding-pattern filings (within 21 days of quarter end) or a Screener-style table | `symbol,quarter,promoter,fii,dii,mf,public,pledged` (one or many stocks), or quarters across columns (`Promoters`, `FIIs`, `DIIs`, `Public`, `No. of Shareholders` rows). Quarters: `Sep-2026`, `Q2FY27`, `Q2 2026-27`, `2026-09-30`; `Q3 2026` is rejected (calendar or fiscal?) |
| `deals` | NSE → Market Data → Large Deals (bulk/block CSV); BSE bulk/block deals | `Date,Symbol,Security Name,Client Name,Buy/Sell,Quantity Traded,Trade Price / Wght. Avg. Price`; quantities like `4,00,000`; BSE `B`/`S`/`P` sides. File name containing "block"/"bulk" tags the kind |

Participant-OI layout checked against NSE's own Oct-2025/Oct-2026 files; bulk-deal header against
NSE's archive `bulk.csv`. NSE's FII/DII CSV header text varies, so those columns match by keyword.

## What it computes

- **cash:** latest buy/sell/net, FII size vs the 20-session average absolute flow, 5/10/20-session,
  month-to-date and previous-month sums, current FII and DII streaks plus the longest runs in
  `--lookback` sessions, largest days, and **absorption**: DII net ÷ FII net outflow over the window,
  plus the same-day share of FII selling matched by DII buying. With `--nifty`: same-day and next-day
  correlation and the average NIFTY return on FII selling vs buying days.
- **participants:** for FII, Client, Pro and DII: index-futures long, short, net, **long %** (long ÷
  (long + short), which Indian commentary calls the "long-short ratio") and L/S; day-over-day change
  labelled long/short buildup, covering or unwinding; FII index calls and puts (long − short each);
  stock futures; percentile of FII long % when 20+ files are loaded.
- **shareholding:** QoQ and YoY change in promoter, FII, DII, MF, public and pledge; flags for rising
  institutions (FII+DII ≥ +1 pp, with streak), FII→DII handover, promoter falling ≥ 0.5 pp, and
  pledges: watch ≥ 10%, red ≥ 20% (same line as `fundamental-screening`), severe ≥ 50% (SEBI makes
  promoters disclose reasons above 50% encumbrance). Pledge rising while promoter stake falls is
  flagged as possible invocation.
- **deals:** buy, sell and net quantity and ₹ crore by symbol and client, average prices, repeat buyers
  and sellers (2+ days in one stock), and same-day round trips.

## Reading it in India

- **FII selling vs SIP money.** Since 2021, steady SIP inflows let DIIs absorb most FII selling, so
  FII outflows alone have rarely meant a crash. Absorption under ~50% for weeks is the warning, as is
  FII and DII selling together. Big single days often come from MSCI/FTSE rebalances, block deals or
  large IPO/QIP allotments; check the date before reading conviction into them.
- **Rupee link.** FPI selling, a weaker rupee, higher US yields and a strong dollar usually travel
  together; a falling rupee raises FPIs' dollar hurdle. Check USD/INR with every long selling streak.
- **Provisional vs final.** Exchange figures (same evening, secondary market only, by client codes)
  differ from NSDL/CDSL final FPI data (T+1, by custodians, includes primary-market investment).
  They can even differ in sign during heavy IPO/QIP months. Keep one source per file. NSE-only and
  combined NSE+BSE+MSEI series differ too.
- **FII long % thresholds.** Defaults ≤ 20% (extreme short) and ≥ 70% (crowded long) are flags, not
  signals. FII long % fell to about 13% in Feb-2025 and 8–9% in Aug–Sep 2025, and the Mar-2025 short
  covering took it to about 66% (Business Standard, citing NSE data). NSE's own file showed 11.1% on
  30-Oct-2026. Sub-20% readings can last for weeks, so use the percentile and day-over-day change
  for timing, and `--long-low 15` for a stricter cut. A one-day swing of 5+ points is flagged.
- **Expiry noise.** NSE index derivatives expire on Tuesday (monthly: last Tuesday; Thursday before
  Sep-2025). Changes spanning a monthly expiry are rollover, and option OI resets every weekly
  expiry, so read options week over week. Holiday shifts are not modelled.
- **Counterparties.** Clients (mostly retail) are often long when FIIs are short. Read their long %
  as contrarian context, not a forecast. DII stock-futures shorts are mostly mutual-fund arbitrage
  hedges, not bearish bets. Contract counts mix NIFTY, BANKNIFTY and other indices, and lot-size
  revisions change counts, so compare long %, not raw contracts, across months.
- **Shareholding.** MF is part of DII. A falling promoter % can be dilution (QIP, ESOPs, merger),
  not selling. Fewer shareholders while institutions add = stock moving from retail to institutions.
- **Deals.** A bulk deal is one client trading over 0.5% of a company's shares in a day. Block deals
  run in a separate window. HFT and market-maker names that buy and sell the same day (common in SME
  stocks) are not conviction. Repeat buying by a known fund or promoter entity is.

## How other skills use it

- `market-pulse`: in the post-market wrap, run `cash` and `participants` on the downloaded files for
  the FII/DII row, the streak and the FII long % line, instead of quoting one day alone.
- `market-regime`: a 5+ session FII selling streak with absorption under 50% adds weight to
  distribution days; heavy DII absorption explains flat days despite FII selling.
- `india-market-analyst`: add one context line (FII 20-session net, DII absorption, FII long %) and
  the stock's shareholding/deal flags to any trade view.
- `fundamental-screening`: use `shareholding` for the multi-quarter trend and pledge flags.
- `fno-options-analysis`: use `participants` for the FII futures and options positioning gauge.

## Caveats

Flows are reported after the fact: context, not timing. Same-day correlation mostly shows FIIs
selling into falling markets and is unstable over a few months. Participant categories rest on
broker-entered client codes; shareholding is up to three weeks stale; deal files only show trades
above disclosure thresholds.

## Output

```
FII/DII (provisional, [source], to [dd-Mon-yyyy]): latest FII [±₹x cr] / DII [±₹y cr];
20 sessions FII [±₹a cr], DII [±₹b cr], DII absorbed [c%]; FII [buying|selling] streak [n] ([±₹s cr])
F&O positioning ([date]): FII index futures [l%] long ([Δ] vs prior day, [activity]); clients [k%] long;
FII index calls net [..], puts net [..]; flags: [..]
Stock: promoter [p%] ([Δ] QoQ, pledge [q%]), FII [f%] ([Δ]), DII [d%] ([Δ]); deals: [repeat buyers/sellers]
```
_Educational analysis, not investment advice. Data: [files + dates]._
