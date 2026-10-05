---
name: pitch-deck
description: |
  Investor pitch deck with problem, solution, market, traction, team, and ask.
  Use for "pitch", "investor deck", "fundraising", "VC".
triggers:
  - "pitch"
  - "pitch deck"
  - "investor deck"
  - "fundraising"
  - "vc deck"
  - "startup pitch"
df:
  mode: deck
  platform: desktop
  scenario: business
  preview:
    type: html
    entry: index.html
  design_system:
    requires: false
---

# Pitch Deck Skill

Produce an investor pitch deck.

## Slides (10–12)
1. **Cover**: company name, one-liner, logo.
2. **Problem**: what pain exists? Who feels it?
3. **Solution**: your product, 2–3 sentences.
4. **Market**: TAM/SAM/SOM numbers, growth rate.
5. **Product**: screenshot/placeholder + 3 key features.
6. **Traction**: metrics chart (users, revenue, growth %).
7. **Business model**: how you make money.
8. **Competition**: 2×2 matrix or feature comparison.
9. **Team**: 3–4 founders/advisors with roles.
10. **Financials**: 3-year projection table.
11. **Ask**: amount, use of funds, timeline.
12. **Thank you**: contact info, logo.

## Rules
- Numbers in big type. Charts inline SVG.
- One idea per slide. No walls of text.
- Consistent branding: logo on every slide, accent color disciplined.
- `data-df-id` on each slide.

## Output
Single `index.html` with slide system.
