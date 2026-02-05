---
name: diagrammer-tailwind-style
description: MANDATORY for any web UI or styling change. Must be followed whenever touching web/src UI, layout, or CSS. Absolutely no shadows, glows, or flares; keep everything flat and token-driven.
---

# Diagrammer Tailwind Styling

Use this skill whenever a task involves changing visual design, spacing, layering, theming, or any Tailwind/CSS in the web app. If you cannot apply it, state why. It assumes Tailwind CSS v4, React 18, Vite, and the existing design tokens defined in [web/src/index.css](web/src/index.css).

## Stack Snapshot
- Tailwind CSS v4 imported in CSS (`@import "tailwindcss"`) with utilities merged via `twMerge` in `cn` ([web/src/lib/utils.ts](web/src/lib/utils.ts)).
- UI primitives built with class-variance-authority (CVA) + Radix + custom tokens: buttons ([web/src/components/ui/button.tsx](web/src/components/ui/button.tsx)), tool rails ([web/src/components/ui/tool-rail.tsx](web/src/components/ui/tool-rail.tsx)), toolbars ([web/src/components/ui/toolbar.tsx](web/src/components/ui/toolbar.tsx)).
- Global tokens and layout variables live in [web/src/index.css](web/src/index.css). Prefer adjusting tokens over introducing new ad-hoc colors.

## Design Tokens (quick reference)
Keep colors and spacing aligned to the tokens declared in `:root` in [web/src/index.css](web/src/index.css):
- Buttons: `--btn-bg`, `--btn-border`, `--btn-text`, hover set, pressed set.
- Flyouts/panels: `--flyout-bg`, `--flyout-text`, `--flyout-border`, `--flyout-item-*`.
- Tiles and list items: `--tile-*` variables for bg, hover, text, borders.
- Accent/status: `--accent-color`, `--status-ok`, `--status-warn`, `--status-error`, plus HSL semantic tokens `--primary`, `--secondary`, `--accent`, `--success`, `--warning`, `--destructive`.
- Layout/z-index: `--tool-rail-left`, `--tool-rail-top`, `--tool-rail-width`, `--rails-gap`, `--rails-divider-*`, and stacking scale `--z-canvas`, `--z-chrome`, `--z-toolbar`, `--z-popover`.
- Typography/background: gradient background and Space Grotesk/Inter font set in `body`; radius token `--radius` for rounding.

## Styling Approach
- Prefer Tailwind utilities in JSX; avoid new global CSS unless a rule must be reused across many components. If adding global rules, use `@layer` and keep them minimal.
- Reuse tokens via `bg-[var(--...)]`, `border-[var(--...)]`, and HSL values already present. Avoid new hex colors unless justified and aligned with tokens.
- Compose classes with `cn(...)`; for reusable patterns or stateful styles, add/extend CVA variants instead of sprinkling repeated class strings.
- Respect focus/hover/pressed states already defined in primitives; if you add new states, mirror contrast and transitions used in existing variants.
- Keep motion light; existing pattern uses `animate-[float-in_260ms_ease_both]` and short transitions (~120ms).
- Avoid drop shadows, glow, or heavy visual flare; styles must look clean on eInk (including color eInk) with minimal contrast stress. Prefer flat fills, borders, and subtle state cues over elevation effects. No shadows or flares.

## Component Usage Patterns
- **Buttons**: Use `Button` and extend `buttonVariants` for new variants or sizes. Keep outline/focus styles consistent with existing focus-visible rings.
- **Tool rails / toggles**: For rail buttons, toggles, and popover triggers use `ToolRail`, `RailButton`, `RailToggleItem`, `RailPopoverButton`. They rely on `--btn-*` and `--flyout-*` tokens; preserve pressed styling and spacing grid.
- **Toolbars**: Use `Toolbar` + `ToolbarButton` for grouped controls; orientation handled via CVA variants. Preserve swatch overlay behavior when showing color fills.
- **Top chrome**: Header uses fixed positioning with pointer-events gating (e.g., TopBar, ActionBar, FileStatus). If adding controls here, keep `pointer-events` on wrappers so popovers remain interactive.
- **Popovers**: Use Radix Popover components wrapped in existing primitives. Keep `sideOffset` ~12 and reuse `contentClassName` to align with flyout styling tokens.

## Layout and Layering
- Respect the established stacking: Excalidraw canvas at `--z-canvas`, chrome/toolbars at `--z-chrome`/`--z-toolbar`, popovers at `--z-popover`. Avoid introducing new z-index values unless fitting this scale.
- Positions for rails are tokenized; adjust `--tool-rail-*` only if layout changes globally. For per-component positioning, prefer utility spacing relative to these tokens.
- Many overlays use `isolation: isolate` and `pointer-events: none` wrappers; ensure new interactive children set `pointer-events: auto` as needed.

## Workflow for Style Changes
1) Identify the target component and see if a primitive already exists (Button, Toolbar, ToolRail). Extend variants before inventing new bespoke components.
2) Choose tokens first (background, border, text, radius). Only add new tokens if the change cannot be expressed with existing ones.
3) Apply Tailwind utilities in JSX with `cn`; keep spacing to the Tailwind scale and rounded corners aligned to `--radius` or existing radii.
4) Validate focus/hover/active states and contrast; ensure accessible text sizes and hit areas (`h-9`/`h-10` for primary buttons, `size-11` for tool buttons).
5) Check layering and positioning against Excalidraw canvas and overlays; popovers must sit above toolbars, and rails should not block canvas interactions.

## Accessibility and Quality Checks
- Maintain focus-visible styles; never remove outlines without providing an alternative.
- Ensure color contrast for text/icons against backgrounds, especially for pressed/hover states.
- Test hover/pressed/disabled states for both mouse and keyboard interactions.
- Keep animations optional and subtle; avoid motion that interferes with drawing interactions.
