---
name: Dutchie Ecommerce
description: Manage retail menus and orders via Dutchie Plus API.
---

# Dutchie Skill

## Capabilities
- **Menu Management**: List products, check stock levels (`dutchie.list_menu`).
- **Order Management**: Retrieve recent orders and check status (`dutchie.list_orders`).

## Usage
- Use this skill when the user asks about "retail sales", "online menu", or "recent pickup orders".
- If the user asks for "sales data", combine this with `dutchie.list_orders` to aggregate totals.

## Constraints
- Read-only for now (no order creation).
- Requires the user to have connected their Dutchie account in Settings.
