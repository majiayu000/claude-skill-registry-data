---
name: inventory-audit
description: Audit TinyCart inventory CSV data for duplicate SKUs, conflicting prices, and low-stock products, then write a concise Markdown report.
---

# Inventory audit

Use this skill when asked to inspect TinyCart inventory data.

1. Read `data/inventory.csv`; never modify it.
2. Run `python scripts/inventory_trace.py data/inventory.csv --verbose` so the audit is reproducible.
3. Confirm duplicate SKUs and low-stock rows directly from the CSV.
4. Write `reports/inventory-audit.md` with `Summary`, `Duplicate SKUs`, `Low stock`, and `Recommendation` sections.
5. Include exact SKUs and quantities. Do not change application code during an audit.
