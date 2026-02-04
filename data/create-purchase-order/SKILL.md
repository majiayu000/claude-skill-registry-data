---
name: create-purchase-order
description: Create purchase order (PO) in NexERP database
---

# Create Purchase Order Skill

Creates a purchase order (PO) record in the NexERP system. A purchase order represents goods/services to be ordered from a supplier.

## Usage

```bash
python main.py \
  --supplier-name "ACTION BOLT" \
  --order-date "2025-10-26" \
  --items '[{"product_name": "WIRE D1.2", "quantity": 100, "unit_price": 10.50}]' \
  --json
```

## Required Fields

- `--supplier-name`: Supplier name (fuzzy match supported)
- `--order-date`: Order date (YYYY-MM-DD format)
- `--items`: JSON array of line items

### Item Fields

Each item must have:
- `product_name`: Product name or SKU (fuzzy match supported)
- `quantity`: Quantity to order (positive number)
- `unit_price`: Price per unit

Optional item fields:
- `discount`: Line discount percentage (0-100)
- `remark`: Line item remark/notes

## Optional PO Fields

- `--supplier-ref`: Supplier's reference number
- `--expiry-date`: PO expiry date (YYYY-MM-DD)
- `--tax-rate`: Tax rate as decimal (default: 0.06 for 6% tax)
- `--remark`: PO remark/notes

## Output

Returns JSON with PO details:

```json
{
  "success": true,
  "po_number": "PO25100036",
  "txn_id": 2126,
  "supplier": "ACTION BOLT & NUTS SDN BHD",
  "order_date": "2025-10-26",
  "items_count": 1,
  "subtotal": 1050.00,
  "tax": 63.00,
  "grand_total": 1113.00,
  "status": "Pending"
}
```

## Error Handling

Returns error JSON if:
- Supplier not found (suggests alternatives)
- Product not found for any item
- Invalid date format
- Invalid amounts or quantities
- Database connection fails

## Database Tables

Writes to 3 tables:
1. `tbl_porder_txn` - PO header
2. `tbl_porder_item` - Line items
3. `tbl_porder_movement` - Stock movement tracking

## Document Number Format

PO numbers follow pattern: `PO{YY}{MM}{NNNN}`
- Example: `PO25100036` = October 2025, PO #36

## Business Rules

- Supplier must exist and be active (Status_i = 1)
- Products must exist in tbl_product_code
- Order date must be valid date format
- Quantities must be positive
- Amounts rounded to 2 decimal places
- Default tax rate: 6% (for purchase orders)
- PO status defaults to 'P' (Pending)
- Automatic calculation: SubTotal + Tax = GrandTotal

## PO Status Values

- `P`: Pending (default)
- `A`: Approved
- `C`: Confirmed
- `R`: Received
- `X`: Cancelled

## Integration

This skill is called by the Database Agent when processing purchase order documents.

## Examples

### Single Item PO

```bash
python main.py \
  --supplier-name "ACTION" \
  --order-date "2025-10-26" \
  --items '[{"product_name": "WIRE D1.2-L105.8", "quantity": 100, "unit_price": 10.50}]' \
  --json
```

### Multi-Item PO with Expiry Date

```bash
python main.py \
  --supplier-name "NINGBO" \
  --order-date "2025-10-26" \
  --expiry-date "2025-11-26" \
  --supplier-ref "REF-2025-ABC" \
  --items '[
    {"product_name": "WIRE D1.2", "quantity": 200, "unit_price": 5.00},
    {"product_name": "BOLT M10", "quantity": 1000, "unit_price": 0.50, "discount": 15}
  ]' \
  --remark "Urgent order - deliver by Nov 15" \
  --json
```

### With Custom Tax Rate

```bash
python main.py \
  --supplier-name "Dell" \
  --order-date "2025-10-26" \
  --items '[{"product_name": "Laptop", "quantity": 5, "unit_price": 3500.00}]' \
  --tax-rate 0.08 \
  --json
```

## Testing

```bash
# Test with verbose output
python main.py --supplier-name "ACTION" --order-date "2025-10-26" \
  --items '[{"product_name": "WIRE", "quantity": 50, "unit_price": 10.00}]' \
  --verbose --json

# Test error handling (invalid supplier)
python main.py --supplier-name "XYZ_NONEXISTENT" --order-date "2025-10-26" \
  --items '[{"product_name": "WIRE", "quantity": 50, "unit_price": 10.00}]' \
  --json
```

## Exit Codes

- `0`: Success
- `1`: Error (invalid input, database error)
- `2`: Not found (supplier/product not found)
