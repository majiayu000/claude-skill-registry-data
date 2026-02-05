---
name: ordinals-marketplace
description: Browse and search 1Sat Ordinals marketplace on GorillaPool. View listings, search inscriptions, check sales, and find NFTs.
allowed-tools: "Bash(bun:*)"
---

# Ordinals Marketplace

Browse and search 1Sat Ordinals marketplace.

## When to Use

- Search for ordinals/NFTs
- View marketplace listings
- Check recent sales
- Find specific inscriptions
- Browse collections

## Features

**Search Inscriptions**: Find ordinals by:
- Inscription ID
- Collection name
- Content type (image, text, etc.)
- Price range

**View Listings**: Browse:
- Active sales listings
- Recently listed
- Price sorted

**Sales History**: Check:
- Recent sales
- Price trends
- Volume statistics

## Usage

```bash
# Search inscriptions
bun run /path/to/skills/ordinals-marketplace/scripts/search.ts "query"

# View active listings
bun run /path/to/skills/ordinals-marketplace/scripts/listings.ts

# Recent sales
bun run /path/to/skills/ordinals-marketplace/scripts/sales.ts
```

## API Endpoints

GorillaPool Ordinals API:
- Search: `GET https://ordinals.gorillapool.io/api/inscriptions/search`
- Listings: `GET https://ordinals.gorillapool.io/api/market/listings`
- Sales: `GET https://ordinals.gorillapool.io/api/market/sales`

## Response Data

Returns:
- Inscription IDs
- Content type and size
- Current listings and prices
- Sales history
- Collection information
