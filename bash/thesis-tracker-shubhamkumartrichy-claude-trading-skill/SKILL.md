---
name: thesis-tracker
description: |
  Keeps every Indian stock or F&O trade idea as a written, falsifiable thesis in one JSON file the
  trader owns, and walks it through an enforced lifecycle (idea, watching, entry-ready, active,
  closed, or invalidated / expired) with a dated history. Flags reviews due, kill levels hit from a
  price file, results and expiry dates ahead, and delivery holdings about to turn long-term (STCG
  20% to LTCG 12.5%). Closing reviews split outcome from process (right/wrong thesis x good/bad
  result), stats by source skill and setup, export to the trading-discipline journal. thesis.py,
  stdlib only, offline.

  Use when the user asks: "track this idea", "add TCS to my watchlist with a reason", "what are my
  open theses", "anything due today", "did my stop or kill level get hit", "is my thesis still
  valid", "close the trade and review it", "was I right or just lucky", "which source of ideas
  actually works", "write a hypothesis I can test", or at the start of any session where earlier
  trade ideas exist.
---

# Thesis Tracker

A trade without a written reason cannot be reviewed; it can only be remembered, and memory edits
itself to protect the ego. This skill makes the reason, the entry trigger and the conditions that
prove it wrong explicit *before* money moves, then holds the trader to them afterwards.

## Commands

```bash
T="python3 scripts/thesis.py --store ~/trading/theses.json"   # the store lives with the user's files
$T add TCS --direction long --horizon swing --source breakout-planner --setup breakout --tag it \
   --statement "Deal wins revive IT; the 8-week base breaks out and holds above 3400" \
   --trigger "daily close above 3400 on 1.5x volume" --trigger-price 3400 \
   --kill "Q2 TCV below last quarter" --kill-price 3330 --stop 3340 --target 3520 --target 3650 \
   --risk-pct 1 --catalyst 2026-11-20:"Q2 results"
$T add NIFTY --direction short --horizon swing --segment options --expiry 2026-11-24 ...
$T transition T0001 entry-ready
$T transition T0001 active --entry-price 3405 --qty 100 [--date 2026-11-14]
$T update T0001 --stop 3390 --note "trailed below the swing low"
$T note T0001 "Held the 20-DMA on falling volume" --reviewed       # schedules the next review
$T due --prices ltp.csv [--days 7] [--ltcg-days 45]                 # start of every session
$T list [--state active] [--symbol TCS] [--tag it] [--due] [--all];  $T show T0001;  $T stale --days 21
$T transition T0001 closed --exit-price 3520 --reason target --charges 160
$T postmortem T0001                     # draft: facts from the record + the questions to ask
$T postmortem T0001 --thesis right --stop-honoured yes --mistake none --lesson "..."
$T stats [--since 2026-04-01]
$T export --journal thesis_journal.csv [--closed-only] [--overwrite]
$T hypothesis --symbol DIXON --expected-win-rate 45 --margin 10
```

Every command takes `--json` and `--as-of YYYY-MM-DD` (default today, IST). Bad input prints one
`error:` line and exits 2. `--prices` is any CSV with `symbol` and `ltp` (or `close`) columns.

## Lifecycle

| From | Allowed to | Needs |
|---|---|---|
| idea | watching, entry-ready, invalidated, expired | statement (at `add`) |
| watching | entry-ready, invalidated, expired | |
| entry-ready | active, watching, invalidated, expired | trigger, kill criteria, stop (premium for bought options) |
| active | closed | `--entry-price --qty` to enter; `--exit-price --reason` to close |
| expired | watching (revive) | |
| closed, invalidated | nothing: final | invalidating needs `--note` saying what proved it wrong |

Illegal moves are refused with the allowed list. Every change lands in the thesis history with its
date; `update` records old and new values. Widening a live stop, or rewriting the statement or kill
criteria while active, is allowed but flagged in the history and counted against plan adherence.
Closed theses are frozen (later thoughts go in `note`). Reviews default to 7 / 30 / 90 days by horizon.

## Why written kill criteria matter

The stop limits the loss; the kill criteria end the *idea*. "Q2 deal wins below last quarter",
"stock enters ASM stage 2", "promoter pledge rises" are thesis-breaking even when price is above the
stop. Written down before entry, they turn a later exit from a negotiation with hope into a lookup.
A thesis without them cannot reach entry-ready.

## How Claude uses it across sessions

- **The store file is the memory.** At the start of a session where the user trades, run `due`
  (with a prices file if live quotes are available) and lead with kill hits, then reviews due.
- **Never edit the past.** Do not rewrite history entries or the JSON by hand; use `update` / `note`,
  which keep the earlier values. Never delete a thesis.
- **Ask before closing, invalidating or expiring.** `due` and `stale` only suggest; the trader confirms
  the state change, the fill price and the reason.
- Register ideas from other skills with `--source` (breakout-planner, results-season, the stock
  screener, momentum-scanner, pair-trading) so `stats` can say which sources actually make money.

## Postmortem and stats

The postmortem separates the decision from the dice. Result comes from the record (₹ and R, using
the stop at entry). Whether the thesis was right comes from the trader: did the written statement
come true? The quadrant is right/good (earned), right/bad (variance or execution), wrong/good
(luck: do not repeat it) or wrong/bad (deserved); zero P&L is breakeven, never a loss. Plan checks
(entry within 1% of the trigger, exit not beyond the stop, early exit, stop widened) are filled from
the record and can be overridden with `--entry-at-trigger`, `--stop-honoured`, `--exited-early`.
`stats` gives win rate, average R, expectancy, results by source, setup, tag, horizon, direction and
segment, the quadrant table, plan-adherence rate (and followed vs broken expectancy) and the most
common mistakes. Fewer than 30 closed theses: every number is provisional.

## India-specific notes

- **Results dates** are the commonest catalyst: add them with `--catalyst`; `due` warns when one falls
  inside an active holding. Read the reaction with `results-season`.
- **LTCG clock.** For long delivery positions, `due` uses `../indian-tax-for-traders/scripts/tax.py`
  (listed equity is long-term after 12 months) to list holdings turning long-term within
  `--ltcg-days`, with the STCG-vs-LTCG saving on the current gain. It never overrides a kill level.
- **F&O expiry.** Futures and options theses need `--expiry`; `due` lists it ahead and flags an
  expired contract. A bought option with no stop counts the whole premium as risk.
- **Surveillance.** Entry into ASM/GSM, an F&O ban or a trade-for-trade move belongs in `--kill`:
  margins jump and exits thin. Shorts cannot be carried in delivery, so they need another segment.

## How it connects

- `trading-discipline`: run its pre-trade gate before `transition ... active`; `export` writes rows in
  its journal format (`date,symbol,side,entry,exit,stop,qty,charges` + `exit_date,setup,mistake,
  segment,notes`), so `../trading-discipline/scripts/discipline.py review` and
  `../position-sizing/scripts/risk.py journal` read them. Active theses export with a blank exit
  (open trade); use `--closed-only` for `risk.py`, which has no open-trade concept.
- `backtest-lab`: `hypothesis` prints a card (statement, evidence for and against, the backtest to run
  with `../backtest-lab/scripts/backtest.py`, pass marks set in advance, kill criteria, sample size).
  Claude fills it in conversation; only a surviving idea is registered with `add`.
- `portfolio-review` checks the whole book, this skill why each position is in it; `position-sizing` sizes it.

## Output

```
Thesis check as of Tue 20 Oct 2026 IST (1 open in /home/me/trading/theses.json)
Target reached (1)
  T0001 TCS  LTP ₹3,600 past ₹3,520  unrealised +₹19,500 (+3.00R): book, trail, or restate the thesis
Turning long-term within 30 days (1)
  T0001 TCS  bought 2025-11-03: wait 15 days (sell on or after 2026-11-04) to convert STCG 20% into LTCG 12.5%
```

Storage: one indented JSON file with `schema_version`; each save writes a temp file and renames it
over the store, keeping the previous version as `theses.json.bak`. A store from a newer version is
refused, as is a store that changed on disk mid-command. The script writes only the store (and the
journal CSV you name); default `./theses.json` in the current folder, never inside the skill.

Limits: no prices are fetched; worded kill conditions are checked by the trader, not the script. Holidays
and lot-size changes are not modelled. Tax figures ignore cess and the ₹1.25 lakh exemption.

_Educational discipline tool, not investment advice. The thesis and the decision stay yours._
