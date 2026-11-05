---
name: design-md
description: Use when creating, auditing, or applying a DESIGN.md specification file for a project to guide AI coding agents in generating visually consistent UI matching specific brand aesthetics, design tokens, typography, and component patterns.
domain: content
subdomain: design
category: content
version: 1.0.0
author: VoltAgent / oyi77
license: MIT
tags:
- design-system
- design-md
- design-tokens
- ui-guidance
- agent-instructions
- frontend
triggers:
- design-md
- create design md
- design system spec
- brand design md
- ui design guidance
- agent design system
argument-hint: "[project_root or brand_name]"
---

# DESIGN.md: AI Agent Design System Specification

## Overview

`DESIGN.md` is the companion to `AGENTS.md` for user interfaces. While `AGENTS.md` defines how an agent should build, test, and run code, `DESIGN.md` defines how the project's user interface must look, feel, and behave. It acts as a single, plain-text source of visual truth that AI coding agents read directly, eliminating guesswork around colors, typography, spacing, and component variants.

Based on the Google Stitch and VoltAgent `awesome-design-md` standard, this skill provides the methodology to author, audit, and enforce project-specific `DESIGN.md` specifications that prevent visual drift and AI slop.

## When to Use

**Trigger phrases:**
- "design-md", "create design md", "design system spec"
- "brand design md", "ui design guidance", "agent design system"

Use when:
- Establishing a new web or mobile frontend and ensuring coding agents generate consistent styling.
- Aligning a product with an existing brand archetype (e.g., Linear precision-dark, Stripe editorial-clean, Vercel monochrome).
- Auditing an existing project's UI for token violations and inconsistent component styles.
- Creating an exportable, framework-agnostic design specification that works across React, Next.js, Vue, Tailwind, or vanilla CSS.

## When NOT to Use

- Writing raw component implementation code or fixing backend logic (use `development/role-software-engineer`).
- Auditing WCAG accessibility standards in isolation (use `content/accessibility-audit` or `better-accessibility`).
- Executing a post-generation design cleanup pass on existing screens (use `content/unslop` or `content/hallmark`).

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "The agent already knows Tailwind classes, it doesn't need a DESIGN.md." | Without a specification, agents invent random shades (`bg-purple-600` on one page, `bg-blue-500` on another), pick arbitrary paddings, and generate fragmented UIs. |
| "A Figma link in the prompt is sufficient." | AI agents cannot reliably inspect deep Figma component hierarchies from raw links without dedicated tooling. Markdown design tokens are parseable in zero network calls. |
| "A DESIGN.md is just a list of hex codes." | Colors are only 20% of a design system. Spacing ladders, type scales, surface elevations, and anti-patterns prevent visual chaos. |
| "Every screen in our app can have its own unique layout style." | Inconsistent component shapes and button hierarchies destroy user trust. Shared constraints create a professional product feel. |

## Standard DESIGN.md Specification Structure

Every valid `DESIGN.md` document contains five mandatory sections:

```text
PROJECT_ROOT/DESIGN.md
├── 1. Design Philosophy & Aesthetic Archetype
├── 2. Core Token Ladder (Color, Typography, Spacing)
├── 3. Component Primitive Standards (Buttons, Cards, Inputs, Badges)
├── 4. Surface & Elevation Hierarchy (Background, Surface, Overlay)
└── 5. Negative Rules & Anti-Patterns ("NEVER do X")
```

## Workflow: Authoring a Project DESIGN.md

### Phase 1: Aesthetic Archetype Selection

Identify the primary visual identity that matches the product:

| Archetype | Primary Palette | Mood & Focus | Example Brands |
|---|---|---|---|
| **Technical Dark / Precision** | Neutral dark (`zinc-900`), single neon or violet accent | Dense data, high contrast, monospace accents | Linear, Supabase, Cursor |
| **Monochrome Minimalist** | Stark black and white, zero decorative gradients | Crisp typography, precision borders, Geist/Inter | Vercel, xAI, Warp |
| **Editorial Warmth / Clean** | Warm paper canvas (`#fbfbfa`), charcoal text, serif accents | Approachable, intellectual, refined | Notion, Claude, Substack |
| **Vibrant Fintech / Enterprise** | Deep navy/slate canvas, emerald/indigo actions, soft shadows | Trustworthy, high polish, clear hierarchy | Stripe, Mercury, Coinbase |

### Phase 2: Token Architecture

Define strict token ladders with exact CSS variables or Tailwind class mappings:

```markdown
### Color Tokens
- Canvas: `bg-background` (`#09090b` dark / `#ffffff` light)
- Surface: `bg-card` (`#18181b` dark / `#f4f4f5` light)
- Border: `border-border` (`#27272a` dark / `#e4e4e7` light)
- Primary Action: `bg-primary` (`#3b82f6`) with `text-primary-foreground`
- Muted Text: `text-muted-foreground` (`#a1a1aa` dark / `#71717a` light)

### Typography Scale
- Font Family: Sans (`Inter`, `Geist`), Mono (`JetBrains Mono`, `Geist Mono`)
- Display: 36px / line-height 40px / font-semibold / tracking-tight
- Heading: 24px / line-height 32px / font-medium / tracking-normal
- Body: 14px / line-height 20px / font-normal
- Caption/Code: 12px / line-height 16px / font-mono
```

### Phase 3: Component Primitive Standards

Define standard classes for core primitives:

```markdown
### Button Specifications
- Primary: `h-9 px-4 rounded-md bg-primary text-primary-foreground text-sm font-medium hover:bg-primary/90 transition-colors`
- Secondary: `h-9 px-4 rounded-md border border-input bg-background hover:bg-accent hover:text-accent-foreground text-sm font-medium`
- Destructive: `h-9 px-4 rounded-md bg-destructive text-destructive-foreground hover:bg-destructive/90 text-sm font-medium`

### Card Specifications
- Container: `rounded-lg border border-border bg-card p-6 text-card-foreground shadow-xs`
```

### Phase 4: Anti-Patterns & Constraint Rules

Explicitly enumerate banned patterns to constrain AI generation:
1. **NEVER** use raw emojis as UI icons or bullet points. Use Lucide SVG icons.
2. **NEVER** use iridescent multi-color gradients on text or card backgrounds.
3. **NEVER** use arbitrary padding values (e.g. `p-[13px]`). Adhere strictly to the 4px scale (`p-3`, `p-4`, `p-6`).
4. **NEVER** use pure black text (`#000000`) on white; use charcoal (`#18181b` or `#0f172a`).

### Phase 5: Verification & Agent Test Drive

Test the `DESIGN.md` by instructing an agent:
> *"Read DESIGN.md and generate a settings billing card with a current plan badge, renewal date, and upgrade button."*

Verify output against token definitions and anti-patterns.

## Verification

- [ ] `DESIGN.md` authored in project root or target directory
- [ ] Contains all 5 mandatory sections (Philosophy, Tokens, Primitives, Elevation, Anti-Patterns)
- [ ] Color tokens define functional semantic roles, not arbitrary palettes
- [ ] Typography scale specifies exact sizes, weights, line-heights, and tracking
- [ ] Negative rules explicitly ban AI slop markers (raw emojis, neon gradients, arbitrary spacing)
- [ ] Agent test drive verified: generated sample component strictly obeys token definitions
