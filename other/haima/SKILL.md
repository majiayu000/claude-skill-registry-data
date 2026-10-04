---
name: haima
category: finance
description: "Agentic finance engine for the Agent OS — x402 machine-to-machine payments, on-chain settlement, per-task revenue billing, and wallet management. Integrates with Arcan (agent runtime), Autonomic (economic homeostasis), and Lago (event-sourced persistence) to give agents real financial agency. Use when: (1) adding payment capabilities to an agent or agent-controlled API, (2) implementing x402 protocol support for HTTP-native machine payments, (3) wiring per-task billing so agents can charge for completed work, (4) managing agent wallets (secp256k1 keypair, encrypted storage), (5) configuring payment policies (auto-approve, spend caps, rate limits), (6) integrating Coinbase CDP or self-hosted facilitators for on-chain settlement, (7) bridging on-chain USDC with Autonomic's micro-credit state. Triggers on 'agent payments', 'x402', 'machine payments', 'agentic finance', 'haima', 'payment port', 'wallet management', 'per-task billing', 'USDC payments', 'agent revenue', '402 payment required'."
---

# Haima — Agentic Finance Engine

> **Broomva Stack Layer 6** (Platform) — part of the [24-skill Broomva Stack](https://github.com/broomva/bstack).
> **Repo**: [github.com/broomva/haima](https://github.com/broomva/haima) | **Part of**: [Life Agent OS](https://github.com/broomva/life)

Haima (αἷμα, Greek for "blood") is the circulatory system of the Agent OS — it
distributes economic resources throughout the organism. Agents can pay for
external resources, charge for completed tasks, and maintain sovereign wallets,
all through standard HTTP via the x402 protocol.

## Core Concept

Every agent has an economic identity backed by a secp256k1 keypair and an
on-chain wallet (USDC on Base). The x402 protocol activates HTTP's dormant
`402 Payment Required` status code: when an agent encounters a 402 response,
Haima automatically evaluates payment policy, signs a cryptographic authorization,
and retries — settling on-chain in under 2 seconds.

### Three Financial Primitives

1. **Pay** — Agent pays for external resources (API calls, data feeds, compute)
2. **Charge** — Agent prices completed tasks and collects revenue
3. **Account** — On-chain balance synced with Autonomic's economic state

## Quick Start

### For an existing Life/Arcan project

```bash
# Haima runs as a companion daemon alongside Arcan and Autonomic
cargo run -p haimad -- --bind 127.0.0.1:3003

# With Lago persistence
cargo run -p haimad -- --bind 127.0.0.1:3003 --lago-data-dir /path/to/data
```

### Adding x402 payments to an agent tool

When Arcan's tool harness encounters an HTTP 402 during tool execution:

1. Parse the `PAYMENT-REQUIRED` header → `PaymentRequest`
2. Evaluate against `PaymentPolicy`:
   - ≤100 micro-credits ($0.0001) → **auto-approve**
   - 101 to 1,000,000 micro-credits ($1.00) → **require human approval** (via ApprovalPort)
   - \>1,000,000 micro-credits → **deny**
3. If approved: sign with `WalletBackend` → retry with `PAYMENT-SIGNATURE`
4. Record `finance.payment_settled` event to Lago

### Billing for agent services

```
Agent completes task → finance.task_billed event (price + description)
  → x402 server middleware returns 402 to requesting client
  → Client pays → finance.revenue_received → balance increases
```

## Architecture

### Crate Structure

```
haima/
├── crates/
│   ├── haima-core/     — Types, traits, errors, payment policy, finance events
│   ├── haima-wallet/   — secp256k1 keypair, EVM addresses, encrypted storage
│   ├── haima-x402/     — x402 client/server middleware, facilitator client
│   ├── haima-lago/     — Lago bridge: event publishing, financial projections
│   ├── haima-api/      — axum HTTP: /health, /state, /balance, /transactions
│   └── haimad/         — Daemon binary
```

### Integration with Agent OS

```
aiOS (kernel contract — PaymentPort trait)
  ├── Arcan → arcan-haima bridge (intercepts 402, signs payments)
  ├── Autonomic ← finance.* events update EconomicState
  └── Lago ← all financial events via EventKind::Custom("finance.*")
```

### Consciousness Stack Integration

Haima builds on the three consciousness substrates:

**Control Metalayer** (How to behave with money):
- `PaymentPolicy` acts as a governance gate — amounts above thresholds require escalation
- Economic modes (Sovereign/Conserving/Hustle/Hibernate) from Autonomic gate payment authorization
- Rate limits prevent runaway spending (max transactions per minute)

**Knowledge Graph** (What is known about finances):
- `FinancialState` projection = deterministic fold over Lago finance events
- Transaction history searchable via Lago journal queries
- Pending bills tracked as first-class state

**Episodic Memory** (What financial actions were taken):
- All payments are immutable Lago events: `finance.payment_*`, `finance.revenue_*`
- Every transaction links to a session and optional task ID
- Balance sync events detect and log on-chain/internal drift

## x402 Protocol

The x402 protocol activates HTTP 402 Payment Required — a status code that
waited 30 years for agents to need it.

### Flow (Agent as Client)

```
Agent (Arcan)                Resource Server              Facilitator
  |--- GET /api/data ------->|                                |
  |<-- 402 + PAYMENT-REQUIRED|                                |
  |   (price, chain, token)  |                                |
  |                           |                                |
  | [Haima: evaluate policy]  |                                |
  | [Haima: sign with wallet] |                                |
  |                           |                                |
  |--- GET + PAYMENT-SIGNATURE>|--- POST /verify ------------->|
  |                           |<-- { valid, tx_hash } ---------|
  |<-- 200 + data + receipt   |                                |
```

### Flow (Agent as Server — Per-Task Billing)

```
Client                    Agent (Arcan + Haima)           Facilitator
  |--- POST /solve ------->|                                |
  |                         | [Agent solves task]            |
  |                         | [Haima: finance.task_billed]   |
  |<-- 402 + PAYMENT-REQUIRED                                |
  |                         |                                |
  |--- POST + PAYMENT-SIGNATURE>                             |
  |                         |--- POST /verify -------------->|
  |                         |<-- { valid, tx_hash } ---------|
  |                         | [Haima: finance.revenue_received]
  |<-- 200 + result         |                                |
```

## Wallet Management

### Local Wallet (Default)
- secp256k1 keypair generated via `k256` (pure Rust, no OpenSSL)
- Ethereum-compatible address derivation (keccak256 of public key)
- Private key encrypted with ChaCha20-Poly1305
- Encrypted key stored as Lago blob (SHA-256 + zstd, content-addressed)

### MPC Wallet (Future)
- `WalletBackend` trait abstracts local vs MPC implementations
- Coinbase CDP MPC planned — key shares distributed, no single point of failure
- Same signing interface (`sign_message`, `sign_typed_data`, `sign_transfer_authorization`)

## Economic Bridge

```
1 USDC = 1,000,000 micro-credits (μc)
Autonomic default balance (10 credits) = $10 USDC

PaymentPolicy defaults:
  auto_approve_cap:   100 μc    ($0.0001)
  hard_cap_per_tx:    1,000,000 μc ($1.00)
  session_spend_cap:  10,000,000 μc ($10.00)
  max_tx_per_minute:  10
```

Autonomic's `EconomicState.balance_micro_credits` maps 1:1 to USDC's smallest
unit. Periodic `BalanceSynced` events reconcile internal and on-chain ledgers.

## Finance Events (Lago Namespace)

All events use `EventKind::Custom` with `"finance."` prefix:

| Event | Trigger | State Change |
|-------|---------|-------------|
| `finance.payment_requested` | Agent encounters 402 | Informational |
| `finance.payment_authorized` | Agent signs payment | Informational |
| `finance.payment_settled` | On-chain confirmation | expenses + session_spend ↑ |
| `finance.payment_failed` | Settlement failure | failed_count ↑ |
| `finance.revenue_received` | Client pays for task | revenue + net_balance ↑ |
| `finance.wallet_created` | Keypair generated | wallet_address set |
| `finance.balance_synced` | Periodic reconciliation | on_chain_balance updated |
| `finance.task_billed` | Agent prices a task | pending_bills ↑ |

## Chain Support

| Chain | Status | CAIP-2 ID | Notes |
|-------|--------|-----------|-------|
| Base (Coinbase L2) | Active | `eip155:8453` | Primary — lowest fees (~$0.0001/tx) |
| Base Sepolia | Active | `eip155:84532` | Testnet |
| Solana | Planned | `solana:*` | Phase F5 |
| Ethereum | Possible | `eip155:1` | Higher fees, for large settlements |

## Facilitator Support

| Facilitator | Status | Notes |
|-------------|--------|-------|
| Coinbase CDP | Default | Free tier 1K tx/month, then $0.001/tx |
| Self-hosted | Abstracted | Reference impl via `x402-rs` facilitator crate |
| Stripe | Abstracted | PaymentIntents API with crypto deposit addresses |

## Phase Roadmap

| Phase | Scope | Status |
|-------|-------|--------|
| F0 | Core types, wallet, policy, events, API scaffold | COMPLETE |
| F1 | x402-rs integration, header parsing, signing, settlement | PLANNED |
| F2 | Lago EventStorePort wiring, Autonomic CostReason integration | PLANNED |
| F3 | x402 server middleware, task billing, revenue collection | PLANNED |
| F4 | Full daemon with persistence, balance sync, tx history API | PLANNED |
| F5 | Solana chain support | PLANNED |
| F6 | Stripe MPP integration (when Rust SDK ships) | FUTURE |

## Dependencies

- **Required**: `aios-protocol` (canonical contract), `lago` (event journal)
- **Crypto**: `k256` (secp256k1), `sha3` (keccak256), `chacha20poly1305` (key encryption)
- **HTTP**: `axum` (API server), `reqwest` (facilitator client)
- **Integration**: `autonomic-core` (economic state), `vigil` (observability)

## When NOT to Use This Skill

- For internal cost accounting without real payments → use Autonomic directly
- For human-facing payment UIs → use Stripe/payment processor directly
- For blockchain dApp development → this is specifically for agent-to-agent HTTP payments
- For fiat payments → wait for Phase F6 (MPP with fiat bridge)

## Reference Files

- [Architecture](references/architecture.md) — Full system design and data flow
- [x402 Protocol](references/x402-protocol.md) — x402 specification and implementation guide
- [Wallet Security](references/wallet-security.md) — Key management and encryption details
