---
name: currency-converter
description: Convert between fiat and cryptocurrencies using daily updated exchange rates from the currency-api. Use when the user needs currency conversion or current exchange rates. No API key required.
---

# Currency Converter Skill


Use this skill to convert between different currencies and cryptocurrencies using the free and open `fawazahmed0/currency-api`.

## Usage

Run the conversion script:

```bash
python3 scripts/convert.py --base [BASE] --target [TARGET] --amount [AMOUNT]
```

- `--base`: The source currency code (e.g., `twd`, `usd`, `jpy`). Defaults to `twd`.
- `--target`: The destination currency code (e.g., `usd`, `btc`, `eth`).
- `--amount`: The amount to convert. Defaults to `1.0`.
- `--list`: List all supported currency codes.

## Endpoints used:
- Primary: `https://latest.currency-api.pages.dev/v1/currencies/{base}.json`
- Fallback: `https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{base}.json`

## Notes
- This API has no API key requirement and no rate limits.
- Updates daily.
