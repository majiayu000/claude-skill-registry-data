---
name: create-purchase-claim
description: Create purchase claim (PCL) for price/quantity discrepancies with supplier
---

# Create Purchase Claim Skill

## Purpose

Creates a **Purchase Claim (PCL)** record when there are price or quantity discrepancies. Triggered by a **Discrepancy Report** comparing invoice vs quotation.

## When to Use

- Invoice price differs from quotation
- Quantity short delivery
- Quality issues requiring compensation
- Price overcharge

## Usage

```bash
python create-purchase-claim/main.py \
  --supplier-name "NINGBO" \
  --claim-date "2025-10-27" \
  --claim-type "price_difference" \
  --claim-amount "200.00" \
  --items '[{"product_name": "WIRE D1.2", "quoted_price": 6.00, "invoiced_price": 7.00, "quantity": 200}]' \
  --invoice-reference "PI25100065" \
  --description "Price difference from approved quotation" \
  --json
```

## Output

```json
{
  "success": true,
  "pcl_number": "PCL25090003",
  "txn_id": 48,
  "supplier": "NINGBO METALWIRE PRODUCTS CO.,LTD",
  "claim_date": "2025-10-27",
  "claim_amount": 200.00,
  "claim_type": "price_difference",
  "invoice_reference": "PI25100065"
}
```

## Document Format

- **Format**: `PCL{YY}{MM}{NNNN}`
- **Example**: `PCL25090003` = September 2025, claim #3

## Claim Types

- `price_difference` - Overcharged on price
- `quantity_shortage` - Delivered less than ordered
- `quality_issue` - Defective goods (financial claim)
- `other` - Other discrepancies

---

**Database**: tbl_pclaim_txn, tbl_pclaim_item
**Inventory Impact**: No (financial only)
