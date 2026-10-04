---
name: pnp-markets-solana
description: Create, trade, and settle permissionless prediction markets on Solana. Use when building prediction market infrastructure, creating social media markets (Twitter/YouTube/DeFiLlama), setting up custom oracle resolution, P2P betting, or autonomous agent-driven forecasting. Supports V2 AMM, P2P (V3), and custom oracle markets with any SPL token collateral (including Token-2022).
license: MIT
metadata:
  author: pnp-protocol
  version: "2.0.0"
tags:
  - solana
  - prediction-markets
  - oracle
  - betting
  - forecast
  - market-making
  - autonomous-agents
  - p2p-markets
  - social-media
  - defi
  - info-finance
compatibility: Requires Node.js 18+, Solana RPC endpoint (mainnet or devnet), funded wallet with SOL for transaction fees, and any SPL token (including Token-2022) as collateral
---

# PNP Markets (Solana)

Create and manage prediction markets on Solana with any SPL token collateral. Supports V2 AMM markets, P2P direct bets, custom oracle resolution for AI agents, and social media markets (Twitter, YouTube, DeFiLlama).

## When to Use This Skill

Use when the user wants to:
- **Create prediction markets** on Solana (V2 AMM, P2P, or custom oracle)
- **Trade on markets** (buy/sell YES/NO outcome tokens)
- **Settle markets** as an oracle after the trading period ends
- **Redeem winning positions** after settlement
- **Create social media markets** (Twitter engagement, YouTube views, DeFiLlama metrics)
- **Use custom tokens** as prediction market collateral (any SPL token including Token-2022)
- **Build autonomous AI agents** that create, trade, and resolve markets
- **Build info finance infrastructure** using market prices as probability signals

**Triggers**: `prediction market`, `betting`, `oracle`, `settlement`, `forecast`, `YES/NO`, `outcome token`, `market resolution`, `P2P bet`, `custom oracle`, `social media market`, `autonomous market`, `info finance`, `market creation`, `prediction`, `wager`, `binary outcome`

Do not use when:
- The task is generic Solana wallet operations (use solana-dev-skill instead)
- The task is token swaps/DEX trading without prediction markets (use jupiter-skill)
- The task is NFT-related (use metaplex-foundation/skill)
- The task is about other prediction market protocols (use their specific skill)

---

## Program IDs & Core Constants

| Item | Address | Notes |
|------|---------|-------|
| **PNP Program (Mainnet)** | `8PyE2dizL52ga7ytqLtqRyjwWp4yXEx8M5Z4BAHgHuTb` | Main prediction market program |
| **PNP Program (Devnet)** | `pnpkv2qnh4bfpGvTugGDSEhvZC7DP4pVxTuDykV3BGz` | Devnet testing program |
| **USDC Mint** | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` | Common collateral (6 decimals) |
| **USDT Mint** | `Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB` | Alternative stable (6 decimals) |
| **WSOL Mint** | `So11111111111111111111111111111111111111112` | Wrapped SOL (9 decimals) |

### Precision Reference

| Token Type | Decimals | Example |
|-----------|----------|---------|
| USDC / USDT | 6 | 1 USDC = `1_000_000n` |
| SOL (wrapped) | 9 | 1 SOL = `1_000_000_000n` |
| Decision tokens (YES/NO) | 6 | Minted per-market by the program |

```typescript
// Conversion helpers
const usdcToRaw = (amount: number) => BigInt(Math.floor(amount * 1_000_000));
const daysFromNow = (days: number) => BigInt(Math.floor(Date.now() / 1000) + days * 86400);

// Example
const liquidity = usdcToRaw(100);  // 100 USDC -> 100_000_000n
const endTime = daysFromNow(7);    // 7 days from now -> Unix timestamp as bigint
```

> [!IMPORTANT]
> **Collateral can be any SPL token or Token-2022 token.** Pass the token's mint address as `baseMint` or `collateralTokenMint`. Make sure to use the correct decimals for the chosen token (e.g., USDC/USDT = 6, SOL = 9). Common mints are listed in the table above for reference.

---

## Prerequisites

1. **Solana Wallet**: Base58-encoded private key with SOL for fees (~0.05 SOL minimum)
2. **Collateral Tokens**: Any SPL token (including Token-2022) for market liquidity — USDC, USDT, SOL, or any custom token
3. **RPC Endpoint**: Mainnet RPC URL (public or dedicated like Helius/QuickNode)

```bash
# Install dependencies
cd scripts && npm install

# Set environment variables
export PRIVATE_KEY=<base58_private_key>
export RPC_URL=https://api.mainnet-beta.solana.com  # or dedicated RPC
```

---

## Quick Start

```typescript
import { PNPClient } from 'pnp-sdk';
import { PublicKey } from '@solana/web3.js';

const client = new PNPClient(
  process.env.RPC_URL || 'https://api.mainnet-beta.solana.com',
  process.env.PRIVATE_KEY!  // Base58 string or Uint8Array
);

// Collateral can be any SPL token (including Token-2022) — use the mint address of your chosen token
const USDC = new PublicKey('EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v');

// Create a prediction market
const result = await client.market.createMarket({
  question: 'Will Bitcoin reach $100K by end of 2025?',
  initialLiquidity: 1_000_000n,  // 1 USDC (6 decimals) — adjust decimals for your collateral token
  endTime: BigInt(Math.floor(Date.now() / 1000) + 30 * 24 * 60 * 60),
  baseMint: USDC,  // Any SPL or Token-2022 mint
});

console.log('Market created:', result.market.toBase58());
// Returns: { signature: string, market: PublicKey }
```

> [!TIP]
> Use `PNPClient.parseSecretKey(process.env.PRIVATE_KEY)` to handle both Base58 strings and JSON array formats automatically.

---

## Market Lifecycle & State Machine

Markets follow a strict state progression:

### V2 AMM Market (Standard)

```
CREATED ──────► ACTIVE ──────► ENDED ──────► RESOLVED ──────► CLAIMED
   │               │              │               │               │
   │          Trading live    No new trades   Oracle declares  Winners redeem
   │          Users buy/sell  allowed         YES/NO winner    collateral
   │          YES/NO tokens
   │
   └── initialLiquidity locked, PNP global oracle resolves
```

### Custom Oracle Market (Agent-Controlled)

```
CREATED ──► [15-MIN BUFFER] ──► ACTIVE ──► ENDED ──► RESOLVED ──► CLAIMED
   │               │                │          │           │           │
   │    setMarketResolvable(true)  Trade     Wait for   settleMarket() redeem
   │    MUST call within 15 min!   live      endTime    (oracle only)
   │
   └── Market starts frozen. If not activated within 15 minutes,
       it is PERMANENTLY FROZEN and cannot be recovered.
```

### State Transition Rules

| From | To | Method | Condition |
|------|-----|--------|-----------|
| CREATED | ACTIVE | `setMarketResolvable(market, true)` | Custom oracle only; must be within 15 min of creation |
| ACTIVE | ENDED | *(automatic)* | Unix timestamp reaches `endTime` |
| ENDED | RESOLVED | `settleMarket({market, yesWinner})` | Oracle-only; can only be called after `endTime` |
| RESOLVED | CLAIMED | `redeemPosition(market)` | Any winner; available forever after resolution |

---

## Core Operations: Read-Only (No Wallet Required)

These operations fetch data without executing transactions. Initialize with just an RPC URL:

```typescript
const readOnlyClient = new PNPClient('https://api.mainnet-beta.solana.com');
```

### `fetchMarketAddresses()` — Discover V2 Markets

```typescript
const addresses: string[] = await client.fetchMarketAddresses();
console.log(`Found ${addresses.length} V2 AMM markets`);
// Returns: string[] of market public key base58 addresses
```

### `fetchMarket(pubkey)` — Get On-Chain Market Data

```typescript
const { account } = await client.fetchMarket(new PublicKey('HxnpHygK1v7TqodWqAv6RvcEiK9zxAgw5jPZ6rskgj2E'));

// MarketType fields:
// account.question: string
// account.creator: PubkeyLike
// account.resolvable: boolean
// account.resolved: boolean
// account.end_time: U64Like (Unix timestamp)
// account.winning_token_id: 'yes' | 'no' | 'none' | null
// account.yes_token_mint: PubkeyLike
// account.no_token_mint: PubkeyLike
// account.collateral_token: PubkeyLike
// account.market_reserves: U64Like
// account.initial_liquidity: U64Like
```

### `getMarketPriceV2(market)` — Get Current Prices & Multipliers

```typescript
const priceData = await client.getMarketPriceV2(marketAddress);

console.log({
  yesPrice: priceData.yesPrice,           // 0-1 range (e.g., 0.65 = 65%)
  noPrice: priceData.noPrice,             // 0-1 range (e.g., 0.35 = 35%)
  yesMultiplier: priceData.yesMultiplier, // Payout ratio if YES wins (e.g., 1.54x)
  noMultiplier: priceData.noMultiplier,   // Payout ratio if NO wins (e.g., 2.85x)
  marketReserves: priceData.marketReserves, // Total collateral locked (UI units)
  yesTokenSupply: priceData.yesTokenSupply, // YES tokens minted (UI units)
  noTokenSupply: priceData.noTokenSupply,   // NO tokens minted (UI units)
});

// AMM Price Formulas:
// yesPrice = (marketReserves * yesTokenSupply) / (yesTokenSupply^2 + noTokenSupply^2)
// noPrice  = (marketReserves * noTokenSupply) / (yesTokenSupply^2 + noTokenSupply^2)
// yesMultiplier = 1 + (noTokenSupply / yesTokenSupply)^2
// noMultiplier  = 1 + (yesTokenSupply / noTokenSupply)^2
```

### `fetchSettlementCriteria(market)` — Get AI Resolution Info

```typescript
const criteria = await client.fetchSettlementCriteria(marketAddress);
// Returns: { category, reasoning, resolvable, resolution_sources, settlement_criteria }
```

### `fetchSettlementData(market)` — Get Settlement Decision

```typescript
const data = await client.fetchSettlementData(marketAddress);
// Returns: { answer: 'YES'|'NO', reasoning: string }
```

### `trading.getMarketInfo(pubkey)` — Extended Market Info

```typescript
const info = await client.trading.getMarketInfo(new PublicKey(marketAddress));
// Returns: { address, question, id, creator, initialLiquidity, marketReserves,
//            endTime, resolvable, resolved, winningTokenId,
//            yesTokenMint, noTokenMint, collateralToken,
//            yesTokenSupplyMinted, noTokenSupplyMinted }
```

---

## Core Operations: Market Creation (Wallet Required)

### Standard V2 AMM Market — `market.createMarket(params)`

Creates a V2 AMM market using PNP's global oracle for resolution.

```typescript
const result = await client.market.createMarket({
  question: 'Will SOL hit $250 by end of March?',
  initialLiquidity: 10_000_000n,  // 10 USDC (6 decimals)
  endTime: BigInt(Math.floor(Date.now() / 1000) + 7 * 86400),  // 7 days
  baseMint: new PublicKey('EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'),
});

console.log('Market:', result.market.toBase58());
// Returns: { signature: string, market: PublicKey }
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `question` | `string` | Yes | The prediction question |
| `initialLiquidity` | `bigint` | Yes | Initial liquidity in raw units (decimals depend on collateral token) |
| `endTime` | `bigint` | Yes | Unix timestamp when trading ends |
| `baseMint` | `PublicKey` | No | Collateral token mint — any SPL or Token-2022 token |

### Custom Oracle Market — `createMarketWithCustomOracle(params)`

**When to use**: When your AI agent needs full control over market resolution. Your agent's wallet becomes the oracle.

```typescript
const result = await client.createMarketWithCustomOracle({
  question: 'Will BTC hit $150K by Dec 2026?',
  initialLiquidity: 10_000_000n,  // 10 USDC (6 decimals)
  endTime: BigInt(Math.floor(Date.now() / 1000) + 30 * 86400),
  collateralMint: new PublicKey('EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'),
  settlerAddress: AGENT_WALLET_PUBKEY,  // Your agent's wallet is the oracle
  yesOddsBps: 5000,  // Optional: 50/50 odds (range: 100-9900)
});

// Returns: { market: PublicKey, signature: string }
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `question` | `string` | Yes | The prediction question |
| `initialLiquidity` | `bigint` | Yes | Initial liquidity in raw units |
| `endTime` | `bigint` | Yes | Unix timestamp when trading ends |
| `collateralMint` | `PublicKey` | Yes | Collateral token mint |
| `settlerAddress` | `PublicKey` | Yes | Oracle wallet that will settle the market |
| `yesOddsBps` | `number` | No | Initial YES odds in basis points (100-9900, default 5000) |

> [!WARNING]
> After creation, you **must** call `setMarketResolvable(market, true)` within **15 minutes** or the market is permanently frozen.

### V2 Market with Custom Odds — `createMarketV2WithCustomOdds(params)`

```typescript
const result = await client.createMarketV2WithCustomOdds({
  question: 'Will Ethereum flip Bitcoin by 2026?',
  initialLiquidity: 50_000_000n,  // 50 USDC
  endTime: daysFromNow(90),
  collateralTokenMint: USDC,
  yesOddsBps: 2000,  // 20% YES / 80% NO
  oracle: CUSTOM_ORACLE_PUBKEY,  // Optional: custom oracle
});
// Returns: { signature: string, market: string }
```

---

## Social Media Markets

### Twitter — `createMarketTwitter(params)`

```typescript
const result = await client.createMarketTwitter({
  question: 'Will this tweet cross 5000 replies?',
  tweetUrl: 'https://x.com/username/status/123456789',
  initialLiquidity: 1_000_000n,  // 1 USDC
  endTime: daysFromNow(7),
  collateralTokenMint: USDC,
});
// Returns: { signature: string, market: string, detectedTwitterUrl?, isTweetIdFormat? }
```

Supported URL formats: `https://x.com/user/status/ID`, `https://twitter.com/user/status/ID`

### YouTube — `createMarketYoutube(params)`

```typescript
const result = await client.createMarketYoutube({
  question: 'Will this video cross 1B views?',
  youtubeUrl: 'https://youtu.be/VIDEO_ID',
  initialLiquidity: 1_000_000n,
  endTime: daysFromNow(30),
  collateralTokenMint: USDC,
});
// Returns: { signature: string, market: string, detectedYoutubeUrl? }
```

Supported: `https://youtu.be/ID`, `https://youtube.com/watch?v=ID`, `https://youtube.com/shorts/ID`

### DeFiLlama — `createMarketDefiLlama(params)`

```typescript
const result = await client.createMarketDefiLlama({
  question: 'Will Uniswap TVL exceed $5B this quarter?',
  protocolName: 'uniswap-v3',
  metric: 'tvl',
  initialLiquidity: 5_000_000n,
  endTime: daysFromNow(30),
  collateralTokenMint: USDC,
});
// Returns: { signature: string, market: string, detectedProtocol?, detectedMetric? }
```

---

## P2P Markets (V3)

### Create P2P Market — `createP2PMarketGeneral(params)`

Direct peer-to-peer betting where the creator takes one side.

```typescript
const result = await client.createP2PMarketGeneral({
  question: 'Will our DAO pass Proposal #42?',
  initialAmount: 100_000_000n,  // 100 USDC (raw units, 6 decimals)
  side: 'yes',                   // Creator bets YES
  creatorSideCap: 500_000_000n,  // Max 500 USDC on creator's side
  endTime: daysFromNow(14),
  collateralTokenMint: USDC,
});
// Returns: { signature: string, market: PubkeyLike, yesTokenMint: PubkeyLike, noTokenMint: PubkeyLike }
```

### Simple P2P — `createP2PMarketSimple(params)`

UI-friendly wrapper that handles USDC conversion automatically:

```typescript
const result = await client.createP2PMarketSimple({
  question: 'Will it rain tomorrow?',
  side: 'yes',
  amountUsdc: 50,              // 50 USDC (human-readable, SDK converts)
  daysUntilEnd: 1,             // Defaults to 30 days
  creatorSideCapMultiplier: 5, // 5x initial = 250 USDC cap (default)
});
```

### P2P Social Media Variants

- `createP2PMarketTwitter(params)` — P2P + Twitter URL detection
- `createP2PMarketYoutube(params)` — P2P + YouTube URL detection
- `createP2PMarketDefiLlama(params)` — P2P + DeFiLlama metrics
- `createP2PMarketTwitterSimple(params)` — UI-friendly P2P Twitter
- `createP2PMarketYoutubeSimple(params)` — UI-friendly P2P YouTube
- `createP2PMarketDefiLlamaSimple(params)` — UI-friendly P2P DeFiLlama
- `createMarketP2PWithCustomOdds(params)` — P2P with custom initial odds

---

## Core Operations: Trading (Wallet Required)

### Buy Tokens (V2 AMM) — `trading.buyTokensUsdc(params)`

Purchases YES or NO outcome tokens using USDC collateral.

```typescript
const result = await client.trading.buyTokensUsdc({
  market: marketPubkey,
  buyYesToken: true,   // true = YES, false = NO
  amountUsdc: 10,      // 10 USDC (human-readable, SDK converts using mint decimals)
  minimumOut: 0n,      // Optional: minimum tokens received (slippage protection)
});

// Returns:
// { signature: string, usdcSpent: number, tokensReceived: number,
//   before: BalanceSnapshot, after: BalanceSnapshot }
```

### Sell Tokens (V2 AMM) — `trading.sellTokensBase(params)`

```typescript
const result = await client.trading.sellTokensBase({
  market: marketPubkey,
  burnYesToken: true,                     // true = sell YES, false = sell NO
  amountBaseUnits: 5_000_000n,            // Raw token units (6 decimals)
});
// Returns: { signature: string, tokensSold: number, usdcReceived: number }
```

### Buy Tokens (P2P/V3) — `buyV3TokensUsdc(params)`

```typescript
const result = await client.buyV3TokensUsdc({
  market: marketPubkey,
  buyYesToken: true,
  amountUsdc: 10,       // Human-readable USDC
});
// Returns: { signature: string }
```

**Key Differences**:
- **V2 AMM**: Uses `trading.buyTokensUsdc()` — human-readable `amountUsdc`
- **P2P/V3**: Uses `buyV3TokensUsdc()` — human-readable `amountUsdc`
- **Selling (V2)**: Uses `trading.sellTokensBase()` — raw units `amountBaseUnits`

---

## Core Operations: Settlement (Oracle Required)

### Activate Market — `setMarketResolvable(market, resolvable, forceResolve?)`

**When to use**: Immediately after creating a custom oracle market. Activates trading.

```typescript
await client.setMarketResolvable(marketAddress, true);
// Signature: setMarketResolvable(market: PublicKey | string, resolvable: boolean, forceResolve?: boolean)
// Returns: { signature: string }
```

> [!CAUTION]
> Must be called within **15 minutes** of creation. After that, the market is permanently frozen and cannot be recovered. Create a new market instead.

For P2P markets: `setMarketResolvableP2p(market, resolvable)`

### Settle Market (Proxy-Assisted)

After endTime passes, use the proxy server to get the AI-suggested resolution, then settle:

```typescript
// 1. Wait for settlement criteria (retries every 2s for up to 15 min)
const { resolvable, answer, criteria } = await client.waitForSettlementCriteria(marketAddress);

// 2. Settle the market if resolvable
if (resolvable) {
  // Use the anchorMarket module for V2 settlement
  const result = await client.anchorMarket.settleMarket({
    market: new PublicKey(marketAddress),
    yesWinner: answer === 'YES',
  });
  console.log('Settled:', result.signature);
}
```

---

## Core Operations: Redemption (Winner Required)

### Redeem Position (V2) — `redeemPosition(market)`

Converts winning outcome tokens back to collateral after market settlement.

```typescript
const { account: market } = await client.fetchMarket(marketPubkey);
if (!market.resolved) throw new Error('Market not settled yet');

const result = await client.redeemPosition(marketPubkey);
// Returns: { signature: string }
```

### Redeem P2P Position — `redeemP2PPosition(market)`

```typescript
const result = await client.redeemP2PPosition(marketPubkey);
// Returns: { signature: string }
```

---

## Error Handling

### Common Errors & Recovery

| Error | Cause | Solution |
|-------|-------|----------|
| `0x1770 (InvalidLiquidity)` | Liquidity below minimum | Use >= 1 USDC (`1_000_000n`) |
| `Insufficient funds for rent` | Not enough SOL for account creation | Ensure >= 0.05 SOL in wallet |
| `Blockhash not found` | Transaction expired before confirmation | Retry; use faster RPC (Helius/QuickNode) |
| `15-minute buffer expired` | Didn't call `setMarketResolvable` in time | Market is permanently frozen; create new one |
| `TokenAccountNotFound` | Missing Associated Token Account | SDK auto-creates ATAs, ensure SOL for rent |
| `Oracle mismatch` | Wrong wallet trying to settle | Only designated oracle can settle |
| `Market not ended` | Trying to settle before end time | Wait until market's `endTime` passes |
| `Market not tradable: ended` | Trying to trade after endTime | Market has ended; no more trades allowed |
| `Insufficient collateral balance` | Wallet balance below trade amount | Ensure wallet has enough USDC |
| `VALIDATION_ERROR` | Invalid parameters | Check input types and ranges |
| `TRANSPORT_ERROR` | Network/RPC failure | Retry with exponential backoff |
| `PROGRAM_ERROR` | On-chain program error | Check `.programErrorCode` and `.logs` for details |

### Error Handling Code Pattern

The SDK uses typed errors (`SdkError`, `ValidationError`, `TransportError`, `ProgramError`):

```typescript
import { SdkError, ValidationError, TransportError, ProgramError } from 'pnp-sdk';

async function safeMarketOperation<T>(
  operation: () => Promise<T>,
  operationName: string
): Promise<{ ok: boolean; result?: T; error?: { code: string; message: string; retryable: boolean } }> {
  try {
    const result = await operation();
    return { ok: true, result };
  } catch (error: any) {
    console.error(`${operationName} failed:`, error.message);

    if (error instanceof TransportError || error.message?.includes('Blockhash')) {
      return {
        ok: false,
        error: { code: 'TRANSPORT_ERROR', message: 'Network error. Retry with backoff.', retryable: true },
      };
    }

    if (error instanceof ProgramError) {
      return {
        ok: false,
        error: {
          code: `PROGRAM_ERROR_${error.programErrorCode ?? 'UNKNOWN'}`,
          message: error.message,
          retryable: false,
        },
      };
    }

    if (error instanceof ValidationError) {
      return {
        ok: false,
        error: { code: 'VALIDATION_ERROR', message: error.message, retryable: false },
      };
    }

    if (error.message?.includes('Market not tradable')) {
      return {
        ok: false,
        error: { code: 'MARKET_ENDED', message: error.message, retryable: false },
      };
    }

    return {
      ok: false,
      error: { code: 'UNKNOWN', message: error.message || String(error), retryable: false },
    };
  }
}

// Usage
const result = await safeMarketOperation(
  () => client.market.createMarket(params),
  'Create Market'
);
if (!result.ok && result.error?.retryable) {
  // Retry with exponential backoff
}
```

---

## Production Hardening

### 1. Compute Unit Budgets

PNP operations use these approximate CU limits internally:

| Operation | CU Limit |
|-----------|----------|
| Market creation (V2) | 400,000 |
| Trading (mint/burn) | 600,000 |
| Settlement | 800,000 |
| Set market resolvable | 800,000 |

The SDK sets these automatically. For custom transactions, set explicit budgets:

```typescript
import { ComputeBudgetProgram, Transaction } from '@solana/web3.js';

const tx = new Transaction();
tx.add(
  ComputeBudgetProgram.setComputeUnitLimit({ units: 400_000 }),
  ComputeBudgetProgram.setComputeUnitPrice({ microLamports: 50_000 })
);
```

### 2. Priority Fees

During network congestion, increase priority fees:

| Congestion | microLamports |
|-----------|---------------|
| Normal | 10,000 |
| Moderate | 50,000 |
| High | 100,000+ |

### 3. Timeout & Retry Pattern

```typescript
async function executeWithRetry(
  action: () => Promise<string>,
  maxRetries = 3,
  timeoutMs = 30_000
): Promise<string> {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await Promise.race([
        action(),
        new Promise<string>((_, reject) =>
          setTimeout(() => reject(new Error('Timeout')), timeoutMs)
        ),
      ]);
    } catch (error: any) {
      if (attempt === maxRetries) throw error;
      const delay = Math.pow(2, attempt - 1) * 1000;
      console.log(`Retry ${attempt} after ${delay}ms...`);
      await new Promise(r => setTimeout(r, delay));
    }
  }
  throw new Error('Max retries exceeded');
}
```

### 4. Input Validation

```typescript
function validateMarketParams(params: { question: string; initialLiquidity: bigint; endTime: bigint }) {
  if (!params.question || params.question.length === 0) throw new Error('Question cannot be empty');
  if (params.initialLiquidity < 1_000_000n) throw new Error('Min liquidity is 1 USDC (1_000_000n)');
  if (params.endTime <= BigInt(Math.floor(Date.now() / 1000))) throw new Error('End time must be in the future');
}
```

### 5. RPC Failover

```typescript
const RPC_URLS = [
  process.env.RPC_URL || 'https://api.mainnet-beta.solana.com',
  'https://mainnet.helius-rpc.com/?api-key=YOUR_KEY',
  'https://solana-mainnet.g.alchemy.com/v2/YOUR_KEY',
];
```

---

## SDK Quick Reference

| Method | Scope | When to Use |
|--------|-------|-------------|
| `market.createMarket({...})` | Write | Standard V2 AMM markets |
| `createMarketWithCustomOracle({...})` | Write | Agent-controlled market resolution |
| `createMarketV2WithCustomOdds({...})` | Write | V2 with non-50/50 starting odds |
| `createP2PMarketGeneral({...})` | Write | P2P direct bets (raw units) |
| `createP2PMarketSimple({...})` | Write | P2P direct bets (UI-friendly) |
| `createMarketTwitter({...})` | Write | V2 markets linked to tweets |
| `createMarketYoutube({...})` | Write | V2 markets linked to videos |
| `createMarketDefiLlama({...})` | Write | V2 markets linked to DeFi metrics |
| `setMarketResolvable(market, true)` | Write | Activate custom oracle markets (15 min!) |
| `setMarketResolvableP2p(market, true)` | Write | Activate P2P custom oracle markets |
| `trading.buyTokensUsdc({...})` | Write | Buy YES/NO tokens on V2 markets |
| `trading.sellTokensBase({...})` | Write | Sell YES/NO tokens on V2 markets |
| `buyV3TokensUsdc({...})` | Write | Buy tokens on P2P/V3 markets |
| `redeemPosition(market)` | Write | Redeem V2 winning position |
| `redeemP2PPosition(market)` | Write | Redeem P2P winning position |
| `getMarketPriceV2(market)` | Read | Current prices and multipliers |
| `fetchMarket(pubkey)` | Read | On-chain market account data |
| `fetchMarketAddresses()` | Read | List all V2 market addresses |
| `fetchMarkets()` | Read | All V2 markets with full data |
| `fetchSettlementCriteria(market)` | Read | AI resolution criteria |
| `fetchSettlementData(market)` | Read | Settlement decision |
| `waitForSettlementCriteria(market)` | Read | Retry until criteria available |
| `trading.getMarketInfo(pubkey)` | Read | Extended market info |
| `trading.getBalances(market)` | Read | User's token balances for market |
| `trading.getPrices(market)` | Read | Token supply-based price shares |
| `PNPClient.parseSecretKey(str)` | Static | Parse Base58 or JSON array private key |
| `client.uiToRaw(amount, decimals)` | Util | Convert UI amount to raw bigint |
| `PNPClient.detectTwitterUrl(text)` | Static | Extract Twitter URL from question |
| `PNPClient.detectYoutubeUrl(text)` | Static | Extract YouTube URL from question |
| `PNPClient.detectDefiLlamaUrl(text)` | Static | Extract DeFiLlama format from question |

---

## Script Quick Reference

All scripts are located in `scripts/` and use `dotenv/config` to load `.env`.

| Script | Purpose | Run Command |
|--------|---------|-------------|
| `create-market.ts` | Create standard V2 AMM market | `tsx scripts/create-market.ts` |
| `create-market-x.ts` | Create Twitter/X engagement market | `tsx scripts/create-market-x.ts` |
| `create-market-yt.ts` | Create YouTube views market | `tsx scripts/create-market-yt.ts` |
| `create-market-p2p.ts` | Create P2P betting market | `tsx scripts/create-market-p2p.ts` |
| `create-market-custom.ts` | Create custom oracle market | `tsx scripts/create-market-custom.ts` |
| `market-data.ts` | Fetch market info & settlement data | `tsx scripts/market-data.ts` |
| `trade.ts` | Buy/sell outcome tokens | `tsx scripts/trade.ts --buy --market <addr> --outcome YES --amount 10` |
| `settle.ts` | Resolve market as oracle | `tsx scripts/settle.ts --market <addr> --outcome YES` |
| `redeem.ts` | Claim winnings after settlement | `tsx scripts/redeem.ts --market <addr>` |

---

## Resources

- **PNP SDK**: [`pnp-sdk` on npm](https://www.npmjs.com/package/pnp-sdk)
- **PNP Docs**: [docs.pnp.exchange/pnp-sdk](https://docs.pnp.exchange/pnp-sdk)
- **Mainnet Explorer**: [Solscan](https://solscan.io)
- **SDK Documentation**: [references/api-reference.md](references/api-reference.md)
- **Types & Precision**: [references/types-and-precision.md](references/types-and-precision.md)
- **PDA & Addresses**: [references/program-addresses.md](references/program-addresses.md)
- **Advanced Examples**: [references/examples.md](references/examples.md)
- **Use Cases**: [references/use-cases.md](references/use-cases.md)

---

## Skill Structure

```
solana-skill/
├── SKILL.md                             # Main entry point (this file)
│   ├── When to Use / Triggers
│   ├── Program IDs & Precision
│   ├── Quick Start
│   ├── Market Lifecycle / State Machine
│   ├── Core Operations (Read-Only, Creation, Trading, Settlement, Redemption)
│   ├── Error Handling
│   ├── Production Hardening
│   └── SDK Quick Reference
│
├── README.md                            # Human-facing overview for GitHub
│
├── references/
│   ├── api-reference.md                # Complete method signatures & parameter docs
│   ├── types-and-precision.md          # TypeScript interfaces, decimal constants
│   ├── program-addresses.md            # Program IDs, PDA derivations, token mints
│   ├── examples.md                     # Advanced code patterns
│   └── use-cases.md                    # Real-world prediction market patterns
│
├── scripts/                             # CLI utilities for testing
│   ├── create-market.ts
│   ├── create-market-custom.ts
│   ├── create-market-x.ts
│   ├── create-market-yt.ts
│   ├── create-market-p2p.ts
│   ├── market-data.ts
│   ├── trade.ts
│   ├── settle.ts
│   └── redeem.ts
│
└── package.json
```

**Progressive disclosure**: SKILL.md covers 80% of use cases. Reference files handle the deep details.
