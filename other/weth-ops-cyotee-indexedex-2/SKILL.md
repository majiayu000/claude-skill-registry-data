---
name: weth-ops
description: "Inspect WETH balances and prepare authorized native-token wrap or unwrap operations on the verified target chain."
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

# WETH ops (cast)

## Goal
Convert native ETH <-> WETH9.

## Prerequisites
WETH address from the current task-selected deployment/registry; see [token reference](../erc20-ops/references/common-tokens.md) for historical context only.

## Safety
Confirm chain and WETH address. Confirm value before deposit.

## Inspect
```bash
cast call $WETH "balanceOf(address)(uint256)" $USER --rpc-url $ETH_RPC_URL
cast balance $USER --rpc-url $ETH_RPC_URL -e
```

## Execute
```bash
cast send $WETH "deposit()" --value 0.01ether \
  --rpc-url $ETH_RPC_URL --private-key $PRIVATE_KEY

AMOUNT=$(cast to-wei 0.01 ether)
cast send $WETH "withdraw(uint256)" $AMOUNT \
  --rpc-url $ETH_RPC_URL --private-key $PRIVATE_KEY
```

## Verify
```bash
cast call $WETH "balanceOf(address)(uint256)" $USER --rpc-url $ETH_RPC_URL
cast balance $USER --rpc-url $ETH_RPC_URL -e
```

## Common failures
- Wrong WETH address on L2
- Insufficient ETH for gas + value
