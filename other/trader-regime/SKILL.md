---
name: trader-regime
description: Detect current market regime using npx neural-trader — bull/bear/ranging/volatile classification with recommended strategy. Use when the user asks about market conditions, wants to pick a strategy for current conditions, or before running a backtest/signal that should be regime-aware.
allowed-tools: Bash Read mcp__claude-flow__memory_store mcp__claude-flow__memory_search mcp__claude-flow__neural_predict
argument-hint: "[--symbol SPY] [--symbols AAPL,MSFT]"
---
Detect the current market regime using neural-trader's regime detection engine.

Steps:
1. Ensure neural-trader is available:
   `npm ls neural-trader 2>/dev/null || npm install --ignore-scripts neural-trader`
2. Run regime detection:
   ```bash
   npx neural-trader --regime-detect --symbol TICKER
   ```
   For multiple symbols:
   ```bash
   npx neural-trader --regime-detect --symbols "AAPL,MSFT,GOOGL,AMZN"
   ```
3. Get technical indicators for context:
   ```bash
   npx neural-trader --symbol TICKER --indicators rsi,macd,bollinger,adx,atr
   ```
4. Use SONA for regime prediction:
   `mcp__claude-flow__neural_predict({ input: "indicators: RSI=X, ADX=Y, VIX=Z" })`
5. Search for similar historical regimes:
   `mcp__claude-flow__memory_search({ query: "regime similar to CURRENT", namespace: "trading-analysis" })`
6. Present: regime classification, confidence, recommended strategy type, historical precedents
7. Store analysis:
   `mcp__claude-flow__memory_store({ key: "regime-DATE", value: "REGIME_ANALYSIS", namespace: "trading-analysis" })`
