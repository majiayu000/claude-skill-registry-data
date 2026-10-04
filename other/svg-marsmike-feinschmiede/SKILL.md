---
name: svg
description: Generate SVG diagrams from a compact DSL with brand-resolved colors. Use for charts, flows, and schematic 2D graphics.
---

# feinbild — SVG diagrams

## Quick Start

```
/svg diagram.svg.dsl
```

`feinbild` is a command on your PATH. Two steps: expand a `.svg.dsl` to `.svg`
(brand colors resolved), then render to PNG.

```bash
feinbild svg expand chart.svg.dsl --brand feinschliff   # -> chart.svg
feinbild svg render chart.svg                           # -> chart.png
feinbild verify chart.svg                               # lint: overflow, overlap, label collision
```

`--brand` (or a leading `@brand <name>` line in the DSL) selects the brand;
`render` takes no brand (it consumes already-resolved colors). Write outputs
into the project so other plugins can consume them.

## Default to clean

- **≤3 arrows per flow.** More than that means the layout is wrong — re-chunk or pick another visualization.
- **No text over shapes.** Labels live inside boxes or adjacent via a connector — never on a border.
- **Aspect-aware.** Default 16:9 (1920×1080). If the brief specifies a target slot match it; otherwise embeds get squished.
- **Metaphor, not clutter.** Briefs saying "messy" / "tangled" / "stitched" describe a CONCEPT — convey via composition (overlap, dim color, tight grouping), not by drawing actual chaos.

## References

- [DSL reference](references/dsl-reference.md) — canvas header, basic + extended
  primitives, the 17-name semantic color vocabulary, the `virtual:` viewport.
- [Examples](references/examples.md) — small / medium charts (bar chart, stat
  card grid, annotated chart).
- [Deep examples](references/examples-deep.md) — dense compositions with the
  extended primitive set (`stacked_bar`, `brace`, `callout`, `swatch_grid`,
  `label_box`, `polyline`, `path`); see `examples/yocto-build-pipeline.svg.dsl`.

Workflow: author a `.svg.dsl`, run `feinbild svg expand` then `render`, inspect
the PNG, and do at most one DSL fix loop before escalating to the references above.
