---
name: frontend
description: "Use for UI, styling, layout, components, responsive or interaction work, and React or Next.js component, hook, route or rendering changes."
license: MIT
metadata:
  reviewed: "2026-11-01"
  sources: "MCT (local) ~/.claude/skills/frontend-ui-ux-harness, ~/.claude/skills/ui-system, ~/.claude/skills/design-consistency, ~/.claude/skills/frontend-architecture, ~/.claude/skills/react-quality, ~/.claude/skills/nextjs-app-router, ~/.claude/skills/performance-audit, ~/.claude/skills/react-doctor; emilkowalski/skills (MIT) emil-design-eng/SKILL.md + performance-cheatsheet.md; emilkowalski/skills a81dbca07f2217b7103e510c0f13f8d5b017afc9 skills/review-animations/{SKILL.md,STANDARDS.md}, skills/improve-animations/SKILL.md, skills/animation-performance/SKILL.md, skills/mobile-native/SKILL.md (adapted)"
---

# Frontend

Match the product that exists before adding to it. A narrow request gets a narrow change with visual parity. A redesign happens only when the user asks for one.

## 1. Read the existing UI

Open the nearest screen and the shared components it uses. Find the system the repo already has:

- Components: `components/ui/` and `components.json` (shadcn), Storybook, a design-system package.
- Tokens: `tailwind.config.*`, `@theme` blocks in CSS (Tailwind v4), CSS custom properties, a tokens file.
- Patterns: spacing scale, type scale, radius, shadows, density, icon set, how nearby forms, tables, dialogs and menus behave.

Done when: you can name the components, tokens and icon set the change will reuse.

## 2. Build with what's there

- Reuse an existing component or variant before writing a new one. Add a variant (`cva`, a `variant` prop) rather than one-off classes on a copy.
- shadcn present: add missing primitives with the shadcn CLI so they land where `components.json` says, then compose them. Keep the Radix primitives underneath; they carry the keyboard and ARIA behavior.
- Tailwind present: use theme scale classes and `cn()` for conditional classes. Use an arbitrary value (`p-[13px]`, `bg-[#3b82f6]`) only when no token fits, and say why.
- New colors, radii, shadows, fonts or animation styles need a one-line reason. One-off values drift the system.
- Operational screens (dashboards, settings, tables) stay dense and plain. Hero sections, big gradients and decorative motion belong on marketing pages.
- Use the project's icon set (lucide when it's already installed).
- Text fits its container at mobile and desktop widths, including long names, empty values and translated strings.
- For application motion, read [animation](references/animation.md) and use the existing stack. For a motion audit or review, follow [motion review](references/motion-review.md); for dropped frames, follow [motion performance](references/motion-performance.md). Mocked product illustrations and animated cursor demos use `stageshow`; its demo kit is not an application dependency.
- For phone or PWA interactions, read [mobile behavior](references/mobile.md). Fix the relevant viewport, touch, keyboard or safe-area behavior without device sniffing or disabling zoom.

Done when: every visual value in the diff traces to an existing token, component or variant, or carries its one-line reason.

## 3. Make every state explicit

| State | Provide |
|---|---|
| Loading | A skeleton or spinner sized like the content so nothing jumps; submit buttons disabled while pending |
| Empty | What's missing and the next action |
| Error | What failed, what the user can do, a retry where it makes sense |
| Hover, focus, active, disabled | Visible styles for each; a `focus-visible` ring whenever an outline is removed |
| Overflow | Long text, many items, narrow widths: wrap, truncate with the full value available, or scroll inside the component |

Done when: each state that can occur on the changed surface renders something deliberate.

## 4. Accessibility basics

- `<button>` for actions, `<a href>` for navigation, a `<label>` tied to every input.
- Every control is reachable with Tab and works with Enter or Space. Escape closes overlays and focus returns to the trigger.
- Images have `alt` (empty for decorative ones). Icon-only buttons have `aria-label`.
- Text contrast is at least 4.5:1 (3:1 for large text). Color is never the only signal for a state.
- Touch targets are at least 24x24 CSS px, ideally 44x44 on mobile.

Done when: the changed controls work with the keyboard alone and every input has a label.

## 5. React and Next.js

Inline defaults, with detail in the references:

- Server components by default in the App Router. Put `"use client"` on the smallest leaf that needs state, effects, event handlers or browser APIs.
- Keep feature code next to the route or feature that owns it. Promote to shared only when a second owner uses it.
- A component past roughly 300 lines of logic is a candidate for extraction along a real ownership line.
- Prefer composition (`children`, slots) over passing props through three or more layers.

Read the reference that matches the change:

- Components, hooks, state, effects, context, forms, data fetching: `references/react.md`.
- App Router routes, layouts, server/client boundaries, metadata, `loading`/`error` files, route handlers, server actions, caching: `references/nextjs.md`.
- Slow pages, bundle size, rerenders, images, Core Web Vitals: `references/perf.md`.

Done when: the change respects the server/client boundary and the conventions of the folder it lives in.

## 6. Check it

- **React Doctor** after any React change:

  ```bash
  npx -y react-doctor@latest . --verbose --diff
  ```

  A lower score or a new error against the base is a regression: fix it before calling the work done. If the command can't run (offline, unsupported setup), record it as skipped with the error.
- **Typecheck** when props, shared types or route params changed.
- **Responsive.** View the changed surface at 1440x900 and 390x844: no horizontal scroll, no clipped or overlapping text, controls still reachable. Run this through the `qa` skill, which owns the browser tool choice and the evidence line.

Done when: React Doctor ran or has a skip reason, and every visible change has a browser evidence line from `qa`.

## Companion design skills

For new screens and redesigns, load these by name when installed: `frontend-design`, `design-taste-frontend`, `hallmark` (audits and redesigns), `ui-ux-pro-max`. They set direction and taste. On an existing surface, this skill's parity rules win. When none are installed, continue with this skill alone.

## Report

Name the system you followed (components, tokens, variants), any new value with its reason, the React Doctor result and the responsive check.
