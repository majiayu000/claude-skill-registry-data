---
name: evo-reference-data-loader
description: Loads and normalizes vendor master data from Excel and purchase order data from CSV into Python dictionaries for lookup operations.
---

# evo-reference-data-loader

Loads reference data for fraud detection.

## Key Functions

- `load_vendor_database(excel_path)` - Returns {vendor_id: {"name": name, "iban": iban}}
- `load_po_database(csv_path)` - Returns {po_number: {"vendor_id": vid, "amount": float}}

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-reference-data-loader/scripts')
from utils import load_vendor_database, load_po_database

vendors = load_vendor_database('/root/vendors.xlsx')
pos = load_po_database('/root/purchase_orders.csv')
```
