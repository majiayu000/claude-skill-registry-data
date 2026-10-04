---
name: wagmi-react-read
description: useReadContract hook for reading smart contract data. Use when querying contract view/pure functions in React.
---

# Wagmi-React Read

useReadContract and related hooks.

## Basic Read

```typescript
import { useReadContract } from 'wagmi'

const abi = [
  { type: 'function', name: 'balanceOf', stateMutability: 'view',
    inputs: [{ name: 'account', type: 'address' }],
    outputs: [{ name: 'balance', type: 'uint256' }]
  },
  { type: 'function', name: 'decimals', stateMutability: 'view',
    inputs: [],
    outputs: [{ name: '', type: 'uint8' }]
  }
] as const

function TokenBalance({ address, tokenAddress }) {
  const { data, isError, isLoading } = useReadContract({
    abi,
    address: tokenAddress,
    functionName: 'balanceOf',
    args: [address]
  })

  if (isLoading) return <div>Loading...</div>
  if (isError) return <div>Error</div>

  return <div>Balance: {data?.toString()}</div>
}
```

## Read with Watch

```typescript
// Auto-refetch when block changes
const { data } = useReadContract({
  abi,
  address,
  functionName: 'balanceOf',
  args: [address],
  watch: true
})
```

## Multiple Reads

```typescript
import { useReadContracts } from 'wagmi'

const { data } = useReadContracts({
  contracts: [
    { abi, address: tokenA, functionName: 'balanceOf', args: [user] },
    { abi, address: tokenB, functionName: 'balanceOf', args: [user] },
    { abi, address: tokenC, functionName: 'balanceOf', args: [user] },
  ]
})

const [balanceA, balanceB, balanceC] = data ?? []
```

## Query Options

```typescript
const { data } = useReadContract({
  abi,
  address,
  functionName: 'balanceOf',
  args: [address],
  query: {
    enabled: !!address && address !== '0x...',  // conditional
    staleTime: 60 * 1000,     // cache for 1 minute
    refetchInterval: 10000,    // poll every 10 seconds
  }
})
```

## Block Tag

```typescript
const { data } = useReadContract({
  abi,
  address,
  functionName: 'balanceOf',
  args: [address],
  blockTag: 'latest'  // 'latest', 'safe', 'finalized'
})
```

## Manual Refetch

```typescript
const { data, refetch, isRefetching } = useReadContract({ ... })

<button onClick={() => refetch()} disabled={isRefetching}>
  Refresh
</button>
```
