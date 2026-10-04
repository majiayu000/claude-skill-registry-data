---
name: wagmi-config
description: Wagmi createConfig setup with chains and transports. Use when configuring multi-chain support and network connections.
---

# Wagmi Config

Setup wagmi with chains and transports.

## Basic Config

```typescript
import { createConfig, http } from '@wagmi/core'
import { mainnet, sepolia, base } from '@wagmi/core/chains'

export const config = createConfig({
  chains: [mainnet, sepolia, base],
  transports: {
    [mainnet.id]: http('https://mainnet.example.com'),
    [sepolia.id]: http('https://sepolia.example.com'),
    [base.id]: http('https://base.example.com'),
  },
})
```

## With Connectors

```typescript
import { createConfig, http } from '@wagmi/core'
import { mainnet, sepolia } from '@wagmi/core/chains'
import { injected } from '@wagmi/connectors'
import { walletConnect } from '@wagmi/connectors'

export const config = createConfig({
  chains: [mainnet, sepolia],
  connectors: [
    injected(),
    walletConnect({ projectId: '...' })
  ],
  transports: {
    [mainnet.id]: http(),
    [sepolia.id]: http(),
  },
})
```

## Storage Persistence

```typescript
import { createConfig, createStorage, http } from '@wagmi/core'
import { mainnet, sepolia } from '@wagmi/core/chains'

export const config = createConfig({
  chains: [mainnet, sepolia],
  storage: createStorage({ storage: window.localStorage }),
  transports: {
    [mainnet.id]: http(),
    [sepolia.id]: http(),
  },
})
```

## Config Methods

```typescript
import { config } from './config'

// Get viem client
const client = config.getClient({ chainId: 1 })

// Subscribe to state changes
const unsubscribe = config.subscribe(
  (state) => state.chainId,
  (chainId) => console.log('Chain changed:', chainId)
)

// Manually set state
config.setState((state) => ({ ...state, chainId: 1 }))
```

## MultiInjectedProviderDiscovery

Enable EIP-6963 multi-injected provider discovery:

```typescript
export const config = createConfig({
  chains: [mainnet, sepolia],
  multiInjectedProviderDiscovery: true, // default
  transports: { ... },
})
```

## Polling & Batching

```typescript
export const config = createConfig({
  chains: [mainnet, sepolia],
  pollingInterval: 4_000,    // polling interval in ms
  cacheTime: 4_000,          // cache duration
  batch: { multicall: true }, // enable multicall batching
  transports: { ... },
})
```
