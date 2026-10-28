---
name: ui-design
description: Design and polish user interfaces — layout, typography, spacing, colour/theme tokens, states, responsiveness, accessibility — and verify the result visually in the browser. USE WHEN the user asks to "make it look good/modern", "design the UI", "style this", "improve the UX", "responsive", "dark mode", "accessibility", "landing page", "dashboard", or shares a screenshot of a UI to fix.
---

# UI design

Goal: an interface that looks intentional on every screen size, is usable with keyboard and screen reader, and is verified with a real render — not just CSS that "should" work.

## 1. Understand the system you're styling
- For chat / copilot / agent surfaces, or when the user wants a calm "Claude-like" feel, load the `claude-ui-ux` skill as well — it carries that visual language and the assistant-specific UX patterns.
- Find the existing design language: global styles, CSS variables/tokens, Tailwind/theme config, component library (shadcn, MUI, Chakra, Vuetify…), fonts, icon set. `grep_search` for `--color`, `theme`, `tailwind.config`, `tokens`. Reuse these — never introduce a second palette or spacing scale.
- Look at one well-made screen in the app (or the framework docs) and match it.
- If a screenshot was attached, list the concrete problems you see (alignment, contrast, crowding, truncation, inconsistent sizes) before changing anything.

## 2. Principles to apply
- **Hierarchy**: one primary action per view; size/weight/colour express importance; the eye should land on the title, then the key data, then actions.
- **Spacing scale**: stick to a 4/8 px scale; consistent gaps inside groups (tight) vs between groups (loose). Align to a grid; align text baselines and icon centres.
- **Typography**: ≤ 2 families, 3–5 sizes, line-height 1.4–1.6 for body, ~1.2 for headings, max ~70 characters per line; tabular numbers for data.
- **Colour**: neutrals for structure, one brand accent for primary actions/focus, semantic colours only for meaning (success/warn/error). Contrast ≥ 4.5:1 for text, ≥ 3:1 for UI. Support light and dark via tokens, not hard-coded values.
- **States**: every interactive element has hover, focus-visible, active, disabled and loading states; async views have loading, empty and error states with a next action.
- **Motion**: short (120–250 ms), ease-out, used to explain change; respect `prefers-reduced-motion`.
- **Responsive**: mobile-first; container queries or breakpoints at content-driven widths; no horizontal scroll; touch targets ≥ 44 px.
- **Accessibility**: semantic elements (`button`, `nav`, `main`, headings in order), labels for inputs, `alt` text, visible focus ring, keyboard order = visual order, ARIA only when native semantics don't exist, live regions for async status.
- **Copy**: short, specific labels ("Save changes" not "Submit"); helpful empty states; error text says what to do.

## 3. Implement
- Change tokens/variables before components; components before pages. Prefer the component library's primitives.
- Keep styles co-located the way the project does (CSS modules, styled, Tailwind classes, global CSS). Remove dead CSS you replace.

## 4. Verify visually (mandatory)
- Start or reuse the dev server (`run_command`, background), then `browser_inspect` the page: read the screenshot, console errors, failed requests and layout findings (overflow, tiny tap targets, contrast). Repeat with `mobile: true`.
- Walk the states: use `actions` in `browser_inspect` to hover/click/type and capture hover, focus, error and empty states.
- Check both themes if the app supports them. Fix, re-inspect, then `open_browser` to show the user.

## 5. Report
- Before/after description of what changed and why (hierarchy, spacing, contrast…), the screens/viewports verified, and any follow-ups (e.g. a component that still lacks a focus style).
