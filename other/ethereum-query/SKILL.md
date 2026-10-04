---
name: ethereum-query
description: Query Ethereum blockchain data including blocks, transactions, addresses, and gas prices
activation_keywords: [ethereum, eth, block, blockheight, blocknumber, address, balance, gas, gasprice, nonce, chainid]
execution_mode: server
---

# Ethereum Query Skill

Provides read-only Ethereum blockchain data querying capabilities:
- Get latest block number and block details
- Query address balance (ETH)
- Get transaction details by hash
- Check current gas prices
- Get nonce for an address
- Get chain ID and network info

Use `builtin_ethereum_query` tool with fields:
- `operation`: one of "block_number", "block", "balance", "transaction", "gas_price", "nonce", "chain_id"
- `block_number`: (optional) specific block number for block query
- `address`: (optional) Ethereum address for balance/nonce queries
- `tx_hash`: (optional) transaction hash for transaction query
- `network`: (optional) Ethereum network: "mainnet", "sepolia", "holesky" (default: "mainnet")

Note: All operations are read-only. No transaction signing or sending is supported.
