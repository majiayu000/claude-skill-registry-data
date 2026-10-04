---
name: permit2-addresses
description: Canonical Permit2 contract addresses by chain. Use when configuring multi-chain support.
---

# Permit2 Addresses

## Canonical Address

**All chains use the same address:**

```
0x000000000022D473030F116dDEE9F6B43aC78BA3
```

## By Chain ID

| Chain | Chain ID | Status |
|-------|----------|--------|
| Ethereum Mainnet | 1 | ✅ |
| Arbitrum | 42161 | ✅ |
| Optimism | 10 | ✅ |
| Base | 8453 | ✅ |
| Polygon | 137 | ✅ |
| Avalanche | 43114 | ✅ |
| BNB Chain | 56 | ✅ |
| Sepolia (testnet) | 11155111 | ✅ |
| Arbitrum Sepolia | 421614 | ✅ |
| Base Sepolia | 84532 | ✅ |
| Optimism Sepolia | 11155420 | ✅ |
| Foundry (local) | 31337 | ✅ |

## Usage in Code

```typescript
import { PERMIT2_ADDRESS } from '@uniswap/permit2-sdk'

// Or hardcoded (canonical)
const PERMIT2 = '0x000000000022D473030F116dDEE9F6B43aC78BA3'
```

## Dynamic Address (Optional)

```typescript
import { permit2Address } from '@uniswap/permit2-sdk'

const permit2 = permit2Address(chainId)
```

## Frontend Integration

The frontend stores addresses in:

```
frontend/app/addresses/{chain}/base_deployments.json
```

Example usage:

```typescript
import platformSepolia from './app/addresses/sepolia/base_deployments.json'
import platformFoundry from './app/addresses/anvil_base_main/base_deployments.json'

const permit2Address = chainId === sepolia.id 
  ? platformSepolia.permit2 
  : platformFoundry.permit2
```
