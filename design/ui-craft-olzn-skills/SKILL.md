---
name: ui-craft
description: Coordinate the UI Craft skill suite. Use when a user asks for broad UI design, frontend quality, design-system work, interface review, visual polish, UX writing, or when it is unclear which domain skill should lead. Also use for quality, craft, papercut, entropy, and "why does this feel bad?" prompts. Routes work across naming, tokens, components, patterns, copy, motion, interaction, typography, colour, and detail. Use for "make this UI better", "review this interface", "improve this design system", "which skill applies", or multi-skill UI tasks. This is a coordinator, not a replacement for the focused domain skills.
---

# UI Craft

Agent-facing routing and usage guidance for the UI Craft suite.

This is a coordinator skill. It does not replace the ten domain skills. Use it to decide which skill should lead, which supporting skills to check, and how much guidance to load.

---

## Core Rules

Use the narrowest relevant skill first. Do not load or apply every domain skill by default.

For new systems or new features, start with structure before surface:

```text
system-naming -> system-tokens -> surface-typography/surface-colour -> system-components -> system-patterns -> surface-copy -> surface-details/surface-interaction/surface-motion
```

For existing UI polish, start with the surface:

```text
surface-details -> surface-copy -> surface-interaction -> surface-motion -> surface-typography -> surface-colour -> system-components
```

Use shared references only when they change the routing or judgement. Use `references/quality.md` for quality, craft, papercut, entropy, and "why does this feel bad?" prompts. Use `references/` files inside skills for deeper recipes and audits; they are not required for every task.

Keep learnings useful. When a reusable project quirk or library behaviour appears, append a short finding to the relevant `learnings.md`. Installed learnings are local runtime notes and the installer preserves them across updates.

---

## Orchestration Protocol

When invoked directly, act as a router before acting as a specialist.

1. Classify the task: build, review, polish, quality, design-system, naming, copy, motion, accessibility, or mixed.
2. Choose exactly one lead skill from the table below.
3. Load or apply the lead skill first.
4. Add supporting skills only when the task includes decisions owned by those skills.
5. For broad UI work, state the route in one short sentence before acting.
6. Stop once the relevant domains have been covered. Do not inspect the whole suite by default.

Use a supporting skill only when it changes the work:

- Use `system-naming` when labels, commands, component names, prop names, token names, icons, or terminology are being chosen or audited.
- Use `system-tokens` when values need to become reusable scales, semantic tokens, or theme mappings.
- Use `system-components` when reusable APIs, variants, states, composition, or component contracts are involved.
- Use `system-patterns` when multiple components form a workflow such as a form, table, navigation, feedback system, or page layout.
- Use `surface-copy` when surrounding explanatory copy, empty states, errors, onboarding, tooltips, or UX prose need writing.
- Use `surface-interaction` when deciding whether movement, gestures, spatial logic, or frequency are appropriate.
- Use `surface-motion` when implementing easing, timing, transitions, entrances, exits, or animated state changes.
- Use `surface-typography` when type scale, font loading, rhythm, wrapping, or rendering are material to the result.
- Use `surface-colour` when contrast, palette, dark mode, status colour, or colour-blind-safe states are material to the result.
- Use `surface-details` when browser quirks, focus, touch, scroll, safe areas, layout shift, or final polish are material to the result.

For a broad prompt, use this route summary format:

```text
Route: lead with system-patterns for layout, then check system-components for APIs and surface-details for platform polish.
```

Skip the route summary when the user names a specific skill or the task is small and obvious.

---

## Skill Selection

| Task | Lead skill | Also check |
|---|---|---|
| Name a feature, command, button, token, or component | `system-naming` | Relevant domain skill |
| Write or revise explanatory UX text | `surface-copy` | `system-naming` for terms |
| Define spacing, radius, surface edge, shadow, z-index, breakpoints, or theme mappings | `system-tokens` | `surface-colour`, `surface-typography` |
| Build a reusable component | `system-components` | `system-naming`, `system-tokens`, `surface-details` |
| Design a form, table, navigation, feedback system, or page layout | `system-patterns` | `system-components`, `surface-details` |
| Decide whether something should animate or how a gesture should behave | `surface-interaction` | `surface-motion` |
| Implement easing, timing, transitions, entrances, exits, or icon swaps | `surface-motion` | `surface-interaction`, `surface-details` |
| Set up type scale, font loading, wrapping, rhythm, or OpenType features | `surface-typography` | `system-tokens` |
| Build palettes, contrast, dark mode, or colour-blind-safe states | `surface-colour` | `system-tokens` |
| Polish browser details, focus, touch, inputs, scroll, or visual finish | `surface-details` | `surface-motion`, `references/accessibility.md` |
| Review quality, craft, papercuts, entropy, or "why this feels bad" | `references/quality.md` | `system-patterns`, `system-components`, `surface-details` |

---

## When To Use

Use UI Craft for:

- New app screens, product features, settings pages, dashboards, forms, tables, command menus, modals, and navigation structures.
- Design-system setup or audit work.
- Frontend reviews that need visual polish, accessibility, motion, interaction behaviour, naming consistency, and production readiness.
- Rough UI that needs to become coherent, usable, and shippable.
- Browser-specific interface bugs such as iOS input zoom, sticky hover, scroll lock, focus return, layout shift, or animation jank.

Do not use UI Craft for:

- Backend-only work with no user interface.
- Pure infrastructure, deployment, data modelling, or API design.
- Brand strategy or product positioning without an interface or design-system surface.
- Native mobile interface work where web platform rules do not apply.
- HTML prototypes imitating iOS/macOS native UI are co-owned: UI Craft owns the web mechanics, the **hig** suite owns native idiom and metric values — where they conflict on a native-targeting prototype, HIG wins.

---

## Prompt Handling

If the user names a specific domain skill, use that skill directly.

If the user asks a broad UI question, choose a lead skill and name the supporting skills you will check.

If the user asks about quality, craft, papercuts, entropy, or why an interface feels bad, read `references/quality.md`, lead with the Quality Pass in `references/composition.md`, and route each issue to the smallest owning skill set.

If the user asks for a review, lead with findings and cite file/line references where possible. Prioritise bugs, accessibility failures, behavioural regressions, and missing states before subjective taste.

If the user asks to build or change UI, implement the relevant guidance as working constraints, not as a long explanation to the user.

If multiple skills apply, keep the sequence explicit and short. Example:

```text
Lead with system-patterns for form structure, then system-components for field/button APIs, then surface-details for focus and mobile input behaviour.
```

### Boundary With surface-copy

Use `surface-copy` for explanatory and persuasive interface writing: error message bodies, empty state body text, onboarding text, tooltip wording, loading copy, and marketing-style CTAs.

Use `system-naming` for product action labels and terminology: button labels, command names, menu items, confirmation action labels, feature names, component names, token names, and any wording that must stay consistent across UI, code, Figma, docs, analytics, or a glossary.

For full flows, sequence them: `system-naming` establishes the vocabulary and action labels; `surface-copy` writes the surrounding explanatory copy and tone variants.

---

## Common Routes

**"Make this UI better"**: `surface-details` lead; check `surface-motion`, `surface-typography`, and `surface-colour`.

**"Why does this feel low quality?"**: use `references/quality.md`, then lead with `system-patterns` for coherence; check `system-components` and `surface-details`.

**"Fix the papercuts"**: use `references/quality.md`, then lead with `surface-details`; check `system-patterns` when papercuts come from workflow complexity.

**"Build a reusable Button"**: `system-components` lead; check `system-naming`, `system-tokens`, `surface-motion`, and `surface-details`.

**"Design this settings page"**: `system-patterns` lead; check `system-components`, `system-naming`, and `surface-details`.

**"This copy feels unclear"**: `surface-copy` lead; check `system-naming` for established terms.

**"This animation feels wrong"**: `surface-motion` lead; check `surface-interaction` for whether the motion logic is right.

**"Audit the design system"**: `system-tokens` lead; check `system-naming`, `system-components`, `surface-colour`, and `surface-typography`.

**"This interface is inaccessible"**: use `references/accessibility.md` as the cross-suite checklist, then apply the owning domain skill for each issue.
