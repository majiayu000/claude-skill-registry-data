---
name: wallet-create-ordinals
description: Mint new ordinals/NFTs on BSV blockchain using js-1sat-ord SDK. Inscribe images, text, or files as permanent on-chain assets.
allowed-tools: "Bash(bun:*)"
---

# Wallet Create Ordinals

Mint new ordinals/NFTs on BSV blockchain.

## When to Use

- Mint new NFT inscriptions
- Create ordinal collections
- Inscribe images on-chain
- Store files permanently on blockchain

## Usage

```bash
# Mint image ordinal
bun run /path/to/skills/wallet-create-ordinals/scripts/mint.ts <wif> <image-path>

# Mint with metadata
bun run /path/to/skills/wallet-create-ordinals/scripts/mint.ts <wif> <file-path> <metadata-json>
```

## What Gets Created

Minting creates:
- On-chain inscription of file/data
- Unique ordinal ID (txid + output index)
- Permanent, immutable storage
- Tradeable NFT asset

## Requirements

- Funded BSV wallet (WIF private key)
- File to inscribe (image, text, etc.)
- `js-1sat-ord` package for minting
- Sufficient balance for inscription cost + fees

## Cost

Inscription cost depends on file size:
- Stored on-chain permanently
- ~50 sats per byte typical
- Larger files = higher cost

## Output

Returns:
- Transaction ID
- Ordinal inscription ID
- GorillaPool marketplace URL
- Estimated confirmation time
