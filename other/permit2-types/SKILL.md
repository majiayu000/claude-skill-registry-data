---
name: permit2-types
description: TypeScript type references for Permit2 SDK. Use when writing TypeScript code with Permit2.
---

# Permit2 TypeScript Types

Reference types from `@uniswap/permit2-sdk`.

## SignatureTransfer Types

```typescript
import { SignatureTransfer } from '@uniswap/permit2-sdk'
```

### PermitTransferFrom

```typescript
interface PermitTransferFrom {
  permitted: {
    token: string
    amount: bigint
  }
  spender: string
  nonce: bigint
  deadline: bigint
}
```

### Witness

```typescript
interface Witness {
  witness: any
  witnessTypeName: string
  witnessType: Record<string, TypedDataField[]>
}
```

### PermitTransferFromData

```typescript
interface PermitTransferFromData {
  domain: {
    name: 'Permit2'
    chainId: number
    verifyingContract: string
  }
  types: Record<string, TypedDataField[]>
  values: PermitTransferFrom
}
```

## AllowanceTransfer Types

```typescript
import { AllowanceTransfer } from '@uniswap/permit2-sdk'
```

### PermitSingle

```typescript
interface PermitSingle {
  details: {
    token: string
    amount: bigint
    expiration: bigint
    nonce: bigint
  }
  spender: string
  sigDeadline: bigint
}
```

## Constants

```typescript
import { PERMIT2_ADDRESS, MaxUint48, MaxUint160, MaxUint256 } from '@uniswap/permit2-sdk'

// Canonical address (same on all chains)
PERMIT2_ADDRESS // '0x000000000022D473030F116dDEE9F6B43aC78BA3'
```
