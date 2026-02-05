---
name: create-purchase-return
description: Create purchase return (PRT) when returning defective goods to supplier
---

# Create Purchase Return Skill

## Purpose

Creates a **Purchase Return (PRT)** record when returning defective or incorrect goods to supplier. Triggered by a **Quality Inspection Report** showing failed items.

## When to Use

- Quality inspection finds defects
- Wrong items delivered
- Damaged goods received
- Need to return to supplier

## Usage

```bash
python create-purchase-return/main.py \
  --supplier-name "NINGBO" \
  --return-date "2025-10-27" \
  --items '[{"product_name": "WIRE D1.2", "quantity": 20, "unit_price": 8.50, "reason": "Defective"}]' \
  --gr-reference "GR25100048" \
  --json
```

## Output

```json
{
  "success": true,
  "prt_number": "PRT25090002",
  "txn_id": 145,
  "supplier": "NINGBO METALWIRE PRODUCTS CO.,LTD",
  "return_date": "2025-10-27",
  "items_count": 1,
  "total_returned": 170.00,
  "gr_reference": "GR25100048"
}
```

## Document Format

- **Format**: `PRT{YY}{MM}{NNNN}`
- **Example**: `PRT25090002` = September 2025, return #2

## Business Rules

1. **Reverses Inventory**: Reduces stock levels
2. **Links to GR**: References original goods receipt
3. **Tracks Reasons**: Defective, Wrong Size, Damaged, etc.

---

**Database**: tbl_preturn_txn, tbl_preturn_item, tbl_preturn_movement
**Inventory Impact**: Yes (decreases stock)
