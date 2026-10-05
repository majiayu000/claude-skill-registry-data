---
description: Configure and claim creator fee sharing on Pump.fun tokens
---

# PumpFun Fee Sharing

Set up, manage, and claim creator fee sharing on Pump.fun tokens. Supports up to 10 shareholders with configurable basis point splits.

## Prerequisites

- Token creator wallet
- `HELIUS_RPC_URL` configured
- Token must be active (bonding curve or graduated)

## Fee Sharing Setup

### 1. Create Fee Sharing Config

```typescript
import { PUMP_SDK } from "solanaos";

const createConfigIx = await PUMP_SDK.createFeeSharingConfig({
  creator: wallet.publicKey,
  mint: tokenMint,
  pool: null, // null for pre-graduation tokens
});
```

### 2. Set Shareholders

Shares must total exactly **10,000 BPS** (100%). Maximum **10 shareholders**.

```typescript
const updateIx = await PUMP_SDK.updateFeeShares({
  authority: wallet.publicKey,
  mint: tokenMint,
  currentShareholders: [wallet.publicKey],
  newShareholders: [
    { address: wallet.publicKey, shareBps: 7000 },           // 70%
    { address: new PublicKey("Partner..."), shareBps: 2000 }, // 20%
    { address: new PublicKey("Dev..."), shareBps: 1000 },     // 10%
  ],
});
```

### 3. Claim Accumulated Fees

```typescript
const sdk = new OnlinePumpSdk(connection);
const claimResult = await sdk.distributeCreatorFees({
  mint: tokenMint,
  creator: wallet.publicKey,
});
```

## Fee Tier Reference

Fees are tiered by market cap:

| Market Cap (SOL) | Protocol Fee | Creator Fee |
|-------------------|-------------|-------------|
| < 100 | Higher | Lower |
| 100-1000 | Standard | Standard |
| > 1000 | Lower | Higher |

### Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `NoShareholdersError` | Empty array | Provide ≥1 shareholder |
| `TooManyShareholdersError` | >10 shareholders | Reduce to ≤10 |
| `ZeroShareError` | Share ≤ 0 | Set positive values |
| `InvalidShareTotalError` | Sum ≠ 10,000 | Ensure total = 10,000 BPS |
| `DuplicateShareholderError` | Same address twice | Remove duplicates |

## Token Incentives

Track unclaimed $PUMP reward tokens:

```typescript
import { totalUnclaimedTokens, currentDayTokens } from "solanaos";

const unclaimed = totalUnclaimedTokens(userVolumeAccumulator, globalVolumeAccumulator);
const todayTokens = currentDayTokens(globalVolumeAccumulator);
```

## Agent Integration

The `fee-claimer` agent role uses this skill to automatically monitor and claim accumulated creator fees across all managed tokens.
