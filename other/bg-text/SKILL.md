---
name: bg-text
description: >
  Use when writing, editing, or reviewing Bulgarian-language text, or when user
  mentions bg-text. Covers typography, clear writing, editorial review, UX writing,
  business correspondence, localization, and Bulgarian-specific language issues.
  Use this root skill when the repository is loaded directly as a Codex skill.
---

# bg-text

Bulgarian text quality skill for direct repository use.

This root file is a compatibility shim for environments that open a repository-level
`SKILL.md` directly.

Apply these defaults unless the user explicitly requests a different style:

- Use Bulgarian quotation marks: `„…“` and nested `‚…‘`.
- Prefer natural contemporary Bulgarian over Russian-influenced wording or word order.
- Prefer clear, direct phrasing over bureaucratic or literal translated wording.
- Keep UI and product text short, specific, and easy to scan.
- Match the intended address/register. Do not default to formal `Вие` when informal `ти` or a neutral construction fits the audience, product, game, community, or existing style better.
- Use Bulgarian numeric and punctuation conventions such as decimal comma, spaced thousands, and `№`.

Source discipline for this skill:

- Treat IBL BAS, BERON, and the Language Help Desk as primary sources for claims about norm.
- Treat UX-writing, localization, and brevity guidance as editorial or product practice unless a normative source is cited.
- Do not present the repository's dash preferences or UI-copy preferences as universal academic rules.
- `corpusbdr.info` may be useful as a linguistic research corpus, but it is not the primary normative source for standard Bulgarian orthography or punctuation.
- Anchor normative claims, when needed, to these starting points:
  - `https://ibl.bas.bg/ezikovi-spravki/`
  - `https://ibl.bas.bg/ezikovispravki/vaprosi/kavichki-8`
  - `https://ibl.bas.bg/rbe/lang/bg/запетая/`
  - `https://ibl.bas.bg/ezikovispravki/vaprosi/chislitelni-imena-sheyset-i-shestdeset-7-klas-7-i-klas-vii-klas-39-oto-2014-a-5/294`
  - `https://beron.mon.bg/beron`

Load the maintained reference material from `skills/bg-text/references/` as needed:

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

High-confidence externally verified areas in this repo:

- Bulgarian quotation marks and nested quotation marks
- Decimal comma and core punctuation spacing
- Ordinal numerals written with a period or with hyphenated endings
- The literary use of `ѝ`

Areas that should be framed as house style or pragmatic digital practice:

- dash choice in ordinary prose outside strict print typography
- UI punctuation minimization
- anti-bureaucratic phrasing and brevity defaults

For repo-scoped auto-discovery, this repository also provides adapter entrypoints in:

- `.agents/skills/bg-text/SKILL.md`
- `.claude/skills/bg-text/SKILL.md`
- `.cursor/skills/bg-text/SKILL.md`
- `.gemini/skills/bg-text/SKILL.md`

When both this file and `skills/bg-text/SKILL.md` are available, prefer the nested file as the fuller maintained version.
