---
name: dark-mode
description: "A calm second theme, not an inverted first one."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, theme]
    category: web
    related_skills: [web-design, design-tokens, colour-contrast]
    web_designer_stages: [theme, tokens]
---

# Dark Mode and Theming Skill

Dark mode is a complete second colour system, not an inversion of the light one. This skill covers defining both themes as token sets, respecting the user's system preference, offering a manual override, and re-checking contrast in the dark. Load-on-demand only, loaded by the web-designer coordinator for its stages; never auto-loads; never contacts the user directly — the coordinator is the only router.

## When to Use

- When a site offers a theme toggle or must respect the user's OS preference.
- At the theme stage, when the surface model for light and dark is decided.
- At the tokens stage, when both themes are encoded as token sets.
- When a page designed in light has never been seen in dark and its surfaces, images and logos need checking there.
- When elevation, shadows or borders that work in light need a dark equivalent that actually reads.

It is not for inverting the light theme's colours and calling the result dark mode. It is not for a dark theme that has never had its contrast re-checked, or for images and logos that disappear on dark surfaces.

## Prerequisites

- The run is active, the coordinator loaded this skill for its stage(s).
- The light theme is defined, so the dark theme can be designed as its own system rather than derived by inversion.
- Tokens exist or are built alongside, so both themes are token sets.
- The design-tokens skill is available for the token layer, and the colour-contrast skill for the re-check.
- Dark variants of logos and images are available or can be supplied where the light ones fail on dark surfaces.

## How to Run

1. Define the dark theme as its own token set: surfaces, text, accents and elevation, each named by role.
2. Use near-black surfaces, never pure black; use off-white text, never pure white.
3. Desaturate accents for dark surfaces, so they stay calm rather than glaring.
4. Show elevation by making surfaces lighter, not by adding shadows that vanish on dark backgrounds.
5. Respect the system preference by default, and offer a manual toggle that overrides it.
6. Re-check every text and background pair for contrast in dark mode, and provide dark variants of logos and images where the light ones fail.
7. Record the default theme and the surfaces in the theme stage record.
8. Walk the dark theme page by page after the re-check, confirming elevated cards read as lighter surfaces and no element relies on a shadow to be seen.
9. Check borders and dividers in dark mode: a border that relied on a light background may vanish on a dark one.
10. Confirm the toggle itself is visible and usable in both themes, so a user can always switch back.
11. After the re-check, record which pairs changed for dark mode and why, so the change is traceable.
12. Walk the dark theme with images and logos in place, not as placeholders, since a missing dark variant only shows with real assets.

## Quick Reference

- Surfaces: near-black `#121212` / `#1a1a1a`, never pure `#000`.
- Text: off-white `#e0e0e0`, not `#fff`.
- Accent desaturation: 15–30% / 70–80% saturation.
- Elevation: lighter surfaces, not shadows.
- Preference: `prefers-color-scheme`; declare `color-scheme: light dark`.
- Mechanism: CSS variables / `light-dark()`.
- Contrast: re-checked in dark mode; still passes AA.
- Toggle: manual override of the system preference, respected on every page.
- Logos and images: dark variants where the light ones fail on dark surfaces.
- Borders and dividers: checked in dark mode; a light-background border may vanish.
- Toggle: visible and usable in both themes, so a user can always switch back.
- Traceability: pairs changed for dark mode are recorded with the reason.

## Procedure

### 1. What it is

A complete second colour system, not an inversion: near-black surfaces (#121212/#1a1a1a, never pure #000), off-white text (#e0e0e0, not #fff), desaturated accents (15-30% / 70-80% saturation), elevation by lighter surfaces rather than shadows, via prefers-color-scheme, color-scheme: light dark and CSS variables / light-dark().

### 2. How Hermes applies it

Hermes defines both themes as token sets, respects system preference by default, offers a manual toggle that overrides it, re-checks contrast in dark mode, and provides dark variants of logos/images.

### 3. What it returns to the stage

The theme stage record in `gateway/web_designer/machine.py` (`STAGE_RECORDS`) requires `default` and `surfaces`, and the tokens stage record requires `tokens_path`. This skill's work fills the theme record with the default theme and the surface model for both themes, and fills the tokens record with the path to the token file holding both theme sets. A theme record that lists only the light surfaces, or a token set with no dark variants, is incomplete. Contrast results for the dark pairs are recorded with the surfaces, so the dark theme is never recorded as done without its re-check.

Both themes share the same semantic token names, so a theme switch changes values behind one name rather than renaming tokens. The toggle state and the system preference it overrides are recorded with the theme record, so the delivered behaviour — system preference by default, manual toggle overriding it — is visible in the record rather than assumed.

The dark theme is a design task, not a conversion task: every surface, text pair, accent and elevation choice is made for dark, then checked, then recorded. The record keeps the dark pairs and their contrast results with the surfaces, so the theme can be re-checked later without redoing the design. A dark theme recorded without its contrast results is a theme that was designed but never verified.

### 4. Good looks like

Dark mode is calm, not harsh; contrast still passes AA; elevated cards are lighter, not shadowed; images and logos remain visible.

A dark theme that feels calm is a theme that did its job. The calm is the test, not the colour values. Where a surface is harsh, an accent glaring, or a shadow doing nothing, the theme is an inversion wearing a token set. That is why the re-check covers every pair, and why elevation is lighter surfaces rather than shadows.

## Pitfalls

- Pure-black dark surfaces (`#000`) and pure-white text (`#fff`): harsh, not calm.
- Inverting the light theme instead of designing a second colour system.
- Using full-saturation accents on dark surfaces, so they glare.
- Showing elevation with shadows that disappear on dark backgrounds, instead of lighter surfaces.
- Ignoring the system preference, or offering a toggle that does not actually override it.
- Never re-checking contrast in dark mode, so text that passed in light fails in dark.
- Logos and images that vanish on dark surfaces because no dark variant exists.
- Holding light and dark values under different token names, so a theme switch means renaming rather than switching values.
- A border or divider that vanishes on a dark surface because it relied on a light background.
- A toggle that cannot be seen or used in one of the themes.
- Re-checking contrast in light mode only and assuming dark mode follows.

## Verification

- Surfaces are near-black (`#121212` / `#1a1a1a`); no pure `#000` surface and no pure `#fff` text.
- Accents are desaturated to 15–30% / 70–80% saturation.
- Elevated cards are lighter surfaces, not shadowed.
- The system preference is respected by default and the manual toggle overrides it.
- Contrast passes AA in dark mode, and logos and images remain visible.
- Both themes share semantic token names, and the toggle state is recorded with the theme record.
- Borders and dividers are checked in dark mode.
- The toggle is visible and usable in both themes.
- Pairs changed for dark mode are recorded with the reason.
- The visual judger checks the related colour and surface rules, and the a11y judger checks dark-mode contrast. The skill does the work and the judgers check it; the skill never grades its own output.

## Coordinator wiring

Loaded by stages: theme, tokens. Returns: theme stage-record keys `default`, `surfaces` and tokens stage-record key `tokens_path`. Judger boundary: visual judger checks the related colour rules; a11y judger checks dark-mode contrast.
