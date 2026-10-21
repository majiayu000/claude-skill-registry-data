---
name: chart-choice-by-relationship
description: "Use when deciding whether a number needs a chart at all and, if so, which form: pick by the relationship the reader must see (change over time, ranking, part-to-whole, deviation from target, distribution, correlation, flow/funnel, magnitude), not by what looks impressive. Covers when a sentence or a table beats a chart, and which ieeVisualizer mark or template expresses each form."
license: CC-BY-4.0
---

# Choose the chart by the relationship

Start from the sentence the reader should come away with, name the
relationship in it, then pick the form. If the sentence has one number, it
probably needs no chart.

## Step 0: does it need a chart?

| Situation | Use |
|---|---|
| One or two numbers | a sentence: "Orders: 212 in September, up from 188 in August." |
| Exact values will be looked up | a table (sorted, units in the header) |
| A shape, trend, spread or pattern is the point | a chart |
| A process, dependency or flow | a diagram (nodes and edges), not a chart |

## Step 1: name the relationship

| Relationship | Reader's question | First choice | Alternatives | Avoid |
|---|---|---|---|---|
| Change over time | How did it move? | line | column bars for few, discrete periods; slope chart for two points | pie per period, 3D |
| Ranking | Who is biggest? | horizontal bars, sorted | dot plot | unsorted bars, alphabetical order without reason |
| Magnitude comparison | How much bigger? | bars from zero | dot plot (when zero is irrelevant) | bubbles, pictograms with fractional icons |
| Deviation | Above or below target / last year? | diverging bars around the reference | line with reference line | two separate bars the reader must subtract |
| Part-to-whole | What share? | stacked bar (≤ about 4 parts) or sorted bars of shares | pie only for ≤ about 5 parts with one dominant | pie with similar slices or a missing slice; donut |
| Part-to-whole over time | How did the mix change? | stacked area or 100% stacked bars (few parts) | small multiples of lines | many-layer stacked areas (middle layers unreadable) |
| Distribution | How spread, skewed, multi-modal? | histogram; dot/strip plot for small n | ECDF, box plot, quantile dotplot | a bar of the mean alone |
| Correlation | Do two measures move together? | scatter (with n) | heatmap of binned counts for large n | dual-axis line chart |
| Flow / funnel | Where do we lose people? | horizontal bars per stage with counts and step rates | Sankey for branching flows | funnel graphics whose widths are not proportional |
| Spatial | Where? | map only when location matters to the decision | table by region | choropleth of raw counts (map population instead) |
| Uncertainty | How sure? | see `uncertainty-display` | | |

Limits above are guidance, not hard rules: the UK Analysis Function suggests
about four lines per line chart, four parts per stack, four bars per cluster
and five slices per pie; summaries of Wong's guide report the same limit of
about four lines (never more than five). Beyond them, use small multiples or highlight one series
and grey the rest.

## Step 2: map to ieeVisualizer (spec 1.0)

| Form | How |
|---|---|
| Line over time | `timeseries` template (units, forecast split, caller-supplied bounds) or `line` mark |
| Bars, ranking, deviation | `bar` mark, `orientation: "horizontal"` for rankings and long labels; sort the data upstream |
| Stacked / shares | `bar` or `area` with `series`; compute shares upstream and set the unit to `%` |
| Distribution | `histogram` mark (`bins` or `bin_edges`, `density`); scatter of raw points for small n |
| Correlation | `scatter` mark; `heatmap` for binned counts |
| Funnel | `funnel` template (stage counts, step and overall rates with their numerators and denominators), or a horizontal `bar` mark with stage order preserved |
| Reference / target | `reference_line` / `reference_band` annotations, or the template's `target` |
| Fields, functions | `quiver`, `function`, `vector_field_2d` template |
| Grouped comparison, vs previous period | `bar_comparison` template |
| Small multiples, dual-panel | not in one FigureSpec: render one figure per panel with identical axis limits, or place them side by side in a `ViewSpec` grid |
| Flow / architecture diagram | a flow component in a `ViewSpec` (`ieeVisualizer.view`, docs/VIEWS.md); do not fake it with a scatter plot |
| Network, hierarchy, dependencies | `network`, `org_chart`, `dependency_map` templates (`ieeVisualizer.network`, docs/NETWORKS.md) |

If none fits, follow the extensibility ladder in `ieevisualizer-figures`
(template → compose marks → specialist adapter → bespoke code, rarely).

## Good / bad

Bad: pie chart of orders by source with eight similar slices.
Good: horizontal bars, sorted, labelled with counts and shares, "Other"
last regardless of size.

Bad: line chart joining "North, South, East, West" regions (categories are
not a sequence).
Good: sorted bars.

Bad: for an ablation with three seeds per variant, bars of the mean
accuracy.
Good: dot plot of the three seed results per variant with the mean marked
(`ml-results-reporting`).

## Checklist

- [ ] The one-sentence takeaway is written before the chart is chosen.
- [ ] A sentence or table was considered and rejected for a reason.
- [ ] The form matches the relationship in the table above.
- [ ] Categories without natural order are sorted by value; ordered ones
      (stages, months, age bands) keep their order.
- [ ] Series and part counts are within guidance, or highlighted/split.
- [ ] Comparisons across panels use identical scales.

Adapted in part from Anthropic's `data-visualization` skill (Apache-2.0) and
the UK Analysis Function chart guidance (OGL v3.0); changed: rewritten,
reorganised by reader question, ieeVisualizer mapping added. Sources and
licences: `SOURCES.md`.
