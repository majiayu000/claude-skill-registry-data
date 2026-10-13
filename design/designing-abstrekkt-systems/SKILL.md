---
name: designing-abstrekkt-systems
description: >
  Compiles and applies the Abstrekkt brand design system — token-driven,
  accessibility-first, state-machine-correct UI architecture for Abstrekkt
  and FlashFusion products. Activates when building UI, designing components,
  generating design tokens, applying Abstrekkt visual identity, implementing
  Fraunces display typography, brass color palette (#c8a86a), or producing
  frontend architecture for any Abstrekkt sub-brand. Also triggers on:
  component factory, design system, token system, UX architecture, brand
  voice system, Reading Room aesthetic, accessibility enforcement, anti-slop
  gate, FlashFusion frontend, Crimson Pro body type, JetBrains Mono code type,
  design handoff package, construction not recovery UI, or any request to
  build, audit, or extend Abstrekkt-branded frontend output.
version: "1.0.0"
---

# Abstrekkt Design System

Token-driven, accessibility-first, state-machine-correct design system.
"Reading Room at Midnight" aesthetic. Earned authority over decoration.
Construction, not recovery.

## Authority Hierarchy (Immutable)

Conflicts resolve upward. No exceptions.

```
1. RUNTIME CODE COMPATIBILITY   ← absolute
2. DESIGN TOKEN CONSISTENCY     ← single source of truth
3. UI STATE MACHINE CORRECTNESS ← behavioral determinism
4. UX PATTERN CONSISTENCY       ← cohesion layer
5. BRAND VOICE CONSISTENCY      ← linguistic mapping
6. VISUAL AESTHETICS            ← derived, non-authoritative
```

---

## Quick-Start Decision Tree

```
What are you building?
  ├─ New component ──────── Load references/02-component-library.md
  │                          Follow: TypeScript interface → state machine
  │                          → token binding → ARIA → usage example
  ├─ Token question ─────── Load assets/tokens.json + assets/tokens.css
  │                          Rule: NO hardcoded values anywhere
  ├─ UX pattern ─────────── Load references/03-ux-architecture.md
  │                          Navigate → Form → Data → Feedback systems
  ├─ Brand copy/microcopy ── Load references/04-brand-voice.md
  │                          Pattern: declarative, tactical, no hedging
  ├─ Motion/animation ───── Load references/05-motion-system.md
  │                          Max: 500ms. Easing only. No bounce.
  ├─ Accessibility audit ─── Load references/06-accessibility.md
  │                          Floor: WCAG 2.1 AA. 4.5:1 contrast minimum.
  └─ Pre-ship gate ──────── Load references/07-acceptance-criteria.md
                             Run all 14 anti-slop checks before shipping.
```

---

## Usage Examples

**Example 1 — Build a new component**
Request: "Build a Badge component for Abstrekkt"
→ Load references/02-component-library.md
→ Define TypeScript props interface (no `any` types)
→ Map all states: default, hover, active, focus, disabled
→ Bind to tokens only (no raw values)
→ Add ARIA role, keyboard behavior
→ Produce production-ready `.tsx` file

**Example 2 — Apply brand voice to error state**
Request: "Write error copy for failed audit submission"
→ Load references/04-brand-voice.md
→ Pattern: present tense, actionable, specific
→ Result: "Submission failed. Check your connection and retry."
→ NOT: "Oops! Something went wrong. Please try again later."

**Example 3 — Token audit on existing component**
Request: "Audit this component for token compliance"
→ Scan all style values in the file
→ Flag any hardcoded hex, px, or rem not in assets/tokens.json
→ Produce replacement map: raw value → token name
→ Output patch diff

---

## Core Identity

| Dimension | Value |
|---|---|
| Primary color | `#c8a86a` (brass) → `--color-primary-400` |
| Ink color | `#1c1917` (deep brown-black) → `--color-neutral-900` |
| Display font | Fraunces (headings, CTAs) |
| Body font | Crimson Pro (prose, UI) |
| Code font | JetBrains Mono |
| Base unit | 4px (0.25rem) |
| Default radius | 0.375rem (rounded-base) |
| Motion max | 500ms |
| Contrast floor | 4.5:1 (WCAG 2.1 AA) |

---

## Golden Path: Token → Component → Ship

```
1. Token lookup
   └─ All values from assets/tokens.json
   └─ No hardcoded color, spacing, radius, shadow, duration

2. State machine definition
   └─ Every interactive component: default → hover → active
      → focus → loading → disabled → error (if applicable)

3. Props interface
   └─ TypeScript, strict types, no `any`
   └─ Variant enum-based (not string literals)

4. ARIA implementation
   └─ Role + keyboard behavior per references/06-accessibility.md
   └─ Focus ring: 2px primary-400, offset-2

5. Motion binding
   └─ Transitions tied to state transitions only
   └─ Durations from --duration-* tokens
   └─ Easing from --easing-* tokens

6. Self-verification
   └─ Run 14-point anti-slop gate (references/07-acceptance-criteria.md)
   └─ Confirm: 0 hardcoded values, 0 missing states, 0 ARIA gaps
```

---

## Hard Rules (Violations = Reject + Regenerate)

1. **No hardcoded values.** Every style maps to a token.
2. **No partial components.** Full state machine or remove it.
3. **No vague language.** Tactical specificity only.
4. **No missing error states.** Every form input has one.
5. **No invisible focus rings.** 2px minimum, visible on all backgrounds.
6. **No `any` types.** Strict TypeScript throughout.
7. **No placeholder copy.** Deliver per references/04-brand-voice.md patterns.

---

## Component Inventory

| Component | Template File | Status |
|---|---|---|
| Button | templates/Button.tsx | ✅ Complete |
| Input | templates/Input.tsx | ✅ Complete |
| Card | templates/Card.tsx | ✅ Complete |
| Modal | templates/Modal.tsx | ✅ Complete |
| Navbar | templates/Navbar.tsx | ✅ Complete |
| Table | templates/Table.tsx | ✅ Complete |
| Toast + Container | templates/Toast.tsx | ✅ Complete |
| ContactForm (integration) | templates/ContactForm.tsx | ✅ Complete |
| Example Page | templates/example-page.tsx | ✅ Complete |

---

## File Map

```
designing-abstrekkt-systems/
├── SKILL.md                              ← You are here
├── references/
│   ├── 01-design-tokens.md              ← Token architecture + rationale
│   ├── 02-component-library.md          ← Component specs + state machines
│   ├── 03-ux-architecture.md            ← Navigation, layout, form, data, feedback
│   ├── 04-brand-voice.md                ← Microcopy + messaging framework
│   ├── 05-motion-system.md              ← Transitions + keyframes + rules
│   ├── 06-accessibility.md              ← WCAG 2.1 AA + ARIA + contrast ratios
│   └── 07-acceptance-criteria.md        ← Anti-slop gates + acceptance tests
├── assets/
│   ├── tokens.json                      ← DTCG format, source of truth
│   ├── tokens.css                       ← CSS variable export
│   └── tailwind.config.ts               ← Tailwind bridge config
└── templates/
    ├── Button.tsx
    ├── Input.tsx
    ├── Card.tsx
    ├── Modal.tsx
    ├── Navbar.tsx
    ├── Table.tsx
    ├── Toast.tsx
    ├── ContactForm.tsx
    ├── example-page.tsx
    └── globals.css
```

---

## Self-Verification Checklist

Before shipping any design system output:

- [ ] All style values reference tokens (zero hardcoded)
- [ ] All components have complete state machines
- [ ] TypeScript: zero `any` types
- [ ] ARIA roles and attributes present on all interactive elements
- [ ] Focus rings visible (2px primary-400, offset-2)
- [ ] Contrast ratios ≥ 4.5:1 (WCAG 2.1 AA)
- [ ] Motion durations ≤ 500ms, easing curves only
- [ ] Brand voice matches references/04-brand-voice.md patterns
- [ ] 14-point anti-slop gate passed (references/07-acceptance-criteria.md)
- [ ] No placeholder content in deliverable

---

## CLAIMS
- [SOURCED] WCAG 2.1 AA requires 4.5:1 contrast for normal text, 3:1 for large text (≥18pt regular or ≥14pt bold)
- [SOURCED] Fraunces, Crimson Pro, JetBrains Mono are the defined Abstrekkt typefaces per brand identity
- [SOURCED] Brass (#c8a86a) is the Abstrekkt primary brand color
- [GENERATED] Token naming conventions follow DTCG (Design Tokens Community Group) schema for interoperability

## COUNTEREXAMPLE
- A component passing all 14 anti-slop checks can still fail in production if the TypeScript config is not strict mode — enforce `"strict": true` in tsconfig.json
- Correct contrast ratio on desktop may fail on mobile due to smaller rendered font size — test at actual render sizes

## CONTRADICTIONS
- "Progressive disclosure" in references/ reduces SKILL.md size but adds load latency — for time-critical interactions, inline the critical path
- Token-only styling prevents rapid iteration — acceptable tradeoff; token system must be updated when brand evolves
