---
name: black-edge
description: Use when apply institutional trading edge using order flow analysis,
  market microstructure, and dark pool signals. Use when working with black edge.
domain: trading
author: oyi77
license: Apache-2.0
subdomain: trading
version: 2.0.0
tags:
- algorithms
- black
- edge
- markets
- trading
- money
category: trading
---

# Black Edge

## When to Use

**Trigger phrases:**
- "black edge"
- "Help me with black edge"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

parking_data = fetch_satellite_imagery(ticker="WMT")
consensus_revenue = get_analyst_estimates(ticker="WMT")

parking_trend = calculate_occupancy_trend(parking_data, period="3m")
expected_beat = parking_trend > consensus_revenue * 1.05

position_size = calculate_kelly_size(
    edge_confidence=85,
    historical_accuracy=0.72,
    payoff_ratio=2.5
)
```

### Example 2: Options Flow Anomaly

```python
# Detect unusual OTM call buying
flow = fetch_unusual_options_activity(
    min_volume=500,
    otm_percentage=10
)

sweeps = filter_sweep_orders(flow)
catalyst_date = find_next_catalyst(ticker=sweeps[0].ticker)

if sweeps.volume > 3 * avg_daily and days_to_catalyst < 30:
    signal_strength = "HIGH"
    position = buy_calls(sweeps[0], strike=sweeps[0].strike)
```

### Example 3: Dark Pool Accumulation

```python
# Identify institutional accumulation
dark_pool_prints = fetch_ats_volume(ticker="AAPL")

large_blocks = dark_pool_prints[
    dark_pool_prints.volume > 100000
    and dark_pool_prints.price > vwap
]

accumulation_score = calculate_accumulation(
    large_blocks, 
    lookback="20d"
)

if accumulation_score > 75 and price_near_support:
    entry = "LONG"
    target = calculate_measured_move("cup_and_handle")
```

---


Load `references/trading-checklist.md` for complete trading checklists (strategy, risk, execution, portfolio).


## When NOT to Use

- When you cannot afford to lose the capital at risk
- For instruments you do not understand
- When emotional state impairs judgment (revenge trading, FOMO)


## Overview

Black Edge provides market analysis capabilities with risk management.

## Workflow

1. **Research** — Analyze market conditions and opportunities
2. **Plan** — Define entry, exit, and position sizing
3. **Execute** — Place trades with proper order types
4. **Monitor** — Track positions and market changes
5. **Manage risk** — Apply stop-losses and hedging
6. **Review** — Post-trade analysis and journaling

## Risk Management

- Never risk more than 1-2% of portfolio per trade
- Set stop-loss before entering any position
- Diversify across uncorrelated assets
- Size positions based on volatility (ATR)
- Have a maximum daily loss limit

## Key Metrics

- Win rate and profit factor
- Sharpe ratio and max drawdown
- Average risk-reward ratio
- Expectancy per trade
- Correlation to benchmark

## Discipline Rules

- Follow your trading plan — no impulsive trades
- Cut losses short, let winners run
- Review every trade in your journal
- Never revenge trade after a loss
- Take breaks after consecutive losses

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I will cut losses later" | Later never comes. Set stop-losses before entering any trade. |
| "This time is different" | It never is. Follow your strategy, not your emotions. |
| "I do not need to journal" | Journaling reveals patterns in your behavior. Track every trade. |

## Money-Making Overview

Generate alpha from institutional order flow signals, dark pool prints, and options flow sweeps. Each signal is a trade setup with 2-5% target per trade. The edge comes from detecting large institutional positioning before price moves — front-running block orders via tape reading, catching sweeps of out-of-the-money options that indicate smart money direction, and tracking dark pool accumulation that signals conviction on catalysts.

This skill turns market microstructure data into actionable trade plans. Every print, sweep, or accumulation pattern is a setup with defined entry, stop-loss, and target levels.

## Revenue Streams

| Stream | Description | Estimated Income |
|--------|-------------|-----------------|
| Options Flow Scalping | Detect and trade large OTM sweeps on 15-60 min timeframes. Scalp premium expansion driven by delta-gamma hedging flow. | $200-2,000/day |
| Dark Pool Accumulation | Ride institutional position-building over 1-5 days via ATS prints exceeding 20% of daily ADV. Scale into mean-reversion entries against VWAP. | $500-5,000/position |
| Satellite Alt-Data for Earnings | Trade earnings events using parking lot, credit card, or supply chain satellite imagery as leading indicators. Enter 1-2 weeks pre-print. | $1,000-10,000/trade |

**Real Stop-Loss & Target Formulas:**

- **Options sweeps:** Stop = strike debit paid − 30% of debit; Target = $0.50-1.00 above sweeps' average premium
- **Dark pool blocks:** Stop = VWAP − 1.5 × ATR(14); Target = VWAP + 3 × ATR(14) for 1:2 risk-reward
- **Alt-data earnings:** Stop = entry − 0.5 × IV × underlying; Target = entry + (earnings_beat_est × premium_expansion_multiple)

## First Action in 60 Minutes

```python
#!/usr/bin/env python3
"""
Black Edge — Options Flow Edge Scanner

Fetches options chain via yfinance, detects unusual volume sweeps,
and prints actionable trade signals with calculated edge metrics.

Requires: pip install yfinance pandas numpy
"""

import yfinance as yf
import pandas as pd
import numpy as np
import sys

TICKER = sys.argv[1] if len(sys.argv) > 1 else "SPY"


def fetch_options_flow(ticker: str) -> pd.DataFrame:
    """Download options chain and build a flow dataframe."""
    stock = yf.Ticker(ticker)
    expirations = stock.options[:2]          # nearest 2 expiration cycles
    rows = []
    for exp in expirations:
        opt = stock.option_chain(exp)
        for df, opt_type in [(opt.calls, "call"), (opt.puts, "put")]:
            df = df.copy()
            df["type"] = opt_type
            df["expiration"] = exp
            rows.append(df)
    flow = pd.concat(rows, ignore_index=True)
    flow["dte"] = (pd.to_datetime(flow["expiration"]) - pd.Timestamp.today()).dt.days
    return flow


def compute_edge(flow: pd.DataFrame) -> pd.DataFrame:
    """Score each contract for unusual sweep activity and compute edge."""
    col = flow.copy()
    col["dollar_volume"] = col["volume"] * col["lastPrice"]
    col["oi_ratio"] = col["volume"] / col["openInterest"].clip(lower=1)

    # Sweep detection: volume > 3x OI ratio or dollar volume > $1M
    col["sweep"] = (col["oi_ratio"] > 3.0) | (col["dollar_volume"] > 1_000_000)

    # Edge score (0-100): combines volume anomaly, distance from ATM, and sweep flag
    atm = flow[(flow["type"] == "call")]["strike"].median()
    col["distance_pct"] = abs(col["strike"] - atm) / atm

    col["edge_score"] = (
        np.clip(col["oi_ratio"] / 5.0, 0, 50)          # OI ratio component (0-50)
        + np.clip(1 / col["distance_pct"].clip(1e-3), 0, 30)  # proximity boost (0-30)
        + col["sweep"].astype(int) * 20                 # sweep premium (0 or 20)
    )
    return col.sort_values("edge_score", ascending=False)


def main():
    print(f"=== Black Edge — Options Flow Scanner ===\n")
    print(f"Ticker: {TICKER}\n")
    flow = fetch_options_flow(TICKER)
    scored = compute_edge(flow)

    winners = scored[scored["sweep"]].head(10)
    if len(winners) == 0:
        print("No sweep signals detected for", TICKER)
        print("Try again during market hours or on a high-volume ticker.")
        return

    print(f"{'Type':<6} {'Strike':>8} {'Expiry':<12} {'Volume':>8} {'OI':>10} {'Prem':>8} {'Edge':>6}")
    print("-" * 62)
    for _, row in winners.iterrows():
        print(f"{row['type']:<6} {row['strike']:>8.2f} {str(row['expiration'])[:10]:<12} "
              f"{row['volume']:>8.0f} {row['openInterest']:>10.0f} {row['lastPrice']:>7.2f} "
              f"{row['edge_score']:>5.0f}")

    top = winners.iloc[0]
    print(f"\n--- Top Signal ---")
    print(f"Contract: {TICKER} {top['expiration'][:10]} ${top['strike']} {top['type'].upper()}")
    print(f"Edge Score: {top['edge_score']:.0f}/100")
    print(f"Volume / OI: {top['volume']:.0f} / {top['openInterest']:.0f}")
    print(f"Entry Zone: ${top['lastPrice']:.2f} (mid)")
    print(f"Stop-Loss:  ${top['lastPrice'] * 0.70:.2f} (30% of debit)")
    print(f"Target 1:   ${top['lastPrice'] * 1.50:.2f} (50% gain)")
    print(f"Target 2:   ${top['lastPrice'] * 2.00:.2f} (100% gain)")
    print(f"Risk-Reward: 1:1.7 to 1:3.3")


if __name__ == "__main__":
    main()
```

## Output Format

```
=== Trade Signal ===
Setup:     <options_sweep | dark_pool_accum | alt_data_earnings>
Ticker:    <AAPL>
Entry:     <$150.32>
Stop:      <$145.28>  (stop distance = 1.5 x ATR)
Target 1:  <$157.50>  (target distance = 3 x ATR)
Target 2:  <$162.80>  (measured move target)
R:R:       <1:2.4>
Edge:      <HIGH | MEDIUM | LOW>
Conviction: <7/10>
Catalyst:  <earnings 2026-07-25 | no catalyst | sector rotation>
```


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run black edge workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings