---
name: extract-blockchain-media
description: Extract media files (images, videos, documents) from BSV blockchain transactions using the txex CLI tool. Retrieves inscribed ordinals and embedded files.
allowed-tools: "Bash(bun:*)"
---

# Extract Blockchain Media

Extract media files from BSV blockchain transactions using `txex` CLI.

## When to Use

- Extract ordinal inscriptions from transactions
- Retrieve embedded images/videos/files from blockchain
- Download NFT assets
- Access on-chain stored media

## Usage

```bash
# Extract media from transaction ID
bun run /path/to/skills/extract-blockchain-media/scripts/extract.ts <txid>

# Extract to specific output directory
bun run /path/to/skills/extract-blockchain-media/scripts/extract.ts <txid> /path/to/output
```

## What Gets Extracted

The txex tool extracts:
- Images (PNG, JPG, GIF, WEBP)
- Videos (MP4, WEBM)
- Audio files
- Text/JSON data
- Any binary data inscribed in transaction

## Output

Files are saved with:
- Original filename (if embedded in tx)
- Auto-detected file extension
- Saved to current directory or specified path

## Requirements

- `txex` CLI installed: `bun add -g txex`
- Transaction ID of ordinal/inscription
- Internet connection to fetch from blockchain

## CLI Reference

```bash
txex <txid>                 # Extract to current directory
txex <txid> -o /path        # Extract to specific path
```

## Common Use Cases

1. **View NFT Images**: Extract ordinal inscription image
2. **Download Files**: Retrieve documents stored on-chain
3. **Archive Media**: Backup ordinals locally
4. **Content Verification**: Check what's actually inscribed
