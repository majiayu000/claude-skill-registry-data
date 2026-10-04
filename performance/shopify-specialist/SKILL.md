---
name: shopify-specialist
description: Shopify storefront setup, Liquid theme customization, conversion optimization,
  app integration, and storefront performance improvement. Use when asked to customize
  a Shopify theme with Liquid, set up product collections or metafields, optimize
  checkout conversion, integrate a Shopify app, fix a Shopify storefront bug, improve
  Shopify store speed, or set up Shopify Markets for multi-currency.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: commerce-platform
  tags:
  - shopify
  - liquid
  - e-commerce
  - conversion-optimization
  - shopify-apps
  - poppy-monarch
---

# Shopify Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `Shopify theme`, `Liquid template`, `Shopify store`.
- The requested work fits this skill's lane: Liquid theme work, product/checkout optimization, Shopify app setup, store speed.
- The task stays inside this skill's boundary and avoids adjacent areas called out as out of scope: Email marketing automation (use zapier-specialist); social media (use instagram-specialist).

## First actions
1. Identify: Shopify plan tier (affects available features), theme name and version, primary goal (conversion, speed, new feature)
2. `Glob('**/*.liquid', '**/sections/**', '**/snippets/**')` — find theme files if working locally
3. Confirm: Online Store 2.0 (section/block system) vs legacy theme

## Decision rules
- For theme customization: prefer JSON template sections over hardcoded Liquid where possible (OS 2.0)
- For performance: images must use Shopify's `img_url` filter with size parameters; lazy load below the fold
- For apps: evaluate app impact on store speed before recommending (check PageSpeed impact)

## Output contract
- Liquid code with comments on each non-obvious section
- For conversion changes: explain the conversion rationale (e.g., "Added trust badges at cart page to reduce abandonment")

## Constraints
- NEVER modify theme files without noting that changes may be overwritten on theme updates — recommend creating a duplicate theme for testing
- Scope boundary: email marketing automation belongs to zapier-specialist; social media strategy belongs to instagram-specialist

## Reference
- `references/full-guide.md`: full Shopify development guide — Liquid syntax, theme architecture, conversion optimization, app ecosystem, Shopify Markets
