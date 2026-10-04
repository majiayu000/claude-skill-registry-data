---
name: lwc-styling-hooks
description: "Use when theming Lightning base components or custom LWCs with SLDS Styling Hooks — CSS custom properties such as `--slds-c-button-color-background`, `--slds-g-color-brand-base-50`, and `--sds-c-*` — across app, page, component, or Experience Cloud scopes, including SLDS 2 (2e) migration via SLDS Validator / Linter and dark-mode surface work. Triggers: 'how to theme lightning-button', 'custom color without overriding slds classes', 'slds 2 migration for lwc', '--slds-c-button-color-background doesn't work', 'experience cloud brand color in lwc', 'dark mode lwc base components'. NOT for your own component's scoped CSS and shadow-boundary problems — use lwc/lwc-css-and-styling. NOT for Experience Cloud branding sets and palette pickers — use admin/experience-cloud-site-setup."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Operational Excellence
  - Reliability
  - Performance
triggers:
  - "how do i theme a lightning-button without writing raw css"
  - "custom color without overriding slds classes on a base component"
  - "slds 2 migration for an lwc that used to override hex values"
  - "--slds-c-button-color-background does not seem to do anything in my lwc"
  - "experience cloud brand color needs to propagate to base components in my lwc"
  - "dark mode lwc base components and surface tokens"
  - "how do i expose a styling hook from my custom lwc so consumers can theme it"
tags:
  - lwc-styling-hooks
  - slds
  - css-custom-properties
  - theming
  - slds-2
  - design-tokens
inputs:
  - "which component surface is being themed (specific base component, custom LWC, or full page)"
  - "scope of the change: global (app or org), page, Experience Cloud site, or single component instance"
  - "SLDS version target: SLDS 1, SLDS 2 (2e), or both during a migration window"
  - "shadow-DOM vs light-DOM mode of the consuming custom LWC"
outputs:
  - "styling hook plan mapping desired UI changes to component or global hooks"
  - "CSS snippets scoped via `:host` or appropriate root selectors"
  - "SLDS 2 migration checklist for deprecated SLDS 1 hook names"
  - "checker report of `.slds-*` class overrides, raw hex values, and `!important` on hook declarations"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-23
---

# LWC Styling Hooks

Use this skill when you need to change the appearance of a Salesforce base component or a custom LWC and you want that change to survive SLDS upgrades, respect Experience Cloud branding, and avoid fighting the shadow DOM. SLDS Styling Hooks are the public API for theming on the Lightning platform — everything else is implementation detail.

---

## Before Starting

Gather this context first:

- Which specific component surface is being themed — a single base component (`lightning-button`, `lightning-card`), a cluster of them on one page, or an Experience Cloud site?
- What scope should the change have — one component instance, one LWC, an entire app, or the whole site?
- Is the target org on SLDS 1 or SLDS 2 ("2e")? Both render today, but SLDS 2 has renamed, added, and deprecated hooks, and SLDS Validator / SLDS Linter flag unsafe patterns during that migration.
- Is the consuming custom LWC shadow DOM or light DOM? Shadow DOM requires hooks to be set on `:host` or higher; light DOM has a shared style scope and cannot use `:host` the same way.
- Is any existing CSS targeting raw `.slds-*` class names? Those are not a public API and need to be removed before the cascade can be trusted.

---

## Core Concepts

SLDS Styling Hooks give you two layered vectors — global hooks that carry brand and semantic intent across every base component, and component hooks that tune a single component's surface without touching its internals. You should always prefer the highest-level hook that expresses the change, and drop to component hooks only when you truly need a localized deviation.

### Two Hook Tiers: Global And Component

Global hooks use the `--slds-g-*` prefix and express semantic design decisions: `--slds-g-color-brand-base-50` is the brand color anchor, `--slds-g-color-border-base-1` is the default border, and so on. They cascade into every base component that reads them. Component hooks use the `--slds-c-*` prefix (and the older `--sds-c-*` for shared primitives) and target exactly one component: `--slds-c-button-color-background`, `--slds-c-card-color-background`, `--slds-c-input-color-border`. Salesforce owns the mapping from hook name to internal styles, so when SLDS internals change, your theme still works as long as the hook name is stable.

### Cascade Rules Favor Global, Then Override Locally

The intended flow is global hook at a root scope → component hook at a narrower scope → component hook on `:host` of the specific consuming LWC. If you set `--slds-g-color-brand-base-50` on the page root, every base component that reads brand color picks it up. If you then need one button variant to differ, you set `--slds-c-button-color-background` on that one component's `:host`. Don't start with component hooks everywhere — you'll end up reimplementing brand consistency by hand.

### SLDS 2 (2e) Replaces Hex Overrides

SLDS 2, publicly referred to as "2e", is the refreshed design system that Salesforce ships alongside SLDS 1. It introduces new semantic tokens, revised dark-mode surface hooks, and explicit deprecations of older hook names. The SLDS Validator and SLDS Linter tools flag SLDS 1 hook usage that does not have an SLDS 2 equivalent, raw `.slds-*` class overrides, and hardcoded hex colors where a token exists. Running them on an LWC-heavy codebase is the only reliable way to know what will break on the migration.

### Shadow DOM Makes Hooks The Only Stable Vector

In a shadow-DOM LWC, selectors from the parent cannot reach into the component's internal SLDS classes — that's the isolation guarantee. Styling hooks pierce shadow boundaries because they are CSS custom properties, which inherit through the DOM tree regardless of shadow roots. Set the hook on `:host` (shadow DOM) or on the component's host element (light DOM) and the base components inside read the value normally.

### Experience Cloud Theming Flows Through Root-Level Hooks

Experience Cloud sites apply branding by setting global hooks at the site root. A well-behaved LWC used inside an Experience Cloud page should not hardcode colors — it should let the site's brand cascade in through `--slds-g-*`, and only override at `:host` if the component has a deliberate visual deviation.

### Custom LWCs Should Expose Their Own Hooks

If you build a reusable custom LWC, follow the same pattern — accept `--c-<mycomponent>-*` (or `--slds-c-*` if you truly behave like an SLDS primitive) as your theming API, document it, and read from those hooks in your own CSS. That way your consumers theme you the same way they theme SLDS components.

---

## Common Patterns

### Global Brand Hook At Page Root

**When to use:** You want one brand color to drive all base components on a page, app, or site.

**How it works:** Set `--slds-g-color-brand-base-50` (and related semantic tokens like `--slds-g-color-brand-base-60` for hover states) on the page root or on a top-level LWC's `:host`. Every descendant base component that reads brand color picks it up without per-component CSS.

**Why not the alternative:** Setting `--slds-c-button-color-background` everywhere reimplements brand consistency by hand, drifts over time, and still misses every non-button surface.

### Component Hook On `:host` For A Local Deviation

**When to use:** One specific LWC needs a button variant that differs from the app-wide brand — a destructive-action confirmation, a special accent on a single card, etc.

**How it works:** In the LWC's `.css` file, set the component hook on `:host`: `:host { --slds-c-button-color-background: var(--slds-g-color-accent-warning-base-50); }`. That value overrides the inherited brand color only inside this LWC.

**Why not the alternative:** Targeting `.slds-button_brand` with a descendant selector is blocked by shadow DOM in most base components and silently breaks when SLDS renames its internal class.

### Custom LWC Exposes Its Own Hook

**When to use:** You're writing a reusable LWC that will be dropped into pages, apps, or sites with different brands.

**How it works:** Define a hook in your CSS — `:host { background: var(--c-mycard-color-background, var(--slds-g-color-surface-container-1)); }`. Consumers set `--c-mycard-color-background` on a parent scope or on your host and your component themes cleanly, with a sensible SLDS fallback.

**Why not the alternative:** Hardcoding colors forces every consumer to fork your CSS, and targeting your internal class names defeats encapsulation.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Change brand color across the entire app | Global hook (`--slds-g-color-brand-base-50`) at app or page root | One value cascades through every SLDS base component |
| Tweak one button variant in a single LWC | Component hook (`--slds-c-button-color-background`) on `:host` | Localized override without touching global brand |
| Theme an Experience Cloud site end-to-end | Builder-level branding plus global hooks at the site root | Branding flows through the documented public API |
| Expose theming on a reusable custom LWC | Define `--c-<component>-*` hooks with SLDS fallbacks | Consumers theme via CSS custom properties, just like SLDS |
| Migrate an SLDS 1 codebase to SLDS 2 | Run SLDS Validator / Linter, map deprecated hooks to new semantic names | Validator flags exactly what will break on the migration |
| Need a visual change on an internal SLDS class | Stop — use a hook or file a gap instead | Internal class names are not a public API and break on upgrade |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm which component is being themed, what scope the change should have, and whether the target is SLDS 1, SLDS 2, or both.
2. Search the SLDS Styling Hooks catalog — identify the specific hook name(s) involved and confirm they exist for the target SLDS version.
3. Choose scope — prefer global hook at the highest reasonable scope, drop to component hook on `:host` only for deliberate local deviation.
4. Implement the hook — set it in the LWC's CSS file (`:host` for shadow DOM, component root selector for light DOM) or at a parent scope for app-wide changes.
5. Run SLDS Validator / SLDS Linter — catch deprecated hook names, raw `.slds-*` class overrides, and hardcoded hex values before they ship.
6. Run `scripts/check_lwc_styling_hooks.py` against your LWC CSS to catch the same patterns locally.
7. Validate visually in Lightning Experience and Experience Cloud, including dark-mode surfaces if the org uses them.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] No CSS in the change targets `.slds-*` class names directly.
- [ ] Brand and semantic changes use global `--slds-g-*` hooks rather than repeating component hooks.
- [ ] Local deviations use component `--slds-c-*` hooks on `:host` (shadow DOM) or the component root (light DOM).
- [ ] No raw hex values remain where a token exists — SLDS Validator / Linter output is clean.
- [ ] SLDS 2 deprecations are addressed if the target org runs or will run SLDS 2.
- [ ] Reusable custom LWCs expose documented hooks with SLDS fallbacks.
- [ ] `!important` is not used on hook declarations — scope specificity is preferred instead.
- [ ] Experience Cloud pages let site-level branding cascade in rather than hardcoding colors inside the LWC.

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Hook names are case-sensitive and hyphenated** — `--SLDS-C-Button-Color-Background` or `--slds_c_button_color_background` silently does nothing, and the page looks unchanged with no console error.
2. **Component hooks only work where Salesforce exposes them** — not every internal property of every base component is hook-addressable; if no documented hook exists, the property is intentionally private.
3. **Shadow DOM blocks parent CSS from targeting inner SLDS classes** — hooks are the only reliable vector into shadow-DOM base components, which is exactly why SLDS provides them.
4. **`!important` on a hook declaration fights cascade rather than using it** — prefer increasing scope specificity (set the hook at a narrower scope) over `!important`.
5. **SLDS 2 renames and deprecates some SLDS 1 hooks** — the SLDS docs list migration pairs; the SLDS Validator / Linter is the tool that finds every stale reference in a real codebase.
6. **Light-DOM LWCs do not get `:host` semantics** — setting a hook on `:host` in light DOM has no effect; set it on the component's root element selector instead.
7. **Experience Cloud theme overrides component hooks unless you scope higher** — if the site's theme layer sets `--slds-g-color-brand-base-50`, your LWC's attempt to override it at `:host` wins only for that subtree, not globally.
8. **Raw `.slds-*` class overrides may appear to work in SLDS 1 and silently break in SLDS 2** — the migration is the forcing function that surfaces all the upgrade debt teams accumulated.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Styling hook plan | Mapping of desired UI changes to specific `--slds-g-*` or `--slds-c-*` hooks at the right scope |
| Scoped CSS snippets | `:host` (shadow) or component-root (light) selectors that set the chosen hooks |
| SLDS 2 migration checklist | Deprecated SLDS 1 hook names, their SLDS 2 replacements, and affected files |
| Checker report | File-level findings from `check_lwc_styling_hooks.py` on class overrides, hex literals, and `!important` misuse |

---

## Related Skills

- `lwc/experience-cloud-lwc-components` — use when the theming question is really a site-level branding, builder, or theme-layout question.
- `lwc/lwc-base-component-recipes` — use when the goal is to pick the right base component first, then theme it second.
- `lwc/lwr-site-development` — use when the work spans LWR site configuration beyond the CSS-hook layer.
