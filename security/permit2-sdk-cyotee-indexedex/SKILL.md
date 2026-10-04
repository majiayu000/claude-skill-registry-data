---
name: permit2-sdk
description: Uniswap Permit2 SDK for gasless token transfers in IndexedEx. Use when implementing swap/deposit/withdraw with signature-based or allowance-based authorization.
---

# Permit2 SDK for IndexedEx

Comprehensive guide for using Permit2 in the frontend for vault operations.

## Quick Start

```typescript
import { PERMIT2_ADDRESS, SignatureTransfer } from '@uniswap/permit2-sdk'
```

## Two Patterns

### 1. Signature Transfer (Recommended)

Gasless, no pre-approval needed beyond initial Permit2 allowance.

- **Skill**: `permit2-signature-transfer`
- **Use for**: One-time signatures per swap/deposit/withdraw
- **Security**: Signature bound to specific action via witness

### 2. Allowance Transfer

Persistent approvals - user approves once, protocol spends repeatedly.

- **Skill**: `permit2-allowance-transfer`
- **Use for**: Frequent trading, recurring deposits

## Exchange Types (Witness Context)

| Exchange | Selector | Witness Data |
|----------|----------|--------------|
| `exchangeIn` | 0x89d61912 | tokenIn, tokenOut, vault, amountIn |
| `exchangeOut` | 0x612d4427 | tokenIn, tokenOut, vault, amountOut, maxAmountIn |
| `swapSingleTokenExactOut` | (Balancer) | pool, tokenIn, tokenOut, amountOut |

## Key Topics

- **Nonce handling**: `permit2-nonce-management`
- **Wagmi integration**: `permit2-wagmi-integration`
- **TypeScript types**: `permit2-types`
- **Chain addresses**: `permit2-addresses`

## Example: Swap with Witness

```typescript
// Witness binds signature to this exact swap
const witness = {
  actionId: keccak256(encodePacked(
    ['address', 'address', 'address', 'uint256'],
    [tokenIn, tokenOut, vaultAddress, amountIn]
  ))
}

// Get permit data (EIP-712 ready)
const { domain, types, values } = SignatureTransfer.getPermitData(
  permit,           // amount, nonce, deadline
  PERMIT2_ADDRESS,
  chainId,
  { witness, witnessTypeName: 'Witness', witnessType: WITNESS_TYPE }
)

// User signs, then your contract calls Permit2
```
