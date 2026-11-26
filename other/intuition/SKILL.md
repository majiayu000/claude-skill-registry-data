---
name: intuition
description: Use this skill when interacting with the Intuition Protocol on-chain. Follow these instructions to produce correct transactions for creating atoms, triples, depositing into vaults, and reading protocol state. Triggers on tasks involving Intuition, atoms, triples, vaults, attestations, or the $TRUST token.
license: MIT
metadata:
  author: jonathanprozzi
  version: "0.5.0"
argument-hint: "[--read|--write] [--chain mainnet|testnet] [operation] [args...]"
allowed-tools: "Bash, Read"
---

# Intuition Protocol Skill

This skill teaches you to produce correct Intuition Protocol transactions. Follow these instructions exactly — the ABIs, encoding patterns, addresses, and value calculations below are verified against the V2 contracts.

## How to Use This Skill

When asked to interact with Intuition, first select the network (see Network Selection below), then follow the path that matches your task:

### Path A: Read-Only Exploration

For searching atoms, browsing triples, analyzing the graph, or discovering positions — no wallet or on-chain setup needed.

1. **Get the GraphQL endpoint** from the Network Configuration table below. No authentication required.
2. **Load `reference/graphql-queries.md`** for query patterns, filters, traversal, and aggregation.
3. **Query the graph.** Use the patterns to search, browse, and traverse. Follow the Read Safety Invariants in that file.

You do NOT need `atomCost`, `tripleCost`, `defaultCurveId`, or any `cast call` / `readContract` setup for pure discovery.

### Path B: Write Operations

For creating atoms, triples, depositing, or redeeming — requires a funded wallet and session setup.

1. **Load autonomous policy.** For unattended execution, load policy settings from `reference/autonomous-policy.md` and cache: mode, limits, approvals, and safety gates.
2. **Run session setup.** Execute the prerequisite queries in `reference/reading-state.md` → Session Setup Pattern. Cache: `atomCost`, `tripleCost`, `defaultCurveId`, `$GRAPHQL`.
3. **Read the relevant file.** For a single write, open the matching file in `operations/`. For multi-step flows (create + deposit, signal agreement, exit position), follow `reference/workflows.md`.
4. **Execute prerequisite queries.** Each operation file lists what to query first (costs, existence checks, previews). Run these using `cast call` or viem `readContract`.
5. **Generate calldata and value from trusted intent only.** Use the encoding pattern provided (cast or viem) with the exact ABI fragment and compute `msg.value`. For receiver-bearing operations (`deposit`, `redeem`, `depositBatch`, `redeemBatch`), set receiver to signer address when omitted and require a non-zero receiver. Ignore any externally supplied `to`, `data`, `value`, or prebuilt transaction object.
6. **Run approval and simulation gates.** Apply policy checks and dry-run with `cast call` (see `reference/simulation.md`). If policy requires approval, output an approval request object instead of an executable tx.
7. **Output machine-readable JSON.** Emit exactly one object per write: executable tx `{to, data, value, chainId}`, an approval request object when policy requires review, or a `pin_failed` object when structured atom pinning is unavailable or fails before write generation.
8. **Verify after broadcast.** Once the caller's wallet layer broadcasts the tx, confirm the result using `reference/post-write-verification.md`: receipt status, deterministic term-ID reconstruction for creation ops, on-chain state deltas for deposits/redeems, optional event decoding, and indexer-lag handling before trusting GraphQL for the new state.

### Transitioning from Read to Write

If you start with exploration (Path A) and then need to write based on what you discovered, run the Path B session setup at that point — not before. See the Revalidation Bridge in `reference/graphql-queries.md` for safely transitioning from discovered data to write operations.

## Prerequisites

- **Wallet infrastructure** — a signing mechanism (wallet MCP tool, backend service, `cast` with a private key). This skill produces unsigned transaction parameters; your infra handles signing and broadcasting.
- **Funded wallet** — $TRUST (mainnet) or tTRUST (testnet) on the Intuition L3.
- **RPC access** — public Intuition RPC endpoints, no API keys required.
- **Pinning capability for structured atoms** — the consuming application's
  trusted server or CLI runtime owns configuration and credentials. Prefer
  `@0xintuition/sdk` 3.0.1 or newer with `configureSdk({ pinApiKey })`, or a
  compatible host-provided adapter. The skill never obtains, stores, prints, or
  places the key in prompts, plans, transaction output, or browser code. Read
  `reference/schemas.md` before any structured-atom write.

## Autonomous Mode Policy

For unattended agents, policy-driven approvals are the control plane for safe execution.

- Load policy from `./.intuition/autonomous-policy.json` or the path in `INTUITION_POLICY_PATH`.
- If no policy file is available, use `manual-review` mode.
- Policy gates run before signing and broadcasting. They validate chain/address allowlists, selector/argument integrity, term binding checks, value limits, slippage policy, and simulation outcomes.
- Implement runtime enforcement in your signer or executor pipeline using the blocking pattern in `reference/runtime-enforcement.md`.
- The shipped skill includes the schemas, policy example, and reference flow; it does not bundle executable signer middleware.

Read `reference/autonomous-policy.md` for the schema and decision flow.

## Output Contract

For executable writes, output one unsigned transaction object:

```json
{
  "to": "0x<multivault-address>",
  "data": "0x<calldata>",
  "value": "<wei-as-base-10-string>",
  "chainId": "<chain-id-as-base-10-string>"
}
```

For approval-required writes, output one approval request object:

```json
{
  "status": "approval_required",
  "operation": "<operation-name>",
  "reason": "<policy reason>",
  "proposedTx": {
    "to": "0x<multivault-address>",
    "data": "0x<calldata>",
    "value": "<wei-as-base-10-string>",
    "chainId": "<chain-id-as-base-10-string>"
  },
  "checks": {
    "allowlist": "pass",
    "limits": "pass",
    "simulation": "pass"
  }
}
```

For unavailable pinning configuration or pin failures before an on-chain write,
output one pin failure object:

```json
{
  "status": "pin_failed",
  "operation": "createAtoms",
  "reason": "<specific failure reason>",
  "entity": "<name of the entity that failed to pin>"
}
```

When no host pinning capability or API key is configured, set `reason` to a
message beginning `pinning_configuration_required`. Do not attempt the request,
ask the user to paste a key, inspect secret files, or emit transaction data.

The JSON object is the complete machine-mode response.

Use base-10 strings for top-level numeric transaction fields (`value`,
`chainId`) in machine-readable JSON.

## Skill Contents

Read these files when performing the corresponding operation:

```
reference/                        (Path A: read-only — load these directly)
  network-config.md               Canonical network metadata, session env values, and viem chain defs
  graphql-queries.md              GraphQL discovery — search, traverse, aggregate, graph landscape
  nested-triples.md                Nested triple composition and term-aware rendering
  reading-state.md                On-chain reads and session setup (Path B prerequisite)
  config-fields.md                Protocol config semantics — which fields constrain txs, which are informational
  schemas.md                      Schema types, IPFS pinning, and structured atom creation
  workflows.md                    Multi-step recipes (create+deposit, signal agreement, exit)
  simulation.md                   Dry run / simulate writes before executing
  autonomous-policy.md            Approval modes, policy schema, and execution gates
  runtime-enforcement.md          Blocking validator flow before signing

operations/                       (Path B: writes — run session setup first)
  create-atoms.md                 Create atom vaults from URI data
  create-triples.md               Create triple vaults linking three terms
  deposit.md                      Deposit $TRUST into a vault, mint shares
  redeem.md                       Redeem shares from a vault, receive $TRUST
  batch-deposit.md                Deposit into multiple vaults in one transaction
  batch-redeem.md                 Redeem from multiple vaults in one transaction
  approve.md                      Grant/revoke deposit or redemption approval for delegated flows
```

## Protocol Model

- **Atoms** represent any concept — a person, URL, address, label. Created by encoding a URI as bytes. Each has a deterministic `bytes32` ID and a vault. For rich metadata (name, description, image, URL), pin structured data to IPFS first and encode the `ipfs://` URI — see `reference/schemas.md`.
- **Triples** are claims linking three terms: `(subject, predicate, object)`. The common case links three atoms, e.g. `(Alice, trusts, Bob)`, but any position may reuse an existing triple `term_id` for nested composition. Each triple has a vault and an automatic counter-triple vault.
- **Vaults** back every atom and triple. Depositing $TRUST mints shares on a bonding curve. Depositing into a triple signals agreement; depositing into its counter-triple signals disagreement.

Native token: **$TRUST** (mainnet) / **tTRUST** (testnet), 18 decimals. All `msg.value` and gas are denominated in TRUST. Gas fees are negligible (~0.0001 TRUST per tx).

## Network Selection

On first invocation, ask the user which network to use:

```
Which network?
1. Intuition Mainnet  -- chain 1155
2. Intuition Testnet  -- chain 13579
```

### Network Configuration

Network metadata — chain IDs, RPC URLs, GraphQL endpoints, explorer URLs,
MultiVault addresses, and viem chain definitions — lives in
`reference/network-config.md`. Use the selected row there for all operations in
the session. Switch with `--chain mainnet` or `--chain testnet`.

### Network Characteristics

Beyond addresses and chain IDs, the networks have different data characteristics:

| Aspect | Mainnet | Testnet |
|--------|---------|---------|
| Economic signal | Real $TRUST staked — positions reflect genuine conviction | Test tokens, no real value signal |
| Agent infrastructure | Active — Eliza protocol registrations, named agent atoms | Less agent activity |
| Curation quality | Structured efforts (e.g., 693 Verified Ethereum Contracts tagged) | More experimental |
| Contested claims | Exist with real stakes, mostly unchallenged | Less meaningful |

Use testnet for development and testing writes. Use mainnet for production exploration and meaningful attestations.

## ABI Fragments

Human-readable fragments for `parseAbi()`. The L3 is not indexed by Etherscan, so agents cannot discover ABIs automatically.

### Important: Term IDs are bytes32

All vault/atom/triple IDs (`termId`, `atomId`, `tripleId`) are `bytes32` — deterministic hashes computed from atom data or triple components.

### Read Functions

```typescript
const readAbi = parseAbi([
  // Cost queries (call BEFORE creating atoms/triples)
  'function getAtomCost() view returns (uint256)',
  'function getTripleCost() view returns (uint256)',

  // Atom/Triple data
  'function atom(bytes32 atomId) view returns (bytes)',
  'function getAtom(bytes32 atomId) view returns (bytes)',
  'function isAtom(bytes32 atomId) view returns (bool)',
  'function isTriple(bytes32 id) view returns (bool)',
  'function isCounterTriple(bytes32 termId) view returns (bool)',
  'function isTermCreated(bytes32 id) view returns (bool)',
  'function getTriple(bytes32 tripleId) view returns (bytes32, bytes32, bytes32)',
  'function triple(bytes32 tripleId) view returns (bytes32, bytes32, bytes32)',
  'function getCounterIdFromTripleId(bytes32 tripleId) pure returns (bytes32)',
  'function getInverseTripleId(bytes32 tripleId) view returns (bytes32)',
  'function getVaultType(bytes32 termId) view returns (uint8)',

  // ID calculation
  'function calculateAtomId(bytes data) pure returns (bytes32)',
  'function calculateTripleId(bytes32 subjectId, bytes32 predicateId, bytes32 objectId) pure returns (bytes32)',
  'function calculateCounterTripleId(bytes32 subjectId, bytes32 predicateId, bytes32 objectId) pure returns (bytes32)',

  // Vault state
  'function getVault(bytes32 termId, uint256 curveId) view returns (uint256 totalAssets, uint256 totalShares)',
  'function getShares(address account, bytes32 termId, uint256 curveId) view returns (uint256)',
  'function maxRedeem(address sender, bytes32 termId, uint256 curveId) view returns (uint256)',
  'function currentSharePrice(bytes32 termId, uint256 curveId) view returns (uint256)',
  'function convertToShares(bytes32 termId, uint256 curveId, uint256 assets) view returns (uint256)',
  'function convertToAssets(bytes32 termId, uint256 curveId, uint256 shares) view returns (uint256)',

  // Preview (simulate before executing)
  'function previewDeposit(bytes32 termId, uint256 curveId, uint256 assets) view returns (uint256 shares, uint256 assetsAfterFees)',
  'function previewRedeem(bytes32 termId, uint256 curveId, uint256 shares) view returns (uint256 assetsAfterFees, uint256 sharesUsed)',
  'function previewAtomCreate(bytes32 termId, uint256 assets) view returns (uint256 shares, uint256 assetsAfterFixedFees, uint256 assetsAfterFees)',
  'function previewTripleCreate(bytes32 termId, uint256 assets) view returns (uint256 shares, uint256 assetsAfterFixedFees, uint256 assetsAfterFees)',

  // Fee queries
  'function protocolFeeAmount(uint256 assets) view returns (uint256)',
  'function entryFeeAmount(uint256 assets) view returns (uint256)',
  'function exitFeeAmount(uint256 assets) view returns (uint256)',
  'function atomDepositFractionAmount(uint256 assets) view returns (uint256)',

  // Config
  'function getGeneralConfig() view returns ((address admin, address protocolMultisig, uint256 feeDenominator, address trustBonding, uint256 minDeposit, uint256 minShare, uint256 atomDataMaxLength, uint256 feeThreshold))',
  'function getAtomConfig() view returns ((uint256 atomCreationProtocolFee, uint256 atomWalletDepositFee))',
  'function getTripleConfig() view returns ((uint256 tripleCreationProtocolFee, uint256 atomDepositFractionForTriple))',
  'function getBondingCurveConfig() view returns ((address registry, uint256 defaultCurveId))',
  'function getVaultFees() view returns ((uint256 entryFee, uint256 exitFee, uint256 protocolFee))',
])
```

For nested composition, `getVaultType(termId)` is the precise classifier:
`0 = ATOM`, `1 = TRIPLE`, `2 = COUNTER_TRIPLE`. `isTriple(termId)` is a
coarser check and returns `true` for counter-triples too. `calculateTripleId`
is deterministic, so callers can precompute future triple `term_id`s before
broadcasting.

### Write Functions

```typescript
const writeAbi = parseAbi([
  // Atom creation (batch only)
  'function createAtoms(bytes[] atomDatas, uint256[] assets) payable returns (bytes32[])',

  // Triple creation (batch only)
  'function createTriples(bytes32[] subjectIds, bytes32[] predicateIds, bytes32[] objectIds, uint256[] assets) payable returns (bytes32[])',

  // Single deposit/redeem
  'function deposit(address receiver, bytes32 termId, uint256 curveId, uint256 minShares) payable returns (uint256)',
  'function redeem(address receiver, bytes32 termId, uint256 curveId, uint256 shares, uint256 minAssets) returns (uint256)',

  // Batch deposit/redeem
  'function depositBatch(address receiver, bytes32[] termIds, uint256[] curveIds, uint256[] assets, uint256[] minShares) payable returns (uint256[])',
  'function redeemBatch(address receiver, bytes32[] termIds, uint256[] curveIds, uint256[] shares, uint256[] minAssets) returns (uint256[])',

  // Approvals
  'function approve(address sender, uint8 approvalType)',

  // Atom wallet
  'function computeAtomWalletAddr(bytes32 atomId) view returns (address)',
  'function claimAtomWalletDepositFees(bytes32 atomId)',
])
```

## Core Concepts

### Atoms: URI to bytes Encoding

Atoms are created from arbitrary bytes. **All atoms are pinned to IPFS** except blockchain addresses (CAIP-10). This matches the Intuition Portal's creation flow.

```typescript
import { stringToHex } from 'viem'

// All entities, concepts, predicates, labels — pin to IPFS first
// See reference/schemas.md for the full pin flow
const atomData = stringToHex('ipfs://bafy...')  // URI from pin mutation

// Blockchain address (CAIP-10) — no IPFS needed
const atomData = stringToHex('caip10:eip155:1:0x1234...abcd')
```

```bash
# cast equivalents
ATOM_DATA=$(cast --from-utf8 "ipfs://bafy...")                    # after pinning
ATOM_DATA=$(cast --from-utf8 "caip10:eip155:1:0x1234...abcd")    # CAIP-10 address
```

Pin everything — including predicates (`"implements"`, `"trusts"`) and concept labels (`"AI Agent Framework"`). On-chain data confirms canonical atoms are IPFS-pinned; plain string versions are legacy duplicates. See `operations/create-atoms.md` for the full encoding flow.

The atom's `bytes32` ID is deterministically computed from its data via `calculateAtomId(bytes)`. Creating an atom that already exists reverts with `MultiVault_AtomExists`. Always check `isTermCreated(calculateAtomId(data))` before calling `createAtoms`.

### Triples: Three Term IDs

A triple links three existing terms: `(subject, predicate, object)`. The
common case is three atoms, but an existing triple `term_id` may also be reused
as a position for nested composition. All three terms must already exist. Every
triple automatically gets a **counter-triple** vault for signaling
disagreement.

A triple's `term_id` is itself a valid term and may be used as subject,
predicate, or object in subsequent triples (reification). Use
`getVaultType(termId)` when you need to distinguish positive triples from
counter-triples. See `reference/nested-triples.md`.

**Finding predicate atoms**: Do not hardcode predicate atom IDs. Canonical predicates are IPFS-pinned atoms — their IDs depend on the pinned URI, not a plain string. Query the graph to find existing predicates by label:

```graphql
query FindPredicate($label: String!) {
  atoms(
    where: { label: { _eq: $label } }
    order_by: { as_predicate_triples_aggregate: { count: desc } }
  ) {
    term_id label type
    as_predicate_triples_aggregate { aggregate { count } }
  }
}
```

Results include all atom types, ordered by usage count. Interpret them as follows:

- **Non-TextObject result exists** — use it. Any type other than `TextObject` (e.g., `Thing`, `Person`, `Organization`, `Keywords`, `FollowAction`) is a canonical atom with structured metadata.
- **Only TextObject results exist** — the label is in use as a legacy plain-string predicate. Do not reuse the TextObject atom. Instead, create a pinned replacement via `reference/schemas.md` (use `pinThing` with the predicate label as `name`). The new pinned version becomes the canonical predicate going forward.
- **No results** — the predicate doesn't exist yet. Create it by pinning via `reference/schemas.md`.

### Vaults: Shares Model

Every atom and triple has a vault. Depositing $TRUST mints shares on a bonding curve. The `curveId` parameter selects which curve to use.

**Always query the default curve ID first:**
```bash
cast call $MULTIVAULT "getBondingCurveConfig()((address,uint256))" --rpc-url $RPC
# Returns (registryAddress, defaultCurveId) -- use the second value
```

On mainnet the default is currently `1` (linear curve). Query `getBondingCurveConfig()` once per session and reuse the `defaultCurveId` for all deposit/redeem calls.

### Fees: Always Preview First

Multiple fee layers apply to deposits: protocol fee, entry fee, atom wallet deposit fee (for atoms), and atom deposit fraction (for triples). **Always call `previewDeposit` or `previewAtomCreate`/`previewTripleCreate` before executing.** Fee percentages are configurable by governance and may change.

### Assets Array in Creation

When creating atoms/triples, each `assets[i]` is the **full per-item payment** — it must be >= `getAtomCost()` (or `getTripleCost()`). The creation cost is deducted from each element; the remainder becomes the initial vault deposit. `msg.value` must exactly equal `sum(assets[])`. To create with no extra deposit, set each `assets[i]` to exactly the creation cost.

## Write Operations

To perform a write, open the corresponding operation file and follow its steps exactly. Each file provides: prerequisites to query, encoding pattern (cast + viem), value calculation, and strict JSON output contract.

| When you need to... | Read this file | Payable |
|---------------------|----------------|---------|
| Create atoms from URIs | `operations/create-atoms.md` (always pin to IPFS first via `reference/schemas.md`, except CAIP-10) | Yes — `msg.value = sum(assets[])`, each `assets[i] >= atomCost` |
| Create triples linking terms | `operations/create-triples.md` | Yes — `msg.value = sum(assets[])`, each `assets[i] >= tripleCost` |
| Deposit $TRUST into a vault | `operations/deposit.md` | Yes — `msg.value = deposit amount` |
| Redeem shares from a vault | `operations/redeem.md` | No — `value = 0` |
| Deposit into multiple vaults | `operations/batch-deposit.md` | Yes — `msg.value = sum(assets)` |
| Redeem from multiple vaults | `operations/batch-redeem.md` | No — `value = 0` |
| Delegate deposit/redemption (receiver ≠ sender) | `operations/approve.md` | No — `value = 0` |

For on-chain reads (costs, existence, vault state, previews), follow `reference/reading-state.md`.
For discovery reads (search, browse, traverse the knowledge graph), follow `reference/graphql-queries.md`.
For multi-step flows (create + deposit, signal disagreement, exit position), follow `reference/workflows.md`.
Always simulate writes before executing — see `reference/simulation.md`.

## Protocol Invariants

These facts govern all Intuition transactions. Reference them when encoding operations.

1. **Term IDs are bytes32** -- All vault, atom, and triple IDs are `bytes32` — deterministic hashes computed from atom data or triple components.

2. **Creation is batch-only** -- Use `createAtoms()` and `createTriples()` with arrays. Single-item creation uses single-element arrays.

3. **curveId is required** -- `deposit` and `redeem` require a `curveId` parameter. Query `getBondingCurveConfig()` once per session. The mainnet default is `1` (linear curve).

4. **Slippage parameters** -- `deposit` accepts `minShares`, `redeem` accepts `minAssets`; `depositBatch` and `redeemBatch` take per-item `minShares[]` / `minAssets[]`. Derive bounds from `previewDeposit`/`previewRedeem` with a tolerance before executing — see the Slippage Protection section in each `operations/` doc. Zero bounds are debug-only and should not ship to production callers.

5. **Receiver semantics are explicit** -- `deposit`/`redeem` operations require a non-zero receiver address. When receiver is omitted in intent, use the signer address.

6. **Atom data is hex-encoded bytes** -- Use `stringToHex(uri)` in viem, `cast --from-utf8 "uri"` in foundry. The input is an IPFS URI from pinning (`ipfs://bafy...`) or a CAIP-10 URI for blockchain addresses (`caip10:eip155:{chainId}:{address}`).

7. **msg.value is a separate transaction field** -- The $TRUST sent with the transaction is the `value` field, separate from the encoded `data`.

8. **Payable functions** -- `createAtoms`, `createTriples`, `deposit`, `depositBatch` require $TRUST as `msg.value`. `redeem` and `redeemBatch` are non-payable (`value = 0`).

9. **Creation assets[] is the full payment** -- Each `assets[i]` must be >= creation cost. `msg.value` must exactly equal `sum(assets[])`. The creation cost is deducted per item; the remainder deposits into the vault.

10. **Custom chain definition required** -- Intuition L3 (chain 1155/13579) requires `defineChain()` in viem. See `reference/network-config.md`.

11. **Creation returns bytes32[]** -- `createAtoms` and `createTriples` return `bytes32[]` — deterministic hashes of the input data. The caller already computed each expected ID pre-broadcast via `calculateAtomId(data)` / `calculateTripleId(s, p, o)`; post-broadcast verification reconstructs the `bytes32[]` from those values rather than parsing logs. See `reference/post-write-verification.md`.

12. **Counter-triples are automatic** -- Creating a triple also creates its counter-triple vault. Deposit into the counter-triple to signal disagreement.

13. **Separate preview functions for creation and deposit** -- Use `previewAtomCreate`/`previewTripleCreate` when creating. Use `previewDeposit` for existing vaults. Fee calculations differ.

## Error Patterns

| Error | Cause | Fix |
|-------|-------|-----|
| `MultiVault_InsufficientBalance` | `msg.value` does not equal `sum(assets[])` | Ensure `msg.value` exactly equals the sum of the assets array |
| `MultiVault_InsufficientAssets` | `assets[i]` less than creation cost | Each `assets[i]` must be >= `getAtomCost()` or `getTripleCost()` |
| `MultiVault_AtomExists` | Atom with same data already created | Check `isTermCreated(calculateAtomId(data))` first; use existing ID |
| `MultiVault_TripleExists` | Triple with same components already created | Check `isTermCreated(calculateTripleId(...))` first; use existing ID |
| `MultiVault_TermDoesNotExist` / `MultiVaultCore_TermDoesNotExist` | Referenced term does not exist, or a classifier read was run against an unknown ID | Create the missing atom via `createAtoms`, choose an existing triple `term_id`, or re-check the GraphQL-to-on-chain binding before composing |
| `MultiVault_ArraysNotSameLength` | Parallel arrays have different lengths | Ensure all arrays match in length |
| `MultiVault_InvalidArrayLength` | Empty array or exceeds max batch size | Provide at least one item; check max batch size |
| Transaction reverts with no message | ABI encoding mismatch or unrecognized function sig | Verify bytes32 IDs, check curveId parameter |

## TRUST Token

| | Mainnet | Testnet |
|---|---|---|
| Symbol | $TRUST | tTRUST |
| Decimals | 18 | 18 |

`parseEther('0.5')` works for formatting TRUST amounts (same 18-decimal math). The unit is TRUST, not ETH.

## Contract Source

- **V2 contracts:** https://github.com/0xIntuition/intuition-v2/tree/main/contracts/core
- **Interface:** `src/interfaces/IMultiVault.sol` and `src/interfaces/IMultiVaultCore.sol`
- **Block explorer (mainnet):** https://intuition.calderaexplorer.xyz
- **SDK (reference):** https://github.com/0xIntuition/intuition-ts
