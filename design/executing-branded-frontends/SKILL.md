---
name: executing-branded-frontends
description: "Executes production HTML and React artifacts from Loxihart or FlashFusion brand token profiles. Runs mandatory 5-question design gate and 4-gate anti-slop audit before every output. Activates on: build a dashboard, make a component, create an artifact, code this UI, HTML artifact, React component, Loxihart UI, FlashFusion component, brand tokens, design gate, anti-slop audit. Does NOT activate for general UI builds without a brand profile — use the public frontend-design skill instead."
metadata:
  version: "2.1.0"
allowed-tools: "Read, Write"
---

# Executing Branded Frontends — Code Execution Layer

Senior frontend engineer with locked brand context. Operates from confirmed
design briefs and approved token profiles only. Aesthetic direction lives in
`managing-design-briefs` and `elite-ui-design`. This skill ships code.

---

## Core Rule

**Design gate before code. Always. No exceptions.**

If no brief exists for the requested component — stop, run the intake in
`references/design-gate.md`, wait for confirmation, then generate.

---

## Quick-Start Decision Tree

```
Request arrives
  ├─ New artifact / component ──── Design gate → references/design-gate.md
  │                                 ↓
  │                              Which profile?
  │                              ├─ Loxihart ──────── designs/Loxihart-tokens.md
  │                              └─ FlashFusion ─ designs/FlashFusion-tokens.md
  │                                 ↓
  │                              Which output?
  │                              ├─ HTML artifact ── templates/html-artifact.html
  │                              └─ React artifact ── templates/react-component.jsx
  │                                 ↓
  │                              Code → Anti-slop audit → workflows/anti-slop-audit.md
  │                                 ↓
  │                              Deliver
  │
  ├─ Add motion/animation ──────── references/animation-system.md
  ├─ Typography question ───────── references/typography-system.md
  ├─ Accessibility check ───────── references/accessibility.md
  └─ See example output ─────────── examples/
```

---

## Workflow: New Component or Artifact

### Step 1 — Design Gate (mandatory)
Read `references/design-gate.md`.
Run the 5-question intake. Do not skip even one question.
No code is written until the gate is passed.

### Step 2 — Token Load
Based on the confirmed profile:
- Loxihart → read `designs/Loxihart-tokens.md`
- FlashFusion → read `designs/FlashFusion-tokens.md`
- Custom → extract tokens from the brief

Apply tokens as CSS variables at `:root`. Never hardcode hex values in component styles.

### Step 3 — Output Selection
- **HTML artifact** → `templates/html-artifact.html` — single-file, no build step, Claude.ai chat window
- **React artifact** → `templates/react-component.jsx` — hooks, state, Tailwind or CSS-in-JS, Claude.ai JSX

### Step 4 — Generate
Follow the design decisions locked in the brief. Implement:
- Typography from `references/typography-system.md`
- Motion from `references/animation-system.md` (if applicable)
- Accessibility from `references/accessibility.md` (non-negotiable)
- All states: empty, loading, error, success, hover, focus, disabled

### Step 5 — Anti-Slop Audit
Read `workflows/anti-slop-audit.md` and run all 4 gates before delivering.
Do not suppress failures — fix them.

---

## Code Standards

**Functional**
- Works on first render — no TODO stubs, no placeholder functions
- State management complete — no half-wired handlers
- Error and empty states implemented — never blank

**Typed and validated**
- React: PropTypes or TypeScript interfaces on all components
- Inputs: validated, escaped, never raw-interpolated into DOM

**Accessible**
- ARIA roles on custom interactive elements
- Focus rings visible and styled (not removed)
- Color contrast ≥ 4.5:1 for normal text, ≥ 3:1 for large text
- Keyboard navigable

**Performant**
- Animations on `transform` + `opacity` only (no layout-triggering props)
- Images: `width` + `height` set, `loading="lazy"` below fold
- No inline styles for values that change frequently — use CSS variables

**Distinctive**
- Font choice justified — no system-ui, no generic sans fallbacks as primary
- Color usage follows profile or brief token system
- Layout has at least one intentional asymmetry or grid-breaking element
- Background is atmospheric — not a flat solid unless intentional

---

## Anti-Pattern Blacklist

| Anti-pattern | Why it fails |
|---|---|
| `font-family: Inter, system-ui` as primary | Generic. 40% of AI UIs default here. |
| Purple gradient on white background | Category default. Instantly forgettable. |
| Card grid as primary layout | Default Tailwind dashboard smell. |
| Shallow glassmorphism as entire aesthetic | 2021 trend, now a slop signal. |
| `#ffffff` or `#000000` as background | Always off-white or near-black. |
| Sidebar without written justification | Adds chrome, hides hierarchy. |
| Tooltip as only affordance | Invisible until hover. Not accessible. |
| Spinner as loading state | No skeleton, no optimistic UI. Low effort. |
| "Clean and modern" in any comment | Describes nothing. Cut it. |
| Accent color >10% of visible surface | Dilutes emphasis. Everything becomes accent. |

---

## Profile Reference

Load only the relevant profile — never both simultaneously.

| Profile | Token file | Aesthetic summary |
|---|---|---|
| Loxihart | `designs/Loxihart-tokens.md` | Void surface, electric violet, Space Grotesk + Inter, flat cards, dense enterprise |
| FlashFusion | `designs/FlashFusion-tokens.md` | Void-dark (#0B0B14), semi-transparent blur(12px) cards, Instrument Serif + Geist + Geist Mono, violet/magenta/cyan gradient |

> ⚠ Deprecated FF tokens (v2 → do not use): Poppins as heading, JetBrains Mono, Instrument Sans,
> flat black cards, #0F0618/#1A0B2E surfaces, #F472B6 magenta, 90deg gradient.

**Cross-profile isolation is mandatory.**

---

## Output Quality Bar

Before delivering, confirm:
1. Clear point of view — one visual decision that makes it memorable
2. All states implemented (empty, loading, error, success)
3. Passes all 4 anti-slop audit gates
4. A senior designer would not be embarrassed by this

If any answer is no — fix before delivering.
