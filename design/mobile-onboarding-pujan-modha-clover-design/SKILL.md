---
name: mobile-onboarding
description: |
  Mobile app onboarding flow — 3–5 screens with swipe indicators, value props,
  and CTA. Use for "onboarding", "walkthrough", "tutorial", "first run".
triggers:
  - "onboarding"
  - "walkthrough"
  - "tutorial"
  - "first run"
  - "app intro"
df:
  mode: prototype
  platform: mobile
  scenario: design
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
---

# Mobile Onboarding Skill

Produce a mobile onboarding flow.

## Structure
- **3–5 screens** shown as a horizontal scroll or swipeable stack.
- **Each screen**: illustration (CSS gradient/SVG), headline, body, CTA.
- **Indicators**: dot pagination at bottom.
- **Skip / Next**: top-right skip link, bottom full-width next button.
- **Final screen**: "Get started" primary CTA + "Already have an account? Sign in".

## Rules
- One value prop per screen. No walls of text.
- Illustrations: abstract geometric shapes in DS colors.
- Swipeable via CSS scroll-snap, no JS.
- Progress: dot indicators animate width on active.
- `data-df-id` on each screen.

## Output
Single `index.html`, inline CSS.
