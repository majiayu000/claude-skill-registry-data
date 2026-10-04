---
name: svg
description: Use when authoring custom data viz that doesn't fit a predefined chart layout — brand-aware SVG infographics via compact DSL.
---

# SVG Infographic Authoring

Generate brand-perfect SVG infographics using a compact DSL. Colors resolve against the active feinschliff brand pack — no per-skill palette. Use when the predefined chart layouts (`bar-chart`, `stacked-bar`, `kpi-grid`, `scorecard`, `funnel`) don't fit and a custom viz is needed.

## Quick start

Author a `.svg.dsl` file, expand it, then render. The default brand is `feinschliff`; override via `--brand <name>`, `FEINSCHLIFF_BRAND=<name>`, or an inline `@brand <name>` directive at the top of the DSL.

```bash
cd /path/to/feinschliff
uv run python -m lib.diagrams.svg_expand chart.svg.dsl   # add --brand <name> to override
uv run python -m lib.diagrams.render chart.svg            # → chart.png
```

Inspect the PNG. If something is off, adjust the DSL (positions, sizes, semantic colors) and re-run. One fix loop max — escalate to references if more is needed.

## References

- [DSL reference](references/dsl-reference.md) — primitives, semantic colors, layout
- [Examples](references/examples.md) — small / medium / complex fixtures
