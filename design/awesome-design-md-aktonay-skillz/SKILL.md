---
name: awesome-design-md
description: >
  Apply production-grade brand design systems from 70+ top companies (Apple, Stripe,
  Linear, Vercel, Airbnb, Ferrari, Figma, Coinbase, etc.) into any project using portable DESIGN.md files.
license: MIT
---

# Awesome DESIGN.md Skill

Use this skill when you want to design, skin, or refactor an application to match the exact aesthetic, design tokens, typography, and visual rules of world-class brands.

## Available Brand Design Systems

Over 70 curated brand designs are included locally in `./design-md/`:
- **Tech & DevTools**: `apple`, `stripe`, `linear`, `vercel`, `figma`, `cursor`, `github`, `hashicorp`, `clickhouse`, `supabase`, `framer`
- **Fintech & Crypto**: `coinbase`, `binance`, `revolut`, `composio`, `cal`
- **Consumer & Lifestyle**: `airbnb`, `ferrari`, `bmw`, `bmw-m`, `bugatti`, `dji`, `elevenlabs`, `clay`
- **Media & Editorial**: `aljazeera`, `dell-1996`, `expo`

## How to Apply a Brand Design System

1. Browse or query the target brand inside `./design-md/<brand>/DESIGN.md`.
2. Extract the frontmatter design tokens (colors, fonts, radii, spacing, shadows).
3. Apply the brand's aesthetic guidelines and component patterns to your CSS/Tailwind configuration or stylesheet.
4. Ensure the output strictly respects the design tokens rather than generic AI defaults.

## Key Principles
- **No generic AI aesthetics**: Never default to purple/blue gradients with rounded-2xl cards.
- **Honor token hierarchy**: Always use the brand's defined canvas, foreground, primary, and secondary color variables.
- **Typography pairing**: Use the designated Google or system fonts identified in the file.
