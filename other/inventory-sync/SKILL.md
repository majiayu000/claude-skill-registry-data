---
name: inventory-sync
displayName: Inventory Sync
tagline: Keep inventory levels synchronized across multiple sales channels and warehouses.
description: |
  Synchronizes inventory levels across Shopify, marketplaces, and warehouse
  systems in real-time. Prevents overselling, tracks stock movements, and
  generates reorder alerts when inventory drops below thresholds. Supports
  multi-location inventory management.
department:
  - E-commerce
  - Operations
  - Supply Chain
use_cases:
  - Inventory Management
  - Multi-channel Sync
  - Supply Chain
tools_required:
  - Shopify MCP
agents_compatible:
  - Claude / Claude Code
  - Cursor
  - Windsurf
  - ChatGPT
  - Any MCP-compatible agent
author: Webrix
verified: true
updatedAt: 2026-05-08
version: 1.0.0
exampleInput: |
  Sync inventory between our Shopify store and Amazon marketplace.
  Alert when any SKU drops below 20 units.
exampleOutput: |
  Inventory Sync Report

  CHANNELS SYNCED
  Shopify:     1,240 SKUs synced
  Amazon:      980 SKUs synced
  Warehouse A: Primary source of truth

  LOW STOCK ALERTS (< 20 units)
  SKU-1042 "Premium Widget":    8 units — reorder triggered
  SKU-2089 "Starter Kit":       14 units — approaching threshold
  SKU-3156 "Cable Pack":        19 units — approaching threshold

  SYNC STATS
  Last Sync:       2 minutes ago
  Discrepancies:   3 resolved automatically
  Oversell Risk:   0 SKUs
---

# Inventory Sync

Keep inventory levels synchronized across multiple sales channels and warehouses.

**Integrations:** Shopify

## When to Use

- The user sells across multiple channels and needs inventory consistency
- Overselling is a problem that needs to be prevented
- The user mentions "inventory sync", "stock levels", or "multi-channel inventory"

## Steps

### Step 1: Define Source of Truth

Identify the primary inventory source and sync direction.

### Step 2: Configure Sync Rules

Set sync frequency, conflict resolution, and buffer quantities.

### Step 3: Set Reorder Alerts

Configure low-stock thresholds and reorder notifications.

## Output

Deliver:
- Inventory sync configuration
- Low stock alert rules
- Sync status dashboard
