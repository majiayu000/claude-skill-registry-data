---
name: pokemon-card-prices
description: Look up Pokemon Trading Card Game prices from the TCGCSV API. Use this when users ask about card prices, market values, or availability for specific Pokemon cards in English sets. Supports flexible card name matching, rarity abbreviations (IR, SIR, etc.), and "did you mean?" suggestions for misspelled set or card names. Returns current market price, listing prices, and card details without loading entire CSV files into context.
license: MIT
---

# Pokemon Card Prices

## Execution Instructions

To use this skill, execute the main script with the set name followed by the card name:

```bash
node scripts/main.js <set-name> <card-name>
```

Examples:

- `node scripts/main.js "Obsidian Flames" "Charizard"`
- `node scripts/main.js "Scarlet Violet 151" "Charizard EX SIR"`
- `node scripts/main.js "Base Set" "Pikachu"`

## Overview

This skill enables you to look up current market prices and availability for Pokemon Trading Cards using the TCGCSV API, which aggregates data from TCGPlayer. The skill handles flexible card name matching, supports rarity abbreviations, and provides intelligent suggestions for misspellings.

## Quick Examples

**Look up a card's price:**

> "What's the current price for a Charizard EX Ultra Rare from Obsidian Flames?"

**Find all rarities of a card:**

> "Show me prices for all Pikachu cards in Base Set"

**Get set release information:**

> "When was Scarlet & Violet released?"

**Handle misspelled names:**

> "What's the price for Pikachu SIR from Scarlet Voilet?"
> (Skill suggests: "Did you mean 'Scarlet & Violet'?")

## How It Works

The skill uses a two-step process to fetch card pricing data:

1. **Fetch groups endpoint** (`fetch-groups.js`): Retrieves all available sets and performs flexible matching to find the requested set. If not found exactly, suggests similar set names.

2. **Fetch ProductsAndPrices CSV** (`fetch-card-prices.js`): Once the set is located, fetches the CSV file for that set and filters for the requested card. Only the matching card data is returned, not the entire file (which can be hundreds of KB).

## Features

- **Flexible Card Name Matching**: Uses fuzzy string matching to find cards even with minor typos
- **Rarity Support**: Automatically normalizes rarity abbreviations (IR→Illustration Rare, SIR→Special Illustration Rare, etc.)
- **Multiple Rarities**: When a card has multiple rarity versions, returns all of them
- **Helpful Suggestions**: Provides "did you mean?" suggestions for misspelled set or card names
- **Efficient Data Transfer**: Processes large CSV files server-side, only returning relevant filtered results

## Supported Information

Each card result includes:

- **Card Name** - Full product name
- **Rarity** - Rarity designation (Common through Ultra Rare variants)
- **Market Price** - Current market price
- **Lowest Price** - Lowest available price
- **Average / Median Price** - Average of current listings
- **TCGPlayer Link** - Direct link to the card on TCGPlayer for purchasing

### Sample Output

When you look up a card, you'll receive results in this format:

| Card                   | Rarity                    | Market Price | Lowest  | Average | TCGPlayer                                        |
| ---------------------- | ------------------------- | ------------ | ------- | ------- | ------------------------------------------------ |
| Charizard ex - 183/165 | Ultra Rare                | $23.41       | $18.00  | $26.10  | [Link](https://www.tcgplayer.com/product/517017) |
| Charizard ex - 199/165 | Special Illustration Rare | $251.97      | $193.40 | $254.41 | [Link](https://www.tcgplayer.com/product/517045) |

Every card result includes a clickable TCGPlayer link for easy access to purchase options and additional details.

## Rarity Abbreviations

The skill recognizes these common rarity abbreviations:

- `IR` → Illustration Rare
- `SIR` → Special Illustration Rare
- `DR` → Double Rare
- `UR` → Ultra Rare
- `HR` → Hyper Rare

See `references/rarity-mappings.md` for complete rarity reference.

## API Reference

See `references/api-docs.md` for details on:

- Groups endpoint structure (set browsing)
- ProductsAndPrices CSV format
- Available data fields

## Scripts

- `scripts/fetch-groups.js` - Fetches and searches through available sets with fuzzy matching
- `scripts/fetch-card-prices.js` - Fetches and filters ProductsAndPrices CSV for specific cards
- `scripts/main.js` - Orchestrates the above scripts
