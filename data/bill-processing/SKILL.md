---
name: bill-processing
description: Extract data from bill/receipt images and return JSON for lunch-splitter app
version: 1.0.0
---

# Bill Processing Skill

This skill extracts structured data from restaurant bills and receipts.

## When to Use

Activate this skill when:
- User uploads an image of a bill or receipt
- User mentions processing a bill/receipt
- User asks to extract data from a restaurant bill

## Output Format

Return ONLY a JSON object in this exact format:

```json
{
  "people": [],
  "items": [
    {"id": 0, "name": "Item Name", "price": 0.00, "personQuantities": {}}
  ],
  "nextPersonId": 0,
  "nextItemId": 1,
  "tax": 0,
  "tip": 0,
  "isTransposed": false
}
```

## Field Specifications

- **items**: Array of menu items with sequential IDs starting from 0
  - `id`: Sequential number (0, 1, 2, ...)
  - `name`: Exact item name from bill
  - `price`: Item price as decimal number
  - `personQuantities`: Empty object `{}`
- **people**: Always empty array `[]`
- **nextPersonId**: Always `0`
- **nextItemId**: Number of items extracted
- **tax**: Tax percentage (calculate: (tax_amount / subtotal) × 100)
- **tip**: Tip percentage (calculate: (tip_amount / subtotal) × 100)
- **isTransposed**: Always `false`

## Extraction Rules

1. **Items**: Extract ALL food and drink items with exact names
2. **Prices**: Use exact decimal values (e.g., 12.99, not "~13")
3. **Tax**: If only amount shown, calculate percentage from subtotal
4. **Tip**: If only amount shown, calculate percentage from subtotal
5. **Service charges**: Treat as additional items if not tip/tax
6. **Duplicates**: Create separate entries for each occurrence
7. **Output**: Return ONLY JSON, no markdown code blocks, no explanations

## Example

Input: Image of bill with "Burger $12.99, Fries $4.50, Tax $1.57, Tip $3.52"

Calculation:
- Subtotal: $17.49
- Tax %: (1.57 / 17.49) × 100 ≈ 9%
- Tip %: (3.52 / 17.49) × 100 ≈ 20%

Output:
```json
{
  "people": [],
  "items": [
    {"id": 0, "name": "Burger", "price": 12.99, "personQuantities": {}},
    {"id": 1, "name": "Fries", "price": 4.50, "personQuantities": {}}
  ],
  "nextPersonId": 0,
  "nextItemId": 2,
  "tax": 9,
  "tip": 20,
  "isTransposed": false
}
```
