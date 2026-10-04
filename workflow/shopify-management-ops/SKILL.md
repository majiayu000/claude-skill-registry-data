---
name: shopify-management-ops
description: Run Shopify management from terminal with audit-first checks, product sync, storefront gate control, and optional live publish. Use when the user asks to manage Shopify products, storefront state, or monetization operations.
---

# Shopify Management Ops

## Overview
Use this skill to operate Shopify from terminal in a deterministic way: audit first, then publish. It reuses existing SCBE scripts and outputs artifact-backed reports.

## Trigger Conditions
Use when requests include:
- "post products to Shopify"
- "manage my Shopify store"
- "sync listings"
- "disable password gate"
- "run publish pipeline"

## Core Workflow
1. Run `audit` mode first to validate script health and storefront/admin status.
2. If healthy, run `publish` mode to sync products and images.
3. If storefront shows password gate, run `gate-disable` mode.
4. Run `full-live` mode for the full profit pipeline with live publish.

## Commands
From any shell:

```powershell
pwsh -ExecutionPolicy Bypass -File C:/Users/issda/.codex/skills/shopify-management-ops/scripts/run_shopify_management_ops.ps1 -Mode audit
```

Live product sync:

```powershell
pwsh -ExecutionPolicy Bypass -File C:/Users/issda/.codex/skills/shopify-management-ops/scripts/run_shopify_management_ops.ps1 -Mode publish
```

Disable storefront password gate:

```powershell
pwsh -ExecutionPolicy Bypass -File C:/Users/issda/.codex/skills/shopify-management-ops/scripts/run_shopify_management_ops.ps1 -Mode gate-disable
```

Full profit lane (includes fact gate + launch pack + live publish):

```powershell
pwsh -ExecutionPolicy Bypass -File C:/Users/issda/.codex/skills/shopify-management-ops/scripts/run_shopify_management_ops.ps1 -Mode full-live
```

Parallel tentacle mesh (code + visual + product/pricing + image lanes):

```powershell
pwsh -ExecutionPolicy Bypass -File C:/Users/issda/.codex/skills/shopify-management-ops/scripts/run_shopify_management_ops.ps1 -Mode mesh-audit
```

## Shopify App Connection Notes
You can connect through your Shopify apps by using their Admin API credentials in env secrets.
Required keys for this skill:
- `SHOPIFY_SHOP` (or `SHOPIFY_SHOP_DOMAIN`)
- `SHOPIFY_ACCESS_TOKEN` (or `SHOPIFY_ADMIN_TOKEN`)

If app credentials are saved at User/Machine scope, the runner loads them into the current process before executing scripts.

## Evidence Standard
Always return the report path from the run (JSON artifact under `artifacts/`).
Do not claim live success unless `live_sync.ok=true` in output JSON.
