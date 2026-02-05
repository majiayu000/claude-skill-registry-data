---
name: wallet-send-bsv
description: Send BSV transactions using @bsv/sdk. Build, sign, and broadcast transactions to the BSV blockchain.
allowed-tools: "Bash(bun:*)"
---

# Wallet Send BSV

Send BSV transactions using @bsv/sdk.

## When to Use

- Send BSV to an address
- Create payment transactions
- Build custom transactions
- Broadcast signed transactions

## Usage

```bash
# Send BSV from WIF private key
bun run /path/to/skills/wallet-send-bsv/scripts/send.ts <from-wif> <to-address> <amount-satoshis>

# Example: Send 0.001 BSV (100,000 satoshis)
bun run /path/to/skills/wallet-send-bsv/scripts/send.ts L1abc... 1A2b3c4d5e... 100000
```

## Requirements

- `@bsv/sdk` package installed
- Private key in WIF format
- Sufficient balance to cover amount + fees

## Transaction Flow

1. Parse private key (WIF)
2. Fetch UTXOs from address
3. Build transaction with inputs/outputs
4. Sign transaction
5. Broadcast to BSV network

## Network

Broadcasts to BSV mainnet via WhatsOnChain API.
