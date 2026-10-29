---
name: brand
description: Use when brand voice, visual identity, messaging frameworks, asset management, brand consistency. Activate for branded content, tone of voice, marketing assets, brand compliance, style guides.
domain: content
author: claudekit
license: MIT
subdomain: brand
tags:
- brand
- identity
- voice
- messaging
- assets
- consistency
- style-guide
- guidelines
version: 1.0.0
category: content
---


# Brand

Brand identity, voice, messaging, asset management, and consistency frameworks.

## When to Use


- Brand voice definition and content tone guidance
- Visual identity standards and style guide development
- Messaging framework creation
- Brand consistency review and audit
- Asset organization, naming, and approval
- Color palette management and typography specs

## Workflow

1. **Define** — Establish brand voice, visual identity, and messaging framework
2. **Create** — Develop assets (logos, color palettes, typography, templates)
3. **Validate** — Check consistency against brand guidelines
4. **Sync** — Sync brand guidelines to design tokens (`sync-brand-to-tokens.cjs`)
5. **Approve** — Review and approve assets via approval checklist

## Quick Start

**Inject brand context into prompts:**
```bash
node scripts/inject-brand-context.cjs
node scripts/inject-brand-context.cjs --json
```

**Validate an asset:**
```bash
node scripts/validate-asset.cjs <asset-path>
```

**Extract/compare colors:**
```bash
node scripts/extract-colors.cjs --palette
node scripts/extract-colors.cjs <image-path>
```

All brand scripts are zero-dependency Node (builtins only). They need Node 18+ — check with `node --version`, or install on Debian/Ubuntu with `apt install nodejs`.

## Brand Sync Workflow

```bash
# 1. Edit docs/brand-guidelines.md (or use /brand update)
# 2. Sync to design tokens
node scripts/sync-brand-to-tokens.cjs
# 3. Verify
node scripts/inject-brand-context.cjs --json | head -20
```

**Files synced:**
- `docs/brand-guidelines.md` → Source of truth
- `assets/design-tokens.json` → Token definitions
- `assets/design-tokens.css` → CSS variables

## Subcommands

| Subcommand | Description | Reference |
|------------|-------------|-----------|
| `update` | Update brand identity and sync to all design systems | `references/update.md` |

## References

| Topic | File |
|-------|------|
| Voice Framework | `references/voice-framework.md` |
| Visual Identity | `references/visual-identity.md` |
| Messaging | `references/messaging-framework.md` |
| Consistency | `references/consistency-checklist.md` |
| Guidelines Template | `references/brand-guideline-template.md` |
| Asset Organization | `references/asset-organization.md` |
| Color Management | `references/color-palette-management.md` |
| Typography | `references/typography-specifications.md` |
| Logo Usage | `references/logo-usage-rules.md` |
| Approval Checklist | `references/approval-checklist.md` |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/inject-brand-context.cjs` | Extract brand context for prompt injection |
| `scripts/sync-brand-to-tokens.cjs` | Sync brand-guidelines.md → design-tokens.json/css |
| `scripts/validate-asset.cjs` | Validate asset naming, size, format |
| `scripts/extract-colors.cjs` | Extract and compare colors against palette |

## Templates

| Template | Purpose |
|----------|---------|
| `templates/brand-guidelines-starter.md` | Complete starter template for new brands |

## Routing

1. Parse subcommand from `$ARGUMENTS` (first word)
2. Load corresponding `references/{subcommand}.md`
3. Execute with remaining arguments
## Overview

Brand centralizes a company's voice, visual identity, and messaging so every piece of content stays consistent. It defines the brand framework (voice, tone, palette, typography), validates assets against the guidelines with `scripts/validate-asset.cjs`, and syncs approved colors/type into design tokens via `scripts/sync-brand-to-tokens.cjs` so downstream skills (design-system, ui-styling, banner-design) consume one source of truth.

## When NOT to Use

- One-off visual work with no brand — use design/design-system defaults instead of inventing a brand
- Where brand guidelines already live in a dedicated platform (Frontify, Zeroheight) — keep the source there and import decisions
- Writing marketing copy at length — this skill defines voice; copywriting formulas live in slides/design references
- When the user wants a brand *created from scratch with visual exploration* — route to logo/CIP design first, then formalize here

## Verification

1. `node scripts/validate-asset.cjs <asset>` returns PASS against the active guidelines
2. Colors used by any produced asset are in the approved palette (check with `node scripts/extract-colors.cjs`)
3. Typography follows the style guide (font family, weights, casing rules)
4. Voice sample sounds on-brand: read the copy aloud and confirm it matches the defined tone
5. Token sync is current — `design-system` tokens reflect the latest approved palette (`node scripts/sync-brand-to-tokens.cjs`)

## Anti-Rationalization Table

| Rationalization | Reality |
|-----------------|---------|
| "Every designer knows our brand, no doc needed" | Without a written source of truth each agent/contractor reinterprets; drift compounds per artifact |
| "A logo IS the brand" | Logo is one asset; voice, messaging, and color discipline carry consistency further |
| "I'll fix the palette later" | Late palette changes ripple through every asset; decide tokens before production work |
| "Validation scripts slow me down" | Automated checks catch off-palette hex and wrong casing in seconds, before a human review round |
| "Brand docs are static" | Brands evolve; treat guidelines as a living file reviewed at each asset milestone |

