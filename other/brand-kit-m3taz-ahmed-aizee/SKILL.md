---
name: brand-kit
description: Brand kit generator — visual identity, color, voice, logo, and templates. Lord-style orchestrator for consistent branding. Do not use for project voice tasks — use `project-voice` instead.
personas:
  - BRAND
  - MARKETING
triggers:
  - brand guideline
  - هوية بصرية
  - brand kit
  - logo
  - شعار
  - brand voice
  - دليل براند
tech_stack:
  - matomo-org/matomo
  - plausible/analytics
---
[SKILL] brand-kit
[OBJ] Produce a complete, reusable brand kit — colors, typography, voice, logo guidance, and templates — so every asset stays consistent across freelancer and business contexts.

[RULES]
1. [REQ] Kit components: (1) Mission/positioning, (2) Color palette (primary/secondary/neutral + hex), (3) Typography (heading/body/arabic), (4) Voice & tone, (5) Logo usage, (6) Templates (pitch, post, invoice).
2. [REQ] Color system: define 1 primary, 2-3 secondary, neutral scale; document contrast ratios (WCAG AA). Provide light/dark variants.
3. [REQ] Typography: pair a display + body font; for Arabic include a quality RTL typeface (e.g., Cairo/Tajawal) with proper shaping.
4. [REQ] Voice doc: adjectives (e.g., bold, precise), banned words, emoji policy, CTA style. Consumed by `personal-branding` + `copy-frameworks`.
5. [CMD] Context7 IDs: `matomo-org/matomo` (brand measurement), `plausible/analytics` (reach).
6. [REQ] Logo rules: clear-space, min-size, mono/color variants, forbidden distortions. Provide SVG + PNG.
7. [REQ] Templates: pitch deck slide, proposal cover, social post frame, invoice header — all reading from the kit variables.
8. [REQ] Arabic/RTL: full mirrored kit (ar palette names, RTL type, Arabic voice). One source of truth, two directions.
9. [REQ] Storage: keep kit as versioned asset (AIOS or repo) + a one-page PDF. Reference from every other skill that produces branded output.
10. [REQ] Governance: any new asset must pass a 10-point kit checklist before publish.

[PROHIBIT]
1. No asset outside the defined palette/type.
2. No unlicensed third-party logo/asset reuse.
3. No Arabic kit missing RTL typeface.
4. No brand voice contradicting the documented tone.
