---
name: approval-ops
description: "Inspect ERC20 allowances and prepare authorized approvals with Cast for IndexedEx router, vault and Permit2 flows."
---

## IndexedEx integration (2026-10-19)

Read the repository `CLAUDE.md` and the relevant Crane/IndexedEx skill before
using this topic. Current product law, registry/CREATE3 deployment, production-first
tests, build-before-test ordering and configured Foundry profiles override generic
examples. This archive-derived guide does not authorize broadcasts, dependency
installs, new product integrations or restoration of retired protocol families.
Use current deployment artifacts and the pinned frontend/tool versions; archived
addresses and API samples are not live verification. Resolve topic names through
`scripts/codex-skill-catalog.json` when they are grouped behind routers.

# ERC20 approval ops (cast)

## Goal

Set or clear ERC20 allowances for a spender (router, vault, Permit2) safely.

## Prerequisites

- Token + spender addresses from address tables
- `foundry-agent-safety` before writes
- `WALLET_ADDRESS` = agent wallet

```bash
export TOKEN=0x...
export SPENDER=0x...
export WALLET_ADDRESS=$(cast wallet address --private-key $PRIVATE_KEY)
```

## Inspect

```bash
cast call $TOKEN "allowance(address,address)(uint256)" $USER $SPENDER --rpc-url $ETH_RPC_URL
cast call $TOKEN "balanceOf(address)(uint256)" $USER --rpc-url $ETH_RPC_URL
cast call $TOKEN "decimals()(uint8)" --rpc-url $ETH_RPC_URL
```

## Dry-run

Reads only. Plan amount: prefer exact amount over max `type(uint256).max` when possible.

## Execute — standard approve

```bash
cast send $TOKEN "approve(address,uint256)" $SPENDER $AMOUNT \
  --rpc-url $ETH_RPC_URL --private-key $PRIVATE_KEY
```

## Execute — USDT-like reset (non-zero → non-zero may revert)

```bash
# 1) reset
cast send $TOKEN "approve(address,uint256)" $SPENDER 0 \
  --rpc-url $ETH_RPC_URL --private-key $PRIVATE_KEY
# 2) set new amount
cast send $TOKEN "approve(address,uint256)" $SPENDER $AMOUNT \
  --rpc-url $ETH_RPC_URL --private-key $PRIVATE_KEY
```

## Verify

```bash
cast call $TOKEN "allowance(address,address)(uint256)" $USER $SPENDER --rpc-url $ETH_RPC_URL
cast receipt $TX --rpc-url $ETH_RPC_URL
```

## Common failures

- USDT-style tokens require zero-first
- Wrong spender (Vault vs Router vs Permit2)
- Amount units ignore decimals

## Related

- `erc20-ops`, `permit2-allowance-cast` (when spender pulls via Permit2)
