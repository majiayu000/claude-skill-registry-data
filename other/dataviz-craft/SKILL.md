---
name: dataviz-craft
description: "A shared reference library for editorial-grade data-visualization craft — Vega-Lite-first with a D3 fallback for charts Vega-Lite can't express. Read by the Designer at chart selection (intent → ranked chart type), the Programmer at implementation (editorial Vega-Lite recipes, annotation layers, axis/label de-clutter, encoding craft), and the Auditor/Critic for chart-quality review. It encodes the FT Visual Vocabulary intent taxonomy, the Cleveland–McGill channel-accuracy ordering, the BBC bbplot de-clutter ruleset, and colorblind-safe encoding rules. Not a pipeline stage — a craft source, like frontend-design."
allowed-tools: Read
---

# Dataviz Craft

A shared library for choosing and building **charts that carry one idea cleanly**. This is not a pipeline stage; it is a reference the **Designer** reads to pick the right chart type for the message, the **Programmer** reads to build it as an editorial Vega-Lite spec, and the **Auditor/Critic** reads to judge whether a chart is honest and legible.

It is the chart-craft counterpart to `frontend-design` (page/visual identity). For color scales it does **not** redefine anything — it cross-references `frontend-design/references/design_tokens.json` `data_color_scales`. For Vega-Lite mechanics (mount/centering/`width:container`/`scale.zero`/`labelExpr`) it **extends** `data2story-pro/programmer/references/component_implementations.json`, it does not duplicate it.

## When to use

- **Designer**: before writing a `chart_spec` per section, name the message's **intent** (deviation / correlation / ranking / distribution / change-over-time / part-to-whole / magnitude / spatial / flow) and pick a ranked candidate from [`references/chart_chooser.json`](references/chart_chooser.json). Record the chart type + intent + what to highlight in `designer.json`. If the chosen type is tagged `vega_lite_native: false`, flag it for the D3 fallback.
- **Programmer**: implement the chosen type from [`references/vega_recipes.json`](references/vega_recipes.json) (editorial Vega-Lite skeleton), add reference/threshold/label layers from [`references/annotation_layers.json`](references/annotation_layers.json), apply the de-clutter config from [`references/axis_label_polish.json`](references/axis_label_polish.json), and obey [`references/encoding_craft.json`](references/encoding_craft.json) (area-not-radius, sort-by-value, no dual-axis, colorblind-safe). For a `native:false` type use [`references/d3_fallback_recipes.json`](references/d3_fallback_recipes.json).
- **Auditor / Critic**: review a chart against the same files — is the chart type right for the stated intent (chart_chooser), does the baseline lie (axis_label_polish zero-baseline rule), is the key datum annotated (annotation_layers), is the encoding accurate and colorblind-safe (encoding_craft, Cleveland–McGill ordering)?

## Core principles

1. **Vega-Lite-first.** Build every chart Vega-Lite can express as a Vega-Lite spec via Vega-Embed (CDN). Reach for D3 **only** for types Vega-Lite cannot express (sankey, treemap, chord, sunburst, force-network) — see [`references/d3_fallback_recipes.json`](references/d3_fallback_recipes.json). D3 is an allowed CDN, not the default.
2. **One chart, one idea.** Each chart answers one question. If a chart needs two sentences to explain, split it. Pick the chart type from the *message intent*, not from what looks impressive — [`references/chart_chooser.json`](references/chart_chooser.json).
3. **Annotate the key datum.** The reader should see the point being made without hunting. Label the line end, draw the threshold/reference line, highlight the one bar that matters with the accent — [`references/annotation_layers.json`](references/annotation_layers.json).
4. **De-clutter the frame.** Remove what doesn't carry information: minor gridlines, redundant axis lines/ticks/titles, legends when a direct label is clearer — [`references/axis_label_polish.json`](references/axis_label_polish.json).
5. **Right channel for the intent.** Prefer the most accurate visual channel the data allows: position > length > angle > area > color (Cleveland–McGill). Encode the key variable in the strongest available channel — [`references/encoding_craft.json`](references/encoding_craft.json), [`references/chart_chooser.json`](references/chart_chooser.json).
6. **Color is borrowed, never reinvented.** Use the story's `--accent` for the highlighted datum and mute the rest. For sequential/diverging/categorical scales, cross-reference [`frontend-design/references/design_tokens.json`](../frontend-design/references/design_tokens.json) `data_color_scales` — the same value means the same color across map, bars and callouts. Colorblind-safe rules live in [`references/encoding_craft.json`](references/encoding_craft.json).

## References

- **[`references/chart_chooser.json`](references/chart_chooser.json)** — the decision core: 9 message intents → ranked chart candidates, each tagged `vega_lite_native`; the purpose-first frame (comparison/composition/distribution/relationship/trend → narrow intent) and the Cleveland–McGill channel-accuracy hierarchy.
- **[`references/vega_recipes.json`](references/vega_recipes.json)** — per-type editorial Vega-Lite recipe skeletons for every native type (bar/grouped/stacked, line/area/layered, slope, dot/lollipop, facet small-multiples, heatmap, strip/beeswarm, connected-scatter, scatter/bubble, choropleth): mark, key encoding notes, highlight, editorial defaults.
- **[`references/annotation_layers.json`](references/annotation_layers.json)** — Vega-Lite annotation techniques: `rule` marks for threshold/reference lines and range bands, `text` + argmax for line-end labels instead of a legend, in-chart callout boxes, conditional highlight of the key datum.
- **[`references/axis_label_polish.json`](references/axis_label_polish.json)** — the BBC bbplot de-clutter ruleset as Vega-Lite config: gridline/tick/axis-line/title removal, legend on top, tick `format`/`labelExpr` ($/%/abbreviated, Vega-expr not JS), the zero-baseline rule, log-scale domain.
- **[`references/encoding_craft.json`](references/encoding_craft.json)** — beyond color: bubble area-not-radius, sort-by-value, the dual-axis warning, colorblind-safe palettes and redundant encoding. Cross-refs `design_tokens.json` `data_color_scales` for the actual scales.
- **[`references/d3_fallback_recipes.json`](references/d3_fallback_recipes.json)** — ONLY the non-native types (sankey, treemap, chord, sunburst, force-network): when to reach for D3, a recipe outline (D3 module + layout generator), and the SVG-mark performance ceiling.
- **[`../frontend-design/references/design_tokens.json`](../frontend-design/references/design_tokens.json)** — (cross-reference, not owned here) `data_color_scales` for sequential/diverging/categorical color.

A chart is well-crafted when its type matches the message intent, the baseline is honest, the one datum that matters is annotated, the frame carries no decoration, the strongest available channel encodes the key variable, and the colors mean the same thing everywhere and survive color blindness.

_license_note: This file encodes uncopyrightable methods and re-authored principles. Taxonomy and intent → chart mapping derive from the Financial Times Visual Vocabulary (method, re-authored — not FT prose). Channel-accuracy ordering from Cleveland & McGill (1984). De-clutter rules adapted from the BBC bbplot R package (MIT). Purpose-first framing and several encoding facts re-authored from rohitg00/data-visualization and chrisvoncsefalvay data-viz references. Vega-Lite mechanics extend the project's own component_implementations.json.
