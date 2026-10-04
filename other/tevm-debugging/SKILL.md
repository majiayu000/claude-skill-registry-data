---
name: tevm-debugging
description: Debug transactions with EVM tracing, gas profiling, and error handling. Use when investigating contract behavior or test failures.
---

# Tevm Debugging

## Basic Tracing

```typescript
const trace = { steps: [], errors: [] }

const result = await client.tevmCall({
  to: contractAddress,
  data: '0x...',
  
  onStep: (step, next) => {
    trace.steps.push({
      pc: step.pc,
      opcode: step.opcode.name,
      stack: step.stack.map(s => s.toString(16)),
      depth: step.depth
    })
    next?.()
  },
  
  onAfterMessage: (result, next) => {
    if (result.execResult.exceptionError) {
      trace.errors.push({
        error: result.execResult.exceptionError.error,
        returnData: result.execResult.returnValue.toString('hex')
      })
    }
    next?.()
  }
})
```

## Gas Profiling

```typescript
const profile = {
  opcodes: new Map(),
  totalGas: 0n,
  storageWrites: 0,
  storageReads: 0
}

await client.tevmCall({
  to: contractAddress,
  data: '0x...',
  
  onStep: (step, next) => {
    const opName = step.opcode.name
    
    // Track storage operations
    if (opName === 'SSTORE') profile.storageWrites++
    if (opName === 'SLOAD') profile.storageReads++
    
    // Track gas by opcode
    const gasCost = BigInt(step.opcode.fee)
    const stats = profile.opcodes.get(opName) || { count: 0, gas: 0n }
    stats.count++
    stats.gas += gasCost
    profile.opcodes.set(opName, stats)
    profile.totalGas += gasCost
    
    next?.()
  }
})

console.log('Storage writes:', profile.storageWrites)
console.log('Gas by opcode:', profile.opcodes)
```

## Error Handling

```typescript
const result = await client.tevmCall({
  to: contractAddress,
  data: '0x...',
  
  onAfterMessage: (result, next) => {
    const err = result.execResult.exceptionError
    if (!err) return next?.()
    
    switch (err.error) {
      case 'revert':
        console.log('Reverted:', result.execResult.returnValue)
        break
      case 'out of gas':
        console.log('Out of gas')
        break
      case 'invalid opcode':
        console.log('Invalid opcode')
        break
    }
    next?.()
  }
})

// Check result
if (!result.errors && result.execResult.exceptionError) {
  console.log('Failed:', result.execResult.exceptionError.error)
}
```

## Time Manipulation

```typescript
// Set next block timestamp
await client.setNextBlockTimestamp(Date.now() + 3600000) // 1 hour ahead

// Mine block with that timestamp
await client.mine({ blocks: 1 })

// Jump forward (via setAccount)
await client.setAccount({
  address: '0x...', // special timestamp address
  balance: BigInt(futureTimestamp)
})
```

## State Snapshots

```typescript
// Save state
const snap1 = await client.snapshot()

// Make changes
await contract.transfer(to, amount)

// Check state
const balance = await contract.balances(user)

// Revert if needed
await client.revert({ id: snap1 })
```

## Access VM Directly

```typescript
const vm = await client.getVm()

const result = await vm.runTx({
  tx,
  block,
  skipNonce: true,
  skipBalance: true
})
```
