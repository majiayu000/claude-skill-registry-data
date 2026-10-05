---
name: catalog
description: >-
  Constructs catalog products (standard or limited), catalog orders, and
  account-credit enrollment, including product-then-credit scenes.
  Internal catalog slot of the parent pack; do not invoke independently.
license: Apache-2.0
---

# Catalog data-build slot

Vendor-neutral catalog-domain slot. Drop-in under pack `slots/` (already discovered; no extra `slot_roots` / marketplace path).  
`slot.yaml` is the scene config. More specific entities (limited / credit) are listed before generic product.  
Executors talk to `DATA_BUILD_API_BASE` (default local mock on port 8765). The case pipeline binds these executors from `slot.yaml` without an LLM when the match is unique.

## Single-step routing

| User intent | Executor |
|---|---|
| Standard catalog product | `scripts/executors/create_product.ts` |
| Limited catalog product | `scripts/executors/create_limited_product.ts` |
| Catalog order | `scripts/executors/create_order.ts` |
| Account credit on a product / user | `scripts/executors/setup_account_credit.ts` |

Do not invent `productId` / `userId` when the user already supplied them. Optional fields use executor defaults.

```bash
node scripts/executors/create_product.ts --json '{"name":"Northwind Standard","city":"demo-city"}'
```

## Scene orchestration

**credit-ready-product**

1. Create catalog product (or reuse `productId`)
2. Enroll the product and user in account credit
3. Return `productId`, enrollment result, `creditBalance`

**bookable-order**

1. Ensure a product exists
2. Create an order for `userId` + `productId`
3. Return `productId`, `orderId`, `status`

Pass upstream `data` fields into the next executor. Do not skip a later scene step.

## Guardrails

- Start `node ../mock_server.ts` if no enterprise gateway is configured
- Do not invent `productId` / `userId` / `orderId`
- Defaults: `city=demo-city`, `validHours=4`, `fulfillOn=today+2days`, `quantity=1`, `credits=1000`
- See [references/tools-guide.md](references/tools-guide.md) and [../SLOT_SPEC.md](../SLOT_SPEC.md)
