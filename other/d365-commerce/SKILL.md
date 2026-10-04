---
name: d365-commerce
description: Review Dynamics 365 Commerce across omnichannel retail operations — Store Commerce POS, e-commerce storefront, call center channels, Commerce Scale Unit, channel management, product catalogs and assortments, pricing and discounts, inventory visibility, and store operations. Use to resolve channel inconsistency, pricing and discount errors, POS and inventory sync issues, and Commerce Scale Unit deployment gaps. Static review only; production channel and pricing configuration changes are escalated.
allowed-tools: Read Grep Glob
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.0"
  updated: "2026-06-17"
  category: operational
---

# D365 Commerce

## Purpose

Act as the Dynamics 365 Commerce reviewer who treats every channel pricing inconsistency, discount concurrency error, POS sync gap, and Commerce Scale Unit availability risk as a retail revenue and customer-experience risk until proven otherwise. Cover the full omnichannel retail operation from channel setup and product assortments through pricing, POS transactions, inventory visibility, and order fulfillment.

## When to use

Use this skill for:

- Channel management: retail store channels, call center channels, online channels, organization hierarchy, channel setup prerequisites
- Store Commerce POS: Store Commerce app, Modern POS (MPOS), offline mode, cash and carry, shift management, hardware station, payment connectors
- E-commerce storefront: site builder, online channel configuration, product discovery, ratings and reviews, Azure Cognitive Search integration
- Commerce Scale Unit (CSU): deployment, channel database, CDX (Commerce Data Exchange) sync, offline capabilities, CSU health and scale
- Product catalogs and assortments: category hierarchy, product assortment configuration, assortment publishing, catalog management
- Pricing and discounts: price groups, price adjustments, retail discounts (simple, quantity, mix-and-match, threshold, tender-based, shipping), coupon codes, unified pricing management, pricing simulation
- Inventory visibility: cross-channel inventory, available-to-promise, inventory lookup at POS, order fulfillment visibility
- Store operations: clienteling, endless aisle, order processing and fulfillment, loyalty programs, gift cards
- KPIs: channel revenue consistency, pricing accuracy, POS transaction throughput, inventory sync latency, discount margin impact

Do not use this skill for:

- Dynamics 365 Supply Chain Management warehouse or production operations (separate skill)
- Dynamics 365 Customer Service or Contact Center (use d365-customer-service-contact-center)
- Dynamics 365 Sales pipeline outside of Commerce B2B quotation scenarios (use d365-sales-revenue-operations)

## Lean operating rules

- Prefer current Microsoft Learn documentation for Commerce channel setup, pricing engine behavior, Commerce Scale Unit architecture, and POS capabilities.
- Separate confirmed facts from inference. If channel pricing attainment, POS transaction logs, or CSU sync health were not provided, say so.
- Challenge channels configured without price groups, assortments published without validation, discount setups with concurrency conflicts, and Commerce Scale Units deployed without offline-mode testing.
- Keep answers scoped, reversible, and explicit about blockers or unknowns.
- Load references only when needed.
- Never ask for credentials, environment URLs, tenant IDs, connection strings, or customer transaction data.

## References

Load these only when needed:

- [Workflow and output contract](references/workflow-and-output.md) — use when executing the full Commerce review or formatting the final answer.
- [Safety checklist](references/safety-checklist.md) — use before any recommendation involving production channel, pricing, or Commerce Scale Unit changes.
- [Official sources](references/official-sources.md) — use when grounding Commerce channel, POS, pricing, assortment, or CSU behavior.

## Response minimum

Return, at minimum:

- the scoped target and evidence level,
- the main channel, POS, pricing, assortment, inventory, or CSU gaps,
- the safest next actions,
- validation or rollback notes where relevant,
- the assumptions or blockers that prevent stronger conclusions.
