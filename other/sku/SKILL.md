---
name: "sku"
version: "1.0.0"
description: "SKU management reference — naming conventions, hierarchy design, lifecycle management, and inventory classification. Use when designing product catalogs, creating SKU schemas, or optimizing inventory by SKU analysis."
author: "BytesAgain"
homepage: "https://bytesagain.com"
source: "https://github.com/bytesagain/ai-skills"
tags: [sku, inventory, product, catalog, retail, warehouse, logistics]
category: "logistics"
---

# SKU — SKU Management Reference

Quick-reference skill for SKU design, product hierarchy, and inventory classification.

## When to Use

- Designing SKU naming conventions for a product catalog
- Building product hierarchy (category → family → variant)
- Performing ABC/XYZ inventory analysis
- Managing SKU proliferation and rationalization
- Understanding UPC/EAN/GTIN barcode relationships

## Commands

### `intro`

```bash
scripts/script.sh intro
```

Overview of SKU concepts — definitions, purpose, and relationship to other identifiers.

### `naming`

```bash
scripts/script.sh naming
```

SKU naming conventions — best practices, encoding schemes, and anti-patterns.

### `hierarchy`

```bash
scripts/script.sh hierarchy
```

Product hierarchy design — categories, families, variants, and attributes.

### `barcodes`

```bash
scripts/script.sh barcodes
```

Barcode and identifier systems — UPC, EAN, GTIN, ISBN, ASIN, and check digits.

### `abc`

```bash
scripts/script.sh abc
```

ABC/XYZ analysis — classifying SKUs by revenue contribution and demand variability.

### `lifecycle`

```bash
scripts/script.sh lifecycle
```

SKU lifecycle management — introduction, growth, maturity, decline, and end-of-life.

### `rationalization`

```bash
scripts/script.sh rationalization
```

SKU rationalization — identifying and eliminating underperforming products.

### `metrics`

```bash
scripts/script.sh metrics
```

Key SKU metrics — inventory turns, fill rate, days of supply, and velocity.

### `help`

```bash
scripts/script.sh help
```

### `version`

```bash
scripts/script.sh version
```

## Configuration

| Variable | Description |
|----------|-------------|
| `SKU_DIR` | Data directory (default: ~/.sku/) |

---

*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*
