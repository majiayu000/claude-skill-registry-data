---
name: smart-contract
description: Read smart contract state and call view/pure contract methods
activation_keywords: [smart contract, contract, abi, erc20, erc721, erc1155, token, tokenbalance, allowance, total supply]
execution_mode: server
---

# Smart Contract Skill

Provides read-only smart contract interaction capabilities:
- Read ERC20 token info (name, symbol, decimals, total supply)
- Check ERC20 token balance for an address
- Check ERC20 allowance for spender
- Read contract storage slots
- Decode contract events/logs
- Get contract code

Use `builtin_smart_contract` tool with fields:
- `operation`: one of "erc20_info", "erc20_balance", "erc20_allowance", "erc721_owner", "erc721_metadata", "code", "storage"
- `contract_address`: Ethereum contract address
- `address`: (optional) wallet address for balance/allowance queries
- `spender`: (optional) spender address for allowance query
- `token_id`: (optional) NFT token ID for ERC721 queries
- `network`: (optional) Ethereum network: "mainnet", "sepolia", "holesky" (default: "mainnet")

Note: Only read-only (view/pure) contract calls are supported. No state-changing transactions.
