---
name: iconography
description: "One consistent icon set with labels where it counts."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, icons]
    category: web
    related_skills: [web-design, component-states]
    web_designer_stages: [icon, components]
---

# Iconography and SVG Icons Skill

Choose and apply one consistent icon set, as inline SVG, so icons act as cognitive shortcuts rather than decoration. This skill covers set selection, sizes, labels, accessible names, and dark-mode behaviour. It does not cover logo design or illustration, and it does not cover icon animation, which belongs to motion design. Load-on-demand only, loaded by the web-designer coordinator for its stages; never auto-loads; never contacts the user directly — the coordinator is the only router.

## When to Use

- For navigation, actions, status and empty states — wherever an icon speeds recognition.
- When a site needs a single icon style across every page and component.
- When an icon-only button is proposed: the skill decides whether the symbol is universal enough to stand alone.
- When an icon must stay crisp at any size and in dark mode.
- When a status must be readable without colour alone, with the icon carrying part of the meaning.
- Not for a logo, a brand mark, or a detailed illustration — those are not icons.
- Not for adding an icon to every label: an icon earns its place by speeding recognition, not by filling space.

## Prerequisites

- The run is active and the coordinator loaded this skill for its stage or stages.
- The design direction is chosen, so the icon style matches the direction rather than fighting it.
- The component inventory is known, so the skill can see every place an icon will appear.
- The colour roles are defined, so icons inherit the right currentColor in each theme.

## How to Run

1. Pick one icon library for the whole site, for example Lucide or Heroicons, and record it as the single set.
   - Check the set covers every icon the inventory needs before committing to it.
   - Do not mix in a second set for one missing icon; draw or drop that icon instead.
2. Use inline SVG, inheriting currentColor, so icons follow the text colour and stay crisp at any size and in dark mode.
   - Inline SVG scales without blur, unlike raster icons.
   - currentColor keeps the icon in step with text colour in light and dark themes.
3. Apply the standard sizes 16/20/24/32px, matched to the text and component they sit beside.
   - Small icons sit beside small text; larger icons mark larger actions.
4. Pair icons with text labels as the default; allow icon-only only for universal symbols such as home, search and close.
   - When in doubt, add the label: a label costs little and a guessed icon costs a tap.
5. Mark decorative icons aria-hidden, and give every interactive icon an accessible name.
   - A decorative icon adds nothing for a screen-reader user, so it stays silent.
   - An interactive icon is a control, so it needs a name that says what it does.
6. Give icon-only buttons a 44x44px target, then record the set and its rules in the stage record.
   - Reach the target size with padding, not by enlarging the icon itself.
7. Re-check after any fix, and record what changed.
   - A changed icon, label or target is re-checked for style, size and accessible name before the stage closes.
   - The set recorded is the one in the final build, not an earlier draft.

## Quick Reference

- One set per site: same stroke, corner radius and weight throughout.
- Format: inline SVG, the modern standard over icon fonts and raster images.
- Standard sizes: 16/20/24/32px.
- Default: icon plus text label.
- Icon-only: only for universal symbols — home, search, close.
- Decorative icons: aria-hidden.
- Interactive icons: an accessible name via aria-label.
- Icon-only button target: 44x44px.
- Colour: inline SVG inherits currentColor, so icons follow text colour and theme.
- Grid: all icons share one grid, so sizes and alignment stay consistent.
- Sizes: matched to the text and component the icon sits beside.
- Rule: no mystery-meat icon without a label, except home, search and close.
- Targets: icon-only buttons reach 44x44px with padding, not a larger icon.
- Themes: icons stay crisp in light and dark mode.

## Procedure

### 1. What it is

Icons as cognitive shortcuts: one consistent set (same stroke, corner radius, weight), inline SVG as the modern standard over icon fonts/raster, standard sizes 16/20/24/32px, icon+text as default, icon-only only for universal symbols, decorative icons aria-hidden, interactive icons with aria-label.

### 2. How Hermes applies it

Hermes picks one library (e.g. Lucide/Heroicons) per site, uses inline SVG inheriting currentColor, pairs icons with labels except for home/search/close, and gives icon-only buttons a 44x44px target and accessible name.

### 3. What it returns to the stage

- `icon` stage record: `icon_set` names the chosen library, the sizes in use, the label rule, and the exceptions (home, search, close) allowed icon-only.
- `components` stage record: `inventory` carries the icon usage per component — which components carry icons, which are icon-only, and the accessible name each interactive icon carries.

### 4. Good looks like

All icons share one style and grid; no mystery-meat icon without a label; icons stay crisp at any size and in dark mode.

## Pitfalls

- Two or more icon styles on one site: mixed stroke weights and corner radii make the interface look assembled from different products.
- Icon fonts or raster icons: they blur at some sizes, fail in dark mode, and load as a font the page does not need.
- An icon-only button for a non-universal action: visitors guess at its meaning, and the guess is often wrong — the mystery-meat icon.
- A decorative icon announced to screen readers: noise that drowns the real content; decorative icons are aria-hidden.
- An interactive icon with no accessible name: a screen-reader user meets an unnamed button.
- A 16px icon as the whole tap target: the visible icon is small and the hit area is smaller still; the target is 44x44px, reached with padding, not by enlarging the icon.
- An icon that means different things on different pages: the same shape used for two actions teaches visitors to distrust every icon.
- An icon used where a label would do: a row of icons with no text that only the designer can read.
- Icons that vanish in dark mode: a dark icon on a dark surface, because the icon never inherited currentColor.

## Verification

- Every icon on the site comes from the one recorded set, with one stroke, corner radius and weight.
- Icons use the standard sizes 16/20/24/32px and stay crisp at any size and in dark mode.
- Every icon except home, search and close carries a text label; no other icon stands alone without one.
- Decorative icons are aria-hidden; every interactive icon has an accessible name.
- Every icon-only button has a 44x44px target.
- The same icon always means the same thing on every page.
- No icon is borrowed from a second set; the one recorded set covers every icon in use.
- The same icon always means the same thing on every page.
- Icons inherit currentColor and stay visible in light and dark themes.
- The icon set recorded in the stage record names the library, the sizes, the label rule and the icon-only exceptions.
- Every icon-only button carries its accessible name in the component inventory.
- The stage record carries the final icon set, not an earlier draft.
- The visual judger checks the single icon style and grid; the a11y judger checks accessible names and the 44x44px targets. The skill does the work and the judgers check it; the skill never grades its own output.

## Coordinator wiring

Loaded by stages: icon, components. Returns: `icon.icon_set` (library, sizes, label rule, icon-only exceptions); `components.inventory` (icon usage and accessible names per component). Judger boundary: visual judger checks icon consistency and crispness; a11y judger checks accessible names and target sizes.
