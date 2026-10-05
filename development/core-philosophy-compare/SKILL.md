---
name: core-philosophy-compare
description: "Compare Drupal core philosophy lenses, debate edges, and supporting evidence without simulating named contributors."
---

# core-philosophy-compare

Compare Drupal core philosophy lenses and the evidence behind them.

## Mandatory Disclosure

Every response must close with:

> Based on public issue queue records and cross-author analysis. Not authored by or endorsed by any named contributor.

## Inputs

Use this skill when the user asks:
- how two philosophies differ
- which debate lines exist on a topic
- which contributors support each side of a tradeoff

## Required Data Sources

- `config/philosophy-lenses.json`
- `analysis/lenses/author-lens-map.json`
- `config/topic-taxonomy.json`
- `analysis/grounding/manifest.json`
- `analysis/grounding/*.json` as needed through `scripts/build-grounding-bundle.py`

## Required Process

1. Determine whether the user is comparing:
   - two lenses directly
   - a topic with multiple competing lenses
   - contributors indirectly through the lenses they support
2. Summarize the difference in:
   - priorities
   - acceptable tradeoffs
   - likely objections
3. Cite named contributors only in the evidence/provenance layer.
4. Prefer configured `tension_axes` as the default source of “normally oppositional viewpoints”.
5. When a comparison touches product direction, governance, release timing, or site-builder value, include the `project-stewardship` review lens and its supporting evidence when available.
6. If the comparison uses corpus-derived evidence, save the full output, unmodified, to `~/Codex/drupal-core-reviews/YYYY-MM-DD-{slug}.md` with the required frontmatter from `AGENTS.md`.

## Hard Rules

- Do not stage mock dialogue between contributors.
- Do not write as if any contributor is speaking.
- Keep the comparison at the level of principles, constraints, and evidence.
- Treat named contributors as supporting evidence, not as the primary unit of opposition.

## Output Structure

### Comparison Target

### Core Difference

### Where They Converge

### Where They Diverge

### Arbiter Lens

### Supporting Evidence
- contributors + issue/CID citations

### Uncertainty
