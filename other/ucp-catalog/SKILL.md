---
name: ucp-catalog
description: >
  Maps merchant product data from Shopify products.json, CSV, or existing JSON
  into the repo's UCP-style catalog JSON. Use after ucp-audit when product data
  needs to be normalized before UCP checkout work or OpenAI ACP feed export.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# UCP Catalog Mapper

Normalize merchant product data into `catalog.json`.

## Inputs

- Shopify public `products.json`: `--source shopify --url https://store.com`
- CSV export: `--source csv --file products.csv`
- Existing JSON: `--source json --file products.json`

The script currently does not implement authenticated WooCommerce, BigCommerce,
or browser scraping adapters. Treat those as future connectors unless code is
added in this repo.

## Run

```bash
python ${CLAUDE_SKILL_DIR}/scripts/map_catalog.py \
  --source shopify \
  --url https://example.com \
  --currency USD \
  --output store/clients/example/catalog.json
```

## Output Contract

Write:

- `catalog.json`
- `mapping-report.md` when `--report` is provided

`catalog.json` contains:

- `products[]`
- `metadata.source`
- `metadata.total_products`
- `metadata.total_variants`
- `metadata.currency`
- `metadata.validation_errors`

Product records should include stable `id`, `title`, `description`,
`price_range`, and at least one `variant`. Variant prices are integers in ISO
4217 minor units.

## Hard Rules

- Never fabricate title, price, availability, SKU, or image data.
- Convert prices to minor units: USD 29.99 becomes `2999`; JPY has no decimal
  multiplier.
- If validation reports errors, keep the output but clearly report the problem
  before using it downstream.

## Downstream

- `ucp-checkout` can use `catalog.json` as local product data.
- `acp-feed` can export `catalog.json` to OpenAI ACP feed JSON.
