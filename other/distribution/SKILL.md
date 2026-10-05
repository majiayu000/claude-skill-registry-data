---
name: distribution
description: >-
  Constructs distributor accounts, inventory binds, commission or markup,
  and browse-and-quote, including the ready-to-sell scene.
  Internal distribution slot of the parent pack; do not invoke independently.
license: Apache-2.0
---

# Distribution data-build slot

Vendor-neutral distributor slot. Drop-in under pack `slots/` (already discovered).  
`slot.yaml` scene `ready-to-sell` is create distributor → bind inventory → set commission.  
Executors talk to `DATA_BUILD_API_BASE` (default local mock on port 8765). The case pipeline binds from `slot.yaml` when the match is unique.

## Single-step routing

| User intent | Executor |
|---|---|
| Create distributor | `scripts/executors/create_distributor.ts` |
| Bind supply / inventory | `scripts/executors/bind_inventory.ts` |
| Set commission | `scripts/executors/set_commission.ts` |
| Browse and quote | `scripts/executors/browse_and_quote.ts` |

```bash
node scripts/executors/create_distributor.ts --json '{"name":"North Channel"}'
```

## Scene: ready-to-sell

This scene **depends on a catalog product** (another domain's material). If `productId` is not in context and the catalog slot cannot produce one, **ask the user for that product material** (reuse an id, or construct via catalog first). Then continue bind → commission. Do not skip those steps.

1. Create distributor → `distributorId`
2. Bind `productId`
3. Set commission rate
4. Return distributor, binding, and commission

Optional fields (`rate`, `region`) use executor defaults. Do not invent `distributorId` / `productId` when the user already supplied them.

## Guardrails

- Start `node ../mock_server.ts` if no enterprise gateway is configured
- Do not invent `distributorId` / `productId`
- Defaults: `region=domestic`, `rate=0.1`
- See [references/tools-guide.md](references/tools-guide.md) and [../SLOT_SPEC.md](../SLOT_SPEC.md)
