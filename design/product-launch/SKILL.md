---
name: product-launch
description: |
  Product launch page with countdown, feature reveals, teaser video placeholder,
  and early-access signup. Use for "launch", "product launch", "coming soon".
triggers:
  - "product launch"
  - "launch page"
  - "coming soon"
  - "teaser"
  - "early access"
df:
  mode: prototype
  platform: desktop
  scenario: marketing
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
---

# Product Launch Skill

Produce a product launch / coming-soon page.

## Sections
1. **Hero**: massive product name, tagline, countdown timer (CSS animation).
2. **Teaser**: gradient placeholder for video/screenshot with play button overlay.
3. **Feature reveals**: 3 cards that fade in on scroll (CSS `animation-timeline`).
4. **Early access**: email signup form (styled input + button).
5. **Social proof**: "Join X others" with avatar stack.
6. **Footer**: minimal links, copyright.

## Rules
- Countdown: CSS-only, updates via JS interval.
- Avatar stack: overlapping circles with colored initials.
- Accent used for CTA and countdown numbers only.
- `data-df-id` on each section.

## Output
Single `index.html`, inline CSS/JS.
