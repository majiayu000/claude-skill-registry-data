---
name: trading-executor
description: Use when execute trades via API with position sizing, order management,
  and slippage monitoring. Use when placing orders on exchanges.
domain: trading
author: oyi77
license: Apache-2.0
subdomain: trading
tags:
- algorithms
- api
- executor
- markets
- monitoring
- trading
allowed-tools:
- Bash(trading:*)
- MCP(mt5:*)
- MCP(slack:*)
- fs
- network
version: 1.0.0
category: trading
---


# Trading Executor

## Overview

Execute trades on broker with proper slippage checks and safe abort procedures. The Executor serves as the final gatekeeper in the trading pipeline, ensuring all orders are placed only under acceptable market conditions with proper validation of execution quality. It implements dry-run testing, real-time slippage monitoring, and intelligent abort mechanisms to prevent poor executions.

## When to Use

**Trigger phrases:**
- "trading executor"
- "Placing market or limit orders on any supported broker (MT5, MT4, CCXT)"
- "Validating slippage before confirming trade execution"
- "Implementing safe abort procedures when market conditions deteriorate"


- Placing market or limit orders on any supported broker (MT5, MT4, CCXT)
- Validating slippage before confirming trade execution
- Implementing safe abort procedures when market conditions deteriorate
- Handling partial fills and monitoring fill completeness
- Integrating execution results with notification systems (Slack, Notion)
- Running dry-run simulations to test order placement without risk
- Managing order lifecycle from placement to confirmation

## The Process

The execution pipeline follows five stages: dry-run validation, order placement, market condition checks, partial fill handling, and safe abort procedures.


### 1. Dry-Run Order Placement (Recommended)

Always run a dry-run first to validate order parameters and check slippage:

```typescript
const dryRun = await broker.order({
  symbol: "XAUUSD",
  type: "market",
  side: "buy",
  volume: 0.1,
  dryRun: true
});

console.log(`Slippage: ${dryRun.slippage} pips`);

if (dryRun.slippage > 2) {
  return { executed: false, reason: "Excessive slippage" };
}
```

### 2. Place Real Order with Validation

After dry-run approval, place the actual order:

```typescript
const result = await broker.order({
  symbol: "XAUUSD",
  type: "market",
  side: "buy",
  volume: 0.1
});

await slack.notify("#trades", `Filled: ${result.ticket}`);
```

### 3. Check Market Conditions Before Execution

Implement comprehensive condition checks before any trade:

```typescript
const conditions = await checkMarketConditions();

if (conditions.spread > 30) {
  await slack.alert({
    channel: "#trading-alerts",
    text: `Spread too wide: ${conditions.spread} pips`
  });
  return { executed: false, reason: "Wide spread" };
}

if (conditions.volume < 100) {
  return { executed: false, reason: "Low liquidity" };
}
```

### 4. Handle Partial Fills

Monitor order status and handle partial fills appropriately:

```typescript
const timeout = 30000; // 30 seconds
const start = Date.now();

while (Date.now() - start < timeout) {
  const status = await broker.getOrderStatus(order.ticket);
  
  if (status.filled === status.requested) {
    return { success: true, fill: status };
  }
  
  if (status.partial > 0) {
    console.log(`Partial fill: ${status.partial}%`);
    // Implement partial fill handling logic
  }
}
```

### 5. Implement Safe Abort Procedures

Abort orders on abnormal conditions:

```typescript
if (abnormalConditionsDetected) {
  await broker.cancelOrder(order.ticket);
  await slack.alert({ channel: "#trading-alerts", text: "Order aborted" });
  return { executed: false, reason: "Abnormal conditions" };
}
```

## When NOT to Use

- Task is about portfolio management, not trading (use portfolio skills)
- Task is about financial analysis (use analysis skills)
- You need to analyze trade results (use analytics skills)
- Task is about risk management (use risk skills)
- You don't have trading capital
- Task requires financial advice (consult advisors)


## Red Flags

- **Excessive slippage detected (>2 pips)**: Broker is offering poor execution quality; abort trade and consider switching brokers or waiting for better conditions
- **Order confirmation delayed beyond timeout**: Network or broker API issues; abort and retry with increased timeout or manual intervention
- **Partial fill followed by cancellation**: Broker system issues; abort remaining fills and investigate cause
- **Price movement after order placement indicating manipulation**: Market integrity concern; abort and report to trading team
- **Multiple failed order attempts**: Systemic connectivity or validation issues; enter alert state for human review
- **Fill quality worse than backtested expectations**: Environment differences (real vs simulated); review and adjust execution parameters

## Verification

Verification covers pre-execution checks, order fill confirmation, post-execution logging, and error handling completeness.


### Pre-Execution Verification
- [ ] Dry-run completed successfully with acceptable slippage (<2 pips)
- [ ] Market condition checks passed (spread, volume, liquidity)
- [ ] Order parameters validated (symbol, side, volume, type)
- [ ] Broker API connection stable and responsive

### Order Execution Verification
- [ ] Order filled within expected time frame (typically <30 seconds)
- [ ] Actual execution price matches expected (slippage within tolerance)
- [ ] Fill quantity matches requested volume
- [ ] Order ticket ID recorded for tracking

### Post-Execution Verification
- [ ] Slack notification sent to configured channel with order details
- [ ] Order status recorded in Notion trade log
- [ ] Position appears in broker account within expected timeframe
- [ ] No partial fills or abnormal fill patterns detected

### Error Handling Verification
- [ ] Abnormal conditions detected and handled gracefully
- [ ] Orders aborted on spread exceeding threshold
- [ ] Orders aborted on volume drying up
- [ ] Partial fills handled with clear escalation path

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I will cut losses later" | Later never comes. Set stop-losses before entering any trade. |
| "This time is different" | It never is. Follow your strategy, not your emotions. |
| "I do not need to journal" | Journaling reveals patterns in your behavior. Track every trade. |