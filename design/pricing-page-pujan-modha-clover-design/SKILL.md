---
name: pricing-page
description: |
  Standalone pricing page — header, plan tiers, feature comparison table, FAQ.
triggers:
  - "pricing"
  - "pricing page"
  - "plans"
  - "subscription"
  - "compare plans"
df:
  mode: prototype
  platform: desktop
  scenario: sales
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
---

# Pricing Page Skill

## Sections
1. **Hero** — title, one-line subhead, optional monthly/annual toggle.
2. **Plan cards** — one per tier. Name, price (display font), positioning,
   4–6 bullets, CTA. Recommended tier gets accent border/badge.
3. **Comparison table** — feature rows × tier columns. ✓ / — / value cells.
   Sticky header. Group into 2–3 sections.
4. **FAQ** — 4–6 collapsible items via `<details><summary>` (no JS).
5. **Footer CTA** — single line + button.

## Rules
- Plausible prices (not "$X / month").
- Accent on recommended tier + one CTA only.
- Table clean at 1024px; stacks/scrolls below 768px.
- No fake feature names.
- `data-df-id` on each tier card and table row.

## Output
Single `index.html`, inline CSS.
