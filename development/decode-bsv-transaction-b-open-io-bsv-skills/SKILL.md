---
name: decode-bsv-transaction
description: Decode BSV transaction hex into human-readable format using WhatsOnChain API. Shows inputs, outputs, scripts, and transaction details.
allowed-tools: "Bash(bun:*)"
---

# Decode BSV Transaction

Decode BSV transaction hex using WhatsOnChain API.

## When to Use

- Decode raw transaction hex
- Analyze transaction structure
- View inputs and outputs
- Inspect scripts and signatures

## Usage

```bash
# Decode transaction by hex
bun run /path/to/skills/decode-bsv-transaction/scripts/decode.ts <tx-hex>

# Decode transaction by txid (fetches from chain)
bun run /path/to/skills/decode-bsv-transaction/scripts/decode.ts <txid>
```

## API Endpoints

WhatsOnChain Transaction API:
- Decode: `POST https://api.whatsonchain.com/v1/bsv/main/tx/decode`
- Get TX: `GET https://api.whatsonchain.com/v1/bsv/main/tx/hash/{txid}`

## Response

Returns decoded transaction with:
- Version, locktime
- Inputs (previous outputs, scripts, signatures)
- Outputs (value, addresses, scripts)
- Transaction size and fees
