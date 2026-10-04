---
name: wagmi-overview
description: Vanilla JS Ethereum library built on viem. Use for wallet connections, contract interactions, and blockchain queries.
---

# Wagmi Overview

Vanilla JS Ethereum library built on viem for wallet connections and contract interactions.

## Install

```bash
pnpm add @wagmi/core @wagmi/connectors viem@2.x
```

## Quick Start

```typescript
import { createConfig, http } from '@wagmi/core'
import { mainnet, sepolia } from '@wagmi/core/chains'

export const config = createConfig({
  chains: [mainnet, sepolia],
  transports: {
    [mainnet.id]: http(),
    [sepolia.id]: http(),
  },
})
```

## Skills

- **Config**: `wagmi-config` - Configuration setup
- **Read**: `wagmi-read-contract` - Read contract data
- **Write**: `wagmi-write-contract` - Write to contracts
- **Connectors**: `wagmi-connectors` - Wallet connections
- **Transports**: `wagmi-transports` - Network transports

## Core Concepts

- **Config** - Chain and transport setup
- **Connectors** - Wallet adapters (MetaMask, WalletConnect, etc.)
- **Actions** - Read/write blockchain data
- **Transports** - HTTP/WebSocket connections
