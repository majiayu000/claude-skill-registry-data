---
description: Buy and sell tokens on Pump.fun bonding curves and AMM pools
---

# PumpFun Trading

Execute buy and sell trades on the Pump.fun protocol using the native Pump SDK. Supports both bonding curve trading (pre-graduation) and AMM pool trading (post-graduation).

## Prerequisites

- Funded Solana wallet via `solanaos birth`
- `HELIUS_RPC_URL` configured
- Understanding of bonding curve mechanics

## Trading Flow

### 1. Check Token State

Before trading, always check if the token is on the bonding curve or has graduated:

```typescript
const sdk = new OnlinePumpSdk(connection);
const summary = await sdk.fetchBondingCurveSummary(mint);

if (summary.isGraduated) {
  // Use AMM trading instructions
} else {
  // Use bonding curve trading instructions
}
```

### 2. Buy on Bonding Curve

```typescript
import { OnlinePumpSdk, getBuyTokenAmountFromSolAmount } from "solanaos";
import BN from "bn.js";

const sdk = new OnlinePumpSdk(connection);

// Fetch state
const [buyState, global, feeConfig] = await Promise.all([
  sdk.fetchBuyState(mint, user),
  sdk.fetchGlobal(),
  sdk.fetchFeeConfig(),
]);

// Calculate expected tokens
const solAmount = new BN(100_000_000); // 0.1 SOL
const expectedTokens = getBuyTokenAmountFromSolAmount({
  global, feeConfig,
  mintSupply: buyState.bondingCurve.tokenTotalSupply,
  bondingCurve: buyState.bondingCurve,
  amount: solAmount,
});

// Build instructions
const buyIxs = await sdk.buyInstructions({
  ...buyState, mint, user,
  amount: expectedTokens,
  solAmount,
  slippage: 0.05, // 5%
});
```

### 3. Sell on Bonding Curve

```typescript
import { getSellSolAmountFromTokenAmount } from "solanaos";

const [sellState, global, feeConfig] = await Promise.all([
  sdk.fetchSellState(mint, user),
  sdk.fetchGlobal(),
  sdk.fetchFeeConfig(),
]);

const tokenAmount = new BN(1_000_000_000);
const expectedSol = getSellSolAmountFromTokenAmount({
  global, feeConfig,
  mintSupply: sellState.bondingCurve.tokenTotalSupply,
  bondingCurve: sellState.bondingCurve,
  amount: tokenAmount,
});

const sellIxs = await sdk.sellInstructions({
  ...sellState, mint, user,
  amount: tokenAmount,
  solAmount: expectedSol,
  slippage: 0.05,
});
```

## Risk Management

| Control | Value |
|---------|-------|
| Always use slippage | 3-5% recommended |
| Check `bondingCurve.complete` | Before trading |
| Use `BN` for all amounts | Never use JS `number` |
| Max position per trade | Follow Kelly Criterion |
| Circuit breaker | -10% daily → pause 24h |

## Integration with Swarm

Swarm agents with the `sniper`, `momentum`, and `graduation` roles use this skill automatically via the OODA trading loop.
