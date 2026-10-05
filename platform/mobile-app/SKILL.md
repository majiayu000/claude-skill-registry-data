---
name: mobile-app
description: |
  Mobile app screen inside a pixel-accurate device frame. Single screen,
  single job. Use for "mobile app", "iOS app", "Android app", "phone screen".
triggers:
  - "mobile app"
  - "ios app"
  - "android app"
  - "phone screen"
  - "app ui"
  - "app mockup"
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

# Mobile App Skill

Produce a single mobile screen mockup, framed inside a device chrome.

## Archetypes
| Brief | Screen |
|---|---|
| feed, inbox, timeline, list | Feed |
| article, post, item, product detail | Detail |
| sign-up, welcome, walkthrough | Onboarding |
| profile, account, bio | Profile |
| checkout, payment, form | Checkout |
| timer, map, single big number | Focus |

## Rules
- **One screen, one job.** No multi-tab tours.
- Tap targets ≥44px.
- Accent budget = 2.
- Display headings in serif; numerics in mono.
- No external images — CSS gradients or SVG placeholders.
- `data-df-id` on every interactive element.

## Output
Single `index.html` with inline CSS. Device frame via CSS/SVG.
