---
name: aetherbrowser-shopify-nav
description: "Navigate Shopify admin and storefront pages through AetherBrowser for merchandising and operations tasks. Use when working on products, collections, orders, settings, or marketing surfaces in browser mode."
---

# AetherBrowser Shopify Nav

## Workflow

1. Route via dispatcher.
- `python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\browser_chain_dispatcher.py --domain admin.shopify.com --task navigate --engine playwriter`

2. Open target admin area.
- Home: `https://admin.shopify.com`
- Products: `https://admin.shopify.com/store/<store>/products`
- Collections: `https://admin.shopify.com/store/<store>/collections`
- Marketing: `https://admin.shopify.com/store/<store>/marketing`

3. Validate session + page title.
- `python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\playwriter_lane_runner.py --session 1 --task title`

4. Capture structure snapshot for follow-up automation.
- `python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\playwriter_lane_runner.py --session 1 --task snapshot`

## Rules

- Prefer `playwriter` for authenticated admin pages.
- Do not execute destructive actions without explicit task instruction.
- Record lane packets and execution outputs for audit.
