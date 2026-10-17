---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: ebay
repo: remorses/ebay-cli
description: |
  `ebay` CLI and TypeScript SDK to search eBay and read listings through the user's logged-in Chrome
  (playwriter extension, fetch only, no clicks). `ebay search` filters by price, condition, auction or
  buy it now, sold listings, location, seller and item specifics. `ebay item` reads price, shipping,
  specifics, description and seller stats. `ebay seller` reads feedback and negative reviews. ALWAYS
  load this skill when the user wants to find something to buy on eBay, compare eBay prices, check what
  an item sold for, read an eBay listing URL, or check if an eBay seller is trustworthy.
---

# ebay

Every time you use this skill, read both in full. Never pipe them to `head`, `tail` or `sed`:

```bash
ebay --help
curl -s https://raw.githubusercontent.com/remorses/ebay-cli/main/README.md
```

The README ends with an **Agent notes** section (shopping workflow and gotchas). Follow it.

If `ebay` is not on PATH, install it from the README Setup section.
