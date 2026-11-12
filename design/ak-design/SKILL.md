---
name: ak-design
description: "Design brand identity, logos, banners, posters, design tokens and visual campaign assets."
when_to_use: "Invoke for brand systems or corporate identity; not for UI code patterns."
category: design
keywords: [brand, logo, CIP, banners, posters, identity]
argument-hint: "[design-type] [context]"
license: Proprietary; includes MIT-licensed third-party material, see LICENSE.txt
metadata:
  author: agentkit
  version: "2.4.1"
---

# Design

Own art direction, brand identity and visual deliverables. UI implementation belongs to the
installed frontend-design/frontend-development/ui-styling capability; do not treat this as a
React or Tailwind recipe. Resolve brief, audience, brand assets, format and acceptance first.
For a named real brand load `references/brand-asset-protocol.md`; never fabricate its logo.
Reuse settled preferences and ask only for a material missing decision.

## Select the deliverable

| Deliverable | Load |
|---|---|
| Logo | `references/logo-builtin-usage.md` |
| Corporate identity | `references/cip-builtin-usage.md` |
| Slides | `references/slides-create.md` |
| Banner | `references/banner-sizes-and-styles.md` |
| Poster | `references/poster-builtin-usage.md` |
| Social image | `references/social-photos-design.md` |
| Icons | `references/icon-builtin-usage.md` |

Additional end-to-end examples live in `references/deliverable-recipes.md`; open only the
selected section. Use `references/design-workflow.md` for new/vague briefs and
`references/design-critique-guide.md` for concept, brand, legibility and output review.
Inspect exports for clipping, resolution and visual fidelity; report limitations honestly.

## References

| Topic | File |
|-------|------|
| Design Routing | `references/design-routing.md` |
| Brand Asset Protocol | `references/brand-asset-protocol.md` |
| Design Critique Guide | `references/design-critique-guide.md` |
| Design Workflow (junior-designer mode) | `references/design-workflow.md` |
| Handoff & Critique Gate (for `ak-frontend-design`/`ak-show-off`/`ak-slides`) | `references/handoff-gate.md` |
| Logo Built-in Usage | `references/logo-builtin-usage.md` |
| Logo Design Guide | `references/logo-design.md` |
| Logo Styles | `references/logo-style-guide.md` |
| Logo Colors | `references/logo-color-psychology.md` |
| Logo Prompts | `references/logo-prompt-engineering.md` |
| CIP Built-in Usage | `references/cip-builtin-usage.md` |
| CIP Design Guide | `references/cip-design.md` |
| CIP Deliverables | `references/cip-deliverable-guide.md` |
| CIP Styles | `references/cip-style-guide.md` |
| CIP Prompts | `references/cip-prompt-engineering.md` |
| Slides Create | `references/slides-create.md` |
| Slides Layouts | `references/slides-layout-patterns.md` |
| Slides Template | `references/slides-html-template.md` |
| Slides Copy | `references/slides-copywriting-formulas.md` |
| Slides Strategy | `references/slides-strategies.md` |
| Banner Sizes & Styles | `references/banner-sizes-and-styles.md` |
| Social Photos Guide | `references/social-photos-design.md` |
| Icon Built-in Usage | `references/icon-builtin-usage.md` |
| Icon Design Guide | `references/icon-design.md` |
| Poster Built-in Usage | `references/poster-builtin-usage.md` |
| Poster Design Guide | `references/poster-design.md` |
| Poster Prompt Engineering | `references/poster-prompt-engineering.md` |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/logo/search.py` | Search logo styles, colors, industries |
| `scripts/logo/generate.py` | Generate logos with Gemini AI |
| `scripts/logo/core.py` | BM25 search engine for logo data |
| `scripts/cip/search.py` | Search CIP deliverables, styles, industries |
| `scripts/cip/generate.py` | Generate CIP mockups with Gemini |
| `scripts/cip/render-html.py` | Render HTML presentation from CIP mockups |
| `scripts/cip/core.py` | BM25 search engine for CIP data |
| `scripts/icon/generate.py` | Generate SVG icons with Gemini 3.1 Pro |
| `scripts/poster/search.py` | Search poster styles, palettes, layouts, textures |
| `scripts/poster/generate.py` | Generate model-agnostic poster prompts |
| `scripts/poster/analyze.py` | Analyze poster references with Gemini vision |
| `scripts/poster/cluster.py` | Rebuild poster clusters and CSV data |
