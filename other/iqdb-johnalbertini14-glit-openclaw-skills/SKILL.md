---
name: iqdb-onchain-storage
description: On-chain immutable data storage using IQ Labs tech stack (IQDB, hanLock, x402). Use when building Solana-based persistent storage, on-chain databases, tamper-evident records, password-encoded data, or paid file inscription. Triggers on tasks involving on-chain CRUD, Solana PDA storage, rolling hash verification, Hangul encoding, or HTTP 402 payment-gated inscription.
---

# IQDB On-Chain Storage (Code-In Tech)

## Overview

Build on-chain relational databases on Solana using IQ Labs' tech stack. Three tools:

- **IQDB** — Full CRUD relational database on Solana via Anchor PDAs. Tables, rows, rolling keccak hash for tamper-evident history.
- **hanLock** — Password-based Hangul syllabic encoding (base-11172). Lightweight data encoding for on-chain privacy. Zero dependencies.
- **x402** — HTTP 402 payment-gated file inscription to Solana. Quote → Pay (USDC/SOL) → Broadcast chunk transactions → Download.

## Quick Start

### Prerequisites
- Node.js 18+
- Solana CLI (`solana --version`)
- A Solana wallet with devnet SOL (`solana airdrop 2`)

### Network Support
- **Mainnet:** Fully supported. Program ID: `9KLLchQVJpGkw4jPuUmnvqESdR7mtNCYr3qS4iQLabs` (via `@iqlabs-official/solana-sdk`).
- **Devnet:** Supported via legacy SDK (`@iqlabsteam/iqdb`). Program: `7Vk5JJDxUBAaaAkpYQpWYCZNz4SVPm3mJFSxrBzTQuAX`.

### Install (New Official SDK — recommended)
```bash
npm install @iqlabs-official/solana-sdk @solana/web3.js
```

### Install (Legacy SDK — devnet only)
```bash
npm install @iqlabsteam/iqdb @coral-xyz/anchor @solana/web3.js
```

### Environment Variables (Legacy SDK)
```bash
ANCHOR_WALLET=/path/to/keypair.json    # Required — Solana keypair for signing
ANCHOR_PROVIDER_URL=https://api.devnet.solana.com  # Required — RPC for writes
NETWORK_URL=https://api.devnet.solana.com  # Required — RPC for reads (must match ANCHOR_PROVIDER_URL)
```

**Legacy SDK note:** Set `NETWORK_URL` to match `ANCHOR_PROVIDER_URL`. The SDK uses separate connections for reads and writes.

**RPC Note:** Public Solana RPCs rate-limit aggressively. Add 2-3 second delays between rapid transactions on mainnet. Use a dedicated RPC provider (Helius, Alchemy, QuickNode) for production.

### Minimal Example — New SDK (Mainnet)
```javascript
const { Connection, Keypair, SystemProgram, PublicKey } = require('@solana/web3.js');
const { writer, reader, setRpcUrl, contract } = require('@iqlabs-official/solana-sdk');

// Monkey-patch for Node v24 Buffer compatibility
const seedModule = require('@iqlabs-official/solana-sdk/dist/sdk/utils/seed');
const origFn = seedModule.toSeedBytes;
seedModule.toSeedBytes = (v) => Buffer.from(origFn(v));

setRpcUrl('https://api.mainnet-beta.solana.com');
const connection = new Connection('https://api.mainnet-beta.solana.com', 'confirmed');

// Write a row (requires root + table initialized first — see references/iqdb-core.md)
const sig = await writer.writeRow(
  connection, signer, 'my-db-root', 'players',
  JSON.stringify({ name: 'Alice', score: '1500', level: '12' })
);

// Read rows
const rows = await reader.readTableRows(tablePda);
```

### Minimal Example — Legacy SDK (Devnet)
```javascript
// Use CommonJS — the SDK bundles CJS internally
const { createIQDB } = require('@iqlabsteam/iqdb');

const iqdb = createIQDB();

// Ensure root PDA exists (idempotent)
await iqdb.ensureRoot();

// Create a table (idempotent — use ensureTable over createTable)
await iqdb.ensureTable('players', ['name', 'score', 'level'], 'name');

// Write a row — data must be a JSON STRING, not an object
await iqdb.writeRow('players', JSON.stringify({
  name: 'Alice', score: '1500', level: '12'
}));

// Read all rows — requires userPubkey as string
const rows = await iqdb.readRowsByTable({
  userPubkey: 'YOUR_WALLET_PUBKEY',
  tableName: 'players'
});
console.log(rows);
```

## Architecture

```
Root PDA (per wallet)
  └── Table PDA (per table name)
       └── Rows stored as transaction data
            └── hash: keccak(domain || prev_hash || tx_data)
```

- **Root PDA** — One per wallet. Initialized via `ensureRoot()`.
- **Table PDA** — Created via `ensureTable()` or `createTable()`. Has column schema and ID column.
- **Rows** — Written as JSON strings via `writeRow()`. Append-only — each write is a new transaction.
- **Rolling hash** — Each write appends to an immutable hash chain. Enables tamper detection without full replication.

## Core Operations

See `references/iqdb-core.md` for full API.

| Operation | Method | Cost |
|-----------|--------|------|
| Init root | `contract.initializeDbRootInstruction()` / `ensureRoot()` | ~0.01 SOL rent |
| Create table | `contract.createTableInstruction()` / `ensureTable()` | ~0.02 SOL rent |
| Write row | `writer.writeRow()` / `iqdb.writeRow()` | ~0.005-0.01 SOL |
| Read rows | `reader.readTableRows()` / `readRowsByTable()` | Free (RPC read) |
| Update/Delete | `pushInstruction(table, txSig, before, after)` | TX fee only |
| Extension table | `createExtTable(base, rowId, extKey, cols, idCol?)` | ~0.02 SOL rent |

**Cost reference (mainnet):** Root + 3 tables + 5 data rows = ~0.09 SOL total.

### Important Constraints
- **Row data size limit:** Keep row JSON under ~100 bytes. The on-chain program enforces a transaction size limit (`TxTooLong` error). For larger data, split across multiple rows or use hanLock sparingly (encoded output is larger than input).
- **Append-only writes:** `writeRow` always appends. Use `pushInstruction` for updates/deletes.
- **pushInstruction writes to instruction log, not row data.** `readRowsByTable` returns raw rows and does NOT reflect updates/deletes from `pushInstruction`. To see the full picture including corrections, use `searchTableByName` which returns both `rows` (raw) and `instruRows`/`targetContent` (instruction history). Your application must apply instruction corrections on top of raw rows.
- **CommonJS required:** The SDK uses dynamic `require()` internally. Use `.cjs` files or `"type": "commonjs"` in package.json. ESM imports will fail.

## hanLock Encoding

See `references/hanlock.md` for full API.

Encode data with a password before writing on-chain for lightweight privacy:

```javascript
const { encodeWithPassword, decodeWithPassword } = require('hanlock');

const encoded = encodeWithPassword('short secret', 'mypassword');
// → Korean syllable string like "깁닣뭡..."

// Write encoded data on-chain
await iqdb.writeRow('secrets', JSON.stringify({ owner: 'Alice', data: encoded }));

// Later — decode
const decoded = decodeWithPassword(encoded, 'mypassword');
// → 'short secret'
```

**Note:** hanLock encoding expands data size (~3x). Keep input short to stay within the on-chain row size limit.

## x402 Payment Flow

See `references/x402-payments.md` for full API.

Payment-gated file inscription to Solana:

1. **Quote** — `POST /quote` with file metadata → get price in USDC/SOL
2. **Pay** — Send payment transaction to provided address
3. **Inscribe** — `POST /inscribe` with payment proof → file chunked into Solana transactions
4. **Download** — `GET /download/:txId` → reconstruct file from on-chain chunks

## Use Cases

- **Discord RPG Bot** — On-chain character persistence, provable item ownership, immutable game state
- **Governance** — Tamper-evident proposal/vote storage with rolling hash audit trail
- **Compliance logs** — Verifiable edit history for call center records
- **Paid storage** — Monetize data inscription via x402

## References

- [IQ Labs SDK](https://www.npmjs.com/package/@iqlabs-official/solana-sdk) — Official Solana SDK (mainnet)
- [@iqlabsteam/iqdb](https://www.npmjs.com/package/@iqlabsteam/iqdb) — Legacy SDK (devnet)
- [hanLock](https://www.npmjs.com/package/hanlock) — Hangul syllabic encoding
- [Solana Web3.js](https://www.npmjs.com/package/@solana/web3.js) — Solana client library
