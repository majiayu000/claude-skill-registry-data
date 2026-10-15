---
name: finance-ml
description: >
  ML-driven financial analysis patterns. Price prediction models, portfolio optimization,
  risk metrics, technical indicators, backtesting methodology, and financial data processing.
  Use when building trading strategies, analyzing financial data, or integrating with Aster DEX.
---

# Finance ML

Use this skill for machine learning work on financial time series, trading signals, risk analysis, portfolio allocation, backtests, and Aster DEX signal support.

Keep the main workflow cautious: financial ML is easy to overfit, leak future data into features, and mistake backtest results for deployable trading evidence.

## How To Use

- `/finance-ml`
  Apply financial ML patterns to the current analysis.

- `/finance-ml <task>`
  Guide a specific task: prediction, optimization, backtest, indicators, risk, or Aster DEX signal review.

## When To Apply

Use this skill when:

- building price prediction or classification models;
- calculating technical indicators or engineered features;
- designing trading strategies or portfolio allocation logic;
- computing risk metrics and drawdown behavior;
- running backtests, walk-forward validation, or out-of-sample checks;
- processing financial statements, bank data, market data, or crypto exchange data;
- connecting ML signals to Aster DEX trading workflows.

Do not use this skill to give personalized financial advice or to execute trades without the explicit approval required by the active safety rules.

## Required Inputs

Ask for or infer the smallest safe input set:

- Objective: forecast, classification signal, allocation, risk report, anomaly detection, or trading decision support.
- Asset universe, symbols, venue, instrument type, timeframe, and bar interval.
- Data source, data fields, date range, timezone, corporate actions, and missing-data policy.
- Target definition: return horizon, direction label, volatility target, drawdown threshold, or allocation goal.
- Constraints: transaction costs, slippage, leverage, shorting, liquidity, max position size, max drawdown, regulatory or policy limits.
- Validation plan: train/test split, walk-forward windows, baseline, benchmark, and metrics.
- Execution scope: analysis only, paper trading, or live-trading proposal requiring approval.

Never invent market data, account balances, positions, validation output, or execution results.

## Core Workflow

1. Define the financial objective and the decision the model is meant to support.
2. Confirm data scope, frequency, horizon, and point-in-time availability.
3. Select a model family based on target type, data volume, feature shape, and interpretability needs.
4. Build features without look-ahead leakage; align labels after features and split by time.
5. Choose baselines before complex models.
6. Backtest with realistic costs, slippage, liquidity, and position sizing.
7. Validate out of sample with walk-forward or time-series splits.
8. Report risk metrics, failure modes, assumptions, and whether the result is analysis-only or trade-supporting.
9. For Aster DEX workflows, present signal, confidence, position sizing, and risk checks, then require user confirmation before any order action.

## Model Selection Logic

- Use statistical baselines such as ARIMA/GARCH for interpretable price or volatility forecasts with simpler structure.
- Use tree models such as Random Forest or XGBoost for tabular, feature-based direction, return, or ranking tasks.
- Use LSTM or other sequence models only when the sequence length, data volume, and validation plan justify the complexity.
- Use Transformers only for high-volume sequence or multimodal tasks where long-range dependencies matter and compute cost is acceptable.
- Use portfolio optimization when the target is allocation under expected return, covariance, risk, and constraint assumptions.
- Prefer the simplest model that beats a naive baseline after transaction costs and out-of-sample testing.

## Leakage, Risk, And Compliance Constraints

- Split by time, not random rows, for time-series prediction.
- Build features using only information available at the decision timestamp.
- Account for survivorship bias, corporate actions, stale prices, missing bars, and timestamp alignment.
- Include transaction costs, spread, slippage, liquidity, and market-impact assumptions in trading backtests.
- Treat high Sharpe, low drawdown, or high hit rate without out-of-sample evidence as suspect.
- Never commit API keys, account identifiers, private market feeds, credentials, position records, or local files.
- Do not present model output as personalized financial advice.
- Do not place, modify, or cancel orders without explicit approval and the active trading safety gates.

## Validation Gates

Use checks appropriate to the task:

- Baseline comparison: naive return, buy-and-hold, equal-weight, or simple technical-rule baseline.
- Time-aware split: train, validation, test, and walk-forward windows.
- Leakage audit: feature timestamp, target horizon, rolling windows, and scaler fit boundaries.
- Backtest realism: costs, slippage, liquidity, fills, position limits, and rejected orders.
- Risk metrics: volatility, Sharpe, Sortino, max drawdown, VaR, Calmar, turnover, and exposure.
- Stress checks: regime split, drawdown period, fee sensitivity, and parameter sensitivity.
- Reproducibility: data source, date range, seed, library versions, and exact commands when available.

## Output Expectations

Return:

- Objective, asset universe, time horizon, and data source.
- Model or method choice and why it fits the target.
- Feature and label summary with leakage controls.
- Backtest and validation approach.
- Risk metrics and interpretation.
- Trade or allocation constraints, if applicable.
- Evidence from commands, calculations, plots, or inspected outputs.
- Clear limitations, failure modes, and next checks.

## Minimal Examples

Model-routing example:

```text
Task: predict next-day direction from daily OHLCV and indicators.
Default choice: XGBoost or Random Forest baseline before LSTM.
Validation: walk-forward split with transaction costs and buy-and-hold benchmark.
```

Aster DEX signal support:

```text
Signal package: BUY / SELL / HOLD, confidence, position-size proposal, risk metrics.
Required gate: user confirmation before any order action.
```

## Reference Map

- [Finance ML workflow](references/ml-workflow.md)
- [Features, labeling, and data](references/features-labeling-and-data.md)
- [Models and selection](references/models-and-selection.md)
- [Backtesting, risk, and validation](references/backtesting-risk-and-validation.md)
- [Examples and troubleshooting](references/examples-and-troubleshooting.md)

## Cross-References

- **aster-trading** skill: MCP tools for Aster DEX.
- **data-analyst** agent: statistical analysis and visualization.
- **docs/SECURITY_PLAYBOOK.md**: DeFi trading security rules.
- **xlsx** skill: spreadsheet output for reports.
- **docs/FINANCE_ML_STACK.md**: broader finance ML reference.
