---
name: landing-page-minimal
description: |
  Ultra-minimal landing page — one headline, one subhead, one CTA, nothing else.
  Use for "minimal landing", "coming soon", "waitlist", "single CTA".
triggers:
  - "minimal landing"
  - "simple landing"
  - "waitlist"
  - "single cta"
  - "squeeze page"
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

# Minimal Landing Skill

Produce an ultra-minimal landing page.

## Structure
- **Centered content**: vertically and horizontally centered.
- **Headline**: massive display type, 1–2 words.
- **Subhead**: one sentence, muted color.
- **CTA**: single button or email input + button.
- **Footer**: minimal copyright, maybe one link.

## Rules
- No navigation. No secondary links.
- Background: solid color or very subtle gradient.
- Typography is the design. Every weight and size matters.
- `data-df-id` on headline, subhead, CTA.

## Output
Single `index.html`, inline CSS.
