---
name: create-purchase-receipt
description: Create goods receipt (GR) record when receiving goods from supplier
---

# Create Purchase Receipt Skill

## Purpose

Creates a **Goods Receipt (GR)** record in NexERP when goods are physically received from a supplier. This is triggered by a **Delivery Order** from the supplier.

## When to Use

- Supplier truck arrives with goods
- Driver provides Delivery Order (DO)
- Warehouse receives and inspects goods
- Need to update inventory levels

## Database Tables

- **tbl_preceipt_txn** - Goods receipt header
- **tbl_preceipt_item** - Line items received
- **tbl_preceipt_movement** - Inventory movement records

## Usage

```bash
python create-purchase-receipt/main.py \
  --supplier-name "NINGBO METALWIRE" \
  --receipt-date "2025-10-27" \
  --items '[
    {
      "product_name": "WIRE D1.2-L105.8",
      "quantity": 200,
      "unit_price": 8.50,
      "po_reference": "PO25100055"
    }
  ]' \
  --delivery-order "DO-2024000" \
  --json
```

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| supplier_name | string | Supplier name (fuzzy match) |
| receipt_date | string | Receipt date (YYYY-MM-DD) |
| items | JSON array | Line items received |

## Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| delivery_order | string | Supplier's DO number |
| po_reference | string | Related PO number |
| remark | string | Any notes |

## Item Fields

| Field | Required | Description |
|-------|----------|-------------|
| product_name | Yes | Product name or SKU |
| quantity | Yes | Quantity received |
| unit_price | Yes | Price per unit |
| discount | No | Discount percentage (0-100) |
| remark | No | Item-specific notes |

## Output (JSON)

### Success
```json
{
  "success": true,
  "gr_number": "GR25100048",
  "txn_id": 2210,
  "supplier": "NINGBO METALWIRE PRODUCTS CO.,LTD",
  "receipt_date": "2025-10-27",
  "items_count": 1,
  "subtotal": 1700.00,
  "grand_total": 1700.00,
  "delivery_order": "DO-2024000"
}
```

### Error
```json
{
  "success": false,
  "error": "Supplier 'XYZ' not found"
}
```

## Document Number Format

- **Format**: `GR{YY}{MM}{NNNN}`
- **Example**: `GR25100048` = October 2025, receipt #48

## Business Rules

1. **Supplier Validation**: Must exist in tbl_supplier
2. **Product Validation**: Must exist in tbl_product_code
3. **Inventory Update**: Automatically updates stock levels
4. **PO Linking**: Can link to existing PO for tracking
5. **No Tax Calculation**: GR records quantities only (tax on invoice)

## Example Scenarios

### Scenario 1: Full Delivery
```bash
# All items from PO received
python create-purchase-receipt/main.py \
  --supplier-name "ACTION BOLT" \
  --receipt-date "2025-10-27" \
  --items '[
    {"product_name": "WIRE D1.2", "quantity": 200, "unit_price": 8.50}
  ]' \
  --po-reference "PO25100055" \
  --json
```

### Scenario 2: Partial Delivery
```bash
# Only 150 out of 200 units received
python create-purchase-receipt/main.py \
  --supplier-name "ACTION BOLT" \
  --receipt-date "2025-10-27" \
  --items '[
    {"product_name": "WIRE D1.2", "quantity": 150, "unit_price": 8.50}
  ]' \
  --po-reference "PO25100055" \
  --remark "Partial delivery - 50 units backordered" \
  --json
```

### Scenario 3: Multi-Item Delivery
```bash
python create-purchase-receipt/main.py \
  --supplier-name "NINGBO" \
  --receipt-date "2025-10-27" \
  --delivery-order "DO-2024000" \
  --items '[
    {"product_name": "WIRE D1.2-L105.8", "quantity": 100, "unit_price": 8.50},
    {"product_name": "WIRE D0.8-L133.5", "quantity": 200, "unit_price": 7.30}
  ]' \
  --json
```

## Integration with Database Agent

```python
# After Document Agent extracts Delivery Order
extracted_data = {
    "document_type": "delivery_order",
    "issuer": "NINGBO METALWIRE PRODUCTS CO.,LTD",
    "do_number": "DO-2024000",
    "po_reference": "PO25100054",
    "delivery_date": "2025-10-27",
    "line_items": [
        {"description": "WIRE D1.2-L105.8", "qty_delivered": 100, "unit_price": 8.50}
    ]
}

# Call skill via Bash
result = bash_tool.execute(
    f"python skills/purchasing/create-purchase-receipt/main.py "
    f"--supplier-name '{extracted_data['issuer']}' "
    f"--receipt-date '{extracted_data['delivery_date']}' "
    f"--delivery-order '{extracted_data['do_number']}' "
    f"--items '{json.dumps(items)}' "
    "--json"
)
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Supplier not found | Invalid supplier name | Check tbl_supplier |
| Product not found | Invalid SKU/name | Check tbl_product_code |
| Invalid date | Wrong date format | Use YYYY-MM-DD |
| Negative quantity | Invalid input | Quantity must be > 0 |

## Testing

```bash
# Test with sample delivery order
python create-purchase-receipt/main.py \
  --supplier-name "NINGBO" \
  --receipt-date "2025-10-27" \
  --items '[{"product_name": "WIRE D1.2", "quantity": 50, "unit_price": 8.50}]' \
  --verbose --json
```

## Notes

- GR updates inventory immediately
- Can create GR without PO (direct receipt)
- Multiple GRs can reference same PO (partial deliveries)
- GR is the SOURCE for Purchase Return (if defects found)

---

**Database**: carrickc (MariaDB)
**Tables**: tbl_preceipt_txn, tbl_preceipt_item, tbl_preceipt_movement
**Document Format**: GR25100048
**Inventory Impact**: Yes (increases stock)
