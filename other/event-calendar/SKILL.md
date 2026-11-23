---
name: event-calendar
description: |
  Offline calendar of the dates that move Indian markets: NSE/BSE F&O expiries (holiday-shifted),
  exchange holidays, long weekends and special sessions, results-season windows (SEBI LODR),
  trader tax dates, India macro releases (CPI, WPI, IIP, GDP, PMI, auto sales, GST, AMFI), RBI MPC,
  Union Budget, US FOMC/CPI/jobs, NIFTY and MSCI rebalances, plus your own results, board-meeting,
  ex-date and lock-in events. Every date is labelled computed, expected-by-rule, verified (with
  source) or unverified. events.py exports .ics and answers "is there event risk in my holding
  window?".

  Use when the user asks: "what's on this week", "economic calendar India", "when is the next RBI
  policy", "when is expiry", "is Monday a holiday", "events before my exit date", "any event risk
  in this trade", "Fed meeting date", "when is CPI", "Budget date", "results season dates",
  "advance tax due date", "export market calendar to Google Calendar", or before any multi-day trade.
---

# Event Calendar (India)

Most surprise losses on a good chart come from a date the trader forgot: RBI at 10:00, a results
gap, a Tuesday expiry, a three-day weekend. This skill lists those dates offline and says how much
to trust each one.

## Commands

```bash
python3 scripts/events.py week [--from 2026-11-16] [--next]        # Mon-Sun, grouped by IST day
python3 scripts/events.py month --month 2026-12 --min-impact medium
python3 scripts/events.py range --from 2026-11-16 --to 2027-03-31 --category rbi,fomc,budget
python3 scripts/events.py next --category rbi --count 2            # also: expiry, results, macro, us, index, tax
python3 scripts/events.py window --from 2026-11-16 --to 2026-12-04 --symbols TCS,INFY --events q3.csv
python3 scripts/events.py ics --out india-events.ics --from 2026-11-16 --to 2027-03-31
python3 scripts/events.py staleness [--days 60 --max-age 120 --strict]
```
Common flags: `--events FILE` (repeatable), `--category` (names or groups: macro, us, policy,
index, holidays, results, company), `--min-impact low|medium|high`, `--today` (pretend date),
`--reference FILE`, `--json`. Dates are ISO or 31-Oct-2026; numeric dates that could be DD/MM or
MM/DD exit 2, using the same parser as `results-season`. All times are IST.

## Where each date comes from

| Status | Events | Trust |
|---|---|---|
| **computed** | F&O expiries and holiday shifts (`../fno-options-analysis/scripts/options.py`), exchange holidays, long weekends, NSE monthly-expiry weeks, results-season windows (Q1–Q3 within 45 days of quarter end, Q4 within 60), advance tax (15 Jun/Sep/Dec/Mar), ITR due dates (31 Jul; 31 Aug for ITR-3/4 without audit, as reported for Finance Act 2026; 31 Oct for audit cases), last FY session and the March LTCG/loss-harvesting window | Exact while the holiday list covers the year; flagged beyond it |
| **expected (rule)** | India CPI (12th, 16:00), WPI (14th, 12:00), IIP (28th, 16:00); a weekend moves each to Monday. GDP (last weekday of Feb/May/Aug/Nov, 16:00), auto sales and GST (1st), Budget (1 Feb), NIFTY semi-annual rebalance (close of the March/September NSE monthly expiry) | Publisher's stated rule; confirm on the day |
| **rough (uncertain rule)** | PMI (first/third working day, 10:30), AMFI (around the 10th), US jobs beyond the reference file (first Friday), MSCI beyond the file (near the 1st of Mar/Jun/Sep/Dec), May GDP | Placeholder date; check before relying on it |
| **verified** | `references/events-2026-27.csv`: RBI MPC FY2026-27, FOMC 2026–27, BLS CPI and jobs to Dec 2027, MSCI reviews to Nov 2027, MoSPI GDP to Feb 2027, Muhurat and Budget-day sessions | Source URL plus `verified_on` date |
| **UNVERIFIED** | Reference rows with a blank `verified_on` (Budget 2027-28 on 1 Feb) | Confirm before use |

Where the reference file has rows for a category, it replaces the rule estimates for those dates.
RBI, FOMC and US CPI have no dependable rule, so they appear only from the file.

## Refreshing dates (Claude's job)

1. Run `staleness` at the start of a planning session. It warns when a tracked category (RBI,
   FOMC, BLS, MSCI, GDP) ends within `--days`, when upcoming rows were verified more than
   `--max-age` days ago, when a row is unverified, and when the holiday list in `options.py` is
   about to run out. `--strict` exits 1, so freshness tooling can call it with `--json`.
2. For each warning, WebSearch the primary source: rbi.org.in (MPC schedule press release),
   federalreserve.gov (FOMC calendar), bls.gov/schedule, msci.com (index review dates), the
   mospi.gov.in Advance Release Calendar, and the Parliament Budget Session notice.
3. Edit the CSV row (`date,category,title,impact,source,verified_on`), with the URL and today's date.
   Never add a date you could not find at a source. Leave `verified_on` blank instead, and the row
   will print as UNVERIFIED. Cite the source when quoting a date to the user.

## Your events (`--events`)

Two CSV shapes, which can be mixed across files:
- `symbol,date,timing`: the same file `results-season` uses for `calendar-check`. Timing is
  pre-market, market-hours, post-market or HH:MM. An optional `category` column takes results,
  board meeting, ex-date/dividend/bonus/split, AGM or lock-in.
- `date,category,title[,impact][,symbol]` for anything else.

Collect dates with WebSearch (exchange board-meeting and corporate-action pages, IPO lock-in
schedules) or a broker MCP, and save them to a file. Duplicates (same symbol, date and category)
are merged, and a row with a known timing replaces one without. Results or board meetings with
unknown timing count both the meeting day and the next session.

## Reading the calendar (India specifics)

- **RBI policy day:** the decision comes at 10:00 IST, mid-session. Banks, NBFCs, realty, autos
  and USD/INR swing in the first hour, and the press conference follows at about 12:00. Don't
  place tight intraday stops before 10:00.
- **Budget day:** the speech starts at 11:00 IST. Exchanges have opened on weekend Budget days
  (Saturday 1 Feb 2025, and Sunday 1 Feb 2026 from 09:15 to 15:00). Expect a whipsaw while the
  speech runs, a re-pricing on STT and capital-gains changes, and an IV crush the next day.
- **Expiry days:** NIFTY expires weekly on **Tuesday** (NSE) and SENSEX on **Thursday** (BSE). The
  last one of the month is the monthly expiry, and a holiday moves an expiry to the previous
  session (Mon 23 Nov 2026). Expect gamma-driven moves and pinning in the last hour, plus extra
  ELM on short options. Physically settled stock F&O carries delivery risk in expiry week.
- **Results** are usually filed after 15:30, so the next session's open is the reaction. MoSPI
  data (CPI, IIP, GDP) also lands at 16:00, after the close. FOMC decisions arrive around
  23:30–00:30 IST and US data at 18:00–19:00 IST, so India reacts the next morning through GIFT
  Nifty.
- **Long weekends** concentrate global news into one gap, and option sellers do not earn extra theta
  for the closed days.
- **Index rebalances** (NIFTY in Mar/Sep, MSCI quarterly) put large passive orders into one close.
  Added and removed stocks can print odd closing prices.

## `window` and the discipline gate

`window` lists everything inside a holding window. It marks RISK on RBI, Budget, FOMC, results,
board meetings, lock-in expiries and any high-impact event from your file, and ends with
`Event risk: YES/NO` and `trading-discipline gate: pass --event yes|no`. Add `--include-expiry` for
option positions. Positions with no company event get a reminder of the season deadline, and
risk events reacting within 2 sessions after the exit are flagged NEAR.

## How other skills use it

- `market-pulse`: put the next day's rows from `week` in the "Today/events" line of the brief.
- `results-season`: `calendar-check` reads the same events file. Use this skill for the macro
  backdrop around the results.
- `trading-discipline`: pass the `window` verdict as `--event`.
- `options-strategies`: run `next --category policy` and `window --include-expiry` before selling
  premium through RBI, the Budget or FOMC (see its event playbook).
- `india-market-analyst`: step 6 (event risk first) runs `window` for the planned hold.

## Limits

Government holidays other than weekends are not modelled for MoSPI and OEA releases, so a rule date
can slip by a day. Holiday-dependent dates after `HOLIDAYS_KNOWN_UNTIL` in `options.py` are
flagged. No live data is fetched, and the file is only as fresh as its last `verified_on`.

_Educational analysis, not investment advice._
