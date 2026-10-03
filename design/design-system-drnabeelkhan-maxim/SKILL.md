---
name: maxim:design-system
description: Maxim Design System Intelligence — token architecture (primitive→semantic→component), component library governance, CSS variable systems, Tailwind integration, design-to-code handoff, Storybook, Figma token export. Activate for design system creation, token audits, component specs, dark mode systems, brand-to-token sync. Powered by Maxim behavioral science + Atomic Design + TOGAF governance.
argument-hint: "[create|tokens|audit|component|slides] [args]"
confidence: 🟢 HIGH
---

# Maxim Design System Intelligence

> Maxim behavioral layer active. Behavioral science applied to every output.
> External reference: `community-packs/ui-ux-pro-max/.claude/skills/design-system/`

## Agents in This Skill

### 1. token-architect
Owns the three-layer token system from primitive to component.
- Enforces three-layer structure: Primitive → Semantic → Component (never skip layers)
- Applies Miller's Law (7±2) to token naming: each namespace must have ≤9 top-level groups
- Applies Gestalt Similarity to token grouping — visually related tokens must be semantically grouped
- Generates: CSS variables, Tailwind config, JSON token export
- Absorbs external token patterns from: `community-packs/ui-ux-pro-max/.claude/skills/design-system/scripts/generate-tokens.cjs`
- Output: Token architecture document + CSS variables file + Tailwind theme extension

**Three-Layer Enforcement:**
```
Primitive (raw values — never used directly in components)
  --color-blue-600: #2563EB
       ↓
Semantic (purpose aliases — what the color MEANS)
  --color-primary: var(--color-blue-600)
       ↓
Component (component-specific — isolated customization)
  --button-bg: var(--color-primary)
```

### 2. component-architect
Owns component specification, state matrix, and variant system.
- Applies Atomic Design (Brad Frost): Atoms → Molecules → Organisms → Templates → Pages
- Applies TOGAF Component Governance for enterprise-scale versioning and deprecation
- Defines: default / hover / active / focus / disabled / error states for every interactive component
- Enforces: accessibility compliance (WCAG 2.1 AA minimum) on every component spec
- Proactively loops: `ui-styling` skill for Tailwind/shadcn implementation
- Output: Component spec matrix + state table + accessibility checklist per component

### 3. design-handoff-specialist
Owns design-to-code handoff quality and token compliance validation.
- Runs token validation: `community-packs/ui-ux-pro-max/.claude/skills/design-system/scripts/validate-tokens.cjs`
- Flags hardcoded values (hex, px, font names) — requires token replacement
- Validates Figma → Code token parity
- Generates handoff documentation: component name, token map, props, accessibility notes
- Output: Handoff spec + validation report + hardcoded-value violation list

### 4. slide-system-builder
Owns brand-compliant presentation generation using design tokens.
- Uses the contextual decision system from external: `data/slide-strategies.csv`, `data/slide-layouts.csv`, `data/slide-color-logic.csv`
- Applies Minto Pyramid for deck narrative structure
- Applies Duarte Sparkline for emotional arc (What Is → What Could Be pattern breaks)
- Applies Dual Coding Theory — every key point needs visual + verbal encoding
- Enforces: ALL slides import `design-tokens.css`, use `var()` exclusively, NO hardcoded hex
- Output: Full HTML slide deck with Chart.js, keyboard navigation, token-compliant styling

## Maxim Behavioral Framing

**Core Principle:** A design system is a cognitive load reduction tool for both users and development teams. Every architectural decision is a behavioral decision — it determines how fast teams can build, how consistent users experience the product, and how much mental effort both groups must exert.

**Framework Selection by Task:**

| Task | Framework |
|---|---|
| Token architecture | Atomic Design + Miller's Law + Gestalt Similarity |
| Component governance | TOGAF Component Model + Semantic Versioning |
| Dark mode / theming | Semantic token layer (primitives never change, semantics swap) |
| Handoff quality | Don Norman's Design Principles (visibility, feedback, constraints) |
| Slide generation | Minto Pyramid + Duarte Sparkline + Dual Coding Theory |

## Dispatch

| Argument | Agent | External Reference |
|---|---|---|
| `create` | token-architect + component-architect | `references/token-architecture.md` + `templates/design-tokens-starter.json` |
| `tokens` | token-architect | `references/primitive-tokens.md` + `references/semantic-tokens.md` + `references/component-tokens.md` |
| `audit` | design-handoff-specialist | `scripts/validate-tokens.cjs` |
| `component` | component-architect | `references/component-specs.md` + `references/states-and-variants.md` |
| `slides` | slide-system-builder | `data/slide-strategies.csv` + `data/slide-layouts.csv` + `data/slide-color-logic.csv` |
| `tailwind` | token-architect + design-handoff-specialist | `references/tailwind-integration.md` |

## Proactive Agent Loops

- **Always** loop `brand` skill — tokens must derive from brand primitives
- **Always** loop `ui-styling` skill — tokens must map correctly to Tailwind/shadcn config
- Loop `engineering` skill when component specs are being implemented in code
- Loop `design` skill for visual consistency validation across the token system

## Confidence Tagging

🟢 HIGH — brand guidelines exist, token architecture defined, Maxim behavioral layer fully applied
🟡 MEDIUM — partial token system or no existing brand guidelines
🔴 LOW — no design system exists yet (flag: start with `create` subcommand + `brand` skill first)

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
