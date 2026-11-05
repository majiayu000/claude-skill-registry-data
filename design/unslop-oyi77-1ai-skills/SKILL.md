---
name: unslop
description: Use when turning vibecoded, generic, AI-looking UI into a crafted interface with character. Audits visual slop (purple gradients, glows, emoji labels, shouty copy) and applies a structured 9-pass redline redesign across spacing, color, icons, copy, typography, layout, details, visuals, and motion.
domain: content
subdomain: design
category: content
version: 1.0.0
author: Damir Sokolovsky / oyi77
license: CC-BY-4.0
tags:
- ui-design
- anti-slop
- design-refactor
- visual-hierarchy
- frontend
- polish
triggers:
- unslop
- remove ai slop
- fix vibecoded ui
- unslopping
- redline ui review
- clean up ai interface
- redesign
- revamp
- restyle
- de-slop ui
- generic ai design
argument-hint: "[file_path or component or url]"
---
# Unslop: Eliminating Vibecoded AI UI

## Overview

`unslop` transforms generic, AI-generated ("vibecoded") interfaces into intentional, character-driven designs. AI models consistently default to a recognizable signature: dark backgrounds with purple/indigo neon gradients, glassmorphism cards with glowing borders, emoji-bulleted feature cards, shouty copy ("Unlock Superhuman 10x Productivity!"), and arbitrary spacing.

This skill audits the screen for slop markers, anchors a distinctive visual direction from the product's actual purpose, and applies a disciplined **9-pass redline review** in order: Spacing → Color → Icons → Copy → Type → Layout → Details → Visuals → Motion.

Attribution: Created by Damir Sokolovsky ([@heydamir](https://x.com/heydamir)), licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Source repository: [heydamir/unslop](https://github.com/heydamir/unslop). The upstream skill also ships optional Playwright snapshot and story-video tooling (`scripts/snapshot.mjs`, `scripts/story.mjs`) which this port intentionally omits — see When NOT to Use.

## When to Use

**Trigger phrases:**
- "unslop", "unslopping", "remove ai slop"
- "fix vibecoded ui", "clean up ai interface"
- "redline ui review", "make this look less like ai"

Use when:
- An AI-generated landing page, dashboard, or component looks generic or stereotypically "AI-built".
- Reviewing PRs with excessive purple gradients, neon borders, or floating glassmorphic cards.
- Replacing generic placeholder illustrations and blobs with actual product screenshots or functional data displays.
- Elevating UI craft before investor demos, product launches, or commercial release.

## When NOT to Use

- Backend logic, data layer, or API endpoint tasks.
- When the codebase already follows a strict, hardened design system (use `impeccable` or `hallmark`).
- When only fixing a functional bug or accessibility defect without restyling.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "The purple gradient makes it look modern and high-tech." | Purple neon gradients on dark backgrounds are the universal signature of low-effort AI generation. Real products use restrained palettes derived from their domain. |
| "Users like emojis in section titles." | Emojis as UI icons look juvenile and amateurish. Use monochrome SVG icon sets (Lucide, Radix, Phosphor) sized consistently at 16–20px. |
| "Adding glows and borders makes cards pop." | Glowing borders create visual noise and destroy visual hierarchy. Rely on subtle 1px borders, background contrast, or pure whitespace for card separation. |
| "I should rewrite everything in one big pass." | Changing layout, copy, colors, and typography simultaneously causes regressions. Follow the 9 passes in sequence. |

## Workflow: The 9-Pass Redline Review

### Phase 1: Slop Audit

Scan the interface and catalog all instances of AI slop:
- **Color Slop**: `#8b5cf6`, `#6366f1` gradients, radial glowing blobs, iridescent borders.
- **Icon Slop**: Raw emojis (🚀, ✨, 💡, 🔥) used as navigation icons or card headers.
- **Copy Slop**: "Supercharge your workflow", "Unlock the power of AI", "Next-generation platform".
- **Structural Slop**: Identical 3-column feature grids with centered icons and 2-sentence descriptions.
- **Detail Slop**: `backdrop-blur` on every element, rounded-3xl corners on everything, floating decorative shapes.

### Phase 2: Anchor Direction

Determine three foundational anchors before touching code:
1. **World**: What domain is this? (e.g., developer terminal, financial ledger, medical dashboard, industrial console).
2. **Color Anchor**: Exactly ONE functional accent color carrying meaning (e.g., amber for warnings, emerald for live status, deep navy for actions). Everything else is neutral.
3. **Signature Detail**: One distinctive, well-crafted element (e.g., an authentic monospace data table, an SVG sparkline, a dense activity ticker).

### Phase 3: The 9 Passes (In Exact Order)

```text
[1. Spacing] ──► [2. Color] ──► [3. Icons] ──► [4. Copy] ──► [5. Type]
                                                                  │
[9. Motion] ◄── [8. Visuals] ◄── [7. Details] ◄── [6. Layout] ◄───┘
```

1. **Pass 1 — Spacing**: Enforce a strict 4px/8px scale. Remove arbitrary paddings (`p-[17px]`). Ensure consistent gutter between cards and containers.
2. **Pass 2 — Color**: Strip neon gradients. Replace with a neutral scale (`zinc`, `slate`, or custom neutral) + 1 accent color. Contrast ratio ≥ 4.5:1 for body text.
3. **Pass 3 — Icons**: Replace all emojis with cohesive SVG icons (e.g., Lucide React). Standardize icon size to 16px or 20px with matching stroke width (1.5px or 2px).
4. **Pass 4 — Copy**: Strip marketing filler. State exact functionality: what it does, who it is for, what input it takes.
5. **Pass 5 — Type**: Restrict to 1–2 font families. Set a clear type scale (e.g., 12/14/16/20/24/32px). Use `font-medium` or `font-semibold` instead of `font-black`.
6. **Pass 6 — Layout**: Break predictable 3-card symmetry. Use asymmetric density: anchor the primary action or live preview in 2/3 width, secondary controls in 1/3 width.
7. **Pass 7 — Details**: Remove outer glow shadows (`shadow-[0_0_50px_rgba(...)]`). Replace with crisp 1px borders (`border-border/60`) and subtle elevation (`shadow-xs` or `shadow-sm`).
8. **Pass 8 — Visuals**: Remove decorative abstract 3D blobs. Replace with real UI previews, realistic empty states, or actual data visualizations.
9. **Pass 9 — Motion**: Eliminate float/pulse animations on static content. Limit motion to interactive state transitions (150–200ms ease-out on hover/press).

## Verification

- [ ] All purple/neon iridescent gradients removed or replaced with neutral scale
- [ ] Zero raw emojis used as UI icons or bullet points
- [ ] Marketing filler copy replaced with concrete, technical functionality
- [ ] 9 passes executed in order without skipping phases
- [ ] Text contrast meets WCAG AA (≥ 4.5:1 for normal text)
- [ ] Layout uses asymmetric visual weight rather than identical 3-box cards
- [ ] Visual artifacts show functional product previews, not abstract blobs
