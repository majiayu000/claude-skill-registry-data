---
name: meowkit-design
description: Use this skill to generate well-branded interfaces and assets for MeowKit (AI Agent Toolkit for Claude Code), either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping.
user-invocable: true
---

Read the README.md file within this skill, and explore the other available files.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

## Quick orientation

- **Primary logo:** `/meow` slash-prompt mark. Fira Code 500, gradient `#1D4ED8 → #3B82F6`, slash in solid `#2563EB`, blinking caret. No bitmap files — render in code. See `preview/brand-logo.html` and `preview/logo-hifi.html`.
- **Palette:** Royal Blue `#2563EB` primary, accent glow `#60A5FA`, deep-space `#05070A → #1E3A5F` for dark mode.
- **Type:** Inter 400/500 for headings + body, Fira Code 500 for code/prompts/taglines. Headings use weight 400 (not bold) with `letter-spacing: .02em`.
- **Tokens:** all variables live in `colors_and_type.css` — source of truth is `design-tokens.json` mirrored from the upstream `packages/docs/app/global.css`.
- **UI kits:** `ui_kits/website/` (docs-site design recreation), `ui_kits/cli/` (terminal sessions).
- **Voice:** CLI-first, disciplined, playful-adjacent. Slash-commands (`/mk:plan`), Unicode glyphs (`✓ ✗ → ✋`), no illustrated mascot.
