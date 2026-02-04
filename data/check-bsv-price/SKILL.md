---
name: check-bsv-price
description: Get current BSV price and exchange rate information from WhatsOnChain API. Returns USD price, market cap, and price changes.
allowed-tools: "Bash(bun:*)"
---

# Check BSV Price

Get current BSV price from WhatsOnChain API.

## When to Use

- Check current BSV/USD exchange rate
- Calculate transaction values in USD
- Monitor BSV price movements
- Display market information

## Usage

```bash
bun run /path/to/skills/check-bsv-price/scripts/price.ts
```

## API Endpoint

WhatsOnChain Exchange Rate API:
- `GET https://api.whatsonchain.com/v1/bsv/main/exchangerate`

## Response

Returns current price information including:
- Rate (USD)
- Currency
- Timestamp

## No Authentication Required

WhatsOnChain API is public and doesn't require API keys for basic queries.
