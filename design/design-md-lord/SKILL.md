---
name: design-md-lord
description: Lord skill for DESIGN.md-driven UI work — pick, import, and apply real-world brand design references (Refero catalog, 2000+ DESIGN.md files) through aiZee's DesignLibrary. Use when a UI task needs a concrete visual direction instead of generic AI styling. Do not use for brand kit tasks — use `brand-kit` instead. Do not use for design research tasks — use `design-research` instead.
triggers:
  - design md lord
  - design.md
  - design system
  - brand design
  - refero
  - ui style reference
  - landing page design
  - dashboard design
  - pricing page
  - design tokens
  - هوية بصرية
personas:
  - UX
  - UI
  - DEV
tech_stack:
  - tailwind-4-3
lord: true

---

# Design MD Lord

[OBJ] Apply real-world design references (DESIGN.md files — Refero catalog, brand systems) to UI work via aiZee's `DesignLibrary`. Extract tokens, typography, spacing, components, and Do/Don't rules from references — as inspiration, never verbatim copying.

[RULES]
1. [CMD] For live evidence gathering (screens/flows/sections beyond the bundled catalog), use the `design-research` skill — Refero + Mobbin MCP. This skill applies the locked direction; that skill finds it.
2. [CMD] Browse the Refero catalog (styles.refero.design) for DESIGN.md references matching the project's vibe — 2000+ styles extracted from real sites.
3. [CMD] With the Refero MCP server configured (`refero` in `.devin/mcp_config.json`), search styles semantically instead of guessing.
4. [CMD] Import a reference into the local library: `DesignLibrary.import_brand(name, source)` accepts a `DESIGN.md` path or raw markdown — lands in `design-library/<name>/DESIGN.md` and loads immediately.
5. [CMD] Load + mix references: `DesignLibrary.load("apple")`, `.mix(["stripe", "linear"])` for cross-brand fusion, `.suggest(project_type)` for recommendations, `.detect_project_type(dir)` to auto-detect.
6. [REQ] Match reference to page type: landing/hero → bold brands (Linear, Vercel, Framer); dashboard/SaaS → density-first (Linear, Stripe, Sentry); pricing → conversion-focused (Stripe, Cal.com); docs → readability-first (Vercel, Notion); mobile → Apple/Google HIG.
7. [REQ] Extract, don't copy: pull semantic tokens (`--color-*` + role), type scale, spacing rhythm, radii, shadows, component patterns, and the Do/Don't rules — then apply to THIS project's design system, not a clone.
8. [REQ] Token discipline: every color/spacing/type choice must trace to a token in the reference or the project's `@theme`. NEVER invent ad-hoc values outside the token system.
9. [REQ] Honor the reference's Do/Don't section — it encodes what makes the style work (e.g., Apple's restraint, Linear's density, Stripe's elevation).
10. [REQ] Mix at most 2-3 references: colors/components/elevation from one, typography/layout from another. More sources = incoherent slop.
11. [PROHIBIT] Never copy brand names, logos, or trademarked assets — references guide style only.
12. [REQ] After applying, run `DesignSlopVerifier` — references prevent generic-AI output only if actually followed.
13. [REQ] RTL/Arabic projects: prefer references with clean geometric type; verify logical-property friendliness of spacing tokens.

[WORKFLOWS]
1. New page design: detect project type → `suggest()` or search Refero → pick 1-2 references → `import_brand()` → `load()`/`mix()` → extract tokens → map to `@theme`/components → build → `DesignSlopVerifier` → a11y pass.
2. Import a Refero style: find style on styles.refero.design (or MCP search) → copy `DESIGN.md` content → `DesignLibrary.import_brand("<name>", <content>)` → use like any catalog brand.
3. Refresh a stale UI: `detect_project_type()` → suggest modern references → diff current tokens vs reference → update `@theme` → verify components pick up tokens.
4. Product-first direction (design-db): `aizee design system "<product>" --variance 1-10 --motion 1-10 --density 1-10 [--out MASTER.md]` aggregates style + palette + typography + landing pattern + motion preset from the vendored corpus (ui-ux-pro-max-skill, MIT). `aizee design search "<q>" [--domain style|product|color|typography|google-fonts|icons|ux|landing|chart|gsap|react|app|reasoning] [--stack <name>]` for point queries; `aizee design domains|stacks` to list capabilities. Empty result = honest "no verified match" — never fabricate.

[VERIFY]
1. `DesignSlopVerifier` runs a tiered catalog (~44 deterministic rules ported from impeccable/hallmark/taste-skill): FLOOR (never ship — lorem/fake data, icon-only buttons, missing focus, layout-prop animation, 100vw, no reduced-motion guard, low contrast, tiny/skipped text — NOT waivable), REFLEX (unguided-model defaults — gradient washes/text, AI violet palette, eyebrow chips, marquees, icon tiles, hard-offset shadows, glow halos, oversized H1 — waivable on the record via `<!-- waive:<rule-id> -->` or `data-slop-waive`), FINISH (craft advisories — em-dash overuse, meta dots, glued arrows, decorative status dots). CLI: `aizee design slop <file.html|- >` exits 1 on slop.
2. `aizee design lint <brand|--all>` validates DESIGN.md files against the structured spec (YAML frontmatter, hex tokens, WCAG AA contrast pairs, typography, heading). Prose-only seeds warn, don't fail.
3. Rendered-DOM checks the regex layer can't see (viewport overflow, text truncation, computed contrast, spacing rhythm) go through `judge_fn` / browser evidence — taste-skill-style screenshot loop at 3 widths.
