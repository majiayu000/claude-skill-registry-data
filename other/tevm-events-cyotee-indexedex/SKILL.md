---
name: tevm-events
description: EVM step-by-step tracing for debugging contract execution. Use when debugging contracts or profiling gas usage.
---

# EVM Events

Monitor EVM execution at opcode level.

## Event Types

- `onStep` - Each EVM instruction
- `onNewContract` - Contract deployment
- `onBeforeMessage` - Before call execution
- `onAfterMessage` - After call execution

## Basic Usage

```typescript
const result = await client.tevmCall({
  to: contractAddress,
  data: '0x...',
  
  onStep: (step, next) => {
    console.log(`PC: ${step.pc}, Opcode: ${step.opcode.name}`)
    next?.()
  }
})
```

## InterpreterStep Properties

```typescript
interface InterpreterStep {
  pc: number                    // Program counter
  opcode: {
    name: string               // e.g., 'SSTORE', 'CALL'
    fee: number               // Gas cost
    dynamicFee?: bigint
  }
  gasLeft: bigint
  gasRefund: bigint
  stack: Uint8Array[]
  memory: Uint8Array
  depth: number                // Call depth
  address: Address             // Current contract
}
```

## Gas Profiling

```typescript
const profile = { opcodes: new Map(), totalGas: 0n }

await client.tevmCall({
  to: contractAddress,
  data: '0x...',
  
  onStep: (step, next) => {
    const gasCost = BigInt(step.opcode.fee)
    const stats = profile.opcodes.get(step.opcode.name) || { count: 0, total: 0n }
    stats.count++
    stats.total += gasCost
    profile.opcodes.set(step.opcode.name, stats)
    profile.totalGas += gasCost
    next?.()
  }
})

// Results
for (const [op, stats] of profile.opcodes) {
  console.log(`${op}: ${stats.count}x, ${stats.total}g`)
}
```

## Debugging Reverts

```typescript
await client.tevmCall({
  to: contractAddress,
  data: '0x...',
  
  onAfterMessage: (result, next) => {
    if (result.execResult.exceptionError) {
      console.log('Error:', result.execResult.exceptionError.error)
      console.log('Return:', result.execResult.returnValue)
    }
    next?.()
  }
})
```

## Mining Events

```typescript
await client.mine({
  blockCount: 1,
  
  onBlock: (block, next) => {
    console.log('Block:', block.header.number)
    next?.()
  },
  
  onReceipt: (receipt, blockHash, next) => {
    console.log('Tx:', receipt.transactionHash)
    next?.()
  },
  
  onLog: (log, receipt, next) => {
    console.log('Log:', log.address, log.topics)
    next?.()
  }
})
```
