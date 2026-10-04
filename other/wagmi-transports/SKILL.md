---
name: wagmi-transports
description: HTTP and WebSocket transports for blockchain connectivity. Use when configuring network connections.
---

# Wagmi Transports

Network connection setups.

## HTTP Transport

```typescript
import { createConfig, http } from '@wagmi/core'
import { mainnet, sepolia } from '@wagmi/core/chains'

export const config = createConfig({
  chains: [mainnet, sepolia],
  transports: {
    [mainnet.id]: http('https://mainnet.example.com'),
    [sepolia.id]: http('https://sepolia.example.com'),
  },
})

// With options
[mainnet.id]: http({
  url: 'https://mainnet.example.com',
  fetchOptions: {
    headers: { 'X-API-KEY': '...' }
  }
})
```

## WebSocket Transport

```typescript
import { createConfig, webSocket } from '@wagmi/core'
import { mainnet, sepolia } from '@wagmi/core/chains'

export const config = createConfig({
  chains: [mainnet, sepolia],
  transports: {
    [mainnet.id]: webSocket('wss://mainnet.example.com'),
    [sepolia.id]: webSocket('wss://sepolia.example.com'),
  },
})
```

## Fallback Transport

Multiple RPC URLs with fallback:

```typescript
import { createConfig, fallback, http } from '@wagmi/core'
import { mainnet } from '@wagmi/core/chains'

export const config = createConfig({
  chains: [mainnet],
  transports: {
    [mainnet.id]: fallback([
      http('https://mainnet.example.com'),
      http('https://backup.example.com'),
      http('https://another-backup.com')
    ], {
      timeout: 10_000,
      retryCount: 3,
      retryWait: async (retries) => Math.min(1000 * 2 ** retries, 5000)
    })
  },
})
```

## Custom Transport (EIP-1193)

```typescript
import { createConfig, custom } from '@wagmi/core'
import { mainnet } from '@wagmi/core/chains'

export const config = createConfig({
  chains: [mainnet],
  transports: {
    [mainnet.id]: custom(window.ethereum)
  },
})
```

## Batch with Multicall

Wagmi enables multicall batching by default:

```typescript
export const config = createConfig({
  chains: [mainnet, sepolia],
  batch: {
    multicall: {
      batchSize: 1024,  // calls per batch
      wait: 10          // ms to wait before sending
    }
  },
  transports: { ... }
})
```

## Polling Configuration

```typescript
export const config = createConfig({
  chains: [mainnet],
  pollingInterval: 4_000,   // 4 seconds
  cacheTime: 4_000,       // 4 seconds cache
  transports: { ... }
})
```
