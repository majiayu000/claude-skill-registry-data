---
name: tevm-setup
description: Initialize Tevm clients for in-memory or fork mode. Use when setting up Tevm for testing or local development.
---

# Tevm Setup

## createMemoryClient (Standalone)

```typescript
import { createMemoryClient } from 'tevm'

const client = createMemoryClient()
```

## createTevmNode (Fork Mode)

```typescript
import { createTevmNode, http } from 'tevm'

const node = createTevmNode({
  fork: {
    transport: http('https://mainnet.infura.io/v3/YOUR-KEY')
  }
})

await node.ready() // Wait for initialization
```

## createTevmTransport (Viem Integration)

```typescript
import { createTevmTransport } from 'tevm/memory-client'
import { createPublicClient, http } from 'viem'

const client = createPublicClient({
  chain: mainnet,
  transport: createTevmTransport()
})
```

## Configuration Options

```typescript
const client = createMemoryClient({
  // Mining behavior
  miningConfig: { type: 'auto' | 'manual' },
  
  // Logging
  logger: console,
  
  // Fork configuration
  fork: {
    transport: http('https://...'),
    blockNumber: 19000000n
  }
})
```

## With Ethers Provider

```typescript
import { createTevmNode } from 'tevm'
import { BrowserProvider } from 'ethers'
import { requestEip1193 } from 'tevm/decorators'

const node = createTevmNode().extend(requestEip1193())
const provider = new BrowserProvider(node)
```
