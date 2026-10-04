---
name: mpp-dev
description: |
  Comprehensive development support for MPP (Machine Payments Protocol) — the open, IETF-draft-style
  HTTP payment standard co-authored by Stripe and Tempo, built on HTTP 402 with a Challenge /
  Credential / Receipt model. Covers protocol design, client (payer) integration, server (payee)
  middleware, MCP server monetization, service discovery, method selection (Tempo, EVM/x402-compatible,
  Stripe Shared Payment Tokens, Lightning, and other rails), security review, and testing.

  USE THIS SKILL whenever the user:
  - Asks about MPP, the Machine Payments Protocol, paymentauth.org, mpp.dev, or mpp-specs
  - Wants to add pay-per-request/agentic pricing to an API using the `mppx` package
  - Integrates MPP with Express, Hono, Next.js, Elysia, or a plain fetch/Request-Response server
  - Builds an AI agent or coding agent that pays for tools/APIs autonomously via MPP
  - Implements an MCP server with payment-gated tools using the MPP JSON-RPC/MCP transport
  - Needs to choose or implement a payment method (Tempo, EVM/Permit2/EIP-3009, Stripe SPT, Lightning)
  - Asks how MPP relates to or interoperates with x402
  - Reviews an MPP integration for security issues (Challenge binding, replay, secret handling)
  - Writes or reviews tests for an MPP client/server integration

  Even if the user just says "add payments to my agent's API calls", "let my MCP server charge for
  tool calls", or "accept stablecoins and cards on the same endpoint", invoke this skill — these are
  MPP's core use cases even when the user doesn't name the protocol.
model: opus
---

# MPP (Machine Payments Protocol) Development Guide

MPP is an **open, IETF-draft-style HTTP payment standard**, co-authored by **Stripe and Tempo**,
that layers a `Payment` HTTP Authentication Scheme on top of `402 Payment Required` so any HTTP
client — especially an AI agent — can pay for a resource as part of the request itself, with no
pre-provisioned account, API key, or billing relationship. Spec source: `github.com/tempoxyz/mpp-specs`
(published at `paymentauth.org`). Docs/directory: `mpp.dev`. TypeScript SDK: `mppx` on npm (SDKs
also exist for Python, Rust, Go, Ruby).

## Quick Orientation

| Role | Description |
|---|---|
| **Client / Payer** | Sends a request, receives a **Challenge** (402), fulfills it (signs a tx, mints a token), retries with a **Credential** |
| **Server / Payee** | Returns a **Challenge** describing accepted methods, verifies the **Credential**, settles, returns the resource + a **Receipt** |
| **Relay** (optional) | Third-party infra exposing only `validate`/`broadcast` — MPP defines no relay API shape; Tempo's first-party relay is `api.tempo.xyz` |

**Payment Flow:**
1. Client requests resource → server returns `402` with `WWW-Authenticate: Payment ...` (the Challenge)
2. Client fulfills the Challenge (signs, pays, mints) → retries with `Authorization: Payment ...` (the Credential)
3. Server verifies + settles → returns `200` + `Payment-Receipt` header (the Receipt)

Always capitalize **Challenge**, **Credential**, **Receipt** as protocol proper nouns in docs/UI copy.

---

## Package Reference

```bash
npm i mppx              # TypeScript SDK — client, server, framework middlewares, CLI (package is `mppx`, NOT `mpp` or `@wevm/mppx`)
npm i -g mppx            # also installs the `mppx` CLI (account/session management, curl-like paid requests)
```

```
mppx/client       — payment-aware fetch wrapper, hooks, CLI internals
mppx/server       — Mppx.create({ secretKey, methods }), .charge(), .compose()
mppx/express | mppx/hono | mppx/nextjs | mppx/elysia   — framework middlewares + discovery()
mppx/tempo | mppx/evm | mppx/stripe | mppx/x402         — per-method exports
```

Other official SDKs: `tempoxyz/pympp` (Python), `tempoxyz/mpp-rs` (Rust). `viem` is a required peer
dependency for TypeScript client/server code.

---

## Implementation Paths

Choose your path and read the reference file — don't guess wire formats or signing schemes from
memory, since this is a fast-moving, brand-new protocol; the reference files below are grounded in
the actual spec/SDK source, not general payment-protocol intuition.

| Task | Reference File |
|---|---|
| Understand the wire protocol (Challenge/Credential/Receipt formats, status codes, error codes, versioning) | [references/protocol-core.md] |
| Choose/implement a **payment method** (Tempo, EVM, Stripe, Lightning, ...) and its signing scheme | [references/methods.md] |
| Build a **client** that pays for resources | [references/client.md] |
| Build a **server** that charges for resources, incl. multi-method `compose()` | [references/server.md] |
| Monetize an **MCP server** tool, or wire up service **discovery** | [references/mcp-and-discovery.md] |
| **Security review** an integration, or write tests for one | [references/security-testing.md] |
| Understand or implement **MPP ↔ x402 interoperability** | [references/x402-interop.md] |

---

## Minimal Working Examples

### Client — TypeScript

```ts
import { Mppx, tempo } from 'mppx/client'
import { privateKeyToAccount } from 'viem/accounts'

const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`)
const mppx = Mppx.create({ methods: [tempo({ account })] })

const res = await mppx.fetch('/api/photo')   // transparently handles 402 → sign → retry
const data = await res.json()
```

### Server — Express

```ts
import express from 'express'
import { Mppx, tempo } from 'mppx/express'

const app = express()
const mppx = Mppx.create({ methods: [tempo()] })   // reads MPP_SECRET_KEY from env

app.get('/premium', mppx.charge({ amount: '1' }), (req, res) => {
  res.json({ data: 'paid content' })
})
```

### MCP Server — Payment-Gated Tool

```ts
import { Mppx, tempo } from 'mppx/server'
import { Transport } from 'mppx'
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'

const mppx = Mppx.create({
  secretKey: process.env.MPP_SECRET_KEY!,
  methods: [tempo.charge({ /* ... */ })],
  transport: Transport.mcpSdk(),
})

const server = new McpServer({ name: 'paid-tools', version: '1.0.0' })

server.tool('get_premium_data', schema, async (params, extra) => {
  const result = await mppx.charge({ amount: '0.01' })(extra)
  if (result.status === 402) throw result.challenge   // -> McpError code -32042
  return result.withReceipt({ content: [{ type: 'text', text: 'premium data' }] })
})
```

---

## Status Code Cheat Sheet

| Meaning | Status |
|---|---|
| Payment needed (no/expired/invalid credential) | **402** — always, including retries after a failed proof |
| Non-payment auth failure | **401** |
| Payment succeeded, still not authorized by policy | **403** — never 402 |
| Payment succeeded | **200** + `Payment-Receipt` header |

`Cache-Control: no-store` is mandatory on every 402; `Cache-Control: private` is mandatory
whenever a `Payment-Receipt` is present. Full error-code table in [references/protocol-core.md].

---

## Common Issues & Solutions

| Issue | Solution |
|---|---|
| `Missing secret key` at server startup | Set `MPP_SECRET_KEY` (≥32 bytes) or pass `secretKey` to `Mppx.create()` |
| Payment retried endlessly / server keeps issuing fresh Challenges | Cap `maxPaymentRetries` on the client; check the server isn't rejecting valid Credentials |
| Credential accepted from a different Challenge (replay) | Bug in method implementation — the signature must derive from `challenge.id`/`challenge.realm`; see the binding checklist in [references/security-testing.md] |
| Want to accept both crypto and cards on one route | Use `mppx.compose()` with `tempo.charge()` + `stripe.charge()`, see [references/server.md] |
| Want one route to accept both native MPP and x402 clients | Use `evm.charge({ x402: { facilitator } })`, see [references/x402-interop.md] |
| Stripe SPT creation failing / insecure | SPT must be minted **server-side** with a Stripe secret key — never client-side |
| Using Tempo chain id `98865` | Deprecated — use mainnet `4217` or testnet (Moderato) `42431` |
| Terminology nitpicks in review (escrow, USDC vs USDC.e) | Say "reserve"/"lock up" not "escrow"; say "USDC.e" for Tempo's bridged token, plain "USDC" elsewhere |

---

## Environment Variables

```bash
# Server
MPP_SECRET_KEY=...             # >=32 bytes; HMAC root for Challenge-id binding — treat like a JWT signing key
WALLET_ADDRESS=0x...           # or Tempo account — recipient of settled funds

# Client
PRIVATE_KEY=0x...              # EVM/Tempo signer (viem Account)

# Stripe method (server-side only)
STRIPE_SECRET_KEY=sk_...
STRIPE_NETWORK_ID=...          # for Shared Payment Token issuance
```

---

## Reference Files

- **[references/protocol-core.md]** — Wire protocol: Challenge/Credential/Receipt formats, HTTP status semantics, Challenge-id HMAC binding, error codes, versioning, intents (charge/session/subscription/zero-dollar)
- **[references/methods.md]** — Per-rail signing schemes: Tempo (TIP-20, gasless, sessions), EVM (Permit2/EIP-3009/tx/hash), Stripe (Shared Payment Tokens), plus pointers for Lightning/Solana/Hedera/Stellar
- **[references/client.md]** — `mppx/client` patterns: fetch wrapper, hooks, dual-protocol clients, agent spend limits (access keys), CLI
- **[references/server.md]** — `mppx/server` patterns: Express/Hono/Next.js/Elysia middlewares, `compose()`, discovery, refunds
- **[references/mcp-and-discovery.md]** — MCP transport binding (`_meta` fields, `-32042`/`-32043`), OpenAPI discovery, MPPScan/MPP Services directory, agent-permissions.json
- **[references/security-testing.md]** — `MPP_SECRET_KEY` handling, Challenge-binding review checklist, common protocol mistakes, test conventions and a concrete test checklist
- **[references/x402-interop.md]** — MPP vs. x402 positioning, dual-protocol `evm.charge()` pattern, when to use which
