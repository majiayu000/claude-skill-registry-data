---
name: ui-token-first
description: Enforce UI token usage for Espresso Engineered frontend work. Use when editing Svelte/SvelteKit UI, styling typography, voice lines, headers, cards, surfaces, or layout so styles come from frontend/src/lib/ui tokens instead of app.css or ad-hoc CSS.
---

# UI Token First

## Overview

Apply UI framework tokens (typography, color, surfaces) for all UI styling in this repo. Avoid new CSS in `frontend/src/app.css` or local hardcoded styles unless no token exists.

## Workflow

1. Identify the UI elements being changed (headers, voice lines, cards, surfaces, etc.).
2. Pull tokens from `frontend/src/lib/ui` and apply them with `toStyleString`.
3. Remove or avoid ad-hoc font/color rules that bypass the tokens.
4. Confirm voice text rules in `docs/ee-ui-execution-standard.md`.

## Token Sources

- Typography: `frontend/src/lib/ui/foundations/typography.ts` (`textStyles`, `fontFamilies`)
- Colors: `frontend/src/lib/ui/foundations/color.ts` (`colorCss`)
- Surfaces: `frontend/src/lib/ui/components/card.ts` (`pageSurface`, `recordListShell`, `secondarySurface`)
- CSS utilities: `frontend/src/lib/ui/style.ts` (`toStyleString`, `toCssVars`)

## Patterns to Use

- Voice lines: use `.voice-line` or `.voice-text` + `textStyles.voice` and `colorCss.text.ink.muted` via `toStyleString`. Never add new `font-family` CSS for voice text.
- Headers: use `textStyles.headingPrimary|Secondary|Tertiary` + `colorCss.text.ink.*`.
- Subtext/helper: use `textStyles.helper` + muted ink.
- Surfaces: wrap sections with `recordListShell`/`pageSurface` tokens and wire CSS vars rather than hardcoded backgrounds/borders.

## Quick Checks

- Search for `font-family`, `color: #`, or new `app.css` rules; replace with UI tokens.
- If you add a new text element, it should map to a `textStyles.*` token.
