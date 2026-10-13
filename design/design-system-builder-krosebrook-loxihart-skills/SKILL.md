---
name: design-system-builder
description: Build cohesive, scalable design systems with design tokens, component libraries, documentation, and governance. Use when creating company-wide design systems, style guides, or component libraries for product teams. Also triggers on requests mentioning design tokens, component API design, Storybook setup, CVA variants, Style Dictionary, atomic design, theme configuration, or contribution workflows for shared UI libraries. Even if someone just says "I need a component library" or "set up our design system" — use this skill.
metadata:
  version: "1.0.0"
allowed-tools: "Bash, Read, Write, Glob"
---

<essential_principles>

### 1. Tokens → Components → Docs → Governance

Every design system follows this build order. Tokens are the foundation — components consume tokens — docs make components discoverable — governance keeps it alive. Skipping steps creates tech debt.

### 2. Accessible by Default

WCAG 2.2 AA minimum. Keyboard navigation, screen reader support, focus management, and color contrast are non-negotiable in every component. Not bolted on later.

### 3. API Consistency Across Components

All components share the same prop conventions: `variant`, `size`, `disabled`, `className` escape hatch, `...rest` spread. Consumers learn one pattern and apply it everywhere.

### 4. Tree-Shakeable from Day One

Use `sideEffects: false`, per-component exports, and zero-runtime CSS (Tailwind + CVA recommended). Target under 100KB gzipped for the entire system.

### 5. Design-Engineering Parity

Tokens in code must match Figma tokens exactly. Style Dictionary transforms a single source of truth into platform-specific outputs (CSS, iOS, Android). No manual syncing.

</essential_principles>

<intake>

**Identify starting point from the user's request:**

| User Says | Route To |
|-----------|----------|
| "New design system" / "start from scratch" / "set up our system" | `workflows/new-system.md` |
| "Add a component" / "build a button/card/modal" / "component API" | `workflows/add-component.md` |
| "Document our system" / "Storybook" / "component docs" | `workflows/document-system.md` |
| "Design tokens" / "token architecture" / "Style Dictionary" | `references/token-architecture.md` |
| "CVA" / "component patterns" / "testing components" / "bundle size" | `references/component-patterns.md` |
| "Governance" / "contribution workflow" / "versioning" / "release" | `references/governance.md` |
| "What tech stack?" / "Tailwind vs Styled Components" | `references/tech-stack-comparison.md` |

**If ambiguous, ask:**
"Are you starting a new design system, adding components to an existing one, or documenting what you already have?"

</intake>

<routing>

| Workflow | Purpose | When to Read |
|----------|---------|--------------|
| `workflows/new-system.md` | Full setup: charter → tokens → structure → first components | Starting from zero |
| `workflows/add-component.md` | Design API → implement → test → document a single component | Adding to existing system |
| `workflows/document-system.md` | Storybook, component docs, getting-started guides | System exists, needs docs |

| Reference | Purpose | When to Read |
|-----------|---------|--------------|
| `references/token-architecture.md` | 3-tier token system, JSON format, Style Dictionary config | Setting up or modifying tokens |
| `references/component-patterns.md` | CVA variants, file structure, testing strategy, bundle optimization | Building or reviewing components |
| `references/governance.md` | Contribution flow, versioning, release automation, quality gates | Establishing team processes |
| `references/tech-stack-comparison.md` | CSS/JS framework tradeoffs (Tailwind+CVA, Styled Components, CSS Modules, Vanilla Extract) | Choosing or evaluating tech stack |

| Script | Purpose | When to Run |
|--------|---------|-------------|
| `scripts/build-tokens.js` | Transform token JSON into CSS/JS/iOS/Android outputs via Style Dictionary | After creating or modifying token files |
| `scripts/generate-component.js` | Scaffold a new component with implementation, tests, stories, and barrel export | Adding a new component to the library |

| Asset | Purpose | When to Use |
|-------|---------|-------------|
| `assets/starter-tokens.json` | Complete starter token file with colors, spacing, typography, shadows, radii | Bootstrapping a new token system |
| `assets/style-dictionary.config.json` | Ready-to-use Style Dictionary config for CSS + JS output | Setting up token build pipeline |
| `assets/storybook-theme.js` | Branded Storybook theme matching design system tokens | Configuring Storybook appearance |

**After reading the relevant workflow/reference, follow it exactly.**

</routing>

<quick_reference>

**Recommended stack:** Tailwind + CVA (class-variance-authority) for new systems

**Component file pattern:**
```
ComponentName/
├── ComponentName.tsx      (implementation)
├── ComponentName.test.tsx (tests)
├── ComponentName.stories.tsx (Storybook)
└── index.ts               (barrel export)
```

**Atomic design hierarchy:**
- `primitives/` — atoms (Button, Input, Text, Icon)
- `components/` — molecules (Card, FormField, SearchInput)
- `patterns/` — organisms (Navigation, Modal, DataTable)
- `layouts/` — templates (AppShell, Dashboard)

**Token tiers:**
- Tier 1: Primitive (raw values — `blue-500: #3b82f6` or `blue-500: oklch(60% 0.19 261)`)
- Tier 2: Semantic (contextual — `color-primary: {blue-500}`)
- Tier 3: Component (specific — `button-bg: {color-primary}`)

> **Color space note:** Define primitive tokens in OKLCH for new systems — perceptually uniform lightness produces consistent palette steps and smooth gradients. Keep hex fallbacks for browser compatibility. Existing locked brand profiles (FlashFusion v3, Loxihart) stay in hex — OKLCH is for new token authoring only.

**Quality gates for v1.0:**
- [ ] 20+ components documented
- [ ] WCAG 2.2 AA accessibility audited
- [ ] 80%+ test coverage
- [ ] Bundle size under 100KB gzipped
- [ ] Storybook deployed to public URL
- [ ] 2+ consuming products using the system
- [ ] Visual regression baseline established (`npx vizzly tdd` or Chromatic)

</quick_reference>

## CLAIMS

- [SOURCED] Three-tier token architecture (primitive → semantic → component) is the industry standard approach — documented in Style Dictionary, Theo, and Figma Variables
- [GENERATED] `sideEffects: false` in package.json is required for tree-shaking to work in webpack/Rollup — without it, all components are included even if only one is imported
- [GENERATED] CVA (class-variance-authority) over hand-rolled variant strings because it provides TypeScript inference on variant props at zero runtime cost beyond Tailwind itself

## GAPS / BLINDSPOTS / UNKNOWN-UNKNOWNS

- RSC (React Server Components) compatibility is a growing constraint on component library architecture — client/server component boundaries affect which hooks are safe
- CSS-only component approaches (no JS) are not covered — valid for static sites and performance-critical contexts
- Design system governance tooling (Chromatic, Zeroheight, Supernova) is mentioned but not evaluated
