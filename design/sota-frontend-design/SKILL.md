---
name: sota-frontend-design
description: >
  State-of-the-art web design, UI/UX, and motion engineering standards (2026). Use when building
  OR auditing/reviewing user interfaces: components, pages, design systems, stylesheets, themes,
  forms, navigation, animations, or accessibility. Covers typography, color (OKLCH, dark mode),
  spacing/layout (grid, container queries, subgrid), design tokens and component APIs, UX patterns
  (forms, loading/empty/error states, destructive actions), WCAG 2.2 AA accessibility, motion
  design, and responsive/modern CSS. Trigger keywords: UI, UX, web design, CSS, component,
  accessibility, a11y, responsive, animation, motion design, design system, layout, typography,
  dark mode, design tokens, frontend review, WCAG.
---

# SOTA Frontend Design

## Purpose

Make every interface this agent builds — and every interface it reviews — meet 2026
state-of-the-art for visual craft, UX, accessibility, motion, and CSS architecture. The skill has
two operating modes (BUILD and AUDIT) backed by seven rules files. WCAG 2.2 AA is the hard floor
in both modes; distinctive, intentional design (not template/AI-generic output) is the quality
bar. Rules are written for an expert reader: imperative, numeric, with good/bad pairs.

## BUILD mode

When creating or modifying UI (components, pages, styles, animations):

1. **Lock the system before the screens.** Establish or locate the project's tokens first: type
   scale, color ramps (OKLCH, semantic layer), 4/8pt space scale, radius scale, depth language,
   duration/easing tokens. If a design system exists, conform to it — extend tokens rather than
   inlining values. Read `rules/01` + `rules/03` before writing the first stylesheet.
2. **Default stack:** semantic HTML → CSS grid/flex with `gap` → container queries for component
   responsiveness → logical properties → cascade layers. Headless library or native element
   (`<dialog>`, `popover`, `<details>`) for any interactive widget before hand-rolling.
3. **Build all states, not the happy path.** Every interactive component ships the 9-state
   contract (hover, focus-visible, active, disabled, loading, error, empty, skeleton + default);
   every data view ships loading/error/empty/partial/ideal (`rules/03 §4`, `rules/04`).
4. **Accessibility is built in, not bolted on:** labels, keyboard model per APG, focus management,
   live regions, contrast verified in both themes, `prefers-reduced-motion` honored from the
   first animation (`rules/05`, `rules/06 §6`).
5. **Motion is purposeful:** every animation justifies itself as orientation, feedback,
   continuity, or status; transform/opacity only; durations 200–300ms enter / faster exit
   (`rules/06`).
6. **Be distinctive on purpose:** make ≥ 3 deliberate global design decisions (typeface with
   character, OKLCH accent, signature element) and apply the anti-generic kill list
   (`rules/07 §6`). Spend personality on marketing/empty surfaces; keep product surfaces calm.
7. **Self-check before finishing:** run the relevant rules-file audit checklists against your own
   output. Test mentally (or actually) at 320px, 200% zoom, keyboard-only, dark mode, RTL, and
   with worst-case content (long strings, 0 items, 10k items).

## AUDIT mode

When reviewing existing UI code, designs, or rendered pages:

1. **Scope pass:** identify surfaces (pages/components), the token/system layer (or its absence),
   and the framework. Grep for systemic smells first — they multiply findings: hex/px literals in
   components, `outline: none`, `transition: all`, `user-scalable=no`, placeholder-as-label,
   click-handler `<div>`s, `:focus` without `:focus-visible`, `will-change` in static CSS,
   physical properties (`margin-left`) in new code.
2. **Per-domain pass:** walk each rules file's "Audit checklist" section against the code.
   Prioritize `rules/05` (accessibility) — it carries legal weight — then `rules/04` (UX states),
   then visual/system/motion.
3. **Runtime verification where possible** (Playwright/browser): keyboard-only task completion,
   320px reflow, 200% zoom, both themes, reduced-motion emulation, axe scan. Static review alone
   misses focus order, announcement, and jank.
4. **Rank, don't list.** Findings ordered by severity then by fix leverage (token-level fixes
   beat per-screen fixes).

### Severity conventions

Accessibility findings rank by **WCAG level × user/task impact** — never by fix effort:

| Severity | Definition |
|---|---|
| **Blocker** | WCAG Level A failure preventing task completion for keyboard/AT users (trap, unlabeled required field, SR-silent error, invisible focus on core flow); data-loss UX (wiped form input, no-undo hard delete); broken Back button |
| **Critical** | Level A/AA failure with workaround (contrast < 4.5:1 body text, dialog without focus return, missing landmarks); missing error/loading states on core flows; layout broken at 320px or 200% zoom |
| **Major** | AA failure of limited scope; incomplete state coverage (no empty state, color-only validation); motion without reduced-motion handling; systemic token violations breaking theming; touch targets < 24px |
| **Minor** | AAA/best-practice gaps (24–43px targets, terse alt text); visual drift (rogue radii/shadows/font sizes); generic-template aesthetics; missing polish states |

A small diff never downgrades severity; a locked-out user never rates "Minor".

### Finding format

```
[SEVERITY] <domain>: <one-line problem>
  Where: <file:line or component/page>
  Rule: <rules/NN §section> (+ WCAG SC number if a11y)
  Impact: <who is affected and how>
  Fix: <concrete change, ideally token/pattern-level>
  Effort: trivial | small | medium | large
```

End every audit with: counts per severity, the top 3 highest-leverage fixes, and which checklists
were NOT verified (e.g., no screen-reader pass performed) so coverage is honest.

## Rules index

| File | Read this when... |
|---|---|
| `rules/01-typography-and-color.md` | Choosing/reviewing type scales, fluid type with clamp(), line length/height, variable fonts and loading, OKLCH palettes and ramps, contrast math (4.5:1 / 3:1), semantic color tokens, dark mode architecture |
| `rules/02-layout-spacing-responsive.md` | Spacing systems (4/8pt, gap-over-margin), CSS grid/subgrid layouts, container queries, breakpoints, logical properties/RTL, `:has()`, nesting, cascade layers, anchor positioning/popover, scrolling and overflow |
| `rules/03-design-systems-components.md` | Design tokens (W3C DTCG format, three tiers), theming, component API design (composition, controlled/uncontrolled, asChild), the 9-state completeness contract, headless UI layering, Storybook isolation, versioning |
| `rules/04-ux-patterns.md` | Forms (validation timing, autocomplete/inputmode, error recovery), loading strategy (skeletons vs spinners, optimistic UI), empty/error states, destructive actions (undo > confirm), navigation, touch targets/gestures, feedback timing |
| `rules/05-accessibility.md` | Anything a11y: semantic HTML vs ARIA, keyboard/focus management, focus-visible styling, dialogs/focus traps, live regions, screen-reader test matrix, WCAG 2.2 specifics, top-10 audit failures ranked, severity mapping |
| `rules/06-motion-design.md` | Any animation/transition: purpose test, duration/easing numbers, springs, stagger/choreography, CSS vs WAAPI vs FLIP vs Motion, View Transitions, scroll-driven animation, transform/opacity-only perf, will-change, prefers-reduced-motion |
| `rules/07-visual-craft-distinctiveness.md` | Visual hierarchy and scan paths, Gestalt/alignment, depth languages (borders/shadows/surfaces), icon and detail craft, avoiding generic "AI slop" aesthetics, density calibration, microcopy, visual-drift auditing |

Multiple domains usually apply — e.g., a new dialog touches 03 (API), 04 (confirm/undo),
05 (focus trap), 06 (enter/exit motion). Read every file whose trigger matches.

## Top 10 non-negotiables

1. **WCAG 2.2 AA always**: contrast 4.5:1 text / 3:1 UI (both themes), keyboard-complete, visible
   `:focus-visible` ring, no `outline: none` without replacement, no `user-scalable=no`.
2. **Semantic HTML before ARIA**; ARIA only per complete APG pattern (role + props + keyboard).
   No click-handler `<div>`s, ever.
3. **All states or it isn't done**: hover/focus-visible/active/disabled/loading/error/empty/
   skeleton per component; loading/error/empty/partial/ideal per view.
4. **Tokens, not literals**: components consume semantic tokens only — no hex, no magic px, no
   ad-hoc durations. Dark mode is a token swap and a redesign, never an inversion.
5. **Spacing from the 4/8 scale, parents own it via `gap`** — components carry no outer margins.
6. **Focus is managed**: dialogs trap and restore, SPA route changes move focus and set title,
   deletions relocate focus, errors get focused.
7. **Forms**: visible labels (never placeholder-only), full `autocomplete`/`inputmode` stack,
   validate on blur → re-validate on input, specific adjacent errors, user input never wiped.
8. **Motion**: purpose-driven, transform/opacity only, enter 200–300ms ease-out, exit faster,
   `prefers-reduced-motion` honored in CSS *and* JS — replace movement with fades, don't just
   delete feedback.
9. **Undo over confirm** for destructive actions; when confirming, name the object and
   consequence, verb-label the button, focus cancel.
10. **Distinctive but disciplined**: ≥ 3 deliberate brand decisions, no generic-template kill-list
    items; usability outranks personality everywhere they conflict.
