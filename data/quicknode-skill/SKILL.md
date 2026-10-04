---
name: quicknode-skill
description: "Quicknode blockchain infrastructure for 80+ chains: Core RPC API, Streams, Webhooks, Blazar WSS, Solana gRPC, HyperCore gRPC, SQL Explorer, Metaplex DAS API, Blockbook, Ordinals & Runes API, Swap API, x402, MPP, Agent Subscriptions, CLI, and MCP. Use for any Quicknode product, blockchain data access, or wallet-paid agent access."
---

# Quicknode Blockchain Infrastructure

## Intake Questions
- Which chain and network should Quicknode target?
- Is this read-only or should I create infrastructure (streams, webhooks, IPFS writes)?
- Does this require real-time streaming (Solana gRPC/Blazar WSS/HyperCore gRPC) or standard RPC?
- What endpoint or API key should I use (default: `QUICKNODE_RPC_URL`, optional `QUICKNODE_WSS_URL` / `QUICKNODE_API_KEY`)?
- If no API key exists, does the agent want pay-per-request access (x402, MPP) or a wallet-paid Quicknode account via [Agent Subscriptions](#agent-subscriptions)?
- Any constraints (latency, regions, throughput, destinations)?

## Safety Defaults
- Default to testnet/devnet when a network is not specified.
- Prefer read-only operations and dry runs before creating resources.
- Never ask for or accept private keys or secret keys.

## Confirm Before Write
- Require explicit confirmation before creating or modifying Streams, Webhooks, or IPFS uploads.
- Require explicit confirmation before creating an Agent Subscription, topping up credits, or any action that spends real funds via x402 or MPP.
- If confirmation is missing, return the exact API payload for review.

## Quick Reference

### Infrastructure

| Product | Description | Use Case |
|---------|-------------|----------|
| **Core RPC API** | High-performance blockchain access for 80+ chains | dApp backend, wallet interactions |
| **Dedicated Clusters** | Dedicated private node clusters | High-throughput production, compliance isolation |
| **IPFS** | Decentralized file storage | NFT metadata, asset hosting |

### Real-Time Data

| Product | Description | Use Case |
|---------|-------------|----------|
| **Streams** | Real-time & historical blockchain data pipelines | Event monitoring, analytics, indexing |
| **Streams Backfills** | On-demand historical data backfill into Streams | Gap recovery, historical re-indexing |
| **Webhooks** | Event-driven notifications | Alerts, transaction monitoring |
| **Solana gRPC** | Solana Geyser streaming — included on Scale/Business, add-on on Build/Accelerate | Real-time account, transaction, slot data |
| **Blazar WSS** | Quicknode-built Solana WebSocket engine — all plans, free | Fast block, account, transaction, and slot subscriptions |
| **HyperCore gRPC** | gRPC streaming for Hyperliquid L1 — included on all paid plans | Trades, order book diffs, events, blocks in real time |

### Indexed Data

| Product | Description | Use Case |
|---------|-------------|----------|
| **SQL Explorer** | Direct SQL access to indexed blockchain data | Trading analytics, historical queries, market analysis |
| **Agent Identity (ERC-8004)** | On-chain agent discovery and reputation records | Agent identity, capability advertising |
| **Blockbook** | Wallet-centric blockchain data via JSON-RPC | Address balances, UTXOs, transaction history |
| **Metaplex DAS API** | Solana Digital Asset Standard — NFTs, cNFTs, fungible tokens, MPL Core | NFT/token queries, compressed NFTs, asset search |
| **Ordinals & Runes API** | Bitcoin inscriptions and Runes protocol data | Inscription lookup, UTXO tracking, Runes balances |

### Trading & DeFi

| Product | Description | Use Case |
|---------|-------------|----------|
| **Swap API** | Multi-DEX aggregated token swaps | Solana (Jupiter/Metis), EVM (0x, OpenOcean, Aerodrome, Velodrome, Titan) |

### Marketplace Add-ons

| Product | Description | Use Case |
|---------|-------------|----------|
| **Solana Priority Fee API** | Recommended priority fees for Solana transactions | Fee estimation, transaction landing |
| **Jito Bundles** | Solana bundle submission and status APIs | MEV-aware transaction delivery |
| **Single Flight RPC** | Request de-duplication for identical in-flight RPC calls | High-concurrency read workloads |
| **Multi-region Transaction Broadcast** | Transaction propagation across multiple regions | Latency-sensitive submission |
| **Scorechain Risk Assessment API** | Wallet and transaction risk data | Compliance, fraud monitoring |
| **Block Timestamp Lookup** | Timestamp-to-block lookup utilities | Time-window to block-range conversion |
| **Multi-chain Stablecoin Balance API** | Stablecoin balances across supported chains | Treasury, payments, portfolio state |
| **Covalent GoldRush APIs** | Multi-chain wallet and portfolio data | Wallet summaries, token/NFT holdings |

### Agent Surface

| Product | Description | Use Case |
|---------|-------------|----------|
| **x402** | Testnet monthly cap plus mainnet pay-per-request via stablecoins | Keyless RPC access, AI agents, pay-as-you-go |
| **MPP** | Testnet monthly cap plus mainnet pay-per-request via IETF Payment Authentication | AI agents, multi-service payments, high-volume sessions |
| **Agent Subscriptions** | Wallet-paid Quicknode account creation, returns a `QN_*` full platform API key | Autonomous agents needing full platform access |
| **Quicknode CLI** | `qn` CLI for endpoints, Streams, Webhooks, KV, and SQL from the terminal | Scripting, CI/CD, infrastructure automation |
| **Quicknode MCP** | Native Claude/OpenAI connector plus generic MCP server — Admin API via MCP | Manage Quicknode from Claude, ChatGPT, Codex, Cursor, or any MCP-capable AI tool |

### Platform

| Product | Description | Use Case |
|---------|-------------|----------|
| **Admin API** | REST API for account management | Endpoint CRUD, usage monitoring, billing |
| **Key-Value Store** | Serverless key-value and list storage (beta) | Persistent state for Streams, dynamic address lists |
| **Quicknode SDK** | Official SDK for Quicknode product APIs | Admin API, Streams, Webhooks, KV, SQL Explorer |

---

## Core RPC API

Quicknode provides low-latency RPC endpoints for 80+ blockchain networks.

`qn rpc call` (CLI) and `qn.rpc.call` (SDK) reach any supported network via **Tooling Access** — a single multichain, read-only endpoint Quicknode provisions automatically with short-lived JWTs. No endpoint setup required. See [references/cli-reference.md](references/cli-reference.md) / [references/sdk-reference.md](references/sdk-reference.md). Use a dedicated endpoint below for a fixed URL, non-read-only methods, or dedicated throughput.

### Endpoint Setup

```typescript
// EVM chains (ethers.js)
import { JsonRpcProvider } from 'ethers';
const provider = new JsonRpcProvider(process.env.QUICKNODE_RPC_URL!);

// EVM chains (viem)
import { createPublicClient, http } from 'viem';
import { mainnet } from 'viem/chains';
const client = createPublicClient({
  chain: mainnet,
  transport: http(process.env.QUICKNODE_RPC_URL!),
});

// Solana
import { createSolanaRpc } from '@solana/kit';
const rpc = createSolanaRpc(process.env.QUICKNODE_RPC_URL!);
```

### Authentication

Quicknode endpoints include authentication in the URL:
```
https://{ENDPOINT_NAME}.{NETWORK}.quiknode.pro/{API_KEY}/
```

For additional security, enable JWT authentication or IP allowlisting in the Quicknode dashboard.

### Supported Networks

| Category | Networks |
|----------|----------|
| **EVM** | Ethereum, Polygon, Arbitrum, Optimism, Base, BSC, Avalanche, Fantom, zkSync, Scroll, Linea, Hyperliquid EVM (HyperEVM) |
| **Non-EVM** | Solana, Bitcoin, NEAR, Stacks, Cosmos, Sei, Aptos, Sui, TON, Hyperliquid (HyperCore) |

Not exhaustive. Full list: https://www.quicknode.com/chains

### Rate Limits & Plans

As of 2026-02-02. Verify current limits in Quicknode docs before sizing a production system.

| Plan | Requests/sec | Credits/month |
|------|-------------|---------------|
| Free Trial | 15 | 10M |
| Build | 50 | 80M |
| Accelerate | 125 | 450M |
| Scale | 250 | 950M |
| Business | 500 | 2B |

See [references/rpc-reference.md](references/rpc-reference.md) for complete RPC documentation including method tables for EVM, Solana, and Bitcoin chains, WebSocket patterns, and batch request examples.

## IPFS

Decentralized file storage with Quicknode's IPFS gateway.

See [references/ipfs-reference.md](references/ipfs-reference.md) for upload examples, metadata examples, and complete IPFS documentation.

## Dedicated Clusters

Dedicated private node clusters for teams requiring deterministic throughput, regional pinning, or compliance isolation. Agents typically do not provision Dedicated Clusters directly — this is an infrastructure decision made by the account owner.

**Marketing:** https://www.quicknode.com/clusters
**Docs:** https://www.quicknode.com/docs/custom-rpc-options

---

## Streams

Real-time & historical blockchain data pipelines that filter, transform, and deliver data to your destinations.

### Stream Types

| Type | Data | Use Case |
|------|------|----------|
| **Block** | Full block data | Block explorers, analytics |
| **Transaction** | Transaction details | Tx monitoring, indexing |
| **Logs** | Contract events | DeFi tracking, NFT sales, token transfers |
| **Receipt** | Transaction receipts | Gas analysis, status tracking |

### Quick Setup

1. Create stream in Quicknode dashboard
2. Select network and data type
3. Add filter function (JavaScript)
4. Configure destination (webhook, S3, database)

See [references/streams-reference.md](references/streams-reference.md) for filter examples and full Streams documentation.

## Streams Backfills

On-demand historical data delivery into an existing Stream. Use Backfills to recover gaps, seed a new data store with history, or re-index a range of blocks without rebuilding your pipeline.

**Docs:** https://www.quicknode.com/docs/streams/backfilling

### When to Use

- A Stream destination was down and you need to replay missed blocks.
- You're launching a new Stream and need historical data from block N to the current head.
- You want to re-process a range of blocks after updating a filter function.

### What to Provide

When asking an agent to trigger a Backfill, provide:
- Stream ID (from the Quicknode dashboard or Admin API)
- Start block number
- End block number (or `latest`)
- Destination confirmation (Backfills deliver to the Stream's existing destination)

See [references/streams-backfills-reference.md](references/streams-backfills-reference.md) for dataset selection, range planning, batching, compression, cost guidance, and automation notes.

## Webhooks

Event-driven notifications for blockchain activity.

### Webhooks vs Streams

| Feature | Webhooks | Streams |
|---------|----------|---------|
| **Setup** | Simple | More configuration |
| **Filtering** | Address/event-based | Custom JavaScript |
| **Destinations** | HTTP endpoint only | Webhook, S3, Postgres, Azure |
| **Processing** | Basic | Full transformation |
| **Use Case** | Simple alerts | Complex pipelines |

See [references/webhooks-reference.md](references/webhooks-reference.md) for API examples and full Webhooks documentation.

## Solana gRPC (formerly Yellowstone gRPC)

High-performance Solana Geyser plugin for real-time blockchain data streaming via gRPC. Included on Scale and Business plans; available as a Marketplace add-on on Build and Accelerate plans.

### Quick Setup

```typescript
import Client, { CommitmentLevel } from "@triton-one/yellowstone-grpc";

// Derive from HTTP URL: https://example.solana-mainnet.quiknode.pro/TOKEN/
const client = new Client(
  "https://example.solana-mainnet.quiknode.pro:10000",
  "TOKEN",
  {}
);

const stream = await client.subscribe();
stream.on("data", (data) => {
  if (data.transaction) console.log("Tx:", data.transaction);
});

stream.write({
  transactions: {
    txn_filter: {
      vote: false,
      failed: false,
      accountInclude: ["PROGRAM_PUBKEY"],
      accountExclude: [],
      accountRequired: [],
    },
  },
  accounts: {},
  slots: {},
  blocks: {},
  blocksMeta: {},
  transactionsStatus: {},
  entry: {},
  accountsDataSlice: [],
  commitment: CommitmentLevel.CONFIRMED,
});
```

### Filter Types

| Filter | Description |
|--------|-------------|
| **accounts** | Account data changes by pubkey, owner, or data pattern |
| **transactions** | Transaction events with vote/failure/account filters |
| **transactionsStatus** | Lightweight transaction status updates |
| **slots** | Slot progression and status changes |
| **blocks** | Full block data with optional tx/account inclusion |
| **blocksMeta** | Block metadata without full contents |
| **entry** | PoH entry updates |

See [references/solana-grpc-reference.md](references/solana-grpc-reference.md) for complete Solana gRPC documentation.

## Blazar WSS

Quicknode-built Solana WebSocket engine. Every standard Solana subscription method (`blockSubscribe`, `accountSubscribe`, `transactionSubscribe`, `logsSubscribe`, and more) rebuilt for reliability and speed. Included free on all plans — no add-on required. Uses the same WSS endpoint URL (`QUICKNODE_WSS_URL`) as standard Solana RPC.

**Docs:** https://www.quicknode.com/docs/solana

### Quick Setup

```typescript
const ws = new WebSocket(process.env.QUICKNODE_WSS_URL!);

ws.on('open', () => {
  ws.send(JSON.stringify({
    jsonrpc: '2.0',
    id: 1,
    method: 'blockSubscribe',
    params: ['all', { commitment: 'confirmed', encoding: 'jsonParsed' }]
  }));
});

ws.on('message', (raw) => {
  const msg = JSON.parse(raw.toString());
  if (msg.params?.result?.value?.block) {
    console.log('New block slot:', msg.params.result.context.slot);
  }
});
```

### Supported Subscription Methods

`blockSubscribe`, `accountSubscribe`, `logsSubscribe`, `programSubscribe`, `signatureSubscribe`, `slotSubscribe`, `slotsUpdatesSubscribe`, `transactionSubscribe`, `voteSubscribe`

## HyperCore (Hyperliquid)

Quicknode's data delivery infrastructure for the Hyperliquid L1 chain. Provides gRPC, JSON-RPC, WebSocket, and Info API access. Currently in public beta. Included on all paid plans.

### Access Methods

| Method | Path / Port | Use Case |
|--------|-------------|----------|
| **Info API** | `/info` (POST) | 50+ methods for market data, positions, orders |
| **JSON-RPC** | `/hypercore` (POST) | Block queries (`hl_getBlock`, `hl_getBatchBlocks`) |
| **WebSocket** | `/hypercore/ws` | Real-time subscriptions (`hl_subscribe`) |
| **gRPC** | Port 10000 | Lowest-latency streaming for trades, orders, books |

### gRPC Stream Types

| Stream | Volume | Description |
|--------|--------|-------------|
| **TRADES** | High | Execution data: coin, price, size, side, fees |
| **ORDERS** | Very High | Order lifecycle with 18+ status types |
| **BOOK_UPDATES** | Very High | L2 order book diffs |
| **TWAP** | Low | Time-weighted average price order updates |
| **EVENTS** | High | Ledger updates, funding, deposits, withdrawals |
| **BLOCKS** | Extreme | Raw HyperCore blocks (gRPC only) |
| **WRITER_ACTIONS** | Low | System-level token transfers |

### HyperEVM

| Path | Debug/Trace | Archive | Use Case |
|------|-------------|---------|----------|
| `/evm` | No | Partial | Standard EVM operations |
| `/nanoreth` | Yes | Extended | Debug, trace, WebSocket subscriptions |

See [references/hypercore-hyperliquid-reference.md](references/hypercore-hyperliquid-reference.md) for complete HyperCore and Hyperliquid documentation.

---

## SQL Explorer

Direct SQL access to indexed blockchain data without requiring infrastructure. Query billions of rows of on-chain data using standard SQL syntax and receive results in seconds.

**Docs:** https://www.quicknode.com/docs/sql-explorer

### Quick Setup

```bash
curl -X POST 'https://api.quicknode.com/sql/rest/v1/query' \
  -H 'x-api-key: YOUR_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "SELECT timestamp, coin, side, price, size FROM hyperliquid_trades WHERE block_time > now() - INTERVAL 1 HOUR ORDER BY block_number DESC LIMIT 10",
    "clusterId": "hyperliquid-core-mainnet"
  }'
```

### Coverage

**Hyperliquid (HyperCore)** - Tables covering trades, orders, fills, funding, order book diffs, perpetual markets, spot markets, blocks, transactions, system actions, builder activity, staking, ledger updates, and more.

### Key Features

- **Infrastructure-free** - No database or indexer setup required
- **Standard SQL** - Full SQL syntax including joins, subqueries, CTEs, window functions
- **40+ pre-built queries** - Common patterns for trading analytics, whale tracking, liquidations
- **Optimized performance** - Monthly partitioning, sort keys, columnar storage
- **REST API** - Execute queries programmatically via HTTPS

See [references/sql-explorer.md](references/sql-explorer.md) for complete table schemas, query examples, optimization tips, and API reference.

## Agent Identity (ERC-8004)

On-chain agent identity and reputation discovery based on the ERC-8004 standard. `erc-8004.quicknode.com` indexes registrations, feedback, validations, and reputation across supported EVM networks.

**API Base:** https://erc-8004.quicknode.com
**REST prefix:** `/v1`

See [references/agent-identity-reference.md](references/agent-identity-reference.md) for verified endpoints, x402 behavior, rate limits, and on-chain registration guidance.

## Blockbook

Wallet-centric blockchain data via the Blockbook JSON-RPC add-on. Provides address balances, UTXO sets, and transaction history across supported chains — particularly useful for UTXO-based chains like Bitcoin where standard RPC methods lack wallet-level indexing.

**Marketing:** https://www.quicknode.com/blockbook
**Docs:** https://www.quicknode.com/docs/bitcoin/blockbook/overview

### Supported Chains

Bitcoin (BTC), Ethereum (ETH), Bitcoin Cash (BCH), Dogecoin (DOGE), Litecoin (LTC), Zcash (ZEC) — each as its own add-on on your endpoint.

### When to Use

- Get the full balance and transaction history for a Bitcoin or UTXO-chain address.
- Fetch UTXOs to construct a transaction.
- Look up confirmed/unconfirmed balance for an address without running a personal indexer.

See [references/blockbook-reference.md](references/blockbook-reference.md) for methods and examples.

## Metaplex DAS API (Solana)

Comprehensive API for querying Solana digital assets — standard NFTs, compressed NFTs (cNFTs), fungible tokens, MPL Core Assets, and Token 2022 Assets. Available as the **Metaplex Digital Asset Standard (DAS) API** add-on on your Quicknode Solana endpoint. Formerly documented in this skill as "Solana DAS API".

**Marketing:** https://www.quicknode.com/metaplex-das-api
**Docs:** https://www.quicknode.com/docs/solana/solana-das-api

### Quick Setup

```javascript
// Get all assets owned by a wallet
const response = await fetch(process.env.QUICKNODE_RPC_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    jsonrpc: '2.0',
    id: 1,
    method: 'getAssetsByOwner',
    params: {
      ownerAddress: 'E645TckHQnDcavVv92Etc6xSWQaq8zzPtPRGBheviRAk',
      limit: 10,
      options: { showFungible: true, showCollectionMetadata: true }
    }
  })
});
const { result } = await response.json();
// result.total — total assets
// result.items — array of asset metadata
// result.cursor — for pagination
```

### Available Methods

| Method | Description |
|--------|-------------|
| `getAsset` | Get metadata for a single asset |
| `getAssets` | Get metadata for multiple assets |
| `getAssetProof` | Get Merkle proof for a compressed asset |
| `getAssetProofs` | Get Merkle proofs for multiple assets |
| `getAssetsByAuthority` | List assets by authority |
| `getAssetsByCreator` | List assets by creator |
| `getAssetsByGroup` | List assets by group (e.g., collection) |
| `getAssetsByOwner` | List assets by wallet owner |
| `getAssetSignatures` | Transaction signatures for compressed assets |
| `getTokenAccounts` | Token accounts by mint or owner |
| `getNftEditions` | Edition details of a master NFT |
| `searchAssets` | Search assets with flexible filters |

See [references/metaplex-das-reference.md](references/metaplex-das-reference.md) for complete DAS API documentation with all methods, parameters, and examples.

## Ordinals & Runes API

Bitcoin inscription and Runes protocol data via a Quicknode Marketplace add-on. Query inscription metadata, satoshi data, Rune details, and collection data through JSON-RPC and ORD-compatible REST on your Bitcoin endpoint. 21 methods available.

**Marketing:** https://www.quicknode.com/ordinals-runes
**Docs:** https://www.quicknode.com/docs/bitcoin/ord_getInscription

### When to Use

- Look up inscription details (content type, sat number, rarity, genesis transaction) for a given inscription ID.
- Query Rune etching details, minting parameters, and live supply.
- Fetch Bitcoin outputs and the inscriptions or Runes they contain.

See [references/ordinals-runes-reference.md](references/ordinals-runes-reference.md) for supported methods and examples.

## Marketplace Add-ons

Endpoint add-ons for specialized capabilities that can be enabled on Quicknode endpoints. Use the add-on docs or dashboard-provided endpoint details for exact API shapes.

### Solana Priority Fee API

```javascript
// Get recommended priority fees
const response = await rpc.request('qn_estimatePriorityFees', {
  last_n_blocks: 100,
  account: 'YOUR_ACCOUNT'
}).send();
```

### Jito Bundles

MEV-aware Solana bundle submission and status APIs for users who have enabled the Jito add-on.

### Single Flight RPC

Request de-duplication for identical in-flight RPC calls. Useful for high-concurrency applications where many workers or users request the same data at the same time.

### Multi-region Transaction Broadcast

Broadcast signed transactions through multiple regions to improve propagation for latency-sensitive transaction submission.

### Scorechain Risk Assessment API

Wallet and transaction risk data for compliance, fraud monitoring, and risk-aware transaction workflows.

### Block Timestamp Lookup

Timestamp-to-block lookup utilities for converting human time windows into block ranges.

### Multi-chain Stablecoin Balance API

Stablecoin balances across supported chains for treasury, payments, and portfolio workflows.

### Covalent GoldRush APIs

Multi-chain wallet and portfolio data, including balances, token holdings, NFT holdings, and transaction history where supported.

See [references/marketplace-addons.md](references/marketplace-addons.md) for current add-on guidance and product-specific reference links.

---

## Swap API

Multi-DEX aggregated token swaps via Quicknode Marketplace add-ons. Supports Metis/Jupiter, 0x, OpenOcean, Aerodrome, Velodrome, Titan Meta Aggregator, and Hyperliquid Exchange API. Each provider is enabled as a separate add-on or product surface on your endpoint/account.

**Marketing:** https://www.quicknode.com/swap-api

### Solana — Metis (Jupiter)

```typescript
import { createJupiterApiClient } from '@jup-ag/api';

const jupiterApi = createJupiterApiClient({
  basePath: process.env.QUICKNODE_METIS_URL!
});

const quote = await jupiterApi.quoteGet({
  inputMint: 'So11111111111111111111111111111111111111112',   // SOL
  outputMint: 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v', // USDC
  amount: 1_000_000_000,  // 1 SOL in lamports
  slippageBps: 50
});

const swapResult = await jupiterApi.swapPost({
  swapRequest: {
    quoteResponse: quote,
    userPublicKey: 'YourPubkey...'
  }
});
// swapResult.swapTransaction — serialized tx ready for signing
```

Set `QUICKNODE_METIS_URL` to your Metis endpoint (e.g., `https://jupiter-swap-api.quiknode.pro/YOUR_TOKEN`). Enable the **Metis Jupiter Swap API** add-on in the Quicknode dashboard.

See [references/swap-api-reference.md](references/swap-api-reference.md) for provider positioning, verified examples, safety defaults, and troubleshooting.

---

## x402 (Pay-Per-Request RPC)

Pay-per-request RPC access via stablecoin payments. No API key required. Three payment models: pay-per-request ($0.001/call), nanopayment (batched via Circle Gateway), and credit drawdown (SIWX auth, $10/1M mainnet credits). Testnet wallets share a monthly cap of 1,000,000 credits per wallet; mainnet wallets are uncapped. Supports USDC on Base/Polygon/Solana and USDG on XLayer. Access 140+ chain endpoints.

### Quick Setup

```typescript
import { createQuicknodeX402Client } from "@quicknode/x402";

const client = await createQuicknodeX402Client({
  baseUrl: "https://x402.quicknode.com",
  network: "eip155:84532", // Base Sepolia payment network
  evmPrivateKey: process.env.PRIVATE_KEY as `0x${string}`,
  paymentModel: "pay-per-request",
});

// Use like normal fetch — payment negotiation is handled automatically
const response = await client.fetch("https://x402.quicknode.com/ethereum-mainnet", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    jsonrpc: "2.0",
    method: "eth_blockNumber",
    params: [],
    id: 1,
  }),
});
```

See [references/x402-reference.md](references/x402-reference.md) for complete x402 documentation including SIWX authentication, credit management, and `@quicknode/x402` setup.

## MPP (Machine Payments Protocol)

Pay-per-request RPC access via IETF Payment Authentication headers. No API key required. Two intent types: charge ($0.001/request) and session ($0.00001/request via off-chain vouchers). Tempo testnet wallets share a monthly cap of 1,000,000 credits per wallet; mainnet wallets are uncapped. Payment via PathUSD or USDC.e on Tempo mainnet, PathUSD on Tempo testnet, or USDC on Solana. Access 140+ chain endpoints.

### Quick Setup

```typescript
import { Mppx, tempo } from 'mppx/client'
import { privateKeyToAccount } from 'viem/accounts'

const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`)

// Polyfills globalThis.fetch — handles 402 challenges automatically
Mppx.create({
  methods: [tempo({ account })],
})

// Charge intent ($0.001/req) — payment is transparent
const response = await fetch('https://mpp.quicknode.com/tempo-mainnet', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    jsonrpc: '2.0',
    id: 1,
    method: 'eth_blockNumber',
    params: [],
  }),
})

const { result } = await response.json()
console.log('Block number:', BigInt(result))
```

See [references/mpp-reference.md](references/mpp-reference.md) for complete MPP documentation including charge vs session intents, Solana setup, CLI usage, and payment receipts.

## Agent Subscriptions

Programmatic Quicknode account creation for autonomous agents. A single POST to `/api/v1/agent/subscriptions` with an x402 or MPP payment creates a paid account synchronously and returns a `QN_*` full platform API key, no dashboard signup or email confirmation required. The same payment SDKs used for x402 and MPP per-request RPC sign the subscription payment.

**Docs:** https://www.quicknode.com/docs/build-with-ai/agent-subscriptions

### When to Use

- Pay-per-request (x402, MPP) when the agent only needs short-lived RPC access with no persistent state.
- Agent Subscriptions when the agent needs the full platform: Streams, Webhooks, Key-Value Store, multiple endpoints, security rules, billing, or any other Admin API surface.

### Discover Plans

To fetch the live plan list, prices, accepted payment networks, asset contract addresses, and recipient (`payTo`) addresses, send the request without a payment header. The server returns HTTP 402 with the details in the body and a `PAYMENT-REQUIRED` header (base64-encoded x402 requirement).

```bash
curl -X POST https://www.quicknode.com/api/v1/agent/subscriptions \
  -H "Content-Type: application/json" \
  -d '{}'
```

Parse the 402 body, pick a plan, then retry the request through the SDK.

### Quick Setup (x402)

```typescript
import { createQuicknodeX402Client } from '@quicknode/x402'

const client = await createQuicknodeX402Client({
  baseUrl: 'https://www.quicknode.com',
  network: 'eip155:8453', // Base Mainnet
  evmPrivateKey: process.env.PRIVATE_KEY as `0x${string}`,
})

const res = await client.fetch(
  'https://www.quicknode.com/api/v1/agent/subscriptions',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      plan_name: 'b6_build', // b6_build | b6_accelerate | b6_scale | b6_business
      interval: 'monthly', // monthly | yearly
      email: 'agent@example.com',
      password: process.env.ACCOUNT_PASSWORD,
      password_confirmation: process.env.ACCOUNT_PASSWORD,
      full_name: 'Autonomous Agent',
      name: 'Agent Account',
      billing_address: {
        line1: '123 Main St',
        city: 'New York',
        postal_code: '10001',
        country: 'US',
      },
    }),
  },
)

const { api_key } = await res.json() // "QN_..." full platform API key
```

The returned `api_key` is the same `QUICKNODE_API_KEY` used everywhere else in this skill. Use it against `https://api.quicknode.com/v0/...` to provision endpoints, configure security, top up credits, read balances, and so on.

> **Paying with Solana?** Use [`@quicknode/x402-solana`](https://github.com/quiknode-labs/x402-solana) to sign x402 payments with a Solana keypair instead of an EVM private key. Once configured, the subscription request body and Admin API steps are identical to the x402 example above. See the [How to Access Solana RPC with x402](https://www.quicknode.com/guides/solana-development/ai-agents/how-to-access-solana-rpc-with-x402-solana) guide for setup details.

### Quick Setup (MPP)

```typescript
import { Mppx, tempo } from 'mppx/client'
import { privateKeyToAccount } from 'viem/accounts'

const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`)

Mppx.create({ methods: [tempo({ account })] })

const subscriptionRes = await fetch(
  'https://www.quicknode.com/api/v1/agent/subscriptions',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      plan_name: 'b6_build', // b6_build | b6_accelerate | b6_scale | b6_business
      interval: 'monthly', // monthly | yearly
      email: 'agent@example.com',
      password: process.env.ACCOUNT_PASSWORD,
      password_confirmation: process.env.ACCOUNT_PASSWORD,
      full_name: 'Autonomous Agent',
      name: 'Agent Account',
      billing_address: {
        line1: '123 Main St',
        city: 'New York',
        postal_code: '10001',
        country: 'US',
      },
    }),
  },
)

const { api_key } = await subscriptionRes.json() // "QN_..." full platform API key
```

### Endpoints

| Method | Path | Auth | Rate limit | Purpose |
|--------|------|------|------------|---------|
| POST | `/api/v1/agent/subscriptions` | Payment header (x402 or MPP) | 20/min, 5/hour by IP + email | Create account and subscription |
| POST | `/api/v1/agent/top_up` | API key + payment header | 30/min by API key | Add credits to an existing subscription |
| GET | `/api/v1/agent/balance` | API key | 60/min by API key | Read current credit balance |

All requests target `https://www.quicknode.com`.

### Plan IDs

`b6_build`, `b6_accelerate`, `b6_scale`, `b6_business`. Map directly to the public Build / Accelerate / Scale / Business plans on [pricing](https://www.quicknode.com/pricing). Use the discovery 402 above when the agent needs to choose a plan dynamically.

### Guard Rails

- **Real funds**: Subscriptions settle in real stablecoins on a mainnet payment network. Confirm plan, interval, and payment network with the user before sending the request.
- **Duplicate email protection**: Re-using an existing email returns an error. Resume failed requests with the same `email` and `password` instead of creating a duplicate account.
- **Payment retry safety**: If validation fails after a payment header is generated, retry with the same signed payment header byte-for-byte. Do not sign a fresh payment for the same attempted operation unless the server requires a new challenge.
- **No free trials**: All subscriptions are production-grade from the first request.
- **Synchronous creation**: Account creation and subscription activation happen in the same request. There is no async job or webhook to wait for.
- **No invented details**: Never fabricate billing details, passwords, or email addresses. Require explicit user input. Password must be 8–64 characters with at least one lowercase letter, one uppercase letter, one number, and one special character.

See [references/agent-subscriptions-reference.md](references/agent-subscriptions-reference.md) for complete endpoint reference, top-up flow, and balance checks.

## Quicknode CLI

Command-line tool (`qn`) for managing Quicknode infrastructure from the terminal. Available on all paid plans.

### Installation

```bash
# Homebrew
brew install quicknode/tap/qn

# Docker
docker pull quiknode/qn-cli:latest
```

### Authentication

Use interactive login for local work, or pass the API key explicitly in non-interactive environments:

```bash
qn auth login
qn auth login --api-key <KEY>
qn auth whoami
```

Credential precedence is `--api-key`, then `--config-file`, then `~/.config/qn/config.toml`. The CLI does not read API keys directly from environment variables.

### Agent Context

```bash
qn agent context
qn agent context -o json
```

### Key Commands

```bash
# Endpoints
qn endpoint list
qn endpoint create --chain ethereum --network mainnet

# RPC (Tooling Access) — no endpoint setup required
qn tooling-access status
qn tooling-access enable
qn rpc call eth_getBlockByNumber '["latest", false]' --network base-mainnet

# Account and chain metadata
qn auth whoami --format json
qn chain credits ethereum --format json

# SQL Explorer
qn sql query "SELECT COUNT(*) FROM hyperliquid_trades" --cluster-id hyperliquid-core-mainnet --format json
qn sql schema hyperliquid-core-mainnet

# Streams / Webhooks / KV
qn stream list
qn webhook list
qn kv set get my-key
```

Use `--format json` for machine-readable output. Mutating commands prompt before acting; require explicit user confirmation before bypassing prompts in automation.

See [references/cli-reference.md](references/cli-reference.md) for complete CLI documentation.

## Quicknode MCP

Native Claude/OpenAI connector and generic MCP server that exposes Quicknode Admin API capabilities to AI assistants via the Model Context Protocol (MCP).

### Setup

**Claude Web/Desktop:** Settings → Customize → Connectors → find Quicknode → Connect.

**Claude Code:**
```bash
claude mcp add --transport http quicknode https://mcp.quicknode.com/mcp
```

Interactive setup uses OAuth: log in to Quicknode, select **Viewer** or **Admin**, and approve access. Use Viewer for read-only inspection and Admin only when the assistant needs to create, delete, or modify resources.

**OpenAI (ChatGPT/Codex):** Install Quicknode from the ChatGPT Apps catalog or via `/plugin` in Codex when available. Use the consolidated OpenAI tab on the Quicknode MCP docs page for current setup details.

### Capabilities

The MCP server provides tools for endpoint management (list, create, delete, rate limits), security rules, usage monitoring, billing, and chain discovery. Agents and users can manage their Quicknode workspace conversationally without leaving their AI tool.

See [references/mcp-reference.md](references/mcp-reference.md) for the complete tool surface and setup instructions.

---

## Quicknode SDK

Official SDK for Quicknode product APIs: Admin API, Streams, Webhooks, Key-Value Store, and SQL Explorer. The `rpc` client (Node `3.7.0+`, other languages `0.7.0+`) also makes JSON-RPC calls to any supported network via Tooling Access — no endpoint setup required. Chain-specific client libraries still apply for typed chain abstractions or a dedicated endpoint.

### Installation

```bash
npm install @quicknode/sdk
```

### Basic Usage

```typescript
import { QuicknodeSdk } from '@quicknode/sdk';

const qn = QuicknodeSdk.fromEnv();

const endpoints = await qn.admin.getEndpoints({
  limit: 20,
  sortBy: 'created_at',
  sortDirection: 'desc',
});

const account = await qn.admin.accountInfo();
const apiCredits = await qn.admin.getApiCredits('ethereum');

const trades = await qn.sql.query(
  'SELECT * FROM hyperliquid_trades LIMIT 5',
  'hyperliquid-core-mainnet'
);
```

See [references/sdk-reference.md](references/sdk-reference.md) for complete SDK documentation.

## Admin API

REST API for programmatic management of Quicknode endpoints, usage, rate limits, security, billing, and teams. Enables infrastructure-as-code workflows.

### Quick Reference

| Resource | Methods | Endpoint |
|----------|---------|----------|
| Chains | GET | `/v0/chains` |
| Account Info | GET | `/v0/account/info` |
| API Credits | GET | `/v0/api-credits/{chain}` |
| Endpoints | GET, POST, PATCH, DELETE | `/v0/endpoints` |
| Metrics | GET | `/v0/endpoints/{id}/metrics` |
| Rate Limits | GET, POST, PUT | `/v0/endpoints/{id}/method-rate-limits`, `/v0/endpoints/{id}/rate-limits` |
| Security | GET | `/v0/endpoints/{id}/security_options` |
| Tooling Access | GET, PATCH, POST | `/v0/tooling-access`, `/v0/tooling-access/token` |
| Usage | GET | `/v0/usage/rpc`, `by-endpoint`, `by-method`, `by-chain` |
| Billing | GET | `/v0/billing/invoices` |
| Teams | GET | `/v0/teams` |

### Authentication

All requests use the `x-api-key` header against `https://api.quicknode.com/v0/`.

```typescript
const QN_API_KEY = process.env.QUICKNODE_API_KEY!;

const res = await fetch('https://api.quicknode.com/v0/endpoints', {
  headers: { 'x-api-key': QN_API_KEY },
});
const endpoints = await res.json();
```

See [references/admin-api-reference.md](references/admin-api-reference.md) for full Admin API documentation including endpoint CRUD, usage monitoring, rate limit configuration, security options, Tooling Access, billing, and teams.

## Key-Value Store (Beta)

Serverless storage for lists and key-value sets, primarily accessed from within Streams filter functions via the `qnLib` helper library. Also available via REST API.

### Stream Integration (qnLib)

**List operations** — manage lists of items (e.g., wallet addresses):
- `qnLib.qnUpsertList` — create or update a list
- `qnLib.qnAddListItem` — add item to a list
- `qnLib.qnRemoveListItem` — remove item from a list
- `qnLib.qnContainsListItems` — batch membership check
- `qnLib.qnDeleteList` — delete a list

**Set operations** — manage key-value pairs:
- `qnLib.qnAddSet` — create a key-value set
- `qnLib.qnGetSet` — retrieve value by key
- `qnLib.qnBulkSets` — bulk create/remove sets
- `qnLib.qnListAllSets` — list all set keys
- `qnLib.qnDeleteSet` — delete a set

See [references/kv-reference.md](references/kv-reference.md) for REST API usage, size limits, and CLI (`qn kv`) commands.

---

## Other Quicknode Products

The following Quicknode products are available but agents typically do not invoke them directly. They are provisioned by account owners through the dashboard or by a human operator.

- **Validator as a Service** — Non-custodial Ethereum staking with custom fee recipients and MEV-boost. https://www.quicknode.com/validator-as-a-service
- **Solana Validator** — Managed Solana validator infrastructure. https://www.quicknode.com/chains/solana/validator
- **Monad Validator** — Managed Monad validator infrastructure. https://www.quicknode.com/chains/monad/validator
- **ChainKit** — No-code blockchain data tooling and integrations. https://www.quicknode.com/chainkit

---

## Common Patterns

### Multi-Chain RPC Setup

```typescript
import { JsonRpcProvider } from 'ethers';

const ethereum = new JsonRpcProvider(process.env.QUICKNODE_ETH_RPC_URL!);
const base = new JsonRpcProvider(process.env.QUICKNODE_BASE_RPC_URL!);

const [ethBlock, baseBlock] = await Promise.all([
  ethereum.getBlockNumber(),
  base.getBlockNumber(),
]);
```

### Real-Time Transaction Monitoring

1. **Create Stream** filtering for your contract address
2. **Add Filter Function** to extract relevant events
3. **Configure Webhook** destination to your server
4. **Process Events** in your backend

### Real-Time Solana Monitoring with Solana gRPC

1. **Connect via gRPC** on port 10000 with your auth token
2. **Subscribe to transactions** filtering by program or account
3. **Process updates** in real-time via the streaming interface
4. **Implement reconnection** with exponential backoff

### Hyperliquid Trading Data Pipeline

1. **Connect via gRPC** on port 10000 for lowest-latency data
2. **Subscribe to TRADES/ORDERS** streams with coin filters
3. **Process events** — handle ~12 blocks/sec throughput
4. **Use Info API** (`/info`) for account state and market metadata

### Historical Trading Analysis with SQL Explorer

1. **Query historical trades** — `SELECT * FROM hyperliquid_trades WHERE block_time > ...`
2. **Aggregate metrics** — Use `GROUP BY` for volume, counts, averages
3. **Join tables** — Combine trades, orders, funding for comprehensive analysis
4. **Export data** — Results as JSON for downstream processing

## Best Practices

### RPC
- Use WebSocket for subscriptions and real-time data
- Implement retry logic with exponential backoff
- Cache responses when data doesn't change frequently
- Use batch requests to reduce API calls

### Streams
- Start with narrow filters, expand as needed
- Test filter functions locally before deployment
- Streams will automatically retry on failures
- Monitor stream health via dashboard

### Security
- Store API keys in environment variables
- Enable IP allowlisting for production
- Use JWT authentication for sensitive operations
- Rotate API keys periodically

### gRPC
- Enable zstd compression to reduce bandwidth (up to 70% for Hyperliquid)
- Implement reconnection logic with exponential backoff — streams can drop
- Use narrow filters (specific accounts, coins, or programs) to minimize data volume
- Set appropriate commitment levels (Solana gRPC: CONFIRMED for most use cases, FINALIZED for irreversibility)
- Send keepalive pings (every 10s for Solana gRPC, every 30s for HyperCore) to maintain connections

### SQL Explorer
- Always filter by time ranges for partition pruning (`WHERE block_time > ...`)
- Use LIMIT on exploratory queries to reduce data scanned
- Leverage sort keys (check schema reference) for optimal query performance
- Start with pre-built queries and customize for your needs
- Monitor query statistics (rows_read, bytes_read) to optimize performance

## Documentation Links

### Quicknode Products
- **Main Docs**: https://www.quicknode.com/docs/
- **Core RPC API**: https://www.quicknode.com/core-api
- **Streams**: https://www.quicknode.com/docs/streams
- **Streams Backfills**: https://www.quicknode.com/docs/streams/backfilling
- **Webhooks**: https://www.quicknode.com/docs/webhooks
- **Blazar WSS**: https://www.quicknode.com/docs/solana
- **Solana gRPC**: https://www.quicknode.com/docs/solana/solana-grpc/overview
- **HyperCore gRPC**: https://www.quicknode.com/docs/hyperliquid/grpc-api
- **IPFS**: https://www.quicknode.com/docs/ipfs
- **SDK**: https://www.quicknode.com/docs/quicknode-sdk
- **Admin API**: https://www.quicknode.com/docs/admin-api
- **Metaplex DAS API (Solana)**: https://www.quicknode.com/docs/solana/solana-das-api
- **Blockbook**: https://www.quicknode.com/docs/bitcoin/blockbook/overview
- **Ordinals & Runes API**: https://www.quicknode.com/docs/bitcoin/ord_getInscription
- **Quicknode CLI**: https://www.quicknode.com/docs/quicknode-cli
- **Quicknode MCP**: https://www.quicknode.com/docs/build-with-ai/quicknode-mcp
- **Hyperliquid**: https://www.quicknode.com/docs/hyperliquid
- **SQL Explorer**: https://www.quicknode.com/docs/sql-explorer
- **SQL Explorer REST API**: https://www.quicknode.com/docs/sql-explorer/using-rest-api
- **Hyperliquid Queries**: https://www.quicknode.com/docs/sql-explorer/hyperliquid-queries
- **Schema Reference**: https://www.quicknode.com/docs/sql-explorer/schema-reference
- **Key-Value Store**: https://www.quicknode.com/docs/key-value-store
- **x402**: https://x402.quicknode.com
- **MPP**: https://mpp.quicknode.com
- **Agent Subscriptions**: https://www.quicknode.com/docs/build-with-ai/agent-subscriptions
- **Agent Identity (ERC-8004)**: https://erc-8004.quicknode.com
- **Swap API (Metis/Jupiter)**: https://www.quicknode.com/docs/solana/metis-overview
- **Build with AI Overview**: https://www.quicknode.com/docs/build-with-ai
- **Agents reference (agents.md)**: https://www.quicknode.com/agents.md

### Chain-Specific Docs
- **Ethereum**: https://www.quicknode.com/docs/ethereum
- **Solana**: https://www.quicknode.com/docs/solana
- **Polygon**: https://www.quicknode.com/docs/polygon
- **Arbitrum**: https://www.quicknode.com/docs/arbitrum
- **Base**: https://www.quicknode.com/docs/base
- **Optimism**: https://www.quicknode.com/docs/optimism
- **Avalanche**: https://www.quicknode.com/docs/avalanche
- **BNB Smart Chain**: https://www.quicknode.com/docs/bnb-smart-chain
- **Hyperliquid**: https://www.quicknode.com/docs/hyperliquid

### LLM-Optimized Documentation
- **Platform Overview (llms.txt)**: https://www.quicknode.com/llms.txt — High-level index of all Quicknode products, chains, guides, and solutions
- **Docs Index (llms.txt)**: https://www.quicknode.com/docs/llms.txt — Per-chain and per-product documentation index (links to `https://www.quicknode.com/docs/{chain-or-product}/llms.txt`)
- **x402 (llms.txt)**: https://x402.quicknode.com/llms.txt
- **MPP (llms.txt)**: https://mpp.quicknode.com/llms.txt

### Additional Resources
- **Quicknode Guides**: https://www.quicknode.com/guides
- **SDK Reference**: https://www.quicknode.com/docs/quicknode-sdk
- **Marketplace**: https://marketplace.quicknode.com/
- **Sample App Library**: https://www.quicknode.com/sample-app-library
- **Guide Examples Repo**: https://github.com/quiknode-labs/qn-guide-examples
