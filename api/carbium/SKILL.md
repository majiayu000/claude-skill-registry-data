---
name: carbium
creator: carbium
description: Build on Solana with Carbium infrastructure — bare-metal RPC, Standard WebSocket pubsub, gRPC Full Block streaming (~22ms), DEX aggregation via CQ1 engine (sub-ms quotes), gasless swaps, and MEV-protected execution via Jito bundling. Drop-in replacement for Helius, QuickNode, Triton, or Jupiter Swap API.
---

# Carbium — Full-Stack Solana Infrastructure

Carbium is bare-metal Solana infrastructure — Swiss-engineered, no cloud middlemen. One platform covering the full transaction lifecycle.

## Overview

| Product | Endpoint | Purpose |
|---|---|---|
| **RPC** | `https://rpc.carbium.io` | Standard JSON-RPC for reads, writes, subscriptions |
| **Standard WebSocket** | `wss://wss-rpc.carbium.io` | Native Solana pubsub (account changes, slots, logs, signatures) |
| **gRPC / Stream** | `wss://grpc.carbium.io` | Yellowstone Full Block streaming (~22ms latency) |
| **Swap API** | `https://api.carbium.io` | DEX aggregation and execution powered by CQ1 engine |
| **DEX App** | `https://app.carbium.io` | Consumer-facing trading interface |
| **Docs** | `https://docs.carbium.io` | Full documentation |

**Key differentiators:**
- **Sub-millisecond DEX quotes** via CQ1 routing engine with binary-native state
- **~22ms Full Block gRPC** — atomic, complete blocks (no shred reassembly)
- **Gasless swaps** — users trade without holding SOL
- **MEV protection** — Jito bundling built into Swap API
- **Swiss bare-metal servers** — sub-50ms RPC latency, 99.99% uptime

---

## When to Use This Skill

| I want to... | Use | Key needed |
|---|---|---|
| Read account data / balances | RPC | RPC key |
| Send a transaction | RPC | RPC key |
| Monitor a wallet in real time | Standard WebSocket | RPC key |
| Confirm a transaction without polling | Standard WebSocket | RPC key |
| Watch program account changes | Standard WebSocket | RPC key |
| Build a wallet app | RPC + Swap API | Both |
| Get a token swap quote | Swap API | API key |
| Execute a swap programmatically | Swap API | API key |
| Execute a swap with Jito bundling | Swap API (bundle endpoint) | API key |
| Compare quotes across all DEX providers | Swap API (quote/all) | API key |
| Swap without users holding SOL | Swap API (gasless flag) | API key |
| Snipe pump.fun tokens (pre-graduation) | gRPC + direct bonding curve tx | RPC key (Business+) |
| React to on-chain events in real time | gRPC (streaming) | RPC key (Business+) |
| Index transactions for a program | gRPC (streaming) | RPC key (Business+) |
| Build an arbitrage / MEV bot | gRPC + Swap API | Both |

---

## Quick Start

### 1. Get API Keys

| Product | Signup | Notes |
|---|---|---|
| RPC + gRPC + WebSocket | [rpc.carbium.io/signup](https://rpc.carbium.io/signup) | One key covers RPC, WebSocket, and gRPC |
| Swap API | [api.carbium.io/login](https://api.carbium.io/login) | Separate key, free account, instant |

Programmatic key provisioning is not yet available. Keys must be created via the dashboards.

### 2. Set Environment Variables

```bash
export CARBIUM_RPC_KEY="your-rpc-key"
export CARBIUM_API_KEY="your-swap-api-key"
```

### 3. Security Rules (Non-Negotiable)

- Never embed keys in frontend/client-side code
- Never commit keys to version control
- Use environment variables: `CARBIUM_RPC_KEY`, `CARBIUM_API_KEY`
- Rotate immediately if exposed
- Keep keys server-side only

---

## Pricing Tiers

| Tier | Price | Credits/mo | Max RPS | gRPC | WebSocket |
|---|---|---|---|---|---|
| Free | $0 | 500K | 10 | No | Yes |
| Developer | $32/mo | 10M | 50 | No | Yes |
| Business | $320/mo | 100M | 200 | Yes | Yes |
| Professional | $640/mo | 200M | 500 | Yes | Yes |

gRPC streaming requires Business tier or above.

---

## RPC

Standard Solana JSON-RPC. Any Solana SDK works: `@solana/web3.js`, `solana-py`, `solana` Rust crate.

**Endpoint:**

```
https://rpc.carbium.io/?apiKey=YOUR_RPC_KEY
```

### TypeScript

```typescript
import { Connection, PublicKey, LAMPORTS_PER_SOL } from "@solana/web3.js";

const connection = new Connection(
  `https://rpc.carbium.io/?apiKey=${process.env.CARBIUM_RPC_KEY}`,
  "confirmed"
);

// Read balance
const pubkey = new PublicKey("YOUR_WALLET_ADDRESS");
const balance = await connection.getBalance(pubkey);
console.log(`Balance: ${balance / LAMPORTS_PER_SOL} SOL`);

// Send transaction
const sig = await connection.sendRawTransaction(transaction.serialize(), {
  skipPreflight: false,
  maxRetries: 3,
});
await connection.confirmTransaction(sig, "confirmed");
```

### Python

```python
from solana.rpc.api import Client
from solders.pubkey import Pubkey
import os

rpc = Client(f"https://rpc.carbium.io/?apiKey={os.environ['CARBIUM_RPC_KEY']}")
pubkey = Pubkey.from_string("YOUR_WALLET_ADDRESS")
resp = rpc.get_balance(pubkey)
print(f"Balance: {resp.value / 1e9} SOL")
```

### Rust

```rust
use solana_client::rpc_client::RpcClient;
use solana_sdk::pubkey::Pubkey;
use std::str::FromStr;

let url = format!(
    "https://rpc.carbium.io/?apiKey={}",
    std::env::var("CARBIUM_RPC_KEY").unwrap()
);
let client = RpcClient::new(url);
let pubkey = Pubkey::from_str("YOUR_WALLET_ADDRESS").unwrap();
let balance = client.get_balance(&pubkey).unwrap();
println!("Balance: {} lamports", balance);
```

### Commitment Levels

| Level | Speed | Guarantee | Use for |
|---|---|---|---|
| `processed` | ~400ms | May roll back | Price feeds, low-stakes UX |
| `confirmed` | ~2s | Supermajority voted | **Default — best balance** |
| `finalized` | ~32s | Fully finalized | Irreversible confirmations, high-value ops |

---

## Standard WebSocket (Solana Pubsub)

Native Solana WebSocket pubsub — any SDK built for Solana WebSocket works with zero modifications.

**Endpoint:**

```
wss://wss-rpc.carbium.io/?apiKey=YOUR_RPC_KEY
```

Auth: same RPC key as query parameter. Available on all tiers (Developer and above recommended for production).

### WSS vs gRPC — When to Use Which

| | Standard WSS | gRPC / Yellowstone |
|---|---|---|
| **Protocol** | JSON-RPC over WebSocket | Binary protobuf over WebSocket (or HTTP/2) |
| **What you get** | Account changes, slot updates, logs, signatures | Full atomic blocks, all transactions |
| **SDK support** | Any Solana SDK (`@solana/web3.js`, `solana-py`) | Yellowstone client or raw WS with JSON filter |
| **Latency** | Sub-100ms subscription ack | ~22ms full block delivery |
| **Tier required** | Developer+ | Business+ |
| **Best for** | Wallets, dApps, monitoring specific accounts | MEV bots, indexers, full-block processing |

**Rule of thumb:** watching specific accounts or signatures → WSS. Processing all transactions or need full block data → gRPC.

### Subscription Methods

| Method | What it streams | Typical use case |
|---|---|---|
| `slotSubscribe` | New slot numbers | Block clock, liveness checks |
| `rootSubscribe` | Finalized slots | Finality tracking |
| `accountSubscribe` | Account data changes | Wallet balance updates, PDA state changes |
| `programSubscribe` | All accounts owned by a program | DEX pool state, staking updates |
| `signatureSubscribe` | Transaction confirmation status | Confirm sent transactions in real time |
| `logsSubscribe` | Transaction logs matching filter | Program event monitoring |
| `blockSubscribe` | Full block data | Block explorers, indexers |
| `slotsUpdatesSubscribe` | Detailed slot lifecycle events | Advanced timing, validator monitoring |
| `voteSubscribe` | Vote transactions | Validator monitoring |

### TypeScript — Watch a Wallet

```typescript
import WebSocket from "ws";

const ws = new WebSocket(
  `wss://wss-rpc.carbium.io/?apiKey=${process.env.CARBIUM_RPC_KEY}`
);

ws.on("open", () => {
  ws.send(JSON.stringify({
    jsonrpc: "2.0",
    id: 1,
    method: "accountSubscribe",
    params: [
      "YOUR_WALLET_ADDRESS",
      { encoding: "base64", commitment: "confirmed" },
    ],
  }));
});

ws.on("message", (raw) => {
  const msg = JSON.parse(raw.toString());
  if (msg.result !== undefined) {
    console.log(`Subscribed, id: ${msg.result}`);
    return;
  }
  if (msg.method === "accountNotification") {
    const { lamports } = msg.params.result.value;
    console.log(`Balance changed: ${lamports / 1e9} SOL`);
  }
});
```

### TypeScript — Confirm Transaction via WSS

```typescript
ws.send(JSON.stringify({
  jsonrpc: "2.0",
  id: 1,
  method: "signatureSubscribe",
  params: ["YOUR_TX_SIGNATURE", { commitment: "confirmed" }],
}));

// signatureSubscribe auto-unsubscribes after first notification
```

### TypeScript — Stream Program Logs

```typescript
ws.send(JSON.stringify({
  jsonrpc: "2.0",
  id: 1,
  method: "logsSubscribe",
  params: [
    { mentions: ["PROGRAM_ID"] },
    { commitment: "confirmed" },
  ],
}));
```

### Using @solana/web3.js (Recommended)

The `Connection` class handles subscriptions natively:

```typescript
import { Connection, PublicKey } from "@solana/web3.js";

const connection = new Connection(
  `https://rpc.carbium.io/?apiKey=${process.env.CARBIUM_RPC_KEY}`,
  {
    commitment: "confirmed",
    wsEndpoint: `wss://wss-rpc.carbium.io/?apiKey=${process.env.CARBIUM_RPC_KEY}`,
  }
);

// Account subscription
connection.onAccountChange(
  new PublicKey("YOUR_WALLET"),
  (info, ctx) => console.log(`Balance: ${info.lamports / 1e9} SOL at slot ${ctx.slot}`),
  "confirmed"
);

// Slot subscription
connection.onSlotChange((slotInfo) => {
  console.log(`Slot: ${slotInfo.slot}`);
});

// Log subscription
connection.onLogs(
  new PublicKey("PROGRAM_ID"),
  (logs, ctx) => {
    console.log(`Tx: ${logs.signature}`);
    logs.logs.forEach(log => console.log(" ", log));
  },
  "confirmed"
);
```

### Python — Watch Account

```python
import asyncio, json, os
import websockets

WALLET = "YOUR_WALLET_ADDRESS"

async def watch_account():
    uri = f"wss://wss-rpc.carbium.io/?apiKey={os.environ['CARBIUM_RPC_KEY']}"
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({
            "jsonrpc": "2.0", "id": 1,
            "method": "accountSubscribe",
            "params": [WALLET, {"encoding": "base64", "commitment": "confirmed"}],
        }))
        ack = json.loads(await ws.recv())
        print(f"Subscribed: {ack['result']}")
        async for raw in ws:
            msg = json.loads(raw)
            if msg.get("method") == "accountNotification":
                val = msg["params"]["result"]["value"]
                print(f"Balance: {val['lamports'] / 1e9} SOL")

asyncio.run(watch_account())
```

### Unsubscribe

Every subscription method has a matching unsubscribe. Use the subscription ID from the ack:

```json
{"jsonrpc": "2.0", "id": 2, "method": "accountUnsubscribe", "params": [SUBSCRIPTION_ID]}
```

| Subscribe | Unsubscribe |
|---|---|
| `slotSubscribe` | `slotUnsubscribe` |
| `accountSubscribe` | `accountUnsubscribe` |
| `programSubscribe` | `programUnsubscribe` |
| `signatureSubscribe` | `signatureUnsubscribe` (auto after first notification) |
| `logsSubscribe` | `logsUnsubscribe` |
| `blockSubscribe` | `blockUnsubscribe` |
| `rootSubscribe` | `rootUnsubscribe` |

For full notification shapes and advanced patterns, see `resources/websocket-reference.md`.

---

## gRPC / Full Block Streaming

Real-time Yellowstone-compatible Full Block stream. ~22ms latency. Atomic complete blocks — no shred reassembly needed.

### Endpoints & Auth

| Method | Format | Use case |
|---|---|---|
| WebSocket query param | `wss://grpc.carbium.io/?apiKey=YOUR_RPC_KEY` | Recommended for TS/Python |
| HTTP/2 header | `x-token: YOUR_RPC_KEY` | For Rust yellowstone-grpc-client |

Requires **Business tier or above**.

### Available Methods

| Method | Description |
|---|---|
| `transactionSubscribe` | Subscribe to real-time transactions with filters |
| `transactionUnsubscribe` | Unsubscribe from transaction stream |

### TypeScript — Subscribe to Program Transactions

```typescript
import WebSocket from "ws";

const PROGRAM_ID = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P";

const ws = new WebSocket(
  `wss://grpc.carbium.io/?apiKey=${process.env.CARBIUM_RPC_KEY}`
);

ws.on("open", () => {
  ws.send(JSON.stringify({
    jsonrpc: "2.0",
    id: 1,
    method: "transactionSubscribe",
    params: [
      {
        vote: false,
        failed: false,
        accountInclude: [PROGRAM_ID],
        accountExclude: [],
        accountRequired: [],
      },
      {
        commitment: "confirmed",
        encoding: "base64",
        transactionDetails: "full",
        showRewards: false,
        maxSupportedTransactionVersion: 0,
      },
    ],
  }));
});

ws.on("message", (raw) => {
  const msg = JSON.parse(raw.toString());
  if (msg.result !== undefined) {
    console.log(`Subscribed, ID: ${msg.result}`);
    return;
  }
  if (msg.method === "transactionNotification") {
    const { signature, slot } = msg.params.result;
    console.log(`tx ${signature} in slot ${slot}`);
  }
});

// Always reconnect on close — see Production Patterns
ws.on("close", (code) => {
  console.warn(`Disconnected (${code}), reconnecting...`);
});
```

### Filter Fields

| Field | Type | Description |
|---|---|---|
| `vote` | bool | Include vote transactions |
| `failed` | bool | Include failed transactions |
| `accountInclude` | string[] | Include txs involving ANY of these accounts |
| `accountExclude` | string[] | Exclude txs involving these accounts |
| `accountRequired` | string[] | Only include txs involving ALL of these accounts |

At least one of `accountInclude` or `accountRequired` must contain values.

### Subscription Options

| Field | Type | Values |
|---|---|---|
| `commitment` | string | `processed` / `confirmed` / `finalized` |
| `encoding` | string | `base64` / `base58` / `jsonParsed` |
| `transactionDetails` | string | `full` / `signatures` / `none` |
| `showRewards` | bool | Include reward information |
| `maxSupportedTransactionVersion` | number | `0` for legacy + v0 |

### Python

```python
import asyncio, json, os
import websockets

PROGRAM_ID = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"

async def subscribe():
    uri = f"wss://grpc.carbium.io/?apiKey={os.environ['CARBIUM_RPC_KEY']}"
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({
            "jsonrpc": "2.0", "id": 1,
            "method": "transactionSubscribe",
            "params": [
                {
                    "vote": False, "failed": False,
                    "accountInclude": [PROGRAM_ID],
                    "accountExclude": [], "accountRequired": [],
                },
                {
                    "commitment": "confirmed", "encoding": "base64",
                    "transactionDetails": "full", "showRewards": False,
                    "maxSupportedTransactionVersion": 0,
                },
            ],
        }))
        async for message in ws:
            data = json.loads(message)
            if "result" in data:
                print(f"Subscribed: {data['result']}")
            elif data.get("method") == "transactionNotification":
                print(f"tx: {data['params']['result']['signature'][:20]}...")

asyncio.run(subscribe())
```

### Rust (HTTP/2 gRPC)

```rust
use yellowstone_grpc_client::GeyserGrpcClient;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut client = GeyserGrpcClient::connect(
        "https://grpc.carbium.io",
        "YOUR_RPC_KEY",  // passed as x-token header automatically
        None,
    )?;
    let (_subscribe_tx, mut stream) = client.subscribe().await?;
    // Define subscription filters and consume stream
    Ok(())
}
```

### Full Blocks vs Shreds

| Metric | Value | Context |
|---|---|---|
| Solana Slot Resolution | ~400ms | The window in which a block is produced |
| Competitor "Shreds" | ~9ms | Fragmented data requiring client-side reassembly |
| Carbium Full Blocks | ~22ms | Atomic, complete data ready for use |

The 13ms difference is negligible within a 400ms slot. Full Blocks provide atomic integrity, zero-logic ingestion, and parsing efficiency.

### Unsubscribe

```json
{"jsonrpc": "2.0", "id": 2, "method": "transactionUnsubscribe", "params": [SUBSCRIPTION_ID]}
```

For complete gRPC reference with response shapes, see `resources/grpc-reference.md`.

---

## Swap API

Aggregated DEX quotes and execution powered by the CQ1 engine — sub-millisecond quotes, ~10ms chain-to-queryable latency, binary-native state.

**Base URL:** `https://api.carbium.io`
**Auth:** `X-API-KEY: YOUR_API_KEY` header on all requests
**Get your key:** [api.carbium.io/login](https://api.carbium.io/login) (free account)

### API Versions

| Version | Surface | Status |
|---|---|---|
| **v2 (Q1)** | `GET /api/v2/quote` | **Current — use this for new integrations** |
| v1 (legacy) | `GET /api/v1/quote`, `/api/v1/swap`, `/api/v1/quote/all`, `/api/v1/swap/bundle` | Legacy — still operational |

> **Important:** v2 and v1 use different parameter names. Do not mix them. v2 (Q1) uses `src_mint`/`dst_mint`/`amount_in`/`slippage_bps`. v1 uses `fromMint`/`toMint`/`amount`/`slippage`.

### v2 / Q1 — Quote + Executable Transaction (Recommended)

The Q1 engine returns both the quote **and** an executable transaction in a single call when `user_account` is included. No separate swap endpoint needed.

```
GET /api/v2/quote
```

| Param | Required | Description |
|---|---|---|
| `src_mint` | Yes | Input token mint address |
| `dst_mint` | Yes | Output token mint address |
| `amount_in` | Yes | Input amount in smallest unit (lamports) |
| `slippage_bps` | Yes | Slippage tolerance in basis points |
| `user_account` | No | Wallet address — if included, response includes executable `txn` field |

**Quote only (no transaction):**

```typescript
const quote = await fetch(
  "https://api.carbium.io/api/v2/quote" +
  "?src_mint=So11111111111111111111111111111111111111112" +
  "&dst_mint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v" +
  "&amount_in=1000000000" +
  "&slippage_bps=100",
  { headers: { "X-API-KEY": process.env.CARBIUM_API_KEY! } }
).then(r => r.json());
// Returns: { srcAmountIn, destAmountOut, destAmountOutMin, priceImpactPct, routePlan }
```

**Quote + executable transaction (include `user_account`):**

```typescript
const quote = await fetch(
  "https://api.carbium.io/api/v2/quote" +
  "?src_mint=So11111111111111111111111111111111111111112" +
  "&dst_mint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v" +
  "&amount_in=1000000000" +
  "&slippage_bps=100" +
  "&user_account=YOUR_WALLET_ADDRESS",
  { headers: { "X-API-KEY": process.env.CARBIUM_API_KEY! } }
).then(r => r.json());
// Returns: { srcAmountIn, destAmountOut, destAmountOutMin, priceImpactPct, routePlan, txn }
// txn is base64-encoded, ready for deserialization and signing
```

```python
import httpx, os

resp = httpx.get(
    "https://api.carbium.io/api/v2/quote",
    params={
        "src_mint": "So11111111111111111111111111111111111111112",
        "dst_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        "amount_in": 1_000_000_000,
        "slippage_bps": 100,
        "user_account": "YOUR_WALLET_ADDRESS",  # include for executable txn
    },
    headers={"X-API-KEY": os.environ["CARBIUM_API_KEY"]},
)
print(resp.json())
```

### v1 Legacy Endpoints

These endpoints are still operational but use the older parameter family. Do not mix v1 params with v2 URLs.

| Endpoint | Method | Params | Description |
|---|---|---|---|
| `/api/v1/quote` | GET | `fromMint`, `toMint`, `amount`, `slippage`, `provider` | Provider-specific quote |
| `/api/v1/quote/all` | GET | `fromMint`, `toMint`, `amount`, `slippage` | Compare quotes across all providers |
| `/api/v1/swap` | GET | `owner`, `fromMint`, `toMint`, `amount`, `slippage`, `provider` + optional flags | Get serialized swap transaction |
| `/api/v1/swap/bundle` | GET | `signedTransaction` | Submit via Jito bundle (MEV protection) |
| `/api/v1/fee/custom` | GET | `payer`, `receiver`, `lamports` | Generate custom fee transfer transaction |

v1 `/swap` supports additional execution flags: `gasless`, `mevSafe`, `priorityMicroLamports`, `feeLamports`, `feeReceiver`, `pool`.

### Full Swap Execute Flow (TypeScript) — v2/Q1

```typescript
import { Connection, VersionedTransaction, Keypair } from "@solana/web3.js";

const connection = new Connection(
  `https://rpc.carbium.io/?apiKey=${process.env.CARBIUM_RPC_KEY}`,
  "confirmed"
);

// 1. Get quote with executable transaction (single call)
const url = new URL("https://api.carbium.io/api/v2/quote");
url.searchParams.set("src_mint", "So11111111111111111111111111111111111111112");
url.searchParams.set("dst_mint", "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v");
url.searchParams.set("amount_in", "100000000");
url.searchParams.set("slippage_bps", "100");
url.searchParams.set("user_account", "YOUR_WALLET_ADDRESS");

const quote = await fetch(url, {
  headers: { "X-API-KEY": process.env.CARBIUM_API_KEY! },
}).then(r => r.json());

if (!quote.txn) throw new Error("No executable transaction — check user_account param");

// 2. Deserialize and sign
const tx = VersionedTransaction.deserialize(Buffer.from(quote.txn, "base64"));
// tx.sign([yourKeypair]);

// 3. Submit via RPC
const sig = await connection.sendRawTransaction(tx.serialize(), { maxRetries: 3 });

// 4. Confirm
await connection.confirmTransaction(sig, "confirmed");
console.log("Swap confirmed:", sig);
```

### Supported DEX Providers

| Provider | ID |
|---|---|
| Raydium | `raydium` |
| Raydium CPMM | `raydium-cpmm` |
| Orca | `orca` |
| Meteora | `meteora` |
| Meteora DLMM | `meteora-dlmm` |
| Pump.fun | `pump-fun` |
| Moonshot | `moonshot` |
| Stabble | `stabble` |
| PrintDEX | `printdex` |
| GooseFX | `goosefx` |

### Slippage Recommendations

| Pair type | Recommended BPS | Percentage |
|---|---|---|
| Stablecoin swaps | 5-10 | 0.05-0.1% |
| Major pairs (SOL/USDC) | 10-50 | 0.1-0.5% |
| Volatile tokens | 50-100 | 0.5-1% |
| Arbitrage | 10 | 0.1% (tight) |

For complete OpenAPI parameter specifications, see `resources/swap-api-reference.md`.

---

## Gasless Swaps

Gasless swaps let users execute on-chain transactions without holding SOL to pay fees.

### How It Works

1. User initiates a swap
2. Carbium advances the SOL fee from an internal fee pool
3. Transaction settles on-chain normally
4. A micro-adjustment on the swap output rebalances the fee pool

### Constraint

Gasless swaps require the **output token to be SOL**. Currently available on the v1 swap endpoint.

### When to Use

- First-time users who received tokens but no SOL
- Embedded wallet experiences with low-friction onboarding
- Swap-first UX where gas funding hurts conversion

### Integration

Add `gasless=true` to a v1 swap request:

```typescript
const res = await fetch(
  "https://api.carbium.io/api/v1/swap" +
  "?owner=WALLET&fromMint=USDC_MINT&toMint=SOL_MINT" +
  "&amount=1000000&slippage=100&provider=raydium&gasless=true",
  { headers: { "X-API-KEY": process.env.CARBIUM_API_KEY! } }
);
```

---

## Pump.fun Pre-Graduation Token Sniping

Carbium Swap API **cannot route pump.fun tokens before graduation** (returns 0 routes). Use: **gRPC to detect launches → build raw bonding curve transactions → submit via RPC**.

Requires **Business tier** RPC key (gRPC access).

### Key Constants

```typescript
const PUMP_PROGRAM       = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P";
const PUMP_GLOBAL        = "4wTV1YmiEkRvAtNtsSGPtUrqRYQMe5SKy2uB4Jjaxnjf";
const PUMP_FEE_RECIPIENT = "CebN5WGQ4jvEPvsVU4EoHEpgzq1VV7AbicfhtW4xC9iM";
const PUMP_EVENT_AUTH    = "Ce6TQqeHC9p8KetsN6JsjHK7UTZk7nasjjnr7XxXp9F1";
const GRADUATION_SOL     = 85_000_000_000n; // 85 SOL in lamports
const TOTAL_SUPPLY       = 1_000_000_000_000_000n; // 1 quadrillion (6 decimals)

const DISCRIMINATORS = {
  create: [0xe4, 0x45, 0xa5, 0x2e, 0x51, 0xcb, 0x9a, 0x1d],
  buy:    [0x66, 0x06, 0x3d, 0x12, 0x01, 0xda, 0xeb, 0xea],
  sell:   [0x33, 0xe6, 0x85, 0xa4, 0x01, 0x7f, 0x83, 0xad],
};
```

### Step 1 — Subscribe to Launches via gRPC

```typescript
import WebSocket from "ws";

const ws = new WebSocket(
  `wss://grpc.carbium.io/?apiKey=${process.env.CARBIUM_RPC_KEY}`
);

ws.on("open", () => {
  ws.send(JSON.stringify({
    jsonrpc: "2.0", id: 1,
    method: "transactionSubscribe",
    params: [
      { vote: false, failed: false, accountInclude: [PUMP_PROGRAM] },
      { commitment: "confirmed", encoding: "jsonParsed",
        transactionDetails: "full", showRewards: false,
        maxSupportedTransactionVersion: 0 },
    ],
  }));
});

setInterval(() => ws.ping(), 30_000); // keepalive

ws.on("message", (raw) => {
  const msg = JSON.parse(raw.toString());
  if (msg.method !== "transactionNotification") return;
  const { signature, transaction } = msg.params.result;
  const logs = transaction.meta.logMessages || [];
  for (const log of logs) {
    if (log.includes("Instruction: Create")) {
      const mint = transaction.meta.postTokenBalances[0]?.mint;
      if (mint) handleNewToken(mint, signature);
    }
  }
});
```

### Step 2 — Derive Bonding Curve PDA

```typescript
import { PublicKey } from "@solana/web3.js";

function deriveBondingCurve(mint: string): PublicKey {
  const [address] = PublicKey.findProgramAddressSync(
    [Buffer.from("bonding-curve"), new PublicKey(mint).toBuffer()],
    new PublicKey(PUMP_PROGRAM)
  );
  return address;
}
```

### Step 3 — Fetch & Parse Bonding Curve State

```typescript
// Bonding curve layout (81 bytes):
// [0-7]   discriminator
// [8-15]  virtualTokenReserves (u64 LE)
// [16-23] virtualSolReserves   (u64 LE)
// [24-31] realTokenReserves    (u64 LE)
// [32-39] realSolReserves      (u64 LE)
// [40-47] tokenTotalSupply     (u64 LE)
// [72]    complete             (bool)

async function fetchBondingCurve(address: PublicKey) {
  const res = await fetch(`https://rpc.carbium.io/?apiKey=${process.env.CARBIUM_RPC_KEY}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      jsonrpc: "2.0", id: 1,
      method: "getAccountInfo",
      params: [address.toBase58(), { encoding: "base64" }],
    }),
  });
  const { result } = await res.json();
  const data = Buffer.from(result.value.data[0], "base64");
  return {
    virtualTokenReserves: data.readBigUInt64LE(8),
    virtualSolReserves:   data.readBigUInt64LE(16),
    realTokenReserves:    data.readBigUInt64LE(24),
    realSolReserves:      data.readBigUInt64LE(32),
    complete:             data.readUInt8(72) === 1,
  };
}
```

### Step 4 — Quote (Constant Product AMM)

```typescript
function quoteBuy(curve: any, solLamports: number): bigint {
  const num = curve.virtualTokenReserves * BigInt(solLamports);
  const den = curve.virtualSolReserves + BigInt(solLamports);
  return num / den;
}

function quoteSell(curve: any, tokens: bigint): bigint {
  const num = curve.virtualSolReserves * tokens;
  const den = curve.virtualTokenReserves + tokens;
  return num / den;
}
```

### Step 5 — Build & Submit Buy Transaction

Buy instruction accounts (order matters, 13 total):

| # | Account | Access |
|---|---|---|
| 0 | PUMP_GLOBAL | read |
| 1 | PUMP_FEE_RECIPIENT | write |
| 2 | mint | read |
| 3 | bondingCurve | write |
| 4 | bondingCurve ATA | write |
| 5 | user ATA | write |
| 6 | user/payer | write, signer |
| 7 | SystemProgram | - |
| 8 | TokenProgram | - |
| 9 | AssociatedTokenProgram | - |
| 10 | Rent sysvar | - |
| 11 | PUMP_EVENT_AUTH | read |
| 12 | PUMP_PROGRAM | read |

Submit with `skipPreflight: true` to save ~200ms:

```typescript
const sig = await connection.sendRawTransaction(signedTx.serialize(), {
  skipPreflight: true,
  preflightCommitment: "confirmed",
  maxRetries: 3,
});
```

### Sniping Flow Summary

```
gRPC "Create" event → extract mint
  → deriveBondingCurve(mint)
  → [optional] fetchBondingCurve() for price check
  → build buy instruction with desired SOL
  → sendTransaction(skipPreflight: true)
  → monitor bonding curve state for exit
  → sell when target % reached or graduation imminent (85 SOL)
```

### Pump.fun Error Handling

| Error | Cause | Fix |
|---|---|---|
| Blockhash expired | Tx took too long | Fresher blockhash; reduce latency |
| Insufficient funds | Not enough SOL | Balance must cover amount + fees (~0.005 SOL) |
| Account not found | Token just created | Retry with small delay (50-100ms) |
| Slippage exceeded | Price moved | Increase `maxSolCost` or reduce size |

For the full sniping example, see `examples/pump-snipe/example.ts`.

---

## Migration

### From Other RPC Providers (Helius, QuickNode, Triton, Alchemy)

Simple URL swap — all use standard JSON-RPC:

```typescript
// Before
const connection = new Connection("https://mainnet.helius-rpc.com/?api-key=...");

// After
const connection = new Connection(
  `https://rpc.carbium.io/?apiKey=${process.env.CARBIUM_RPC_KEY}`
);
```

### From Jupiter Swap API

Parameter mapping (v2/Q1):

| Jupiter | Carbium v2/Q1 (`/api/v2/quote`) |
|---|---|
| `inputMint` | `src_mint` |
| `outputMint` | `dst_mint` |
| `amount` | `amount_in` |
| `slippageBps` | `slippage_bps` |

Key difference: Carbium Q1 returns the executable transaction in the quote response when `user_account` is included. No separate swap call needed.

### From Triton gRPC

Same Yellowstone protocol. Update endpoint only:

```
wss://grpc.carbium.io/?apiKey=YOUR_RPC_KEY
```

For detailed migration guides, see `docs/migration.md`.

---

## Production Patterns

### Retry with Exponential Backoff

```typescript
const delay = (ms: number) => new Promise(r => setTimeout(r, ms));

async function withRetry<T>(fn: () => Promise<T>, retries = 3, baseMs = 300): Promise<T> {
  for (let i = 0; i < retries; i++) {
    try { return await fn(); }
    catch (e) {
      if (i === retries - 1) throw e;
      await delay(baseMs * 2 ** i + Math.random() * 100);
    }
  }
  throw new Error("unreachable");
}
```

> Do NOT blindly retry `sendTransaction` — check `getSignatureStatus` first to confirm the tx did not already land.

### WebSocket / gRPC Reconnect

```typescript
async function connectWithReconnect(connectFn: () => Promise<void>) {
  let backoff = 1000;
  while (true) {
    try {
      await connectFn();
      backoff = 1000; // reset on success
    } catch {
      await delay(backoff);
      backoff = Math.min(backoff * 2, 30_000); // cap at 30s
    }
  }
}
```

Send ping every 30 seconds to prevent silent disconnects.

### Timeout Recommendations

| Operation | Timeout |
|---|---|
| RPC read calls | 5-10s |
| Swap quote | 3-5s |
| Transaction confirmation | 30-60s (with polling) |

### Failure Handling

| Failure | Action |
|---|---|
| Quote: no route found | Retry with wider slippage or different provider |
| Simulation failed | Do NOT send — inspect error, log, alert |
| sendTransaction failed | Check `getSignatureStatus` before retry |
| Transaction not confirmed | Poll with timeout; check blockhash expiry |
| Stream disconnected | Reconnect with exponential backoff |
| HTTP 429 rate limit | Back off immediately; treat as architecture signal |

---

## Error Reference

### HTTP Status Codes

| Code | Meaning | Action |
|---|---|---|
| 401 | Invalid / missing API key | Check key and auth format |
| 403 | Plan restriction (e.g. gRPC on free tier) | Upgrade at rpc.carbium.io |
| 429 | Rate limit exceeded | Back off + retry; review architecture |
| 400 | No route found / bad params | Check mint addresses, slippage, required params |
| 500 | Server error | Retry after 1s |
| 503 | Temporary unavailability | Retry with exponential backoff |

### WebSocket Error Codes

| Code | Message | Cause |
|---|---|---|
| `-32700` | Parse error | Malformed JSON or missing required params |
| `-32601` | Method not found | Method name typo or unsupported method |
| `-32602` | Invalid params | Wrong param types or missing fields |
| `-32603` | Internal error | Server-side error — retry |

---

## Common Token Mints

| Token | Mint Address |
|---|---|
| SOL (wrapped) | `So11111111111111111111111111111111111111112` |
| USDC | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |
| USDT | `Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB` |

---

## Best Practices

### Security
- Keep API keys server-side only — never in frontend bundles or mobile clients
- Use environment variables (`CARBIUM_RPC_KEY`, `CARBIUM_API_KEY`)
- Rotate keys immediately if exposed
- Restrict endpoints by domain/IP in the RPC dashboard where practical

### Rate Limiting
- HTTP 429 is an architecture signal, not just a retry cue
- Separate dev/staging/prod keys
- Isolate retry paths from decision logic
- Do NOT retry `sendTransaction` before checking `getSignatureStatus`

### Transaction Submission
- Use `skipPreflight: true` only after validating the quote — saves ~200ms
- Use `VersionedTransaction` (V0) for Address Lookup Table (ALT) support
- Prefer HTTP polling for confirmations over WebSocket (more reliable)
- Keep blockhashes fresh — they expire after ~60 seconds

### Commitment Levels
- Default to `confirmed` for most operations
- Use `processed` only for price feeds or low-stakes reads
- Use `finalized` for irreversible confirmations and high-value operations

---

## Skill Structure

```
skills/carbium/
├── SKILL.md                              # This file
├── resources/
│   ├── endpoints-and-auth.md             # All endpoints, auth patterns, pricing
│   ├── swap-api-reference.md             # Full Swap API parameter specs
│   ├── grpc-reference.md                 # gRPC filter fields, response shapes
│   └── websocket-reference.md            # All WSS subscription methods and shapes
├── examples/
│   ├── rpc-basic/README.md               # Balance check + send transaction
│   ├── swap-quote/README.md              # Quote → swap → sign → submit
│   ├── swap-bundle/README.md             # MEV-protected Jito bundle
│   ├── grpc-stream/README.md             # Program transaction subscription
│   ├── websocket-monitor/README.md       # Account + slot monitoring via WSS
│   ├── pump-snipe/README.md              # Full pump.fun sniping flow
│   └── gasless-swap/README.md            # Gasless swap execution
├── templates/
│   └── carbium-setup.ts                  # Connection setup + retry helper
└── docs/
    ├── troubleshooting.md                # Error codes, 429 handling
    ├── migration.md                      # From Helius, QuickNode, Jupiter
    └── trading-bots.md                   # Bot architecture patterns
```

---

## References

| Resource | URL |
|---|---|
| Ecosystem Overview | [docs.carbium.io/docs/the-carbium-ecosystem](https://docs.carbium.io/docs/the-carbium-ecosystem) |
| RPC Quick Start | [docs.carbium.io/docs/quick-start-rpc](https://docs.carbium.io/docs/quick-start-rpc) |
| Swap API Quick Start | [docs.carbium.io/docs/quick-start-dex-api](https://docs.carbium.io/docs/quick-start-dex-api) |
| gRPC / Streaming | [docs.carbium.io/docs/solana-grpc](https://docs.carbium.io/docs/solana-grpc) |
| CQ1 Engine | [docs.carbium.io/docs/cq1-engine-overview](https://docs.carbium.io/docs/cq1-engine-overview) |
| RPC Pricing | [docs.carbium.io/docs/carbium-rpc-pricing](https://docs.carbium.io/docs/carbium-rpc-pricing) |
| API Recipes | [docs.carbium.io/recipes](https://docs.carbium.io/recipes) |
| FAQ | [docs.carbium.io/docs/faq](https://docs.carbium.io/docs/faq) |
| Full AI Context | [carbium.io/llms-ctx.txt](https://carbium.io/llms-ctx.txt) |
| RPC Signup | [rpc.carbium.io/signup](https://rpc.carbium.io/signup) |
| Swap API Signup | [api.carbium.io/login](https://api.carbium.io/login) |
| Discord | [discord.gg/jW7BUkQS5U](https://discord.gg/jW7BUkQS5U) |
| Twitter/X | [x.com/carbium](https://x.com/carbium) |
