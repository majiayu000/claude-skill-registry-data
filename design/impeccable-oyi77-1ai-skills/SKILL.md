---
name: impeccable
description: "Use when designing, redesigning, shaping, critiquing, auditing, polishing, animating, or hardening frontend interfaces: websites, dashboards, SaaS apps, mobile screens. Enforces 24 design commands, PRODUCT.md/DESIGN.md artifacts, 4 surface modes (Persuade, Operate, Read, Experience), and strict craft floor against generic AI slop."
domain: content
author: oyi77
version: 4.7.1
category: content
tags:
- design
- frontend
- ui
- ux
- design-system
- impeccable
- anti-slop
- polish
- audit
- critique
triggers:
- "impeccable"
- "design system"
- "critique design"
- "audit design"
- "polish ui"
- "shape feature"
- "init design"
- "document design"
- "craft floor"
- "bolder ui"
- "quieter ui"
- "distill ui"
- "harden ui"
- "animate ui"
- "colorize ui"
- "typeset ui"
- "delight ui"
- "overdrive ui"
- "clarify copy"
- "adapt ui"
- "optimize ui"
- "live variant"
- "onboard flow"
- "redesign ui"
- "revamp ui"
- "restyle component"
- "polish interface"
license: Apache-2.0
subdomain: design
---
# Impeccable

A comprehensive design operating system and language for AI coding agents based on [pbakaus/impeccable](https://github.com/pbakaus/impeccable). Provides a structured 24-verb design vocabulary, dual-truth artifact separation (`PRODUCT.md` for business truth, `DESIGN.md` for visual truth), 4 surface archetypes (Persuade, Operate, Read, Experience), and a deterministic Craft Floor that eliminates generic AI slop, cards-inside-cards, unearned gradients, and un-tinted grays.

## Overview

Most AI models were trained on the same corporate SaaS templates, resulting in repetitive failure modes: Inter for every font, saturated purple-to-cyan gradients, centered three-card hero sections, gray text on colored backgrounds, and rounded-square icon tiles above every heading.

`impeccable` breaks this convergence by introducing:
1. **Durable Context Separation**: Captures durable audience, purpose, and constraints in `PRODUCT.md`, while isolating visual rules, tokens, and font pairings in `DESIGN.md`.
2. **24 Actionable Commands**: Structured verbs covering planning (`shape`, `init`), creation (`document`, `extract`), evaluation (`critique`, `audit`), refinement (`polish`, `bolder`, `quieter`, `distill`, `harden`), and enhancement (`animate`, `colorize`, `typeset`, `layout`, `delight`).
3. **4 Surface Modes**: Tailors visual ambition to the user's intent—Persuade (marketing/landing), Operate (dense web apps/dashboards), Read (documentation/articles), and Experience (portfolios/showcases).
4. **The Craft Floor**: Strict mechanical invariants enforced before any code is committed.

```
[Phase 1: Init / Context] ──────► [Phase 2: Surface Mode & Shape]
   │ (PRODUCT.md)                         │ (Persuade / Operate / Read / Experience)
   ▼                                      ▼
[Phase 4: Floor & Polish] ◄───── [Phase 3: Code & Tokens (DESIGN.md)]
   │ (Contrast, Spacing, States)
   ▼
[Shipped Production Interface]
```

## When to Use

- When building or redesigning websites, web applications, landing pages, dashboards, or mobile interfaces.
- When shaping UX/UI requirements before writing frontend implementation code (`/impeccable shape`).
- When conducting UX critique reviews on hierarchy, cognitive load, and emotional resonance (`/impeccable critique`).
- When executing technical quality audits for accessibility, performance, and responsive behavior (`/impeccable audit`).
- When performing a final polish pass to eliminate visual bugs and establish shipping readiness (`/impeccable polish`).
- When toning down aggressive designs (`/impeccable quieter`) or amplifying bland, timid layouts (`/impeccable bolder`).
- When hardening error states, empty states, input validations, and overflow edge cases (`/impeccable harden`).
- When establishing or reverse-engineering design tokens and CSS custom properties into a canonical `DESIGN.md`.

## When NOT to Use

- When writing backend APIs, database migrations, or business logic without UI (use `development/role-software-engineer`).
- When conducting cybersecurity assessments or network penetration tests (use `cybersecurity/role-penetration-tester`).
- When managing cloud infrastructure, Docker, or Kubernetes clusters (use `devops/role-devops-sre-engineer`).
- When writing purely technical documentation or user manuals without styling (use `operations/role-product-manager`).

## Surface Modes

Every surface must explicitly declare one of four visitor success archetypes:

| Surface Mode | Purpose & User Goal | Visual Ambition & Constraints |
|---|---|---|
| **Persuade** | Visitor decides and acts; design IS the product (landing pages, pricing tables, sales funnels). | Full commitment: bold point-of-view, distinctive art direction, authentic imagery, zero unearned cards. |
| **Operate** | Visitor completes a task (dashboards, admin panels, devtools, editors, settings). | Precision and restraint: scannability, dense tabular data, clear selection states, native affordances outrank expression. |
| **Read** | Visitor understands information (documentation, changelogs, knowledge bases, long-form articles). | Optimized reading flow: 65-75ch measure, disciplined typographic hierarchy, high-contrast legibility, no distracting motion. |
| **Experience** | Visitor is immersed inside the work itself (portfolios, interactive showcases, media galleries). | Artifact leads from the first viewport; interface chrome recedes into the background. |

## Dual-Truth Artifact System: PRODUCT.md vs DESIGN.md

Impeccable strictly isolates product business truth from visual execution:

### 1. PRODUCT.md (Durable Context)
Created via `/impeccable init`. Contains:
- **Audience**: Who uses the product, their mental model, and domain expectations.
- **Purpose**: What core problem the surface solves.
- **Constraints**: Hard technical limits (frameworks, browser support, compliance).
- **Voice**: Tone and communication register (direct, authoritative, playful).
- **Invariants**: Business rules that must never break regardless of visual styling.

### 2. DESIGN.md (Visual System)
Created or updated via `/impeccable document`. Contains:
- **Tokens**: `:root` CSS custom properties for color, spacing, radius, and elevation.
- **Typography Scale**: Display, heading, body, and monospace font pairings with explicit line heights and tracking.
- **Color System**: Canvas, surface, borders, primary brand accents, and functional states (error, warning, success).
- **Component Rules**: Button ergonomics, card constraints, form field states, and motion parameters.

## The 24 Impeccable Design Commands

| Command | Category | Objective & Actionable Playbook | Reference |
|---|---|---|---|
| `craft [feature]` | Build | Full shape-then-build flow with iterative visual feedback. | `references/craft.md` |
| `shape [feature]` | Build | Plan UX architecture, user journeys, and component boundaries before code. | `references/shape.md` |
| `init` | Build | Capture durable product truth and invariants in `PRODUCT.md`. | `references/init.md` |
| `document` | Build | Extract and document existing CSS tokens and component rules into `DESIGN.md`. | `references/document.md` |
| `extract [target]`| Build | Pull reusable tokens, utilities, and components into the design system. | `references/extract.md` |
| `critique [target]`| Evaluate| Heuristic UX design review: cognitive load, hierarchy, and clarity. | `references/critique.md` |
| `audit [target]` | Evaluate| Technical audit: text contrast (>=4.5:1), touch targets (>=44px), CLS, a11y. | `references/audit.md` |
| `polish [target]` | Refine | Final shipping pass: alignment, micro-spacings, hover/active states, borders. | `references/polish.md` |
| `bolder [target]` | Refine | Amplify safe, corporate, or timid designs with strong typographic scale and color. | `references/bolder.md` |
| `quieter [target]`| Refine | Tone down overstimulating, cluttered, or excessively saturated UIs. | `references/quieter.md` |
| `distill [target]`| Refine | Strip unnecessary visual noise, nested wrappers, and redundant containers. | `references/distill.md` |
| `harden [target]` | Refine | Robust edge-case engineering: error boundaries, empty states, text overflow, i18n. | `references/harden.md` |
| `onboard [target]`| Refine | Design activation flows, first-run empty states, and progressive disclosure. | `references/onboard.md` |
| `animate [target]`| Enhance | Add purposeful motion using physics springs and cubic-bezier curves. | `references/animate.md` |
| `colorize [target]`| Enhance | Introduce intentional, strategic accent hues to monochrome layouts. | `references/colorize.md` |
| `typeset [target]` | Enhance | Upgrade font pairings, measure (65-75ch), line height, and tracking. | `references/typeset.md` |
| `layout [target]`  | Enhance | Fix grid rhythm, vertical cadence, flex alignments, and responsive wrapping. | `references/layout.md` |
| `delight [target]` | Enhance | Add memorable signature micro-interactions and tactile feedback moments. | `references/delight.md` |
| `overdrive [target]`| Enhance| Implement advanced shader, canvas, WebGL, or complex geometric effects. | `references/overdrive.md` |
| `clarify [target]` | Fix | Rewrite ambiguous microcopy, form field labels, tooltips, and error alerts. | `references/clarify.md` |
| `adapt [target]`   | Fix | Optimize responsive behavior across mobile, tablet, desktop, and foldables. | `references/adapt.md` |
| `optimize [target]`| Fix | Improve rendering performance, reduce DOM depth, eliminate repaints. | `references/optimize.md` |
| `live`             | Iterate | Visual variant mode: select live DOM nodes in browser for iterative styling. | `references/live.md` |
| `generate [target]`| Iterate | Autonomously generate distinct design alternatives for named elements. | `references/generate.md` |

## The Craft Floor (Strict Anti-Patterns & Refusals)

Every generated UI must satisfy the Craft Floor before completion:

```
[VERIFY]
- Contrast: Body text >= 4.5:1, large display >= 3:1 against computed background.
- Typography: Body measure 65-75ch, tracking >= -0.04em, no raw un-tinted gray text.
- States: Every interactive element has Default, Hover, Active, Focus-Visible, Disabled, Loading.
- Motion: Never transition: all. Never animate width, height, top, or left. Use transform and opacity.
- Browser Surfaces: Style custom scrollbars, selection highlight (::selection), and focus rings.

[REFUSE / BANNED]
- No cards nested inside cards. Cards are not a substitute for spatial hierarchy.
- No purple-to-cyan or violet-to-blue linear gradients on text, buttons, or card borders.
- No unearned blur or floating decorative glowing orbs.
- No kicker / eyebrow tags floating above headings (headings must carry their own weight).
- No pure black (#000000) or pure gray (#808080); always tint darks and neutrals from palette.
- No unicode emoji in UI copy, badges, buttons, or navigation; use clean SVG icons.
```

## Process

1. **Context Ingestion**: Run or read `PRODUCT.md` to establish audience, purpose, and constraints.
2. **Surface Archetype**: Commit explicitly to Persuade, Operate, Read, or Experience.
3. **Design System Tokenization**: Declare all color, typography, spacing, and radius tokens in `:root` (`DESIGN.md`).
4. **Execution via Command Playbook**: Select and execute the matching Impeccable command (`shape`, `craft`, `critique`, `polish`, etc.).
5. **Craft Floor Audit**: Verify contrast ratios, button ergonomics, focus rings, state coverage, and ban compliance.
6. **Delivery & Evidence**: Capture rendered DOM telemetry or visual screenshots verifying zero slop and complete state coverage.

## Workflow

### Step 1: Initialize Context & Document System
```bash
# 1. Inspect existing project context
cat PRODUCT.md 2>/dev/null || echo "Creating PRODUCT.md via init flow..."

# 2. Extract or define CSS design tokens
cat << 'EOF' > styles/tokens.css
:root {
  --canvas-bg: #090a0f;
  --surface-base: #11131b;
  --surface-raised: #181b26;
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-strong: rgba(255, 255, 255, 0.16);
  --text-primary: #f0f2f5;
  --text-secondary: #9aa0a6;
  --accent-brand: #00f0ff;
  --accent-glow: rgba(0, 240, 255, 0.12);
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --font-sans: 'Geist Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  --ease-spring: cubic-bezier(0.16, 1, 0.3, 1);
}
EOF
```

### Step 2: Build Component with Full State Coverage
```html
<button class="impeccable-btn" type="button" aria-busy="false">
  <svg class="icon" aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M5 12h14M12 5l7 7-7 7"/>
  </svg>
  <span>Execute Pipeline</span>
</button>

<style>
.impeccable-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 40px;
  padding: 0 16px;
  font-family: var(--font-sans);
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  background-color: var(--surface-raised);
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-sm);
  cursor: pointer;
  outline: none;
  transition: transform 150ms var(--ease-spring), border-color 150ms ease, box-shadow 150ms ease;
}

.impeccable-btn:hover {
  border-color: var(--accent-brand);
  box-shadow: 0 0 12px var(--accent-glow);
}

.impeccable-btn:active {
  transform: scale(0.98);
}

.impeccable-btn:focus-visible {
  box-shadow: 0 0 0 2px var(--canvas-bg), 0 0 0 4px var(--accent-brand);
}

.impeccable-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}
</style>
```

### Step 3: Run Deterministic Audit Check
```python
def verify_craft_floor(css_content: str) -> list[str]:
    violations = []
    if "transition: all" in css_content:
        violations.append("Banned: 'transition: all' detected. Use explicit properties.")
    if "#000000" in css_content or "#808080" in css_content:
        violations.append("Banned: Untinted pure black/gray detected. Tint with palette.")
    if "linear-gradient(to right, rgb(139, 92, 246)" in css_content or "from-violet" in css_content and "to-cyan" in css_content:
        violations.append("Banned: Generic purple-to-cyan gradient detected.")
    return violations
```

## Verification

- [ ] `PRODUCT.md` exists or durable business context (audience, purpose, invariants) is established.
- [ ] Surface archetype is explicitly classified: Persuade, Operate, Read, or Experience.
- [ ] Design tokens declared at `:root` for color, typography, spacing, and radius.
- [ ] Zero unearned cards-in-cards or centered 3-card hero sections.
- [ ] Text contrast meets WCAG AA (>= 4.5:1 for body, >= 3:1 for display).
- [ ] Motion adheres to physics easing (`cubic-bezier` or spring); zero `transition: all`.
- [ ] Interactive controls provide default, hover, active press, focus-visible, and disabled states.
- [ ] Zero emojis in UI components; SVG vector iconography used exclusively.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "A centered 3-card layout looks standard for SaaS." | It is the ultimate generic AI trope. Ground the layout in the surface mode (Persuade/Operate) with authentic visual hierarchy. |
| "Purple-to-cyan gradient makes the hero button pop." | Saturated tech gradients look dated and amateur. Use high-contrast solid brand fills or subtle dark glass with crisp 1px borders. |
| "I'll use Inter because it's clean and safe." | Defaulting to Inter for every project signals lack of intent. Pick a deliberate display and body pairing that reflects the product voice. |
| "Cards inside cards help group related settings." | Nested cards create claustrophobic visual clutter. Use typography scale, hairline dividers, and intentional whitespace for grouping. |
| "We can add focus rings and keyboard states later." | Accessible focus states (`:focus-visible`) are foundational. Without them, keyboard navigation is completely broken. |
| "Emoji make the buttons feel friendly and modern." | Emojis break enterprise brand integrity and render inconsistently across OS platforms. Always use crisp SVG vector icons. |

## Sub-Skills & Specialized Playbooks

| Sub-Skill | Trigger / Kasus Penggunaan | Berkas Referensi |
| :--- | :--- | :--- |
| `emil-design-skills` | Refining interface motion, UI craft, animation standards, and prototyping decisions | [SKILL.md](../emil-design-skills/SKILL.md) |
| `better-interface` | Cross-discipline interface review across accessibility, layout, writing, typography, color, and UI polish | [SKILL.md](../better-interface/SKILL.md) |
| `interface-review` | Change-scoped review of a branch, PR, or uncommitted diff | [SKILL.md](../interface-review/SKILL.md) |
| `variant` | Exploring design alternatives for one component | [SKILL.md](../variant/SKILL.md) |
| `break` | Stress-testing one component under worst-case scenarios | [SKILL.md](../break/SKILL.md) |
| `state-machine` | Rendering every state of one component on a throwaway page | [SKILL.md](../state-machine/SKILL.md) |
| `build-design` | Building UI from a Figma file or design image | [SKILL.md](../build-design/SKILL.md) |
