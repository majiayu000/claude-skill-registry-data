---
name: coinlore-crypto
description: Access real-time cryptocurrency market data including prices, market cap, and global stats via CoinLore API. Use when the user asks for crypto prices, market rankings, or global crypto stats. No API key required.
---

# CoinLore Crypto Market Data Skill


This skill provides real-time cryptocurrency market data using the free and public CoinLore API.

## Features
- Fetch specific coin data by ID.
- Search for top coins by symbol (BTC, ETH, etc.).
- Get global cryptocurrency market statistics.

## Usage

### Get coin by ID
```bash
python3 scripts/crypto.py get [ID]
```
Example: `python3 scripts/crypto.py get 90` (for Bitcoin)

### Search coin by Symbol
```bash
python3 scripts/crypto.py search [SYMBOL]
```
Example: `python3 scripts/crypto.py search ETH`

### Get Global Market Stats
```bash
python3 scripts/crypto.py global
```

## API Information
- Source: [CoinLore API](https://www.coinlore.com/cryptocurrency-data-api)
- Auth: No API Key required.
- Limitations: Free to use.
