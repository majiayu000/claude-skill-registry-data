---
name: altair-python
description: Use for writing, reviewing, debugging, or testing declarative statistical visualizations in Python with Altair and Vega-Lite, including Chart marks, typed encodings, transforms, parameters/selections, layers, facets, scale resolution, data transformers, and specification export. Do not use for Plotly figures, imperative Matplotlib drawing, dashboard state, or data-cleaning work without an Altair output.
argument-hint: "[Altair chart task, data contract, spec, interaction, or failure]"
---

# Altair Python

Build the smallest valid declarative specification that answers the stated
question. A chart maps data fields to visual channels; it is not a sequence of
drawing commands and does not contain rendered pixels.

## Boundary

Use this skill when a project imports Altair or explicitly requests Altair or a
Vega-Lite specification. Do not introduce it into Plotly/Matplotlib-only code,
Streamlit application-state work, or a pure dataframe transformation. Preserve
the required artifact boundary: Python chart object, JSON spec, HTML, or image.

## Know the objects

| Object | Runtime meaning | Use |
|---|---|---|
| `Chart` | Declarative unit specification over a data source | Add one mark, encodings, transforms, parameters, and properties. |
| Mark | Geometric representation such as point, line, bar, area, rect, rule, or text | Choose from the analytical task and data grain. |
| Encoding channel | Mapping from field/value/datum/expression to x, y, color, size, shape, tooltip, facet, etc. | Declare field type, aggregation, scale, axis, legend, sort. |
| Transform | Vega-Lite data operation inside the specification | Filter, calculate, aggregate, bin, time unit, window, lookup, fold, and related view-local work. |
| Parameter/selection | Named interactive value or selected data subset | Drive filters, conditions, domains, or bound controls. |
| Compound chart | Layer, facet, repeat, horizontal/vertical concat | Compose related views with explicit shared/independent guides. |
| Serialized spec | Validated Vega-Lite JSON-compatible tree | Test, inspect, embed, save, or hand to a renderer. |

Read [the declarative grammar](references/grammar.md) before choosing mark,
grain, encoding type, aggregation, or interaction.

## Ordered workflow

1. State the analytical question, one-row data grain, fields, missing-value
   policy, required ordering, and output host before selecting a mark.
2. Decide whether the displayed grain equals input rows or a derived aggregate,
   bin, window, fold, lookup, or time unit. Make that transformation explicit.
3. Choose the mark from the relationship: position for quantitative comparison,
   line only for meaningful ordered continuity, bar for discrete magnitude,
   rect for two-dimensional bins, rule/text only as annotation.
4. Encode fields with explicit semantic types when inference could be wrong:
   quantitative, temporal, ordinal, nominal, or geographic. Configure sort,
   scale, axis, legend, and tooltip from the contract.
5. Add composition or interaction only when it serves the question. Name
   parameters and resolve scales/guides deliberately.
6. Decide where data lives: inline values, URL, named dataset, or a configured
   transformer. Never disable a row safeguard merely to silence an error.
7. Validate/inspect the serialized spec and test semantic nodes. Render in the
   real host only when visual integration is part of completion.

## Intent to specification

| Question | Typical grammar | Invariant |
|---|---|---|
| Relationship between two measures | point with quantitative x/y | One mark per intended observation; reveal overplotting when material. |
| Trend across ordered time | line with temporal x and quantitative y | Time is sorted; missing intervals/series do not imply false continuity. |
| Compare categories | bar/tick with nominal/ordinal category and quantitative value | Aggregation and category order are explicit; zero baseline policy is defensible. |
| Distribution | binned bar, tick, boxplot, density, or ECDF-style transform | Bin/statistic and units are visible. |
| Two-dimensional magnitude | rect/heatmap with x/y bins and color | Color type/domain and missing bins are defined. |
| Same measure across groups | facet/repeat small multiples | Comparable scales are shared unless independent scales are an explicit need. |
| Overlay observations and summary | layer charts over common data/encodings | Layer order and scale resolution preserve meaning. |
| Interactive subset | parameter/selection plus conditional encoding or filter | Empty-selection and initial-state behavior are defined. |

## Canonical anchor

```python
import altair as alt


def sales_chart(data):
    return (
        alt.Chart(data)
        .mark_line(point=True)
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("revenue:Q", title="Revenue"),
            color=alt.Color("region:N", title="Region"),
            tooltip=[
                alt.Tooltip("date:T"),
                alt.Tooltip("region:N"),
                alt.Tooltip("revenue:Q", format=",.2f"),
            ],
        )
        .properties(title="Revenue by region")
    )
```

The return value remains a chart/specification. Do not call display/save inside
a reusable chart builder unless that side effect is its public contract.

## Data and transform boundary

- Transform in Python when the result is shared outside the chart, requires
  domain validation, or is easier to unit-test as data.
- Transform in Vega-Lite when it is view-local, must react to a parameter, or
  should remain coupled to the visualization grammar.
- Do not both pre-aggregate and declare the same aggregation in an encoding.
- Explicitly retain group keys through aggregate/window operations.
- Treat Altair data transformers as serialization/loading policy, not
  Vega-Lite transforms. Sampling changes the analytical result and requires an
  explicit statistical decision.
- For large data, aggregate/filter upstream or use an intentional external-data
  path. Never globally disable maximum-row protection as a default fix.

Read [data and transform rules](references/data-transforms.md).

## Composition and interaction

Layer when views share coordinates; facet/repeat when subsets need comparable
panels; concatenate when views have distinct coordinates. For compound views,
state whether x/y scales, legends, and axes are shared or independent. Define a
parameter once at the correct scope, then use it through a filter, condition,
or domain. Do not add `.interactive()` as a substitute for a specified
selection behavior.

Read [composition, export, and testing](references/composition-testing.md).

## Verification

Inspect the installed version of Altair and the target renderer before using a
drift-sensitive parameter/transform/export signature. This foundry had no
Altair installation during authoring, so examples are primary-source-grounded
but not locally rendered.

Completion requires: correct input and displayed grain; explicit field types,
aggregation, sort, and scale semantics; stable null/empty behavior; no duplicate
aggregation; intentional data transport; valid serialized specification;
semantic tests for marks/encodings/transforms/parameters; and a host render or
clearly reported missing render evidence when appearance matters.

## References

- [Declarative grammar and encoding](references/grammar.md)
- [Data and transform boundary](references/data-transforms.md)
- [Composition, export, and testing](references/composition-testing.md)
