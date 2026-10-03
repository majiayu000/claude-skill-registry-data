---
name: bg-text
description: >
  Use when writing, editing, or reviewing Bulgarian-language text, or when user
  mentions bg-text. Covers typography, clear writing, editorial review, UX writing,
  business correspondence, localization, and Bulgarian-specific language issues.
---

# bg-text — repo adapter skill

This repository keeps the canonical maintained skill at `skills/bg-text/SKILL.md`.

Use this repo-scoped adapter when the agent discovers skills from standard project
folders such as `.agents/skills/`, `.claude/skills/`, `.cursor/skills/`, or
`.gemini/skills/`.

Apply these defaults unless the user explicitly asks for a different style:

- Use Bulgarian quotation marks: `„…“` and nested `‚…‘`.
- Prefer natural contemporary Bulgarian over Russian-influenced wording or word order.
- Prefer clear, direct phrasing over bureaucratic or literal translated wording.
- Keep UI and product text short, specific, and easy to scan.
- Match the intended address/register. Do not default to formal `Вие` when informal `ти` or a neutral construction fits the audience, product, game, community, or existing style better.
- Use Bulgarian numeric and punctuation conventions such as decimal comma, spaced thousands, and `№`.

Load the maintained reference material from `../../../skills/bg-text/references/` as needed:

- `typography.md` for typography and spacing
- `clear-writing.md` for style and weak phrasing
- `ux-writing.md` for UI copy and microcopy
- `business-writing.md` for email and business correspondence
- `editorial-punctuation.md` for punctuation review
- `editorial-grammar.md` for grammar and agreement
- `anti-patterns.md` for common problems and fixes
- `scoring.md` for quality scoring
- `sources.md` for source hierarchy and attribution
- `addenda.md` for accumulated project-specific notes

If both this adapter and `skills/bg-text/SKILL.md` are visible, prefer the nested
canonical file as the fuller maintained version.
