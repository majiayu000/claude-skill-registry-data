---
name: erc20-ops
description: "Read ERC20 metadata and balances, convert token units and prepare authorized transfers with Cast."
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

# ERC20 ops (cast)

## Goal
Inspect ERC20 metadata/balances and transfer tokens via Foundry cast.

## Prerequisites
- `cast` available (`foundry-tools`)
- `ETH_RPC_URL` or `--rpc-url`
- Token address from an address table (never invent)

## Safety
- Reads do not change chain state (RPC usage may still be metered); `transfer` requires user confirmation (see `foundry-agent-safety`).
- Never print `$PRIVATE_KEY`.

## Inspect
```bash
export TOKEN=0x...   # from address book
export WALLET_ADDRESS=0x...

cast call $TOKEN "name()(string)" --rpc-url $ETH_RPC_URL
cast call $TOKEN "symbol()(string)" --rpc-url $ETH_RPC_URL
cast call $TOKEN "decimals()(uint8)" --rpc-url $ETH_RPC_URL
cast call $TOKEN "balanceOf(address)(uint256)" $USER --rpc-url $ETH_RPC_URL
cast call $TOKEN "totalSupply()(uint256)" --rpc-url $ETH_RPC_URL
```

## Dry-run
No state change for reads. For transfers, re-check balance and recipient.

## Execute (transfer)
```bash
cast send $TOKEN "transfer(address,uint256)" $TO $AMOUNT \
  --rpc-url $ETH_RPC_URL --private-key $PRIVATE_KEY
```

## Verify
```bash
cast call $TOKEN "balanceOf(address)(uint256)" $USER --rpc-url $ETH_RPC_URL
cast call $TOKEN "balanceOf(address)(uint256)" $TO --rpc-url $ETH_RPC_URL
cast receipt $TX --rpc-url $ETH_RPC_URL
```

## Common failures
- Wrong decimals -> amount off by 1eN
- Insufficient balance
- Fee-on-transfer tokens (balance delta != amount)
