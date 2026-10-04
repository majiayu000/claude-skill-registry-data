---
name: lwc-css-and-styling
description: "Styling LWC components — SLDS design tokens, --slds-c-* styling hooks, scoped CSS via shadow DOM, ::part() for restyling base components, light DOM (lwc:render-mode='light'), why CSS doesn't pierce the shadow boundary, !important vs specificity, and SLDS upgrades breaking hand-rolled selectors. NOT for app-scope theming or SLDS 2 hook migration — use lwc/lwc-styling-hooks. NOT for picking shadow vs light DOM — use lwc/lwc-shadow-vs-light-dom-decision."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Operational Excellence
  - Performance
triggers:
  - "lwc style base component slds hook"
  - "--slds-c-button-color-background lwc"
  - "lwc shadow dom css does not pierce"
  - "lwc light dom render mode shared styles"
  - "lwc ::part() restyle internal element"
  - "lwc styling hooks vs deep selector"
  - "slds design tokens lwc theming"
tags:
  - css
  - slds
  - shadow-dom
  - styling-hooks
  - design-tokens
inputs:
  - "Which base component or slot needs custom styling"
  - "Whether the component is in a Lightning Page (themed) or standalone"
  - "Whether the component must theme dynamically (dark mode, brand variants)"
outputs:
  - "Decision: SLDS hook (--slds-c-*) vs ::part() vs light DOM vs slot"
  - "Component CSS file using design tokens, no !important, no internal-selector hacks"
  - "Theming pattern that survives SLDS version upgrades"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-05-05
---

# LWC CSS and Styling

LWC components render inside a shadow DOM by default. Component
CSS is scoped to the component — it does not bleed in or out.
SLDS classes work everywhere because the framework injects them
globally; everything else stops at the shadow boundary. This is
the single fact that determines every styling decision.

The typical confusion: a developer wants to change the background
color of a `lightning-button`. They write
`lightning-button .slds-button { background: red; }` and see no
effect. The reason is the `.slds-button` class lives inside the
button's shadow DOM. Five years ago the answer was a `/deep/`
selector or `::shadow`, both since deprecated. The current answer
is **SLDS styling hooks** — `--slds-c-button-color-background:
red` — which the base components consume from the consumer's CSS
custom property cascade.

For cases where there is no styling hook for the property you
need, the toolbox has three more options: `::part()` (where
the base component exposes a part), light DOM
(`static renderMode = 'light'`), or a slot (let the consumer
render their own element). Each has tradeoffs. Reaching for
`!important` or for the SLDS internal class name is the wrong
answer almost always — the next SLDS upgrade renames the class
and the styling vanishes.

## Recommended Workflow

1. **Read the component's "Styling Hooks" tab in the Component
   Library before writing CSS.** Most base components document a
   list of `--slds-c-*-color-*`, `--slds-c-*-spacing-*`,
   `--slds-c-*-radius-*` properties they consume. If the property
   you need has a hook, set it and stop.
2. **If no hook exists, check `::part()` exposure.** Some base
   components (newer ones especially) expose internal elements via
   `::part(name)`. Style them with
   `lightning-foo::part(bar) { ... }`.
3. **For your own components, prefer SLDS classes over hand-rolled
   styles.** `class="slds-card"` is admin-portable, theme-aware,
   and survives SLDS upgrades. Custom CSS is a maintenance ratchet.
4. **Use design tokens (`--lwc-colorBrand`, `--slds-g-color-*`)
   instead of literal hex codes.** The user might have High
   Contrast mode on, the org might be themed via
   `LightningExperienceTheme`, the page might be in a community
   with a different brand color.
5. **Reach for light DOM only when shadow DOM is the bottleneck.**
   `static renderMode = 'light'` removes the shadow boundary —
   the component participates in global CSS. It also forfeits
   encapsulation; another component's `.button` rule will hit
   yours. Use for small layout components, never for shared base.
6. **Never use `!important` in a base-component override.** It
   binds the override to the current SLDS internal-class name.
   When SLDS updates, your override fails silently and the user
   sees the default style.
7. **Write CSS in `*.css` next to the JS, not inline `style=`.**
   Inline styles bypass the design-token cascade and are harder
   to override per-theme.

## What This Skill Does Not Cover

| Topic | See instead |
|---|---|
| SLDS icon usage and `lightning-icon` | `lwc/lwc-slds-icons` |
| Aura styling | Aura is deprecated for new development |
| Custom Lightning App theming | `admin/branding-themes` |
| Experience Cloud / Community CSS | `lwc/lwc-community-styling` |
