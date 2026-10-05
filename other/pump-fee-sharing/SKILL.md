---
name: pump-fee-sharing
description: "Configure and distribute creator fees to multiple shareholders using the PumpFees program with BPS-based share allocation, admin management, and cross-program fee consolidation for graduated tokens."
metadata:
  openclaw:
    homepage: https://github.com/nirholas/pump-fun-sdk
    requires:
      env:
        - SOLANA_RPC_URL
---

# Fee Sharing — Multi-Party Creator Fee Distribution

Configure and manage creator fee sharing — allowing token creators to distribute accumulated trading fees to multiple shareholders using the PumpFees program with BPS-based share allocation.

## Architecture

```
    Token Creator
         │
         ▼
    ┌─────────────────────┐
    │  SharingConfig PDA  │
    │  (PumpFees program) │
    │  shareholders:       │
    │    [{ addr, bps }]   │
    └─────────────────────┘
         │ distribute
    ┌────┴────┬────┬────┐
    │  40%    │ 30%│ 20%│ 10%
    ▼         ▼    ▼    ▼
   User1   User2 User3 User4
```

## Workflow

### 1. Create Fee Sharing Config

```typescript
const ix = PUMP_SDK.createFeeSharingConfig({
    creator, mint, pool, payer,
    shareholders: [
        { address: userA, shareBps: 5000 },  // 50%
        { address: userB, shareBps: 3000 },  // 30%
        { address: userC, shareBps: 2000 },  // 20%
    ]
});
```

### 2. Update Shareholders

```typescript
const ix = PUMP_SDK.updateFeeShares({
    creator, mint,
    shareholders: [
        { address: userA, shareBps: 4000 },
        { address: userD, shareBps: 3000 },
        { address: userB, shareBps: 3000 },
    ]
});
```

### 3. Distribute Fees

```typescript
const { instructions, isGraduated } = await onlineSdk.buildDistributeCreatorFeesInstructions(mint);
// For graduated: transferCreatorFeesToPump + distributeCreatorFees
// For non-graduated: distributeCreatorFees only
```

## Validation Rules

| Rule | Error Class |
|------|------------|
| At least 1 shareholder | `NoShareholdersError` |
| Maximum 10 shareholders | `TooManyShareholdersError` |
| No zero-share entries | `ZeroShareError` |
| Shares sum to 10,000 BPS | `InvalidShareTotalError` |
| No duplicate addresses | `DuplicateShareholderError` |
| Graduated tokens need pool | `PoolRequiredForGraduatedError` |

## Cross-Program Fee Consolidation

```
Trading fees ──► AMM Creator Vault (PumpAMM)
                        │
                transferCreatorFeesToPump
                        │
                        ▼
                Pump Creator Vault (Pump)
                        │
                distributeCreatorFees
                        │
                        ▼
                Shareholders (proportional)
```

## Patterns to Follow

- Validate shareholder arrays before sending: max 10, sum = 10,000 BPS, no duplicates, no zero shares
- Use `BothPrograms` methods when aggregating across Pump + PumpAMM
- Check `isGraduated` to determine if AMM fee consolidation is needed
- Check `adminRevoked` before attempting to update shareholders

## Common Pitfalls

- Shares must total exactly 10,000 BPS (100%) — not 100, not 1,000,000
- Graduated tokens require the `pool` parameter for config creation
- Two separate creator vaults exist with different PDA seeds (hyphen vs underscore)
- `updateFeeShares` will fail on-chain if `adminRevoked === true`
- Basis points use integer arithmetic — fractional bps are not possible

