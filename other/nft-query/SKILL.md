---
name: nft-query
description: Query NFT token information, ownership, metadata, and collection stats
activation_keywords: [nft, erc721, erc1155, nft owner, nft metadata, collection, token uri, nft balance]
execution_mode: client
---

# NFT Query Skill

Provides NFT data querying capabilities:
- Get NFT owner by contract and token ID
- Get NFT metadata and token URI
- Get NFT balance for an address
- Get collection info (name, symbol, total supply)
- List tokens owned by an address (for supported contracts)
- Decode NFT metadata from URI

Use `builtin_nft_query` tool with fields:
- `operation`: one of "owner", "metadata", "balance", "collection_info", "tokens_of_owner"
- `contract_address`: NFT contract address
- `token_id`: (optional) specific token ID
- `owner_address`: (optional) wallet address for balance/token listing
- `network`: (optional) Ethereum network: "mainnet", "sepolia", "holesky" (default: "mainnet")

Note: All operations are read-only. Supports ERC721 and ERC1155 standards.
