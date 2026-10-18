---
name: forge-ecommerce
description: "Forge: e-commerce and cashflow shops: shop, store, cart, checkout, product, inventory, Shopify, WooCommerce, Etsy, Stripe, order fulfillment, oversell."
---

# Forge playbook — E-commerce / store / digital products

Storefront UI defers to `forge-website`; anything that charges a card defers to **`forge-payments`** (this playbook never re-implements card handling). This file owns the commerce-specific concerns: catalog, cart, inventory correctness, orders, and connectors. Forge context: a cashflow or digital-goods shop / Etsy-style shops.

## Hard rules
- **Real product/listing data with honest empty states.** No lorem/placeholder products passed off as a real catalog; an empty catalog renders a real empty state, never fake inventory or fabricated sales/metrics.
- **Oversell-safe inventory.** Stock decrement is an **atomic conditional update** ("first writer wins", `UPDATE ... SET stock = stock - qty WHERE stock >= qty`) or a reservation row — never a read-then-write that races. Concurrent buyers of the last unit → exactly one succeeds. Prefer soft-reserve at cart/checkout intake, hard-decrement at order confirmation.
- **Idempotent order creation.** `POST /order` (or checkout submit) carries an `Idempotency-Key` with a UNIQUE constraint, because mobile networks retry, users double-tap, and gateways time out — a duplicate submit must return the same order, not create two. (Same pattern as `forge-payments`; keep them consistent.)
- **Connectors gated until keys + approval.** Store/marketplace connectors (Shopify Admin, WooCommerce, Etsy, Stripe) stay disabled until real keys are present AND the owner approves. **No live publish, store-push, listing update, price change, or spend without explicit owner approval.**
- **Money = integer minor units + currency** (see `forge-payments`); no float math on prices, tax, shipping, or discounts.
- Secrets (store API keys, webhook secrets) in env + `.env.example` placeholders only.

## Team (conditional)
Lead: `build-boss` (full store) or `integration-boss` (connector/sync-only). Specialists: `payment-integration` (checkout/charge — via `forge-payments`), `database-reviewer` (inventory + order schema, race-safety), `silent-failure-hunter` (a dropped inventory sync or swallowed order error looks like a clean sale), `typescript-reviewer` / `python-reviewer`. Storefront: `forge-website` team (a11y, responsive, real content). Optional: `codex-reviewer` on the checkout/order/inventory paths.

## Skills / commands / MCP
`forge-website` (storefront, product pages, cart UI), `forge-payments` (checkout + billing), `forge-integration` / `forge-n8n` (connector sync, order-notification automations). Store MCP/SDK docs via Context7 for exact connector APIs. Draft-only for any customer outreach (order emails staged, not blasted — shared with `forge-integration`).

## Fan-out & flow
L2 catalog + cart; L3 catalog + cart + checkout + inventory + orders + a connector; L4 multi-channel store with marketplace sync.
**Parallel:** catalog/product pages ∥ cart logic ∥ inventory service ∥ storefront UI (independent once the product + order schema/contract is fixed).
**Serial:** data model (products, SKUs, minor-units prices, inventory) → catalog → cart → checkout (`forge-payments`) → atomic inventory decrement → order record → fulfillment/notification.

## Domain gates
- Real catalog data or an honest empty state; no fabricated sales/inventory/metrics.
- Inventory decrement is atomic/reservation-based and proven oversell-safe under a concurrent-buyer test.
- Order creation is idempotent (unique idempotency key); a double-submit returns one order.
- Prices/tax/shipping in integer minor units; no float money math; totals reconcile.
- Cart → checkout → order → payment flow works end-to-end in test mode (an integration test, not just green units).
- Connectors inactive until keys + owner approval; no live publish/push/spend performed.
- Customer-facing emails/messages drafted, not auto-sent, without confirmation; idempotency before any order notification (no duplicate "order confirmed" mails on webhook retry).

## Ship-readiness (unique)
Real products with honest empty state; one real purchase flow works end-to-end in test mode; oversell-safe inventory proven under concurrency; idempotent orders proven under double-submit; minor-units money reconciles; store connectors gated + no live push/spend done; order notifications idempotent + draft-gated; secrets in env. Advisory checklist; optionally run `codex-reviewer` on checkout/order/inventory — not a blocker; if a live store/marketplace action was requested, it stays owner-gated.
