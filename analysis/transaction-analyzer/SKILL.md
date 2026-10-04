---
name: transaction-analyzer
description: Analyze Ethereum transactions including details, status, gas usage, and internal transfers
activation_keywords: [transaction, tx, txhash, transaction hash, receipt, status, gas used, internal transaction, token transfer]
execution_mode: server
---

# Transaction Analyzer Skill

Provides comprehensive Ethereum transaction analysis:
- Get transaction details (from, to, value, gas, input data)
- Get transaction receipt and status
- Analyze gas usage (gas used vs gas limit)
- Calculate actual transaction cost
- Get internal transactions/transfers
- Decode token transfer events (ERC20, ERC721)
- Get transaction confirmation time

Use `builtin_transaction_analyzer` tool with fields:
- `operation`: one of "details", "receipt", "gas_analysis", "cost", "token_transfers", "internal_txs"
- `tx_hash`: transaction hash to analyze
- `network`: (optional) Ethereum network: "mainnet", "sepolia", "holesky" (default: "mainnet")

Note: All operations are read-only analysis. No transaction modification is possible.
