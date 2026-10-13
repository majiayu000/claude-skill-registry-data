---
description: "MagicBlock Ephemeral Rollups development patterns for Solana. Covers delegation/undelegation flows, dual-connection architecture (base layer + ER), cranks for scheduled tasks, VRF for verifiable randomness, magic actions for atomic ER-commit + base-layer follow-ups, private payments API (deposits, transfers, withdrawals, swaps, and challenge/login auth flow), commit sponsorship and fee vault wiring, lamports top-up for delegated accounts, and TypeScript/Anchor integration. Use for high-performance gaming, real-time apps, private transfers and swaps, and fast transaction throughput on Solana."
---
# MagicBlock Ephemeral Rollups Skill

## What this Skill is for
Use this Skill when the user asks for:
- MagicBlock Ephemeral Rollups integration
- Delegating/undelegating Solana accounts to ephemeral rollups
- High-performance, low-latency transaction flows
- Crank scheduling (recurring automated transactions)
- VRF (Verifiable Random Function) for provable randomness
- Magic Actions — base-layer instructions chained to an ER commit
- Topping up a delegated account's lamports via `lamportsDelegatedTransferIx`
- Dual-connection architecture (base layer + ephemeral rollup)
- Gaming and real-time app development on Solana
- Private payments (deposits, transfers, withdrawals, and swaps via the Payments API, with optional bearer-token auth for private reads)
- Lifting the default 10-commit sponsorship cap with `magic_fee_vault`

## Key Concepts

**Ephemeral Rollups** enable high-performance, low-latency transactions by temporarily delegating Solana account ownership to an ephemeral rollup. Ideal for gaming, real-time apps, and fast transaction throughput.

**Delegation** transfers account ownership from your program to the delegation program, allowing the ephemeral rollup to process transactions at ~10-50ms latency vs ~400ms on base layer.

**MagicIntentBundleBuilder** (SDK 0.11+) is the current way to schedule commit and commit-and-undelegate intents. The free functions `commit_accounts` and `commit_and_undelegate_accounts` are deprecated.

**Private Ephemeral Rollups (PER)** add a permission account that gates who can interact with a delegated account inside a TEE-backed validator. The recommended pattern is to delegate the permission account itself alongside the permissioned account, so member updates execute on the ER in milliseconds instead of base-layer round-trips.

**Magic Actions** are base-layer instructions scheduled inside an ER transaction via `MagicIntentBundleBuilder.add_post_commit_actions(...)`. They execute atomically once the commit is sealed back to base layer — useful for leaderboard updates, reward distribution, and any side-effect that must run as part of the commit.

**Commit sponsorship**: every delegated account gets 10 free commits to base layer by default. To lift the cap, either re-delegate (refreshes the quota) or attach a `magic_fee_vault` PDA + delegated fee payer to the intent bundle.

**Lamports top-up**: when a delegated account (e.g. a delegated fee payer) needs more lamports on the ER side, use `lamportsDelegatedTransferIx` from the SDK. The transaction is submitted on **base layer** — the Ephemeral SPL Token program creates a single-use lamports PDA, funds it, and delegates it so the ER credits the destination.

**Architecture**:
```
┌─────────────────┐     delegate      ┌─────────────────────┐
│   Base Layer    │ ───────────────►  │  Ephemeral Rollup   │
│    (Solana)     │                   │    (MagicBlock)     │
│                 │  ◄───────────────  │                     │
└─────────────────┘    undelegate     └─────────────────────┘
     ~400ms                                  ~10-50ms
```

## Default stack decisions (opinionated)

1) **Programs: Anchor with ephemeral-rollups-sdk**
   - Use `ephemeral-rollups-sdk` with Anchor features
   - Apply `#[ephemeral]` macro before `#[program]`
   - Use `#[delegate]` and `#[commit]` macros for delegation contexts

2) **Dual Connections**
   - Base layer connection for initialization and delegation
   - Ephemeral rollup connection for operations on delegated accounts

3) **Transaction Routing**
   - Delegate transactions → Base Layer
   - Operations on delegated accounts → Ephemeral Rollup
   - Undelegate/commit transactions → Ephemeral Rollup

## Operating procedure (how to execute tasks)

### 1. Classify the operation type
- Account initialization (base layer)
- Delegation (base layer)
- Operations on delegated accounts (ephemeral rollup)
- Commit state (ephemeral rollup)
- Undelegation (ephemeral rollup)

### 2. Pick the right connection
- Base layer: `https://api.devnet.solana.com` (or mainnet)
- Ephemeral rollup: `https://devnet.magicblock.app/`

### 3. Implement with MagicBlock-specific correctness
Always be explicit about:
- Which connection to use for each transaction
- Delegation status checks before operations
- PDA seeds matching between delegate call and account definition
- Using `skipPreflight: true` for ER transactions
- Waiting for state propagation after delegate/undelegate

### 4. Diagnose possible service-side failures
For unexpected RPC, routing, oracle, or transaction errors that could be service-side:
- Always fetch current data; do not answer from remembered status. Use the direct JSON API `https://status.magicblock.app/api/services` as the source of truth.
- Select the same network the code uses: JSON keys are `mainnet` and `devnet`.
- Match the affected endpoint to the right region/server and service:
  - Regions are `asia`, `europe`, `usa`, and `tee`.
  - Service IDs are listed in `.meta.services`; currently `er` (Ephemeral Rollup), `rpc_router`, `pricing_oracle`, and `vrf_oracle`.
  - Use the server entries under `.environments[network].regions[region].servers`; for mainnet Asia this includes `as.magicblock.app`.
- Interpret `.live_status[service]`: `true` = Operational, `false` = Down, missing/undefined = N/A.
- Interpret `.metrics[service]` as downtime minutes per day aligned with `.meta.days` in UTC.
- When reporting findings, include the network, region, endpoint, service status, and relevant date range. Distinguish live status from historical downtime.
- For direct ER RPC endpoints, optionally correlate with JSON-RPC `getHealth` or `getVersion`, but do not let a single RPC probe replace the status API.

### 5. Add appropriate features
- Cranks for recurring automated transactions
- VRF for verifiable randomness in games/lotteries
- Private payments API for private transfers and swaps

### 6. Deliverables expectations
When you implement changes, provide:
- Exact files changed + diffs
- Commands to install/build/test
- Risk notes for anything touching delegation/signing/state commits

## Progressive disclosure (read when needed)
- Core delegation patterns: [delegation.md](delegation.md)
- Magic Actions (post-commit base-layer instructions): [magic-actions.md](magic-actions.md)
- Topping up a delegated account with lamports: [lamports-topup.md](lamports-topup.md)
- TypeScript frontend setup: [typescript-setup.md](typescript-setup.md)
- Cranks (scheduled tasks): [cranks.md](cranks.md)
- VRF (randomness): [vrf.md](vrf.md)
- Private Payments API: [private-payments.md](private-payments.md)
- Reference links & versions: [resources.md](resources.md)
