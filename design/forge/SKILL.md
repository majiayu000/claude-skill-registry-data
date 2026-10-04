---
name: forge
description: Forge design system for React. Use when writing any React UI in this project, when picking which component to use, when theming, when creating block templates, or when reviewing UI code for accessibility and anti-patterns. Covers components, tokens, theming, motion, patterns, a11y, and anti-patterns.
allowed-tools: Read, Glob, Grep
---

# Forge Design System

Forge is a React component library that ships as `wss3-forge`. Every UI concern (layout, forms, overlays, data display, charts, motion) is covered by a component. All colors, spacing, radius, shadows, and motion live in CSS variables injected by `ForgeProvider`.

**Decision rule:** if the task changes what the user sees, touches, or waits for, load this skill.

## Find by task

Lookup table for the most common requests. Jump straight to the relevant anchor.

| If you're trying to | Read | Skip ahead |
|---|---|---|
| Build a login screen | patterns.md | [#auth](patterns.md#auth) |
| Build signup or forgot-password | patterns.md | [#auth-forgot](patterns.md#auth-forgot) |
| Show a toast on user action | components.md | [#feedback-toast](components.md#feedback-toast) |
| Inline alert (success, error, info) | components.md | [#feedback-decision](components.md#feedback-decision) |
| Errored input with screen-reader feedback | a11y.md | [#inputs](a11y.md#inputs) |
| Icon-only button | a11y.md | [#buttons](a11y.md#buttons) |
| Pricing strip with monthly/yearly toggle | patterns.md | [#pricing](patterns.md#pricing) |
| Pick Modal vs Sheet vs Drawer vs Popover | components.md | [#overlay-decision](components.md#overlay-decision) |
| Pick Card vs StatCard vs KpiCard | components.md | [#cards-decision](components.md#cards-decision) |
| Pick VStack vs HStack vs Grid vs Box | components.md | [#layout-decision](components.md#layout-decision) |
| Pick Input vs Select vs Combobox | components.md | [#forms-decision](components.md#forms-decision) |
| Pick Checkbox vs Switch vs Radio vs Tabs | components.md | [#selection-decision](components.md#selection-decision) |
| Animate items into view, one by one | motion.md | [#stagger](motion.md#stagger) |
| Sticky scroll-jacked phase | motion.md | [#sticky-section](motion.md#sticky-section) |
| Brand color customization | theming.md | [#brand-customization-in-30-seconds](theming.md#brand-customization-in-30-seconds) |
| Theme color won't apply | faq.md | [faq.md](faq.md) |
| Empty state | patterns.md | [#empty-state](patterns.md#empty-state) |
| Loading or error or empty triad | patterns.md | [#triad](patterns.md#triad) |
| Settings page (profile, billing, team) | patterns.md | [#settings](patterns.md#settings) |
| Marketing page (hero, pricing, testimonials) | patterns.md | [#marketing](patterns.md#marketing) |
| Data screen (table, master-detail, kanban) | patterns.md | [#data](patterns.md#data) |
| Dashboard with sidebar | patterns.md | [#dashboard-sidebar--content](patterns.md#dashboard-sidebar--content) |
| Build a docs site | patterns.md | [#docs](patterns.md#docs) |
| Pick Navbar vs AppSidebar (horizontal vs vertical menu) | components.md | [#navigation](components.md#navigation) |

## Review priority (check in this order)

1. **Accessibility.** Focus visible, correct roles, `aria-label` on icon-only buttons, `aria-invalid`/`aria-describedby` on errored inputs, keyboard navigation works, reduced motion respected. See [a11y.md](a11y.md).
2. **Semantics.** Using the right Forge primitive: `Heading` not styled `<h1>`, `Button` not styled `<button>`, `VStack`/`HStack` not flex `<div>`, `Card` not styled container. See [anti-patterns.md](anti-patterns.md).
3. **Motion.** Durations 150 to 300ms for interactions, reduced-motion respected by `ForgeProvider`, no animations over 500ms for UI feedback. See [motion.md](motion.md).
4. **Theme parity.** Code works in both `darkTheme` and `lightTheme`. No hardcoded `rgba(255, 255, 255, ...)` or `#xxx`. Use CSS vars or `color-mix(in srgb, currentColor N%, transparent)`.
5. **Performance.** `VirtualList` when rendering more than 100 rows, lazy routes, `<Motion whileInView>` over `animate` for offscreen content.

## Hard rules

1. Import only from `'wss3-forge'`. No deep imports.
2. Wrap the app in `<ForgeProvider>`. Without it every component renders unstyled.
3. Icons only from `@fluentui/react-icons`. Convention: `{Name}{Size}{Style}` (e.g. `ArrowRight20Regular`).
4. Colors via `var(--...)`. No hardcoded hex, RGB, or color names.
5. Spacing via gap/padding props on Forge primitives. No raw `px`/`rem` when a semantic key exists.
6. Layout via `VStack`, `HStack`, `Stack`, `Grid`, `Flex`, `Box`, `Center`, `Spacer`, `AspectRatio`. No flex divs.
7. Responsive via `useIsMobile`, `useBreakpoint`, or responsive object props. No `@media` queries in app code.
8. Typography via `Heading`, `Text`, `Label`. Never style `<h1>`, `<span>`, or `<p>` manually.
9. No em-dashes anywhere. Period, comma, colon, or line break.
10. No emojis in UI. Use Fluent icons.
11. No decorative colored backgrounds behind icons. Color the glyph itself via `style={{ color: '...' }}`. Only `StatusBadge`, `Avatar` status, and colored `Badge` variants keep a tinted surface.
12. No custom components when Forge provides one. Check [components.md](components.md) first.
13. No custom CSS classes for design-system concerns (spacing, color, radius, shadow, typography). Use props or CSS vars.

For the reasoning behind each rule, see [design.md](design.md). For concrete wrong/right pairs, see [anti-patterns.md](anti-patterns.md).

## What Forge is NOT

Forge is a *restrained* design system. These are baseline anti-aesthetics:
- No aurora-gradient backgrounds. The page reads as flat surfaces with brand-tinted accents, not as a colored sky.
- No glass-on-everything. Backdrop-filter is a tool for the navbar and the modal scrim, not for every card.
- No icon glow / icon-tint backgrounds. Color the glyph itself; let surfaces stay calm.
- No cyan-magenta-violet gradients. They read as AI-template defaults; we build for Linear / Stripe / Vercel restraint.
- No streaming-text fakery, no ASCII art in production UI, no AI-marketing clichés.

When in doubt, restrain. Forge ships polished defaults; consumers reach for them, not around them.

## Pre-delivery checklist

Before claiming done, verify:

- [ ] `tsc --noEmit` clean.
- [ ] Works in both dark and light mode (no hardcoded dark-only colors).
- [ ] Focus ring visible on every interactive element.
- [ ] Icon-only buttons have `aria-label` or `tooltip`.
- [ ] Touch targets at least `size="sm"` (32px) on mobile flows.
- [ ] Motion durations within 150 to 300ms for interactions, reduced-motion respected.
- [ ] No em-dash, no emoji in UI strings.
- [ ] No hardcoded hex/rgba in styles. All colors via CSS var.
- [ ] No fallback or try/catch for scenarios that cannot happen.
- [ ] No trivial comments that restate the code.

## Files in this skill

Load the file that matches your task. Do not load them all at once.

- [getting-started.md](getting-started.md) five-minute install and first screen. Read this first if Forge is not already wired up.
- [components.md](components.md) every export grouped by category, with props table. Read this when picking a component or looking up props.
- [tokens.md](tokens.md) CSS variables, spacing scale, radius, shadows, z-index, motion tokens, breakpoints, color constants. Read this when styling edges Forge does not cover with a prop.
- [theming.md](theming.md) `ForgeProvider` props, `ForgeTheme` fields, default `darkTheme` and `lightTheme`, `createTheme`, `useForge`. Read this when configuring the provider or building a custom theme.
- [motion.md](motion.md) the Motion library (`Motion`, `AnimatePresence`, `Stagger`, gesture, scroll, text/visual effects, canvas backgrounds, motion hooks). Read this when adding animations.
- [patterns.md](patterns.md) full compositions for dashboards, forms, responsive sidebars, list-with-actions, plus quality gates per pattern and block creation rules. Read this when building a page, not a single component.
- [a11y.md](a11y.md) accessibility playbook: what Forge adds automatically per component and what the dev must still add. Read this when working on any interactive surface.
- [anti-patterns.md](anti-patterns.md) wrong/right pairs for the most common mistakes. Skim this when you are about to write a styled native element, a flex div, a `@media` query, or a hardcoded color.
- [design.md](design.md) design rules and the reasoning behind them. Read this when choosing between multiple valid approaches or when the user asks "why".
- [migration.md](migration.md) upgrade notes from previous versions. Read this when bumping `wss3-forge`.
- [faq.md](faq.md) common gotchas and their fixes (unstyled components, 404s, wrong sizes). Read this when something does not behave as expected.

## Typical flow

1. Read the user's request.
2. Open [components.md](components.md) and find the primitive that matches. If the request is a composition, open [patterns.md](patterns.md) first.
3. If the primitive needs a color, radius, or spacing you cannot express with a prop, open [tokens.md](tokens.md).
4. If the request involves animation, open [motion.md](motion.md).
5. If the request touches theming or provider configuration, open [theming.md](theming.md).
6. If the request is interactive (form, menu, dialog, table), skim [a11y.md](a11y.md).
7. Write the code. Run through the Review priority and Pre-delivery checklist. Run `tsc --noEmit` before claiming done.

## Blocks

Block templates live under `src/pages/blocks/blocks/{category}/{slug}/`. Categories: `marketing | dashboard | auth | commerce | settings | content | utility`. Block creation rules are documented in [patterns.md](patterns.md#block-creation).
