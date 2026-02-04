---
name: create-purchase-invoice
description: Create purchase invoice in NexERP database
---

# Create Purchase Invoice Skill

Creates a purchase invoice (PI) record in the NexERP system. A purchase invoice represents goods/services received from a supplier with payment obligations.

## Usage

```bash
python main.py \
  --supplier-name "ACTION BOLT" \
  --invoice-date "2025-10-26" \
  --items '[{"product_name": "WIRE D1.2", "quantity": 25, "unit_price": 10.50}]' \
  --json
```

## Required Fields

- `--supplier-name`: Supplier name (fuzzy match supported)
- `--invoice-date`: Invoice date (YYYY-MM-DD format)
- `--items`: JSON array of line items

### Item Fields

Each item must have:
- `product_name`: Product name or SKU (fuzzy match supported)
- `quantity`: Quantity ordered (positive number)
- `unit_price`: Price per unit

Optional item fields:
- `discount`: Line discount percentage (0-100)
- `remark`: Line item remark/notes

## Optional Invoice Fields

- `--supplier-ref`: Supplier's invoice reference number
- `--tax-rate`: Tax rate as decimal (default: 0.08 for 8% SST)
- `--remark`: Invoice remark/notes

## Output

Returns JSON with invoice details:

```json
{
  "success": true,
  "invoice_number": "PI25100047",
  "txn_id": 2185,
  "supplier": "ACTION BOLT & NUTS SDN BHD",
  "invoice_date": "2025-10-26",
  "items_count": 1,
  "subtotal": 262.50,
  "tax": 21.00,
  "grand_total": 283.50
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
1. `tbl_pinvoice_txn` - Invoice header
2. `tbl_pinvoice_item` - Line items
3. `tbl_pinvoice_movement` - Stock movement audit

## Document Number Format

Invoice numbers follow pattern: `PI{YY}{MM}{NNNN}`
- Example: `PI25100047` = October 2025, invoice #47

## Business Rules

- Supplier must exist and be active (Status_i = 1)
- Products must exist in tbl_product_code
- Invoice date must be valid date format
- Quantities must be positive
- Amounts rounded to 2 decimal places
- Default tax rate: 8% (Malaysian SST)
- Automatic calculation: SubTotal + Tax = GrandTotal

## Integration

This skill is called by the Database Agent after the Document Agent extracts data from uploaded purchase invoice images.

## Examples

### Single Item Invoice

```bash
python main.py \
  --supplier-name "ACTION" \
  --invoice-date "2025-10-26" \
  --items '[{"product_name": "WIRE D1.2-L105.8", "quantity": 25, "unit_price": 10.50}]' \
  --json
```

### Multi-Item Invoice

```bash
python main.py \
  --supplier-name "NINGBO" \
  --invoice-date "2025-10-26" \
  --supplier-ref "INV-2025-ABC" \
  --items '[
    {"product_name": "WIRE D1.2", "quantity": 100, "unit_price": 5.00},
    {"product_name": "BOLT M10", "quantity": 500, "unit_price": 0.50, "discount": 10}
  ]' \
  --remark "Urgent delivery" \
  --json
```

### With Custom Tax Rate

```bash
python main.py \
  --supplier-name "Dell" \
  --invoice-date "2025-10-26" \
  --items '[{"product_name": "Laptop", "quantity": 1, "unit_price": 3500.00}]' \
  --tax-rate 0.06 \
  --json
```

## Testing

```bash
# Test with verbose output
python main.py --supplier-name "ACTION" --invoice-date "2025-10-26" \
  --items '[{"product_name": "WIRE", "quantity": 10, "unit_price": 5.00}]' \
  --verbose --json

# Test error handling (invalid supplier)
python main.py --supplier-name "XYZ_NONEXISTENT" --invoice-date "2025-10-26" \
  --items '[{"product_name": "WIRE", "quantity": 10, "unit_price": 5.00}]' \
  --json
```

## Exit Codes

- `0`: Success
- `1`: Error (invalid input, database error)
- `2`: Not found (supplier/product not found)
