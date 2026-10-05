---
description: Monitor bonding curves, graduation progress, and trade analytics on Pump.fun
---

# PumpFun Analytics

Monitor bonding curve state, calculate price impact, track graduation progress, and analyze token economics on the Pump.fun protocol.

## Prerequisites

- `HELIUS_RPC_URL` or `SOLANA_RPC_URL` configured
- `@coral-xyz/anchor` and `@solana/web3.js` available

## Capabilities

### 1. Bonding Curve State

Fetch the current state of any token's bonding curve:

```typescript
import { OnlinePumpSdk } from "solanaos";

const sdk = new OnlinePumpSdk(connection);
const summary = await sdk.fetchBondingCurveSummary(mint);

console.log("Market Cap:", summary.marketCap.toString());
console.log("Graduated:", summary.isGraduated);
console.log("Token Supply Remaining:", summary.tokensRemaining.toString());
```

### 2. Graduation Progress

Track how close a token is to graduating from the bonding curve to the AMM:

```typescript
import { getGraduationProgress } from "solanaos";

const progress = getGraduationProgress(bondingCurve, global);
console.log(`Progress: ${progress.progressBps / 100}%`);
console.log(`SOL accumulated: ${progress.solAccumulated.toString()}`);
console.log(`Tokens remaining: ${progress.tokensRemaining.toString()}`);
```

### 3. Price Impact Analysis

Calculate the price impact of a trade before executing:

```typescript
import { calculateBuyPriceImpact, calculateSellPriceImpact } from "solanaos";

const buyImpact = calculateBuyPriceImpact(bondingCurve, global, feeConfig, buyAmountLamports);
console.log(`Price impact: ${buyImpact.priceImpactBps / 100}%`);
console.log(`Effective price: ${buyImpact.effectivePrice.toString()}`);

const sellImpact = calculateSellPriceImpact(bondingCurve, global, feeConfig, sellTokenAmount);
console.log(`Price impact: ${sellImpact.priceImpactBps / 100}%`);
```

### 4. Token Price

Get the current buy and sell price per token:

```typescript
import { getTokenPrice } from "solanaos";

const price = getTokenPrice(bondingCurve, global, feeConfig);
console.log(`Buy price: ${price.buyPricePerToken.toString()} lamports`);
console.log(`Sell price: ${price.sellPricePerToken.toString()} lamports`);
```

### 5. Fee Tier Calculation

Calculate the current fee tier based on market cap:

```typescript
import { computeFeesBps, calculateFeeTier } from "solanaos";

const fees = computeFeesBps(global, feeConfig);
console.log(`Protocol fee: ${fees.protocolFeeBps} bps`);
console.log(`Creator fee: ${fees.creatorFeeBps} bps`);
```

### 6. Buy/Sell Quote

Calculate expected tokens for a given SOL amount:

```typescript
import { getBuyTokenAmountFromSolAmount, getSellSolAmountFromTokenAmount } from "solanaos";

const tokens = getBuyTokenAmountFromSolAmount({
  global, feeConfig,
  mintSupply: bondingCurve.tokenTotalSupply,
  bondingCurve,
  amount: solAmountLamports,
});

const sol = getSellSolAmountFromTokenAmount({
  global, feeConfig,
  mintSupply: bondingCurve.tokenTotalSupply,
  bondingCurve,
  amount: tokenAmount,
});
```

## Agent Integration

The OODA trading loop uses these analytics automatically during the **Observe** phase to pull bonding curve data into ClawVault KNOWN memory.
