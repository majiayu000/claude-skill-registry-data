---
name: trading-strategist
description: Use when design and backtest trading strategies using technical indicators,
  fundamental analysis, and statistical models. Use when designing and backtesting
  trading strategies.
domain: trading
license: Apache-2.0
tags:
- algorithms
- markets
- strategist
- trading
- money
- backtesting
version: 2.0.0
author: oyi77
subdomain: ''
type: trading
category: trading
---


# Money-Making Overview

A validated strategy with Sharpe >1.5 and profit factor >1.3 compounds capital at 20-50%+/year. One good strategy can generate $500-5K/month on a $25K account. Multiple uncorrelated strategies scale exponentially.

## Revenue Streams
1. Personal Trading — run your own capital
2. Strategy Subscriptions ($97-497/mo) — sell signal access
3. Strategy Development ($2K-10K) — build for prop firms/hedge funds
4. Backtesting Service ($500-2K) — validate client strategies

## First Action in 60 Minutes
```bash
#!/usr/bin/env bash
# Quick strategy screen: test a simple moving average crossover
mkdir -p ~/trading-strategies/{backtests,reports,optimization}

echo "=== Quick Strategy Screen ==="
echo "Strategy: SMA crossover (50/200)"
echo "Pair: SPY (daily)"
echo "Timeframe: 5 years"
echo ""
echo "Calculate:"
echo "  - Total return vs buy-hold"
echo "  - Max drawdown"
echo "  - Sharpe ratio"
echo "  - Win rate"
echo "  - Profit factor"
echo ""
echo "Gate: Pass only if Sharpe >1.3 AND profit factor >1.5"
echo "If passes → add to optimization queue"
echo "If fails → discard or modify"
```

# Trading Strategist

## Overview

Build and optimize trading strategies with clear entry/exit rules and risk parameters. The Strategist serves as the design arm of the trading team, responsible for creating systematic trading strategies that can be consistently replicated and optimized. It focuses on turning market insights into executable strategies with defined rules, parameters, and risk controls that can be backtested and deployed.

## When to Use

**Trigger phrases:**
- "trading strategist"
- "Design and backtest trading strategies using technical indicators, fundamental a"

- Creating new trading strategies based on market analysis or hypotheses
- Defining precise entry and exit conditions for strategy trading
- Optimizing strategy parameters using historical backtesting
- Testing strategies across different market regimes (bull, bear, sideways)
- Documenting strategy rules and parameters in Notion
- Generating strategy performance metrics and Sharpe ratios
- Maintaining strategy version history and change tracking

## Strategy Design Pipeline

The strategy design pipeline defines entry/exit rules, runs scenario analysis, optimizes parameters, and documents strategies in Notion.

### 1. Define Entry Rules

Create comprehensive entry rule sets:

```typescript
const entryRules = {
  trend: "price > SMA(20)",
  momentum: "RSI(14) < 30",
  volatility: "ATR(14) < 20",
  volume: "volume > SMA(20, volume) * 1.5"
};

const strategy = {
  name: "RSI Reversal",
  entry: entryRules,
  exit: {
    stopLoss: "entry - 2 * ATR(14)",
    takeProfit: "entry + 3 * ATR(14)"
  },
  riskPerTrade: 0.02
};

await notion.createPage("Trading Strategies", strategy);
```

### 2. Scenario Analysis

Test strategy performance across different market conditions:

```typescript
const scenarios = [
  { name: "Bull Market", data: await getData("2020-2021") },
  { name: "Bear Market", data: await getData("2022-2022") },
  { name: "Sideways", data: await getData("2023-2023") }
];

for (const scenario of scenarios) {
  const result = await backtest(strategy, scenario.data);
  console.log(`${scenario.name}: ${result.sharpe}`);
}
```

### 3. Parameter Optimization

Systematically optimize strategy parameters:

```typescript
const params = {
  rsiPeriod: [10, 14, 20],
  rsiOverbought: [60, 70, 80],
  rsiOversold: [20, 30, 40]
};

const results = [];
for (const p of gridSearch(params)) {
  const result = await backtest(strategy.set(p), data);
  results.push({ params: p, sharpe: result.sharpe });
}

const best = results.sort((a, b) => b.sharpe - a.sharpe)[0];
console.log(`Best params: ${JSON.stringify(best.params)}`);
```

### 4. Generate Strategy Report

Create comprehensive strategy documentation:

```typescript
const strategyReport = {
  name: "RSI Reversal Strategy",
  description: "Mean reversion strategy for XAUUSD",
  entryRules: entryRules,
  exitRules: strategy.exit,
  parameters: {
    rsiPeriod: 14,
    overbought: 70,
    oversold: 30,
    atrPeriod: 14
  },
  backtestResults: {
    sharpe: 1.2,
    winRate: 0.60,
    profitFactor: 1.8
  },
  riskControls: {
    maxDrawdown: 0.15,
    riskPerTrade: 0.02
  }
};

await notion.createPage("Strategy Documentation", strategyReport);
```

### 5. Strategy Backtest

Run comprehensive backtest with full metrics:

```typescript
const backtestResult = await backtest(strategy, historicalData, {
  initialBalance: 10000,
  commission: 0.0001,
  slippage: 0.5
});

console.table({
  totalTrades: backtestResult.totalTrades,
  winRate: backtestResult.winRate,
  profitFactor: backtestResult.profitFactor,
  sharpe: backtestResult.sharpe,
  maxDrawdown: backtestResult.maxDrawdown
});
```

## When NOT to Use

- Task is about portfolio management, not trading (use portfolio skills)
- Task is about financial analysis (use analysis skills)
- You need to analyze trade results (use analytics skills)
- Task is about risk management (use risk skills)
- You don't have trading capital
- Task requires financial advice (consult advisors)

## Risk Controls & Verification

### Red Flags

- **Strategy parameters produce overfitting**: Strategy too closely tuned to specific historical data; test on out-of-sample data and reduce parameter complexity
- **Entry rules too complex or contradictory**: Strategy may be too complicated to execute reliably; simplify to essential rules
- **Backtest results inconsistent across scenarios**: Strategy may not be robust; identify scenario-specific weaknesses
- **Sharpe ratio negative or below 0.5**: Strategy not compensating for risk; reject or significantly modify before deployment
- **Profit factor below 1.3**: Strategy not generating sufficient return relative to losses; review risk/reward ratios
- **Drawdown exceeds acceptable threshold (>20%)**: Position sizing or risk management may need adjustment; reduce position sizes or tighten stop losses
- **Strategy parameters frequently need adjustment**: Market regime dependency too high; implement dynamic parameter adaptation

### Verification Checklist

#### Strategy Design Verification
- [ ] Entry rules clearly defined and executable
- [ ] Exit rules properly implemented with stop loss and take profit
- [ ] Parameters quantified with specific values
- [ ] Risk controls documented and configured

#### Backtest Verification
- [ ] Historical data quality validated for backtest period
- [ ] Backtest includes realistic slippage and commission
- [ ] All trades in backtest execute as expected
- [ ] Metrics match expected performance ranges

#### Optimization Verification
- [ ] Grid search covers reasonable parameter range
- [ ] Optimization tested on out-of-sample data
- [ ] Best parameters validated with walk-forward analysis
- [ ] No data snooping bias in optimization process

#### Scenario Testing Verification
- [ ] Strategy tested across bull, bear, and sideways markets
- [ ] Scenario results documented and compared
- [ ] Strategy weaknesses identified for specific scenarios
- [ ] Adjustments made for scenario-specific performance

#### Documentation Verification
- [ ] Notion strategy page includes all rules and parameters
- [ ] Backtest results documented with full metrics
- [ ] Risk controls clearly specified
- [ ] Documentation reviewed and approved by trading team


## Referenced Strategies

The following strategy-level skills are maintained alongside this skill as sub-references for specific strategy implementations:

| Skill | Focus | Primary Signals |
|---|---|---|
| [AlphaEar Strategy](../alphaear-strategy/SKILL.md) | Multi-factor entry/exit scoring | Momentum, volume, sentiment |
| [Investing Algorithm Framework](../investing-algorithm-framework/SKILL.md) | Algorithmic strategy development | Backtesting, signal gen, portfolio opt |
| [Polymarket Fast Loop](../polymarket-fast-loop/SKILL.md) | BTC sprint/fast markets | CEX price momentum (Simmer) |
| [Polymarket Weather Trader](../polymarket-weather-trader/SKILL.md) | Temperature prediction markets | NOAA forecasts (Simmer) |
| [XAUUSD Asia 7-Candle](../xauusd-asia-7c-breakout/SKILL.md) | Gold Asia session breakout | 7-candle HH/LL breakout |

## Anti-Rationalization Table

|Excuse|Truth|
|---|---|
|"I need more data first"|5 years of daily data is enough to start|
|"Backtesting is just curve-fitting"|Walk-forward + out-of-sample validation prevents this|
|"I'll trade when the strategy is perfect"|No strategy survives first contact with live markets|

## Output Format

On completion: "Strategy [name] - Sharpe: [N], PF: [N], Win%: [N]%, MaxDD: [N]%, Status: [PASS/FAIL]"


## Workflow

1. **Discover** — Identify revenue streams matching your assets and constraints
2. **Validate** — Quick test each stream with minimum viable effort
3. **Select** — Rank by expected value / time-to-revenue ratio
4. **Execute** — Deploy using strategy design pipeline
5. **Monitor** — Track leading indicators, adjust allocation
6. **Scale** — Double down on winners, kill losers

## Verification

All strategies must pass verification before live deployment:
- Strategy design verified: entry/exit rules defined, parameters quantified, risk controls documented
- Backtest verified: quality data, realistic slippage/commission, metrics in expected ranges
- Optimization verified: out-of-sample testing, walk-forward analysis, no data snooping
- Scenario testing verified: regime stress tests, correlation analysis, tail risk assessment
- Live trading verified: position sizing, risk limits, emergency stops configured

## Process

1. **Discover** — Identify revenue streams matching your assets and constraints
2. **Validate** — Quick test each stream with minimum viable effort
3. **Select** — Rank by expected value / time-to-revenue ratio
4. **Execute** — Deploy using strategy design pipeline
5. **Monitor** — Track leading indicators, adjust allocation
6. **Scale** — Double down on winners, kill losers
