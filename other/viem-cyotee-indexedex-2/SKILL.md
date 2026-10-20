---
name: viem
description: "Use Viem clients, typed contracts, receipts, events and transaction simulation in the IndexedEx frontend. Verify the locked version."
---

# Viem for IndexedEx

## IndexedEx integration (2026-10-19)

Read the repository `CLAUDE.md` and the relevant Crane/IndexedEx skill before
using this topic. Current product law, registry/CREATE3 deployment, production-first
tests, build-before-test ordering and configured Foundry profiles override generic
examples. This archive-derived guide does not authorize broadcasts, dependency
installs, new product integrations or restoration of retired protocol families.
Use current deployment artifacts and the pinned frontend/tool versions; archived
addresses and API samples are not live verification. Resolve topic names through
`scripts/codex-skill-catalog.json` when they are grouped behind routers.

## Procedure

1. Inspect `frontend/apps/indexedex/package.json`, the workspace lockfile and existing client/chain factories. The archived reference claims Viem 2.47.6; the current manifest range is `^2.43.5`, not proof of an exact resolved version.
2. Reuse the project Wagmi/Viem providers and ABI artifacts. Read-only operations use a public client; signing uses the task-authorized wallet/account.
3. Derive addresses from the current deployment/registry and verify the chain. Preserve bigint token amounts and actual token decimals; nonce uses the library's number type.
4. Simulate a contract write with the actual ABI/account before an authorized write; inspect its receipt and resulting state. Simulation is not permission to broadcast.
5. Use either legacy `gasPrice` or EIP-1559 fee fields, not both. Keep public Anvil test keys confined to isolated local fixtures.
6. Subscribe to events before triggering test actions; use bounded observable-state assertions and dispose subscriptions. Follow `indexedex-ui-tx-testing` for money paths.
7. Verify the locked version's types/docs before using an archived API; do not upgrade dependencies to make a snippet work.

## Read by task

| Need | Reference section |
| --- | --- |
| Client and account setup | [Quick start](references/viem-v2.47.6.md#quick-start) |
| Reads, fees, receipts and events | [Public actions](references/viem-v2.47.6.md#public-actions) |
| Wallet operations and signing | [Wallet actions](references/viem-v2.47.6.md#wallet-actions) |
| Typed ABI reads/writes/simulation | [Contract actions](references/viem-v2.47.6.md#contract-actions) |
| Authorization flows | [EIP-7702](references/viem-v2.47.6.md#eip-7702-actions) |
| Encoding and conversions | [ABI utilities](references/viem-v2.47.6.md#abi-utilities), [utilities](references/viem-v2.47.6.md#utilities) |

The complete collected API body is retained on demand. Its sample addresses and
placeholder parameters are illustrative, not ready-to-broadcast transactions.
IndexedEx contract tests remain production-first; state overrides/connector stubs
do not substitute for required real contract or wallet transaction coverage.

Official API reference: https://viem.sh/docs/actions/wallet/sendTransaction
