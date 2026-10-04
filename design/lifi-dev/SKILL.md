---
name: lifi-dev
description: >
  Comprehensive development support for LI.FI DEX aggregator including SDK, Widget, and API integration
  for cross-chain swaps and bridging. Use when building applications with LI.FI for - (1) Cross-chain
  token swaps and bridges, (2) Multi-chain liquidity aggregation, (3) Trading widget integration, (4)
  Custom DEX aggregation UI, (5) Gas subsidy implementation, (6) Revenue monetization with integrator
  fees, (7) Route optimization across 60+ chains, (8) Intent-based trading systems. Covers SDK usage
  (TypeScript/JavaScript), Widget customization (React/Vue/Svelte), API integration (REST), and
  LI.FI-specific features like cross-chain routing, gas subsidies (LI.Fuel), and multi-protocol
  aggregation across Uniswap, 1inch, Stargate, Across, and 800+ protocols.
---

# LI.FI Development Support

Comprehensive toolkit for building cross-chain swap and bridge applications with LI.FI - the leading DEX and bridge aggregation protocol supporting 60+ chains and 800+ protocols.

## Quick Start

### Product Selection

LI.FI offers three integration methods. Choose based on your use case:

**Quick Decision**:
- Ready-made UI component → **Widget** (5 min integration, highly customizable)
- Full control over UX → **SDK** (TypeScript/JavaScript, frontend & backend)
- Direct API access → **REST API** (language-agnostic, maximum flexibility)
- Existing widget + custom logic → **Widget + SDK combo** (best of both worlds)

**Integration Complexity**:
- Widget: ⭐ (Easiest - drop-in component)
- SDK: ⭐⭐ (Moderate - programmatic control)
- API: ⭐⭐⭐ (Advanced - full customization)

### Common Tasks

**1. Add swap widget to your app**:
- Review [widget_integration.tsx](scripts/widget_integration.tsx) for React integration
- Key points: theme customization, chain filtering, event handling
- Production-ready in under 5 minutes
- See [widget-guide.md](references/widget-guide.md) for advanced customization

**2. Execute cross-chain swap programmatically**:
- Use [sdk_swap_example.ts](scripts/sdk_swap_example.ts) for SDK implementation
- Key points: route optimization, gas estimation, slippage protection
- See [sdk-guide.md](references/sdk-guide.md) for comprehensive SDK patterns

**3. Get best swap route via API**:
- Use [api_routes_example.ts](scripts/api_routes_example.ts) for direct API calls
- Key points: rate limiting, error handling, route comparison
- See [api-reference.md](references/api-reference.md) for complete endpoint documentation

**4. Implement gas subsidy (LI.Fuel)**:
- Use [gas_subsidy_example.ts](scripts/gas_subsidy_example.ts) for LI.Fuel integration
- Solve cold-start problem on new chains
- See [gas-subsidy-guide.md](references/gas-subsidy-guide.md) for implementation details

**5. Monetize with integrator fees**:
- Configure fees in [LI.FI Portal](https://portal.li.fi)
- See [monetization-guide.md](references/monetization-guide.md) for fee structure and withdrawal

## Core Workflows

### Widget Integration

**React/Next.js Integration**:
```typescript
import { LiFiWidget, WidgetConfig } from '@lifi/widget';

// 1. Configure widget
const widgetConfig: WidgetConfig = {
  integrator: 'your-app-name', // Required for analytics and fees

  // Appearance
  variant: 'expandable', // 'default' | 'wide' | 'drawer' | 'expandable'
  theme: {
    palette: {
      primary: { main: '#3f51b5' },
      secondary: { main: '#f50057' }
    },
    shape: { borderRadius: 12 }
  },

  // Chain & token filtering
  fromChain: 1, // Ethereum
  toChain: 137, // Polygon
  fromToken: '0x...', // Specific token address (optional)

  // Advanced configuration
  fee: 0.03, // 0.03% integrator fee
  slippage: 0.005, // 0.5% max slippage

  // Event handlers
  onRouteExecutionStarted: (route) => {
    console.log('Swap started:', route);
  },
  onRouteExecutionCompleted: (route) => {
    console.log('Swap completed:', route);
  }
};

// 2. Render widget
function App() {
  return (
    <div style={{ width: '100%', maxWidth: 500 }}>
      <LiFiWidget config={widgetConfig} />
    </div>
  );
}
```

**Vue.js Integration**:
```vue
<template>
  <div class="widget-container">
    <lifi-widget :config="widgetConfig" />
  </div>
</template>

<script setup>
import { LiFiWidget } from '@lifi/widget';

const widgetConfig = {
  integrator: 'your-app-name',
  variant: 'wide',
  theme: { palette: { primary: { main: '#42b883' } } }
};
</script>
```

**Vanilla JavaScript**:
```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://unpkg.com/@lifi/widget/dist/widget.css">
</head>
<body>
  <div id="lifi-widget"></div>

  <script src="https://unpkg.com/@lifi/widget"></script>
  <script>
    window.lifi.createWidget({
      container: document.getElementById('lifi-widget'),
      config: {
        integrator: 'your-app-name',
        variant: 'default'
      }
    });
  </script>
</body>
</html>
```

See [widget_integration.tsx](scripts/widget_integration.tsx) for complete examples.

### SDK Integration

**Installation**:
```bash
npm install @lifi/sdk
# or
yarn add @lifi/sdk
# or
pnpm add @lifi/sdk
```

**Basic Swap Flow**:
```typescript
import { LIFI } from '@lifi/sdk';
import { createWalletClient, http } from 'viem';
import { mainnet } from 'viem/chains';

// 1. Initialize SDK
const lifi = new LIFI({
  integrator: 'your-app-name', // Required
  apiKey: process.env.LIFI_API_KEY // Optional - higher rate limits
});

// 2. Get available chains and tokens
const chains = await lifi.getChains();
const tokens = await lifi.getTokens({ chains: [1, 137] }); // Ethereum & Polygon

// 3. Get best route for swap
const routeRequest = {
  fromChainId: 1,     // Ethereum
  fromTokenAddress: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', // USDC
  fromAmount: '1000000000', // 1000 USDC (6 decimals)
  toChainId: 137,     // Polygon
  toTokenAddress: '0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359', // USDC on Polygon
  fromAddress: '0x...', // User wallet address

  // Optional optimizations
  options: {
    slippage: 0.005,  // 0.5%
    order: 'RECOMMENDED', // or 'FASTEST', 'CHEAPEST', 'SAFEST'
    allowSwitchChain: true
  }
};

const routes = await lifi.getRoutes(routeRequest);
const bestRoute = routes.routes[0]; // Pre-sorted by 'order' parameter

// 4. Check route details
console.log('Estimated time:', bestRoute.steps.reduce((t, s) => t + s.estimate.executionDuration, 0), 'seconds');
console.log('Gas cost:', bestRoute.gasCostUSD);
console.log('Output amount:', bestRoute.toAmountMin); // Minimum guaranteed

// 5. Execute route
const wallet = createWalletClient({
  chain: mainnet,
  transport: http()
});

// Approve token spending if needed
if (bestRoute.steps[0].action.fromToken.address !== '0x0000000000000000000000000000000000000000') {
  const approvalTx = await lifi.approveToken({
    walletClient: wallet,
    token: bestRoute.steps[0].action.fromToken,
    amount: bestRoute.steps[0].action.fromAmount,
    spender: bestRoute.steps[0].estimate.approvalAddress
  });
  await approvalTx.wait();
}

// Execute swap
const execution = await lifi.executeRoute({
  route: bestRoute,
  walletClient: wallet,

  // Event callbacks
  updateRouteHook: (updatedRoute) => {
    console.log('Route updated:', updatedRoute.status);
  },
  switchChainHook: async (requiredChainId) => {
    // Handle chain switch in your UI
    await wallet.switchChain({ id: requiredChainId });
  },
  acceptExchangeRateUpdateHook: (oldRate, newRate) => {
    // Return true to accept rate changes
    return confirm(`Rate changed from ${oldRate} to ${newRate}. Continue?`);
  }
});

console.log('Swap completed!', execution);
```

**Advanced Route Filtering**:
```typescript
// Filter by specific bridges and exchanges
const routes = await lifi.getRoutes({
  ...routeRequest,
  options: {
    bridges: { allow: ['stargate', 'across', 'hop'] },
    exchanges: { allow: ['uniswap', '1inch'] },

    // Exclude specific protocols
    // bridges: { deny: ['multichain'] },

    // Fee configuration
    integrator: 'your-app',
    fee: 0.03 // 0.03% fee on fromAmount
  }
});
```

See [sdk_swap_example.ts](scripts/sdk_swap_example.ts) for production-ready implementation.

### API Integration

**Base URL**: `https://li.quest/v1`

**Authentication** (Optional):
```bash
# Higher rate limits with API key
curl -H "x-lifi-api-key: YOUR_API_KEY" https://li.quest/v1/...
```

**Get Route Quote**:
```typescript
// GET /quote
const response = await fetch(
  'https://li.quest/v1/quote?' + new URLSearchParams({
    fromChain: '1',
    toChain: '137',
    fromToken: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', // USDC
    toToken: '0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359',   // USDC on Polygon
    fromAmount: '1000000000', // 1000 USDC
    fromAddress: '0x...',

    // Optional
    integrator: 'your-app-name',
    fee: '0.03', // 3% integrator fee (decimal format: 0.03 = 3%)
    slippage: '0.005', // 0.5%
    order: 'RECOMMENDED'
  }),
  {
    headers: {
      'x-lifi-api-key': process.env.LIFI_API_KEY // Optional
    }
  }
);

const quote = await response.json();

// Quote contains single optimized route
console.log('Estimated output:', quote.estimate.toAmount);
console.log('Execution time:', quote.estimate.executionDuration, 'seconds');
console.log('Gas cost:', quote.estimate.gasCosts);
```

**Get Multiple Routes**:
```typescript
// GET /advanced/routes - Returns multiple route options
const response = await fetch(
  'https://li.quest/v1/advanced/routes?' + new URLSearchParams({
    fromChainId: '1',
    toChainId: '137',
    fromTokenAddress: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
    toTokenAddress: '0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359',
    fromAmount: '1000000000',
    fromAddress: '0x...'
  })
);

const { routes } = await response.json();

// Compare multiple routes
routes.forEach((route, i) => {
  console.log(`Route ${i + 1}:`);
  console.log('  Steps:', route.steps.length);
  console.log('  Time:', route.steps.reduce((t, s) => t + s.estimate.executionDuration, 0));
  console.log('  Output:', route.toAmount);
});
```

**Get Supported Chains**:
```typescript
// GET /chains
const response = await fetch('https://li.quest/v1/chains');
const chains = await response.json();

chains.forEach(chain => {
  console.log(`${chain.name} (${chain.id}): ${chain.nativeToken.symbol}`);
});
```

**Get Supported Tokens**:
```typescript
// GET /tokens
const response = await fetch(
  'https://li.quest/v1/tokens?' + new URLSearchParams({
    chains: '1,137,42161' // Ethereum, Polygon, Arbitrum
  })
);

const { tokens } = await response.json();
// Returns: { [chainId]: Token[] }
```

**Check Route Status**:
```typescript
// GET /status
const response = await fetch(
  'https://li.quest/v1/status?' + new URLSearchParams({
    txHash: '0x...',
    bridge: 'stargate', // Optional - speeds up lookup
    fromChain: '1',
    toChain: '137'
  })
);

const status = await response.json();
console.log('Status:', status.status); // 'DONE' | 'PENDING' | 'FAILED'
console.log('Destination tx:', status.receiving?.txHash);
```

See [api_routes_example.ts](scripts/api_routes_example.ts) and [api-reference.md](references/api-reference.md).

### Gas Subsidy Implementation (LI.Fuel)

**Problem**: Users bridging to a new chain lack native gas tokens.

**Solution**: LI.Fuel converts a portion of bridged assets to destination chain's native token.

```typescript
import { LIFI } from '@lifi/sdk';

const lifi = new LIFI({ integrator: 'your-app' });

// Request route with gas subsidy
const routes = await lifi.getRoutes({
  fromChainId: 1,     // Ethereum
  fromTokenAddress: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', // USDC
  fromAmount: '1000000000', // 1000 USDC
  toChainId: 137,     // Polygon
  toTokenAddress: '0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359', // USDC on Polygon
  fromAddress: userAddress,

  // Enable gas subsidy
  fromAmountForGas: '50000000' // Convert 50 USDC to MATIC on Polygon
});

// Route automatically includes gas conversion step
const route = routes.routes[0];

// Verify gas subsidy is included
const gasStep = route.steps.find(step => step.type === 'lifi');
if (gasStep?.includedSteps?.some(s => s.type === 'swap' && s.action.toToken.address === '0x0000000000000000000000000000000000000000')) {
  console.log('Gas subsidy enabled: User will receive native tokens');
}
```

**API Version**:
```typescript
const response = await fetch(
  'https://li.quest/v1/quote?' + new URLSearchParams({
    fromChain: '1',
    toChain: '137',
    fromToken: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
    toToken: '0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359',
    fromAmount: '1000000000',
    fromAddress: userAddress,

    // Add gas subsidy parameter
    fromAmountForGas: '50000000' // 50 USDC → MATIC
  })
);
```

**Limitations**:
- ❌ Not supported with `/contractCalls` endpoint
- ❌ Not supported via Composer (multi-action transactions)
- ✅ Supported via `/quote` and `/routes` endpoints
- ✅ Works with SDK's `getRoutes()` method

See [gas_subsidy_example.ts](scripts/gas_subsidy_example.ts) and [gas-subsidy-guide.md](references/gas-subsidy-guide.md).

### Fee Monetization

**Earn revenue by adding integrator fees to swaps**:

```typescript
// 1. Register at https://portal.li.fi to get your integrator account

// 2. Add fee parameter to SDK/API calls
const routes = await lifi.getRoutes({
  ...routeRequest,

  integrator: 'your-app-name', // Required
  fee: 0.03 // 3% fee (decimal: 0.03 = 3%, 0.001 = 0.1%)
});

// Fee is deducted from fromAmount automatically
// Example: User sends 1000 USDC
//   → 30 USDC goes to you (3%)
//   → 970 USDC is swapped/bridged
```

**Fee Collection**:
```typescript
// Via API
const response = await fetch('https://li.quest/v1/integrators/fees', {
  headers: {
    'Authorization': 'Bearer YOUR_API_TOKEN',
    'x-lifi-api-key': 'YOUR_API_KEY'
  }
});

const { fees } = await response.json();
console.log('Collected fees:', fees);

// Withdraw via Portal or API
await fetch('https://li.quest/v1/integrators/fees/withdraw', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_API_TOKEN',
    'x-lifi-api-key': 'YOUR_API_KEY'
  },
  body: JSON.stringify({
    token: '0x...', // Token to withdraw
    amount: '1000000000' // Amount
  })
});
```

**Base Fee Structure**:
- LI.FI base fee: 0.25% on all transactions
- Your integrator fee: Configurable (typically 0.1% - 1%)
- User pays: LI.FI fee + your fee + protocol fees (DEX/bridge)

**Volume Discounts**:
- High-volume integrators can negotiate reduced LI.FI base fees
- Contact LI.FI team for enterprise pricing

**Important**:
- ⚠️ Must withdraw fees from the same wallet used during integration
- ⚠️ Switching wallets will lock previous fee claims
- ✅ Can set up automatic consolidation and conversion to stablecoins

See [monetization-guide.md](references/monetization-guide.md) for complete setup guide.

## Critical Security Requirements

**Never deploy without**:

1. **Slippage Protection**: Always set `slippage` parameter (default 0.5% = 0.005)
2. **Amount Validation**: Verify `toAmountMin` in routes before execution
3. **Token Approval Limits**: Approve exact amounts, not unlimited allowances
4. **Rate Limiting**: Implement client-side rate limiting for API calls
5. **Error Handling**: Handle network errors, route failures, and bridge delays
6. **Chain Verification**: Verify user is on correct chain before execution
7. **Transaction Monitoring**: Track transaction status across chains
8. **API Key Protection**: Never expose API keys in frontend code (use backend proxy)
9. **User Confirmation**: Show final amounts, fees, and execution time before swap
10. **Bridge Risk Disclosure**: Inform users about bridge security and delays

**Widget Security**:
```typescript
const widgetConfig = {
  integrator: 'your-app',

  // Prevent unlimited approvals (recommended)
  infiniteApproval: false,

  // Set maximum slippage
  slippage: 0.005, // 0.5%

  // Disable risky bridges (optional)
  bridges: { deny: ['bridge-with-issues'] },

  // Add transaction confirmation
  onRouteExecutionStarted: (route) => {
    // Log for monitoring
    analytics.track('swap_started', {
      fromChain: route.fromChainId,
      toChain: route.toChainId,
      amount: route.fromAmount
    });
  }
};
```

**SDK Security**:
```typescript
// ✅ GOOD: Exact approval
await lifi.approveToken({
  token: route.steps[0].action.fromToken,
  amount: route.steps[0].action.fromAmount, // Exact amount
  spender: route.steps[0].estimate.approvalAddress
});

// ❌ BAD: Unlimited approval
await lifi.approveToken({
  token: route.steps[0].action.fromToken,
  amount: ethers.MaxUint256, // Dangerous!
  spender: route.steps[0].estimate.approvalAddress
});

// ✅ GOOD: Rate limiting
const rateLimit = {
  maxRequests: 10,
  perSeconds: 60
};

// ✅ GOOD: Timeout handling
const routePromise = lifi.getRoutes(request);
const timeoutPromise = new Promise((_, reject) =>
  setTimeout(() => reject(new Error('Route timeout')), 30000)
);

try {
  const routes = await Promise.race([routePromise, timeoutPromise]);
} catch (error) {
  // Handle timeout or error
}
```

See [security.md](references/security.md) for complete security checklist.

## Architecture Patterns

### LI.FI Aggregation Architecture

```
┌─────────────────────────────────────────────┐
│         Your Application (dApp)              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│  │ Widget  │  │   SDK   │  │   API   │     │
│  └────┬────┘  └────┬────┘  └────┬────┘     │
└───────┼───────────┼────────────┼───────────┘
        │           │            │
        └───────────┴────────────┘
                    │
        ┌───────────▼────────────┐
        │   LI.FI Smart Router   │
        │  (Route Optimization)  │
        └───────────┬────────────┘
                    │
    ┌───────────────┼───────────────┐
    │               │               │
┌───▼────┐    ┌────▼─────┐   ┌────▼────┐
│ Bridges│    │ DEX Agg  │   │ Solvers │
│        │    │          │   │         │
│Stargate│    │ Uniswap  │   │ 1inch   │
│ Across │    │ Sushiswap│   │ 0x      │
│  Hop   │    │ Curve    │   │ Kyber   │
│Connext │    │ Balancer │   │ ParaSwap│
└────────┘    └──────────┘   └─────────┘
    │              │              │
    └──────────────┴──────────────┘
                   │
          ┌────────▼─────────┐
          │  60+ Blockchains  │
          │ 800+ Protocols   │
          └──────────────────┘
```

### Integration Decision Tree

```
Start: Need cross-chain swap/bridge functionality
  │
  ├─ Need UI component?
  │  │
  │  ├─ Yes → Use Widget
  │  │        │
  │  │        ├─ Basic theme customization → Widget default config
  │  │        ├─ Advanced customization → Widget + custom theme
  │  │        └─ Need custom logic → Widget + SDK hooks
  │  │
  │  └─ No → Need programmatic control?
  │           │
  │           ├─ TypeScript/JavaScript → Use SDK
  │           │                          │
  │           │                          ├─ Frontend → SDK + wallet provider
  │           │                          └─ Backend → SDK + private key signer
  │           │
  │           └─ Other language/platform → Use REST API
  │                                        │
  │                                        ├─ Python/Go/Ruby → Direct HTTP
  │                                        └─ Mobile native → HTTP client
```

### Multi-Step Route Flow

```
User Swap: 1000 USDC (Ethereum) → USDT (Arbitrum)
  │
  ├─ Step 1 (SWAP on Ethereum):
  │  └─ 1000 USDC → 1000 USDT via Uniswap V3
  │
  ├─ Step 2 (BRIDGE):
  │  └─ 1000 USDT (Ethereum) → 998 USDT (Arbitrum) via Stargate
  │     (2 USDT bridge fee)
  │
  └─ Result: 998 USDT on Arbitrum

Optional: Gas Subsidy (LI.Fuel)
  │
  ├─ Step 2a (before bridge):
  │  └─ 50 USDT → 0.05 ETH (for gas on Ethereum)
  │
  └─ Step 2b (on destination):
     └─ Bridge converts 50 USDT → ~40 ARB native tokens
     └─ User receives: 948 USDT + 40 ARB (for gas)
```

### Rate Limiting Architecture

```
Without API Key (per IP):
  ├─ /quote, /routes: 10 requests/minute
  ├─ /chains, /tokens: 20 requests/minute
  └─ /status: 30 requests/minute

With API Key (per key):
  ├─ /quote, /routes: 100 requests/minute
  ├─ /chains, /tokens: 200 requests/minute
  └─ /status: 300 requests/minute

Enterprise (contact LI.FI):
  └─ Custom limits + dedicated infrastructure
```

## Development Setup

### Dependencies

**Widget Installation**:
```bash
# React
npm install @lifi/widget
# Includes all peer dependencies

# Vue
npm install @lifi/widget vue

# Svelte
npm install @lifi/widget svelte

# Vanilla JS (via CDN)
# No installation needed - use <script> tag
```

**SDK Installation**:
```bash
npm install @lifi/sdk viem
# or with ethers
npm install @lifi/sdk ethers

# TypeScript types included
```

**Additional Tools**:
```bash
# For API calls (if not using SDK)
npm install axios
# or use native fetch (Node 18+, all modern browsers)

# For wallet integration
npm install wagmi @wagmi/core viem
# or
npm install @web3-react/core ethers
```

### Environment Setup

```bash
# .env
LIFI_API_KEY=your_api_key_here          # Optional - get from portal.li.fi
INTEGRATOR_NAME=your-app-name           # Required for analytics
INTEGRATOR_FEE=0.03                     # Optional - your revenue %

# Wallet (for backend/scripts)
PRIVATE_KEY=0x...                        # For automated execution
RPC_URL_ETHEREUM=https://eth.llamarpc.com
RPC_URL_POLYGON=https://polygon.llamarpc.com
# ... other chains
```

### Supported Chains

**EVM Chains** (40+):
- Ethereum, Arbitrum, Optimism, Base, Polygon, BSC, Avalanche
- Gnosis, Fantom, Moonbeam, Moonriver, Celo, Aurora, Harmony
- zkSync Era, Polygon zkEVM, Linea, Scroll, Mantle
- And many more...

**Non-EVM Chains** (20+):
- Solana, Bitcoin (experimental), Cosmos ecosystem
- More being added regularly

**Testnet Support**:
- Sepolia, Goerli, Mumbai, Arbitrum Goerli, Optimism Goerli
- Check [api-reference.md](references/api-reference.md) for complete list

### Key Contract Addresses

LI.FI uses partner protocols (Uniswap, Stargate, etc.) - no proprietary contracts to deploy.

**Integration Contracts** (for advanced use):
- LI.FI Diamond Proxy: `0x1231DEB6f5749EF6cE6943a275A1D3E7486F4EaE` (multi-chain)
- Receiver Contract: Varies by chain

**Token Addresses** (commonly used):
- USDC (Ethereum): `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`
- USDC (Polygon): `0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359`
- USDC (Arbitrum): `0xaf88d065e77c8cC2239327C5EDb3A432268e5831`
- USDC (Optimism): `0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85`
- Native tokens: Use `0x0000000000000000000000000000000000000000`

See [api-reference.md](references/api-reference.md) for complete address list.

## Testing

### Widget Testing (React Testing Library)

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import { LiFiWidget } from '@lifi/widget';

describe('LiFi Widget Integration', () => {
  it('should render widget with custom config', () => {
    const config = {
      integrator: 'test-app',
      variant: 'wide',
      fromChain: 1,
      toChain: 137
    };

    render(<LiFiWidget config={config} />);

    expect(screen.getByTestId('lifi-widget')).toBeInTheDocument();
  });

  it('should call onRouteExecutionCompleted', async () => {
    const onComplete = jest.fn();
    const config = {
      integrator: 'test-app',
      onRouteExecutionCompleted: onComplete
    };

    render(<LiFiWidget config={config} />);

    // Simulate swap completion
    // ... trigger swap in test environment

    await waitFor(() => {
      expect(onComplete).toHaveBeenCalled();
    });
  });
});
```

### SDK Testing (Jest/Vitest)

```typescript
import { LIFI } from '@lifi/sdk';
import { describe, it, expect, beforeEach } from 'vitest';

describe('LI.FI SDK', () => {
  let lifi: LIFI;

  beforeEach(() => {
    lifi = new LIFI({
      integrator: 'test-app'
    });
  });

  it('should fetch available chains', async () => {
    const chains = await lifi.getChains();

    expect(chains.length).toBeGreaterThan(0);
    expect(chains[0]).toHaveProperty('id');
    expect(chains[0]).toHaveProperty('name');
  });

  it('should get routes for valid swap', async () => {
    const routes = await lifi.getRoutes({
      fromChainId: 1,
      fromTokenAddress: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', // USDC
      fromAmount: '1000000000', // 1000 USDC
      toChainId: 137,
      toTokenAddress: '0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359', // USDC Polygon
      fromAddress: '0x1234567890123456789012345678901234567890'
    });

    expect(routes.routes.length).toBeGreaterThan(0);
    expect(routes.routes[0]).toHaveProperty('fromAmount');
    expect(routes.routes[0]).toHaveProperty('toAmount');
  });

  it('should handle invalid route request', async () => {
    await expect(
      lifi.getRoutes({
        fromChainId: 1,
        fromTokenAddress: '0xinvalid',
        fromAmount: '1000000000',
        toChainId: 137,
        toTokenAddress: '0x...',
        fromAddress: '0x...'
      })
    ).rejects.toThrow();
  });
});
```

### API Testing (curl)

```bash
# Test chain availability
curl https://li.quest/v1/chains | jq '.[0]'

# Test quote endpoint
curl "https://li.quest/v1/quote?fromChain=1&toChain=137&fromToken=0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48&toToken=0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359&fromAmount=1000000000&fromAddress=0x1234567890123456789012345678901234567890" \
  -H "x-lifi-api-key: YOUR_API_KEY" | jq '.estimate'

# Test with integrator fee
curl "https://li.quest/v1/quote?fromChain=1&toChain=137&fromToken=0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48&toToken=0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359&fromAmount=1000000000&fromAddress=0x...&integrator=test-app&fee=0.03" | jq '.estimate.feeCosts'
```

### E2E Testing (Playwright)

```typescript
import { test, expect } from '@playwright/test';

test('complete swap flow with widget', async ({ page }) => {
  await page.goto('http://localhost:3000');

  // Wait for widget to load
  await page.waitForSelector('#lifi-widget');

  // Configure swap
  await page.fill('input[name="fromAmount"]', '100');
  await page.selectOption('select[name="fromChain"]', '1'); // Ethereum
  await page.selectOption('select[name="toChain"]', '137'); // Polygon

  // Click swap button
  await page.click('button:has-text("Swap")');

  // Verify route display
  await expect(page.locator('.route-summary')).toBeVisible();
  await expect(page.locator('.estimated-output')).toContainText('USDC');

  // In testnet: complete transaction
  // In production: verify swap flow without execution
});
```

## Common Pitfalls

1. **Missing integrator name**: Required for analytics and fee collection
   ```typescript
   // ❌ BAD
   const lifi = new LIFI({});

   // ✅ GOOD
   const lifi = new LIFI({ integrator: 'your-app-name' });
   ```

2. **Ignoring route execution status**: Always monitor multi-step routes
   ```typescript
   // ❌ BAD - Fire and forget
   await lifi.executeRoute({ route, walletClient });

   // ✅ GOOD - Monitor status
   const execution = await lifi.executeRoute({
     route,
     walletClient,
     updateRouteHook: (route) => {
       console.log('Step', route.steps.findIndex(s => s.execution?.status === 'PENDING'));
     }
   });
   ```

3. **Not handling chain switches**: Cross-chain swaps require chain switching
   ```typescript
   // ✅ GOOD
   const execution = await lifi.executeRoute({
     route,
     walletClient,
     switchChainHook: async (chainId) => {
       await walletClient.switchChain({ id: chainId });
     }
   });
   ```

4. **Unlimited token approvals**: Security risk
   ```typescript
   // ❌ BAD
   await token.approve(spender, ethers.MaxUint256);

   // ✅ GOOD
   await lifi.approveToken({
     token: route.steps[0].action.fromToken,
     amount: route.steps[0].action.fromAmount, // Exact amount
     spender: route.steps[0].estimate.approvalAddress
   });
   ```

5. **Exposing API keys in frontend**: Use backend proxy
   ```typescript
   // ❌ BAD - Frontend
   const lifi = new LIFI({
     apiKey: 'pk_live_...' // Exposed in browser!
   });

   // ✅ GOOD - Backend proxy
   // Frontend: Call your backend
   const routes = await fetch('/api/lifi/routes', {
     method: 'POST',
     body: JSON.stringify(routeRequest)
   });

   // Backend: Use API key securely
   const lifi = new LIFI({
     apiKey: process.env.LIFI_API_KEY
   });
   ```

6. **Not handling bridge delays**: Some bridges take hours
   ```typescript
   // ✅ GOOD - Set expectations
   console.log('Estimated time:', route.steps.reduce(
     (total, step) => total + step.estimate.executionDuration,
     0
   ), 'seconds');

   if (route.steps.some(s => s.estimate.executionDuration > 3600)) {
     alert('This route may take over 1 hour. Continue?');
   }
   ```

7. **Wrong fee format**: Use decimal, not percentage
   ```typescript
   // ❌ BAD
   fee: 3 // SDK interprets as 300%!

   // ✅ GOOD
   fee: 0.03 // 3%
   ```

8. **Ignoring rate limits**: Will get throttled
   ```typescript
   // ✅ GOOD - Implement rate limiting
   const rateLimiter = new RateLimiter({
     maxRequests: 10,
     perSeconds: 60
   });

   await rateLimiter.throttle();
   const routes = await lifi.getRoutes(request);
   ```

9. **Not validating user inputs**: Can cause API errors
   ```typescript
   // ✅ GOOD
   if (!ethers.isAddress(fromAddress)) {
     throw new Error('Invalid address');
   }
   if (BigInt(fromAmount) <= 0) {
     throw new Error('Amount must be positive');
   }
   ```

10. **Gas subsidy with contractCalls**: Not supported
    ```typescript
    // ❌ BAD - Will fail
    const routes = await lifi.getRoutes({
      ...request,
      contractCalls: [...],
      fromAmountForGas: '50000000' // Not supported together
    });

    // ✅ GOOD - Use separately
    const routes = await lifi.getRoutes({
      ...request,
      fromAmountForGas: '50000000' // Works
    });
    ```

## Resources

### Official Documentation
- **Main Site**: https://li.fi/
- **Developer Docs**: https://docs.li.fi/
- **SDK Documentation**: https://docs.li.fi/sdk/overview
- **API Reference**: https://docs.li.fi/api-reference/introduction
- **Widget Guide**: https://docs.li.fi/widget/overview

### Integration Guides
- **Gas Subsidy**: https://docs.li.fi/guides/gas-subsidy
- **Latency Optimization**: https://docs.li.fi/guides/latency
- **Fees & Monetization**: https://docs.li.fi/faqs/fees-monetization
- **Security Best Practices**: https://docs.li.fi/guides/security

### Tools & Dashboards
- **LI.FI Portal**: https://portal.li.fi (fee management, analytics)
- **Widget Playground**: https://widget.li.fi (test configurations)
- **Route Explorer**: https://explorer.li.fi (track transactions)
- **API Playground**: https://apidocs.li.fi (test API calls)

### Code Examples
- **GitHub Examples**: https://github.com/lifinance/examples
- **Widget Templates**: https://github.com/lifinance/widget
- **SDK Examples**: https://github.com/lifinance/sdk

### Support
- **Discord**: https://discord.gg/lifi
- **Telegram**: https://t.me/lifiprotocol
- **Twitter**: https://twitter.com/lifiprotocol
- **GitHub Issues**: https://github.com/lifinance/sdk/issues
- **Status Page**: https://status.li.fi/

## Bundled Resources

### Scripts
- **[widget_integration.tsx](scripts/widget_integration.tsx)**: Complete Widget integration examples for React/Vue/Svelte
- **[sdk_swap_example.ts](scripts/sdk_swap_example.ts)**: Production-ready SDK swap implementation with error handling
- **[api_routes_example.ts](scripts/api_routes_example.ts)**: Direct API integration with rate limiting and monitoring
- **[gas_subsidy_example.ts](scripts/gas_subsidy_example.ts)**: LI.Fuel gas subsidy implementation
- **[fee_collection_example.ts](scripts/fee_collection_example.ts)**: Integrator fee setup and collection

### References
- **[widget-guide.md](references/widget-guide.md)**: Complete Widget customization and theming guide
- **[sdk-guide.md](references/sdk-guide.md)**: Comprehensive SDK usage patterns and best practices
- **[api-reference.md](references/api-reference.md)**: Full REST API endpoint documentation with examples
- **[gas-subsidy-guide.md](references/gas-subsidy-guide.md)**: LI.Fuel implementation and optimization guide
- **[monetization-guide.md](references/monetization-guide.md)**: Fee structure, collection, and revenue optimization
- **[security.md](references/security.md)**: Security best practices and audit checklist
- **[supported-chains.md](references/supported-chains.md)**: Complete list of supported chains and tokens
- **[bridge-comparison.md](references/bridge-comparison.md)**: Bridge protocol comparison and selection guide

### Assets
- **[widget-theme-template.ts](assets/widget-theme-template.ts)**: Custom theme configuration template
- **[rate-limiter.ts](assets/rate-limiter.ts)**: Production-ready rate limiting implementation
- **[error-handler.ts](assets/error-handler.ts)**: Comprehensive error handling utilities

## Support Context7 Integration

When the user needs up-to-date documentation or specific implementation details not covered in this skill:

1. Use LI.FI official docs as primary source: https://docs.li.fi/
2. For SDK-specific questions: Use Context7 with "@lifi/sdk"
3. For Widget customization: Use Context7 with "@lifi/widget"
4. Combine Context7 results with this skill's security guidelines

Example:
```
User: "How do I customize the widget theme for dark mode?"
→ Check widget-guide.md for theme basics
→ Use Context7: query-docs with "@lifi/widget" for latest theme options
→ Apply security patterns from security.md for safe integration
```

## Advanced Topics

### Multi-Chain Portfolio Management

Track user balances across all chains:

```typescript
import { LIFI } from '@lifi/sdk';

async function getMultiChainBalances(userAddress: string) {
  const lifi = new LIFI({ integrator: 'portfolio-app' });

  // Get all supported chains
  const chains = await lifi.getChains();

  // Get token balances for each chain
  const balances = await Promise.all(
    chains.map(async (chain) => {
      const tokens = await lifi.getTokenBalances(userAddress, [chain.id]);
      return {
        chain: chain.name,
        tokens: tokens.filter(t => parseFloat(t.amount) > 0)
      };
    })
  );

  return balances.filter(b => b.tokens.length > 0);
}
```

### Route Optimization Strategies

```typescript
// Get multiple routes and compare
const routes = await lifi.getRoutes({
  ...baseRequest,
  options: {
    // Get fastest, cheapest, and recommended routes
    order: 'RECOMMENDED'
  }
});

// Compare routes
const comparison = routes.routes.map(route => ({
  id: route.id,
  outputAmount: route.toAmount,
  executionTime: route.steps.reduce((t, s) => t + s.estimate.executionDuration, 0),
  gasCostUSD: route.gasCostUSD,
  steps: route.steps.length
}));

// Sort by custom criteria
const bestByOutput = [...comparison].sort((a, b) =>
  parseFloat(b.outputAmount) - parseFloat(a.outputAmount)
)[0];

const bestByTime = [...comparison].sort((a, b) =>
  a.executionTime - b.executionTime
)[0];
```

### Custom Event Tracking

```typescript
const widgetConfig = {
  integrator: 'analytics-app',

  // Track all widget events
  onRouteHighValueLoss: (route, loss) => {
    analytics.track('high_value_loss_warning', {
      expectedOutput: route.toAmount,
      actualOutput: route.toAmountMin,
      lossAmount: loss
    });
  },

  onRouteExecutionStarted: (route) => {
    analytics.track('swap_started', {
      fromChain: route.fromChainId,
      toChain: route.toChainId,
      fromToken: route.fromToken.symbol,
      toToken: route.toToken.symbol,
      amount: route.fromAmount
    });
  },

  onRouteExecutionCompleted: (route) => {
    analytics.track('swap_completed', {
      routeId: route.id,
      executionTime: Date.now() - route.executionStartedAt,
      actualOutput: route.toAmountMin
    });
  },

  onRouteExecutionFailed: (route, error) => {
    analytics.track('swap_failed', {
      routeId: route.id,
      error: error.message,
      step: route.steps.findIndex(s => s.execution?.status === 'FAILED')
    });
  }
};
```

### Webhook Integration (Backend)

```typescript
import express from 'express';
import { createHmac } from 'crypto';

const app = express();

app.post('/webhooks/lifi', express.json(), (req, res) => {
  // Verify webhook signature
  const signature = req.headers['x-lifi-signature'];
  const payload = JSON.stringify(req.body);

  const expectedSignature = createHmac('sha256', process.env.LIFI_WEBHOOK_SECRET)
    .update(payload)
    .digest('hex');

  if (signature !== expectedSignature) {
    return res.status(401).send('Invalid signature');
  }

  // Process webhook
  const { event, data } = req.body;

  switch (event) {
    case 'route.completed':
      // Update database, notify user, etc.
      console.log('Route completed:', data.routeId);
      break;

    case 'route.failed':
      // Handle failure, refund user, etc.
      console.log('Route failed:', data.routeId, data.error);
      break;

    case 'fee.collected':
      // Track revenue
      console.log('Fee collected:', data.amount, data.token);
      break;
  }

  res.status(200).send('OK');
});
```

## Performance Optimization

### Caching Strategies

```typescript
// Cache chain and token data (rarely changes)
import { LRUCache } from 'lru-cache';

const chainCache = new LRUCache({
  max: 100,
  ttl: 1000 * 60 * 60 // 1 hour
});

async function getChainsWithCache() {
  const cached = chainCache.get('chains');
  if (cached) return cached;

  const lifi = new LIFI({ integrator: 'your-app' });
  const chains = await lifi.getChains();

  chainCache.set('chains', chains);
  return chains;
}

// Cache routes for same parameters (short TTL)
const routeCache = new LRUCache({
  max: 50,
  ttl: 1000 * 30 // 30 seconds
});

async function getRoutesWithCache(request) {
  const cacheKey = JSON.stringify(request);
  const cached = routeCache.get(cacheKey);
  if (cached) return cached;

  const lifi = new LIFI({ integrator: 'your-app' });
  const routes = await lifi.getRoutes(request);

  routeCache.set(cacheKey, routes);
  return routes;
}
```

### Parallel Route Fetching

```typescript
// Fetch routes for multiple token pairs in parallel
async function getMultipleRoutes(requests) {
  const lifi = new LIFI({ integrator: 'your-app' });

  const routePromises = requests.map(request =>
    lifi.getRoutes(request).catch(err => ({
      error: err.message,
      request
    }))
  );

  const results = await Promise.all(routePromises);

  return results.filter(r => !r.error);
}

// Usage
const routes = await getMultipleRoutes([
  { fromChainId: 1, toChainId: 137, ... },
  { fromChainId: 1, toChainId: 42161, ... },
  { fromChainId: 137, toChainId: 10, ... }
]);
```

### Widget Performance

```typescript
// Lazy load widget
import { lazy, Suspense } from 'react';

const LiFiWidget = lazy(() => import('@lifi/widget').then(m => ({ default: m.LiFiWidget })));

function App() {
  return (
    <Suspense fallback={<div>Loading swap widget...</div>}>
      <LiFiWidget config={widgetConfig} />
    </Suspense>
  );
}
```

## Migration Guides

### From 0x API to LI.FI

```typescript
// Before (0x)
const response = await fetch(
  `https://api.0x.org/swap/v1/quote?` + new URLSearchParams({
    sellToken: 'ETH',
    buyToken: 'DAI',
    sellAmount: '1000000000000000000'
  })
);

// After (LI.FI)
const lifi = new LIFI({ integrator: 'migrated-from-0x' });
const routes = await lifi.getRoutes({
  fromChainId: 1,
  fromTokenAddress: '0x0000000000000000000000000000000000000000', // ETH
  fromAmount: '1000000000000000000',
  toChainId: 1,
  toTokenAddress: '0x6B175474E89094C44Da98b954EedeAC495271d0F', // DAI
  fromAddress: userAddress
});

const bestRoute = routes.routes[0];
// Execute with SDK or display in Widget
```

### From 1inch API to LI.FI

```typescript
// Before (1inch)
const response = await fetch(
  `https://api.1inch.dev/swap/v5.2/1/quote?` + new URLSearchParams({
    src: '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE', // ETH
    dst: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', // USDC
    amount: '1000000000000000000'
  }),
  { headers: { 'Authorization': `Bearer ${API_KEY}` } }
);

// After (LI.FI) - Includes 1inch + other aggregators
const routes = await lifi.getRoutes({
  fromChainId: 1,
  fromTokenAddress: '0x0000000000000000000000000000000000000000',
  fromAmount: '1000000000000000000',
  toChainId: 1,
  toTokenAddress: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
  fromAddress: userAddress,

  // Optional: Prefer 1inch if migrating gradually
  options: {
    exchanges: { allow: ['1inch', 'uniswap', 'sushiswap'] }
  }
});
```

## Enterprise Features

For high-volume applications, contact LI.FI for:

- **Dedicated Infrastructure**: Private RPC nodes and dedicated API instances
- **Custom Rate Limits**: Higher throughput for enterprise needs
- **Volume Discounts**: Reduced fees for high transaction volumes
- **Priority Support**: Dedicated technical support and integration assistance
- **Custom Analytics**: Advanced reporting and monitoring dashboards
- **SLA Guarantees**: Uptime and performance guarantees

Contact: partnerships@li.fi
