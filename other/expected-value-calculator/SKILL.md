---
name: expected-value-calculator
description: Calculate probability-weighted expected value for stock positions using live market data (options flow, earnings history, short interest) and scenario modeling. Use when the user asks for expected value, EV, risk/reward, or scenario analysis of stock positions or a portfolio.
allowed-tools: Bash, Read, WebSearch
---

# Expected Value Calculator

Scenario-based EV for stock positions, built on **fetched data and deterministic math** — never on invented numbers.

## Iron rules

1. **Every market number is fetched or user-provided.** If a data point can't be fetched, it is `n/a` — you may fill it via WebSearch *with the source cited inline*, marked `ESTIMATED`. Never state a market figure from memory.
2. **The model never does the EV arithmetic.** All weighted-sum math runs through `scripts/ev.py`.
3. Missing data lowers confidence (rubric below); it never silently disappears.
4. Output always ends with the disclaimer line.

## Workflow

### 1. Parse positions
From the user: ticker, shares, cost basis, optional stop-loss. Ask only if shares/ticker are ambiguous.

### 2. Fetch data
```bash
uv run <skill-dir>/scripts/fetch_data.py AAPL NVDA ...
```
Returns per ticker: live price, 52-week range, beta, next earnings date, near-the-money put/call volume & OI (±10% strikes — lottery strikes excluded by construction), last-quarters earnings beat rate & avg surprise, short % of float, days-to-cover. Any field that fails is `null` with an `error_*` key.

For `null` fields: one WebSearch attempt (e.g. "TICKER short interest percent float"); cite the source and mark the value `ESTIMATED`. Still nothing → `n/a`.

### 3. Assign scenario probabilities — anchored, not vibes
Start every position at **bull 25 / base 50 / bear 25**, then shift by these rules (skip any rule whose input is null):

| Signal | Condition | Shift |
|---|---|---|
| Options flow | put/call volume ratio < 0.7 | bull +5, bear −5 |
| | put/call volume ratio > 1.3 | bear +5, bull −5 |
| Earnings pattern | beat rate ≥ 0.75 and avg surprise > 0 | bull +5, bear −5 |
| | beat rate ≤ 0.40 | bear +5, bull −5 |
| Squeeze potential | short % of float > 15 and days-to-cover > 5 | bull +5 (from base) |
| | short % of float > 25 | bull +10 (from base), widen bull target |
| Earnings within horizon | next earnings date inside the analysis horizon | move 5 from base to *each* tail |

Caps: no scenario below 10% or above 60%. Round to 5%. Show the applied shifts in the output so the weighting is auditable.

**Targets**: anchor bull/bear targets to the fetched 52-week range and stated catalysts; base ≈ current price ± modest drift. State a one-line rationale per target. Stop-losses are handled by the script (bear outcome floors at the stop).

### 4. Compute
Write the scenarios JSON (format documented in `scripts/ev.py` docstring), then:
```bash
python3 <skill-dir>/scripts/ev.py positions.json
```
The script self-checks its own math on every run and validates probabilities sum to 1.

### 5. Report
Per position: price (with fetch timestamp), position value, scenario table (name, probability, target, return %, one-line rationale), expected return %, expected value $. Then portfolio totals. Then:

- **Data quality**: each input — LIVE / ESTIMATED (source) / n/a.
- **Confidence** (mechanical, not judgment):
  - **HIGH** — price, options, earnings, and short interest all LIVE.
  - **MEDIUM** — price LIVE, one or two other inputs ESTIMATED or n/a.
  - **LOW** — price not live, or 3+ inputs missing. Report EV as a **range**: rerun `ev.py` with each tail probability shifted ±10 points and show the spread instead of a point estimate.

End with: *"Scenario probabilities are model assumptions, not market forecasts. Not financial advice."*
