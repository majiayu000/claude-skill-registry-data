---
name: pga
description: Screen products for FDA, EPA, USDA, CPSC, FCC, and other government agency requirements using AskRosetta. Use when checking regulatory compliance for US imports.
argument-hint: "<product description>"
---

# PGA Screening

Determine which US Partner Government Agencies (PGA) require clearance for an imported product. Screens FDA, EPA, USDA, CPSC, FCC, ATF, DOT, and others — with specific CFR regulation citations.

## When to Use

- User asks "does X need FDA approval?"
- User wants to know regulatory requirements for an import
- User is checking if a product needs special permits or testing

## How It Works

Use the `determine_pga_requirements` MCP tool with the product description.

If MCP is unavailable:

```bash
curl -s -X POST "https://api.askrosetta.ai/api/v1/pga" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ${ASKROSETTA_API_KEY}" \
  -d '{
    "product_description": "<description>",
    "hts_code": "<if known>",
    "intended_use": "<if specified>"
  }'
```

## Response Format

**PGA Screening Result**

- **Requires PGA clearance**: Yes/No
- **Agencies**:
  - FDA — Prior Notice required (21 CFR 1.276), product registration
  - EPA — TSCA certification (15 USC 2601)
  - CPSC — Testing required (16 CFR 1500)
  - (etc.)
- **Risk Level**: Low / Medium / High / Critical
- **Warnings**: any holds or flags

Always include CFR citations — users need them for compliance records.

If no agencies are flagged, confirm the product appears exempt but recommend verifying with a licensed customs broker for high-value or novel product shipments.
