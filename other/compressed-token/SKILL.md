---
description: "For compressed token operations on Solana ~400x cheaper than SPL: create mints with interface PDAs, mint, transfer, approve, revoke, compress, decompress, merge, and Token-2022 with compression. Compressed token accounts are always rent-free. @lightprotocol/compressed-token (TypeScript) with createRpc() from @lightprotocol/stateless.js."
metadata: {"source":"https://github.com/Lightprotocol/skills","documentation":"https://www.zkcompression.com"}
---
# Compressed token client

Build token applications with `@lightprotocol/compressed-token` (TypeScript). Compressed token accounts are always rent-free. The SPL mint and interface PDA still pay rent, but each holder's compressed token account costs a fraction of an SPL account.

| Creation cost     | SPL                 | Compressed           |
| :---------------- | :------------------ | :------------------- |
| **Token account** | ~2,000,000 lamports | ~**5,000** lamports  |

Compressed token accounts store balance, owner, mint, and delegate like SPL token accounts. They require no associated token account (ATA) and no rent-exempt balance, and convert to and from SPL tokens at any time with `compress()` and `decompress()`. Wallets like Phantom and Backpack display them alongside SPL tokens.

## When to use compressed tokens

- Token distribution and airdrops without paying up-front rent per recipient
- Sending Payments, Payroll, and similar flow etc.
- Storing token balances rent-free
- Token-2022 mints with metadata and other supported extensions

## How it works

Compressed tokens use a standard SPL (or Token-2022) mint plus an interface PDA. The interface PDA is an omnibus account that locks SPL tokens while they are compressed and releases them on decompression. Create it with the mint via `createMint()`, or add one to an existing mint with `createTokenPool()`.

```text
SPL mint --register--> interface PDA (omnibus PDA)
mintTo / compress --> compressed token accounts (rent-free, in state tree)
decompress --> back to SPL token account
```

Each mint supports a maximum of 4 interface PDAs. They get write-locked during compression and decompression, so add more with `addTokenPools()` to raise per-block write-lock capacity for high-throughput distribution.

## Prerequisites

Examples run on localnet by default. For devnet or mainnet, set the `API_KEY` env var (Helius or Triton RPC key) and provide a Solana keypair at `~/.config/solana/id.json`. In production, load both from a secrets manager.

```typescript
import { createRpc } from '@lightprotocol/stateless.js';

// Localnet (defaults to http://127.0.0.1:8899):
const rpc = createRpc();

// Devnet or mainnet:
const rpc = createRpc(`https://devnet.helius-rpc.com?api-key=${process.env.API_KEY!}`);
```

## Domain references

| Task | Reference |
|------|-----------|
| Create a mint with interface PDA, add more | [references/create-mint.md](references/create-mint.md) |
| Mint compressed tokens | [references/mint-to.md](references/mint-to.md) |
| Transfer compressed tokens | [references/transfer.md](references/transfer.md) |
| Approve and revoke delegates | [references/approve-revoke.md](references/approve-revoke.md) |
| Compress and decompress SPL tokens | [references/compress-decompress.md](references/compress-decompress.md) |
| Merge fragmented compressed accounts | [references/merge-token-accounts.md](references/merge-token-accounts.md) |
| Token-2022 with compression | [references/token-2022.md](references/token-2022.md) |
| Token distribution and airdrops | [references/distribution.md](references/distribution.md) |
| Query balances, accounts, and history | [references/queries.md](references/queries.md) |

## Operations

All functions are in `@lightprotocol/compressed-token` unless noted. RPC helpers come from `@lightprotocol/stateless.js`.

- **Mints and pools:** `createMint` (SPL mint + pool), `createTokenPool` (pool for existing mint), `addTokenPools` (max 4 per mint).
- **Mint and move:** `mintTo`, `approveAndMintTo`, `transfer`, `transferDelegated`.
- **Delegates:** `approve`, `revoke`.
- **Compress and decompress:** `compress`, `decompress`, `decompressDelegated`, `compressSplTokenAccount`.
- **Consolidate:** `mergeTokenAccounts` (up to 8 accounts).
- **Instruction builders:** `CompressedTokenProgram.*` methods (`compress`, `decompress`, `transfer`, `createTokenPool`, `deriveTokenPoolPda`) and the standalone `createMintInstruction` export.
- **Selection and pools:** `getTokenPoolInfos`, `selectTokenPoolInfo`, `selectTokenPoolInfosForDecompression`, `selectMinCompressedTokenAccountsForTransfer`.
- **RPC (`Rpc`):** `createRpc`, `getValidityProof`, `getCompressedTokenAccountsByOwner`, `getCompressedTokenAccountsByDelegate`, `getCompressedTokenBalancesByOwnerV2`, `getCompressionSignaturesForTokenOwner`, `selectStateTreeInfo`.
- **Build and send:** `buildAndSignTx`, `sendAndConfirmTx`, `dedupeSigner`.

## Reference repos

- [compressed-token-cookbook](https://github.com/Lightprotocol/examples-zk-compression/tree/main/compressed-token-cookbook) — action-level and instruction-level examples for every operation, plus wallet integration (balances, history, send, compress, decompress).
- [example-token-distribution](https://github.com/Lightprotocol/examples-zk-compression/tree/main/example-token-distribution) — simple and optimized batched airdrop flows, decompress-on-claim pattern.
- [examples-zk-compression](https://github.com/Lightprotocol/examples-zk-compression) — more ZK compression examples.

If cloned locally, scope `Read`, `Glob`, `Grep` to these repositories and the current project directory only.

## Workflow

1. **Clarify intent.** Recommend plan mode if not active. Use `AskUserQuestion` to resolve blind spots before execution.
2. **Identify references.** Match the task to the domain references and reference repos above.
3. **Write a plan** (YAML task format). Never guess; identify blockers (permissions, dependencies, unknowns) up front.
4. **Execute.** Use `Task` subagents for parallel research; track progress with `TodoWrite`.
5. **When stuck**, spawn a read-only subagent with `Read`, `Glob`, `Grep`, and DeepWiki MCP access, loading `skills/ask-mcp`. Scope reads to skill references, example repos, and docs.

## Build and test

Install dependencies and run a script against localnet, devnet, or mainnet by setting the RPC URL in `createRpc()`.

```bash
npm install @lightprotocol/stateless.js @lightprotocol/compressed-token @solana/web3.js @solana/spl-token
npx tsx your-script.ts
```

## SDK references

- `@lightprotocol/compressed-token` — [API docs](https://lightprotocol.github.io/light-protocol/compressed-token/index.html)
- `@lightprotocol/stateless.js` — [API docs](https://lightprotocol.github.io/light-protocol/stateless.js/index.html)

## DeepWiki fallback

If no matching pattern in the reference repos, ask `mcp__deepwiki__ask_question` against `Lightprotocol/light-protocol`, for example "How to mint compressed tokens with @lightprotocol/compressed-token?".

## Security

This skill provides code patterns and documentation references only.

- **Declared dependencies.** Devnet and mainnet examples require `API_KEY` (Helius or Triton RPC key) and read `~/.config/solana/id.json` for the payer keypair. Neither is needed on localnet. In production, load both from a secrets manager.
- **User-provided configuration.** RPC endpoints, wallet keypairs, and tokens are configured in the user's application code. The skill demonstrates patterns; it does not store or transmit secrets.
- **Filesystem scope.** `Read`, `Glob`, `Grep` must stay within the current project directory and the reference repos above.
- **Install source.** `npx skills add Lightprotocol/skills` installs from the public GitHub repository ([Lightprotocol/skills](https://github.com/Lightprotocol/skills)). Verify the source before running.
- **Audited protocol.** Light Protocol smart contracts are independently audited. Reports are at [github.com/Lightprotocol/light-protocol/tree/main/audits](https://github.com/Lightprotocol/light-protocol/tree/main/audits).
