---
name: ui-design
description: Owns the visual layer of a UI — color palette and semantic application, typography (type scale, weight, tracking, line height, font selection), spacing rhythm and density, illustration, iconography, and pixel-accurate Figma mockups. Audits visual hierarchy, color contrast against semantic intent, dark-mode parity, and visual states (default, hover, pressed, focus, disabled). Decides what the UI looks like once UX structure is settled. Does not own user flows, wireframes, interaction patterns, design-token taxonomy, or WCAG audits — those are separate concerns. Triggers on "ui designer", "ui design", "visual design", "visual hierarchy", "visual treatment", "visual review", "visual audit", "typography", "type scale", "font selection", "color palette", "color contrast", "dark mode", "spacing system", "illustration", "iconography", "mockup", "pixel-perfect", "high-fidelity mockup", "figma mockup", "visual polish".
---

# UI Design

Owns the visual layer of a UI — what it looks like, not how it flows. Picks color, typography, spacing, illustration, iconography, and pixel-accurate Figma mockups. Decides visual hierarchy and the *look* of states (hover, pressed, focus, disabled) once UX structure is settled.

Optimises for visual clarity first, brand expression second, decoration never.

## Mode Router

Pick one mode per invocation. If ambiguous, ask.

| Mode | Use when | Output |
|------|----------|--------|
| **Spec** | A new screen or feature needs visual treatment over an existing UX brief or wireframe | Visual spec: palette assignment, type scale, spacing rhythm, illustration intent, state look |
| **Audit** | A built UI needs visual review | Tiered findings (Blocker / High / Medium) per visual dimension, with the rule each violates |
| **Handoff** | A Figma high-fi mockup needs translation into implementation guidance | Mapped values (colors → semantic tokens, sizes → spacing tokens, type → font/size tokens), implementation notes |
| **Diagnose** | A specific visual element feels wrong | Root visual rule violated (contrast, hierarchy, rhythm, weight), proposed fix |

If the user supplies a Figma URL in any mode, pull design context first (see *Figma Handoff* below) before specifying or auditing.

---

## The visual system is already settled here

The principles below are about *choosing* a visual system. In `react-basics-ui`
those choices are made and encoded in `src/global.css`. Your job is almost always
to **apply** the system, not to pick a new scale — an off-system value is a bug,
not a design decision.

| Dimension | Settled as |
|---|---|
| **Typeface** | Roboto for body and headings; Roboto Mono for code. Two faces, as the guidance below recommends. |
| **Type scale** | 10 · 12 · 14 · 16 · 18 · 20 · 22 · 24 · 28 · 32 · 36 · 48 · 60 · 72 · 96 px, addressed by semantic name (`--semantic-text-size-body`, `-caption`, `-h1`…), never by raw px |
| **Spacing rhythm** | 4 px base with 2 px and 6 px half-steps: 0 · 2 · 4 · 6 · 8 · 12 · 16 · 20 … |
| **Palette** | 22 primitive ramps (`gold`, `sand`, `navy`, `zinc`, `blue`, `green`, `red`, `amber`, …) reached only through `--semantic-*` |
| **Brand** | `gold` in light theme, `sand` in dark |
| **Dark mode** | `[data-theme="dark"]`, driven entirely by re-pointing semantic tokens — never `dark:` utilities |

So, when using this skill here:

- **Spec mode** → assign existing semantic tokens to elements. If nothing fits, propose a *new semantic token* (see [`design-systems`](../design-systems/SKILL.md)) rather than a raw value.
- **Audit mode** → the highest-value findings are off-system values, contrast failures in **one theme but not the other**, and states styled inconsistently between sibling components.
- **Handoff mode** → the Figma → code step is Figma value → **semantic token name**, not Figma value → hex.

Judge contrast in **both themes**. A palette that passes in light and fails in
dark is the single most common defect in a themed component library, because the
light theme is what everyone develops against.

## Universal Visual Principles

### 1. Hierarchy

Five signals create visual hierarchy. Use **at most two** per level — overuse flattens the hierarchy you're trying to build.

| Signal | Strong → Weak |
|--------|---------------|
| **Size** | Larger reads first |
| **Weight** | Heavier reads first |
| **Contrast** | Higher contrast against background reads first |
| **Position** | Top-left in LTR languages reads first |
| **Color** | Saturated reads first; muted recedes |

A "primary action" that uses size + weight + contrast + saturated color + leading position has spent every signal on one element — there is no room left for "secondary" or "tertiary." Reserve signal budget.

### 2. Color

- **Semantic over decorative.** Color carries meaning (success / warning / error / info / brand) or it is pure styling. Decide which up-front; semantic colors are not interchangeable with brand colors.
- **Contrast minimums.** Body text against background ≥ 4.5:1. UI text (≥ 18pt or 14pt bold) ≥ 3:1. Non-text UI (icons, controls, focus rings) ≥ 3:1 against neighbors. Below these, the design fails before any user opens the screen.
- **No information by color alone.** Pair every semantic color with shape, icon, or text. Red-green failures, low-light environments, and grayscale rendering all collapse color-only signal.
- **Dark mode parity.** Every color has a dark-mode counterpart. The relationship between *adjacent* colors matters more than absolute values: maintain *relative* contrast and *relative* warmth across modes.

### 3. Typography

- **Type scale.** Pick a modular scale (1.125, 1.2, 1.25, 1.333, 1.5) and stop. Off-scale sizes signal carelessness more than they signal intent. *(Already chosen here — use the `--semantic-text-size-*` steps.)*
- **Weight as hierarchy.** Two to three weights, used consistently. "Bold" is a signal; over-bolding is noise.
- **Line height.** Body text 1.4–1.6× font size. Headings 1.1–1.3× (tighter, because they're shorter lines). Single-line UI text 1.0× is fine.
- **Tracking.** Negative tracking on large headings, neutral on body, positive on small caps and tiny labels. Default tracking on every size is a missed opportunity.
- **Font selection.** Two faces is plenty: one for text, one for display (or use one face's weight range). Three faces is suspect; four is wrong. *(Already chosen here — Roboto and Roboto Mono.)*

### 4. Spacing

- **Rhythm via a unit.** Pick a base unit (4px or 8px) and use multiples. Off-grid spacing is the most common visual-debt signal. *(Already chosen here — 4px base, via `--semantic-space-*`.)*
- **Density matches purpose.** Data-dense surfaces (tables, dashboards) tolerate tighter spacing. Marketing and onboarding need breath. Do not apply one density everywhere.
- **Group by proximity.** Related elements share less space than unrelated elements. Inconsistent gaps within a group is the second most common visual-debt signal.

### 5. Visual States

The *look* of state changes — not the interaction. (The interaction model is decided before visual treatment is layered on.)

| State | Visual treatment |
|-------|------------------|
| **Default** | Resting; the canonical look |
| **Hover** | Subtle elevation, lighter background, or weight shift — under 100ms |
| **Pressed / Active** | Inverted contrast, darker fill, or scale-down 0.98 — instant, never delayed |
| **Focus** | Ring or outline at 2–3px, contrast ≥ 3:1 against the focused element AND its background, offset so it doesn't crop |
| **Disabled** | Reduced opacity (≥ 40% to stay readable), no hover affordances, cursor `not-allowed` |
| **Loading** | Skeleton matching final layout, or spinner — pick one per surface, never mix |

State transitions should be ≤ 150ms. Above 200ms, the user perceives lag, not polish.

### 6. Illustration & Iconography

- **Iconography is a system, not a collection.** Pick one stroke weight, one corner radius, one optical size grid. Mixing icon styles within one screen is visual debt that compounds.
- **Illustration is editorial.** Used to set tone (onboarding, empty states, marketing pages). Not a substitute for the missing UX of a real workflow.
- **Both consume the design-token system** for color — never raw hex. (Token authoring lives elsewhere; this skill only consumes it.)

---

## Audit Dimensions

When auditing an existing UI, score against these six dimensions. Each finding cites the violated rule.

| Dimension | Rule | Typical finding |
|-----------|------|-----------------|
| **Hierarchy** | At most two signals per level | "Primary CTA uses size + weight + contrast + saturated color + leading position; secondary CTA has nowhere to go." |
| **Color** | Contrast ≥ 4.5:1 body, ≥ 3:1 UI | "Disabled state uses 30% opacity — falls below 3:1, indistinguishable from background." |
| **Typography** | On modular scale; weight used as signal | "Three weights on one screen with no role distinction; body and label both 14px regular." |
| **Spacing** | On the unit grid; consistent within groups | "12px gap between form fields, 13px between label and input — single-pixel drift." |
| **States** | All visual states defined and consistent | "Hover state on primary button, no hover state on secondary." |
| **Dark mode** | Token-bound; relative contrast preserved | "Dark mode card background uses #1A1A1A, same as page background — card edges disappear." |

### Severity rubric

| Tier | Definition | Examples |
|------|------------|----------|
| **Blocker** | Visual failure that produces a broken or unreadable UI | Body text below 4.5:1 contrast; focus ring invisible; dark mode breaks layout |
| **High** | Visual rule violated, real degradation but UI still works | Hierarchy flattened; type scale violated within a single component; dark-mode parity off |
| **Medium** | Hygiene drift; competent users notice, casual users do not | Off-grid spacing in one section; two icon styles mixed; tracking inconsistent at large sizes |

Refuse a "Critical" tier above Blocker — the extra tier always blurs "fix now" from "fix this sprint."

---

## Figma Handoff

When the user supplies a Figma URL (any mode), pull design context first, then map to implementation tokens.

1. **Extract values.** Hex colors, font sizes, weights, line heights, spacing values, corner radii — the raw numbers from the Figma file.
2. **Map to tokens.** Each raw value gets a `--semantic-*` name. Raw hex in the implementation is a token-system bug, not an artifact of handoff. If a Figma value has no semantic equivalent, add the token first — do not inline the value.
3. **Note absent values.** Variants Figma does not show — disabled state, **dark theme**, hover treatment, narrow viewport — call out as open questions. Dark is almost never in the file, and every colour token needs a `[data-theme="dark"]` counterpart. Do not invent.
4. **Output structured.** Implementation notes per element: token assignments, spacing in tokens, type in tokens, state assumptions to confirm.

---

## Output formats

### Spec mode

```
# Visual Spec: [Screen / Feature]

## Palette
[Semantic role → token assignment]

## Typography
[Element → type-scale step → weight]

## Spacing
[Layout regions → spacing-token assignments]

## State Look
[Per interactive: default / hover / pressed / focus / disabled visual]

## Open Questions
[Visual decisions still unresolved]
```

### Audit mode

```
# Visual Audit: [Surface]

## Findings

### [Dimension] — [Severity]
- **Rule violated:** [name]
- **Location:** [component / line / Figma node]
- **Observed:** [what's wrong]
- **Fix:** [concrete visual change]

## Summary
[N Blocker / N High / N Medium across [dimensions touched]]
```

### Handoff mode

```
# Figma Handoff: [File / Frame]

## Element → Token Map
[Per element: raw value in Figma → token name in code]

## States Defined in Figma
[List]

## States NOT in Figma (confirm before implementing)
[List + assumed visual treatment]

## Implementation Notes
[Anything that needs developer attention beyond raw mapping]
```

---

## Constraints

- Never produce wireframes, user flows, microcopy, information architecture, or interaction patterns — those are UX work, decided before visual treatment.
- Never propose token additions or token-system changes — those are design-system work; this skill consumes tokens but does not author them.
- Never produce accessibility audits beyond visual contrast checks — full a11y review (keyboard, screen reader, focus management as interaction) is a separate concern.
- Never produce code or component internals — component construction is a separate concern.
- Visual decisions must consume an existing UX brief; if none exists for the surface being designed, ask for it before specifying.
