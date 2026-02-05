---
name: new-page
description: Build new pages in this project when asked to create a new page or major page layout. Enforce design_rules.md and client/src/design-tokens.ts, include a full-blue trust-gradient section, include a Buy Now Pay Later style section, include at least two sections with placeholder images, omit the risk section, and run ESLint with eslint.config.cjs after changes.
---

# New Page

## Overview

Create new pages that match the Future Water Systems design system and page conventions while meeting the required section constraints.

## Workflow

1. Read the design sources of truth:
   - design_rules.md
   - client/src/design-tokens.ts
2. Review canonical section patterns:
   - Buy Now Pay Later layout: client/src/components/sections/home/buy-now-pay-later.tsx
   - Full-blue trust-gradient section: client/src/components/sections/home/why-choose-us.tsx
   - Standard page hero usage: client/src/pages/home-kitchen-systems.tsx and client/src/components/marketing/Hero
3. Draft the page outline and ensure all required sections are present (see Requirements).
4. Implement the page and sections using tokenized utilities and shared components.
5. Update routing in client/src/App.tsx if a new route is required.
6. Run linting (see Validation).

## Requirements (non-negotiable)

- Use the standard Hero component (do not copy the Home page hero).
- Include at least one full-blue section using the trust-gradient pattern.
- Include at least one Buy Now Pay Later style section with the same layout DNA.
- Include at least two sections that display placeholder images.
- Do not add the red Risk section.
- Follow the section header structure from design_rules.md (badge, split-color heading, subheading, supporting copy).

## Implementation Notes

- Use design tokens and utilities only (tw-heading-*, tw-body-*, section-padding, container-width).
- Use existing component patterns (Card, Button, card-surface, card-surface-hover, btn-primary, btn-secondary).
- Keep the background rhythm from design_rules.md: alternate white and light-gradient sections; after the blue section, return to a white section.
- For full-blue sections, use inverse badge styling and white text per design_rules.md.

## Placeholder Images

- Use /images/placeholders/educational-placeholder.svg for image placeholders.
- Ensure at least two distinct sections include placeholder images (e.g., a split visual section plus a grid or timeline).
- Keep alt text descriptive and note that images are placeholders.

## Validation

- Run: npx eslint . --config eslint.config.cjs
- Run: npm run build
- Fix any warnings or errors before finishing.
