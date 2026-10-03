---
name: roblox-monetization
description: "Design or review Roblox developer products, passes, subscriptions, and retry-safe purchase fulfillment."
---

# Roblox monetization

Read [`../../references/roblox-engineering.md`](../../references/roblox-engineering.md). Inspect the product catalog, prompt path, receipt owner, persistence layer, and every grant path before editing purchase code.

## Separate prompting from fulfillment

- The client may request a purchase prompt, but never supplies the trusted product, price, ownership, or grant result. Resolve products through server-owned configuration.
- Fulfill developer products through one server-owned `MarketplaceService.ProcessReceipt` callback. A prompt-finished event is presentation feedback, not proof that payment settled.
- Validate the product and recipient. If the recipient or required data is unavailable, defer fulfillment rather than guessing or dropping the receipt.
- Make fulfillment atomic and idempotent around the receipt's purchase identifier. Persist the receipt record and durable grant together when the data model permits it; retries must converge on the existing outcome.
- Return the granted decision only after the durable grant is confirmed. On a transient storage or fulfillment failure, return the current not-processed decision so Roblox can retry.
- Derive pass or subscription entitlement from current server-side marketplace APIs and repository policy. Purchase prompts and client caches do not permanently confer access.
- Keep catalog identifiers centralized. Treat prices, regional behavior, platform policy, and exact marketplace APIs as time-sensitive and verify them against current official Roblox documentation.
- Consequential randomized products also follow `$roblox-security`: choose the outcome on the server, bind it to the durable receipt outcome, and do not allow retries to reroll it.

## Deliverable

Describe the prompt path, fulfillment owner, receipt state machine, durable record, duplicate behavior, unknown-product behavior, and failure/retry policy. Add deterministic tests for duplicate callbacks, reconnects, unavailable players, storage failure, and unknown products. The user performs purchase testing in Studio; never invoke MCP playtest controls.
