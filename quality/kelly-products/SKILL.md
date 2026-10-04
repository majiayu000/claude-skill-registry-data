---
name: kelly-products
description: E-commerce product-management desk (Busabase App-in-Skill) for catalog master data, SKUs, pricing, inventory, channel status, content assets, compliance notes, lifecycle state, and approval-gated product operations. Use when the user invokes $kelly-products or /kelly-products, asks for 电商商品管理, 商品库, SKU 管理, inventory/reorder, product status across Amazon/Shopify/TikTok Shop/eBay, channel publishing approvals, price-change review, quality holds, product lifecycle/archive decisions, or a Busabase-backed product management desk.
metadata:
  category: ecommerce
  tags:
    - risk:local-write
    - industry:ecommerce
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-products
    resources:
      - products
      - channels
      - inventory
      - review
      - settings
    risk: local-write

---

# Kelly Products

## Overview

Use this skill as the seller's product-management command desk. It sits between `kelly-picks` (what to develop), `kelly-listing` (what copy/assets to publish), `kelly-ads` (how it performs in paid channels), and `kelly-inquiry` (what buyers ask). The desk consolidates product master data, SKU pricing, inventory cover, channel status, asset readiness, compliance notes, lifecycle state, and an approval-gated review queue in a Busabase-backed App-in-Skill. Reading a SKU master sheet, a marketplace export, or an inventory CSV is a genuine external operation a browser cannot perform: `scripts/ingest_products.mjs` is the only place a product, channel row, inventory row, or review item enters the system. The AirApp itself only reads Busabase and writes review decisions; every channel publish, price change, SKU archive, or quality-hold change is delegated to the agent (or the user) after explicit approval, recorded by `scripts/execute_decisions.mjs`.

Default behavior is AirApp-first. Unless the user explicitly asks only for explanation, ingest what's due and give the user the clickable AirApp URL (or the local preview URL when local preview is explicitly requested). Use chat-only mode only when the user says "纯聊天", "chat only", "不要打开 UI", or similar; then present numbered review items (`Review #1`) and take verdicts in conversation.

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Kelly Products overview"></td>
    <td width="50%"><img src="assets/screenshots/products.webp" alt="Kelly Products catalog"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Product command desk with visual product cards, margin, inventory value, activity, and approval queue.</td>
    <td><strong>Catalog</strong><br>Image-rich product library with SKU, lifecycle, owner, margin, inventory cover, and status badges.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/detail.webp" alt="Kelly Products detail"></td>
    <td width="50%"><img src="assets/screenshots/review.webp" alt="Kelly Products review queue"></td>
  </tr>
  <tr>
    <td><strong>Product detail</strong><br>Gallery, pricing, inventory, content readiness, compliance notes, channel matrix, and related review cards.</td>
    <td><strong>Review queue</strong><br>Approval-gated publish, price, quality-hold, and lifecycle recommendations with evidence.</td>
  </tr>
</table>

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual quality, responsive layout, and the complete canonical `content/kelly-products-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery, ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and product contracts, stop before the unavailable Busabase operation, and report the exact missing dependency. Do not invent a second data backend.

## Boundary

- The agent reads product exports, inventory sheets, channel-status exports, and listing handoffs; ingesting them is a local-file-only operation: `scripts/ingest_products.mjs` reads a JSON payload file the agent prepares and writes it to Busabase. It never fetches documents from remote systems on its own.
- The AirApp reads and writes Busabase records only. It never publishes a channel listing, changes a price, archives a SKU, lifts a quality hold, or performs any other external side effect.
- Publishing channels, changing prices, archiving SKUs, and lifting quality holds all require a human approval record on a review item; `scripts/execute_decisions.mjs` never performs the action itself — it only writes an execution marker. The agent performs the real follow-up outside the app after explicit approval and reports the concrete result back to the user.
- No seller credentials live in this repo or in Busabase. Never commit local payload files, env files, or generated exports.
- Never invent certifications, test reports, inventory, or supplier facts. Mark them missing and request evidence rather than weakening margin, MAP, low-stock, or compliance gates to make a product pass.

## Busabase Resources

Five Bases under one application Folder (`kelly-products`), declared in `content/kelly-products-app/app/js/config.js` and the generated template sidecars under `content/`:

- `products`: catalog/SKU master data — lifecycle, status, owner, vendor, image/gallery, tags, and JSON-encoded pricing/inventory-rollup/content-readiness/compliance blocks.
- `channels`: one row per product × marketplace channel (Amazon/Shopify/TikTok Shop/eBay) — listing id, status, price, buybox, content score, and channel issue note.
- `inventory`: one row per product × warehouse — on-hand/available/reserved/inbound units, inbound ETA, days of cover, and stock-risk status.
- `review`: the approval-gated review queue — channel publish approvals, price-change review, quality holds, and lifecycle/archive decisions, with the human decision and execution marker on the same row.
- `settings`: one row (`record-id: "config"`) with the seller profile, platform connectors, warehouses, and review policy.

Resources provision lazily through an idempotent Busabase ChangeRequest the first time the app runs in a Space; see `references/products-schema.md` for exact field shapes. Metrics and the recent-activity feed are recomputed client-side from the stored rows on every read (`content/kelly-products-app/app/js/products-model.js`'s `buildSnapshot`/`assembleSnapshot`), so the desk is always fresh regardless of when a browser session loads it relative to the last ingest run.

## First Run And Onboarding

On invocation, check the `products` Base. If it is empty, guide setup before ingesting real products: ask, turn by turn, seller profile (brand, entity, base currency), enabled marketplace platforms, warehouses, and the review policy (price-change threshold, margin floor, low-stock days). Write the answers onto the Settings row, then ingest:

```bash
node skills/kelly-products/scripts/ingest_products.mjs payload.json --apply
```

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL. Start `pnpm --dir content/kelly-products-app dev` only when local preview/debugging is explicitly requested.

Required app views (hash routes):

- `#/overview`: KPI cards (products, active products, average margin, inventory value), visual product cards, review-queue preview, and recent activity (derived from each product's/review item's own timestamps).
- `#/products` and `#/products/<id>`: catalog and product detail with gallery, pricing, inventory, content readiness, compliance notes, channel matrix, and linked review cards.
- `#/inventory`: warehouse and days-cover table with low-stock and stockout-risk badges.
- `#/channels`: product × platform status table with channel issue notes and content scores.
- `#/review`: approval queue with `approve` / `request_changes` / `block` decisions. Decisions write directly onto the review item's own record through `busabase-sdk` — there is no separate decisions bucket.
- `#/settings`: sanitized seller profile, platform connectors, warehouses, review policy, and data-provider state, read live off the Settings Base.

Demo mode:

- `?demo=overview`, `?demo=products`, `?demo=inventory`, `?demo=channels`, `?demo=review`, and `?demo=detail` open deterministic mock scenes for documentation and screenshots.
- `lang=en` or `lang=zh` forces UI chrome language; demo product names and agent notes localize with the chrome.
- Demo mode never reads or writes Busabase. Decision buttons still work in the UI but act on in-memory state only.
- Demo product images are the same real static PNG assets shipped under `content/kelly-products-app/app/assets/product-images/` that the live app uses.

## Ingest Workflow

1. Collect product sources: SKU master sheet, pricing/cost table, warehouse inventory, marketplace/channel exports, content asset checklist, and handoffs from `kelly-picks` or `kelly-listing`.
2. Build a payload shaped like the retired local app's `products_snapshot.json` contract (`seller`, `platforms`, `warehouses`, `review_policy`, `sync`, `products`, `channel_matrix`, `inventory`, `review_items`) — see `references/products-schema.md` for the exact field shapes.
3. Run the write path:

```bash
node skills/kelly-products/scripts/ingest_products.mjs payload.json --apply
```

The script upserts every row into Busabase by natural key (`product_id`, `channel_id`, `inventory_id`, `item_id`) so re-ingests are idempotent, and never clobbers a human decision already recorded on a review item. Without `--apply` it is a dry run.

## Decisions And Execution Workflow

1. The reviewer decides at `#/review`: approve, request changes (with a note), or block. Decisions write `status`/`decision-note`/`decided-at` directly onto the review item's own record. From a standalone local preview the write merges immediately (trusted operator); from the deployed AirApp it creates a pending ChangeRequest for the trusted process to merge.
2. On explicit user request to execute, run `scripts/execute_decisions.mjs` (dry-run by default; `--apply` writes `execution-status: "ready_for_agent"` onto each decided review item with the concrete operation — `publish_channel`, `apply_price_change`, `lift_quality_hold`/`maintain_quality_hold`, `archive_product`, `maintain_block`, or `request_revision` — and a human-readable detail). No external side effects either way; the review item's `status` never changes.
3. The agent then performs the approved follow-up outside the app: publish the channel listing, apply the price change, archive the SKU, or lift/maintain the quality hold through the actual seller platform connectors, then reports the concrete result back to the user (and re-ingests the updated product/channel/inventory state with `scripts/ingest_products.mjs`).

## Safety Defaults

- Never invent certifications, test reports, inventory, or supplier facts. Mark them missing and request evidence.
- Do not weaken margin, MAP, low-stock, or compliance gates to make a product pass.
- Keep channel publishing, price changes, SKU archival, and quality-hold changes approval-gated even if the connector credentials are ready.
- Use stable ids and natural-key upserts so repeated ingests and executions are idempotent.
- Keep demo data deterministic and image-rich so documentation screenshots remain stable.

## Useful Commands

```bash
node skills/kelly-products/scripts/ingest_products.mjs payload.json --apply
node skills/kelly-products/scripts/execute_decisions.mjs
node skills/kelly-products/scripts/execute_decisions.mjs --apply
pnpm --dir skills/kelly-products/content/kelly-products-app dev
```

In normal use, invoke `/kelly-products`, let the skill ingest what's due, and open the AirApp.
