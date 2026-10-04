---
name: tevm-actions
description: Core Tevm actions for contract calls, mining, and state manipulation. Use when executing EVM operations with Tevm.
---

# Tevm Actions

Import from `tevm/actions`:

```typescript
import { 
  tevmCall,
  tevmMine,
  tevmGetAccount,
  tevmSetAccount,
  tevmDeal,
  tevmContract,
  tevmDeploy
} from 'tevm/actions'
```

## tevmCall

```typescript
const result = await tevmCall(node, {
  to: '0x123...',
  data: '0x...',       // calldata
  value: 0n,           // ETH value
  caller: '0x...',     // msg.sender
  gasLimit: 3000000n
})
```

## tevmContract (High-level)

```typescript
import { encodeFunctionData, decodeFunctionResult } from 'viem'

const result = await tevmContract(node, {
  abi,
  address: contractAddress,
  functionName: 'transfer',
  args: [to, amount]
})
```

## tevmMine

```typescript
// Mine pending transactions
await tevmMine(node)

// Mine specific number of blocks
await tevmMine(node, { blocks: 5 })
```

## tevmGetAccount

```typescript
const account = await tevmGetAccount(node, {
  address: '0x...',
  blockTag: 'latest',
  returnStorage: true  // optional
})
```

## tevmSetAccount

```typescript
await tevmSetAccount(node, {
  address: '0x...',
  balance: parseEther('10'),
  nonce: 5n,
  deployedBytecode: '0x...',
  state: {
    [slot]: value
  }
})
```

## tevmDeal (Fund Accounts)

```typescript
// Native ETH
await tevmDeal(node, {
  account: '0x...',
  amount: parseEther('100')
})

// ERC20 tokens
await tevmDeal(node, {
  erc20: '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', // USDC
  account: '0x...',
  amount: 1000000n
})
```
