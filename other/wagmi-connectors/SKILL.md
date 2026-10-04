---
name: wagmi-connectors
description: Wallet connectors for MetaMask, WalletConnect, injected, and more. Use when setting up wallet connections.
---

# Wagmi Connectors

Wallet connection adapters.

## Setup Connectors

```typescript
import { createConfig, http } from '@wagmi/core'
import { mainnet, sepolia } from '@wagmi/core/chains'
import { injected } from '@wagmi/connectors'
import { walletConnect } from '@wagmi/connectors'
import { safe } from '@wagmi/connectors'

export const config = createConfig({
  chains: [mainnet, sepolia],
  connectors: [
    injected(),                    // Browser wallets (MetaMask, etc.)
    walletConnect({ projectId: '...' }),
    safe()
  ],
  transports: { ... }
})
```

## Connect/Disconnect

```typescript
import { connect, disconnect, getConnection } from '@wagmi/core'

// Connect
const { account, chainId, connector } = await connect(config, {
  connector: injected()  // or omit to use first available
})

// Get current connection
const { account, chainId } = getConnection(config)

// Disconnect
await disconnect(config)
```

## Available Connectors

### Injected (Browser Wallets)

```typescript
import { injected } from '@wagmi/connectors'

injected({
  shimDisconnect: true  // persist disconnect state
})
```

### MetaMask

```typescript
import { metaMask } from '@wagmi/connectors'

metaMask({
  shimDisconnect: true,
  flag: 'all'  // or 'ethereum'
})
```

### WalletConnect

```typescript
import { walletConnect } from '@wagmi/connectors'

walletConnect({
  projectId: 'YOUR_PROJECT_ID',
  showQrModal: true,
  qrModalOptions: {
    themeMode: 'dark'
  }
})
```

### Safe (Gnosis Safe)

```typescript
import { safe } from '@wagmi/connectors'

safe({
  allowedDomains: [/gnosis-safe.io$/, /app.safe.global$/],
  debug: false
})
```

### Mock (Testing)

```typescript
import { mock } from '@wagmi/connectors'

mock({
  accounts: [privateKeyToAccount('0x...')],
  chainId: 1
})
```

## Switch Chains

```typescript
import { switchChain } from '@wagmi/core'
import { base } from '@wagmi/core/chains'

await switchChain(config, { chainId: base.id })
```

## Watch Connections

```typescript
import { watchConnections, watchConnector } from '@wagmi/core'

// Watch all connections
watchConnections(config, (connections) => {
  console.log('Connections:', connections)
})

// Watch specific connector
watchConnector(config, 'injected', (connector) => {
  console.log('Injected connector:', connector)
})
```
