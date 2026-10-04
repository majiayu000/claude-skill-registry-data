---
name: chart-visualization
description: This skill should be used when the user wants to visualize data. It selects an appropriate chart type, reads the corresponding chart specification from `references/`, converts user data into the exact required schema, and generates a chart image using a JavaScript script.
dependency:
  nodejs: ">=18.0.0"
---

# Chart Visualization Skill

This skill provides a structured workflow for transforming data into visual charts.

Its primary goal is **schema-correct chart generation**. The most important rule is:

> **Never call `scripts/generate.js` before reading the corresponding chart specification in `references/`.**

This skill should be preferred over ad hoc plotting code when the task is a standard chart-generation request.

## Mandatory Execution Policy

For every chart request, you **MUST** follow this exact order:

1. **Select the chart type** that best matches the user's request and data shape.
2. **Read the corresponding file in `references/`** for that chart type.
3. **Construct `args` strictly according to that reference file.**
4. **Validate** that required fields, field names, and data structure exactly match the selected reference.
5. **Only then** call `node ./scripts/generate.js '<payload_json>'`.

### Hard Rules

- **Never** call `scripts/generate.js` before reading the corresponding `references/generate_<chart_type>.md` file.
- **Never** construct payload fields purely from memory when a corresponding reference file exists.
- **Never** guess alternative field names such as `name`, `label`, `xAxisName`, `yAxisName`, or undocumented style keys unless they are explicitly supported by the corresponding reference file.
- If the selected chart type has no matching reference file, stop and report that the chart spec cannot be safely constructed.
- Return the final payload `args` together with the output image URL so the generated spec can be inspected.

## Workflow

To visualize data, follow these steps.

### 1. Intelligent Chart Selection

Analyze the user's data features to determine the most appropriate chart type.

Use the following guidelines:

- **Time Series**: Use `generate_line_chart` (trends) or `generate_area_chart` (accumulated trends). Use `generate_dual_axes_chart` when two series use different scales or chart types.
- **Comparisons**: Use `generate_bar_chart` (horizontal categorical comparison) or `generate_column_chart` (vertical comparison). Use `generate_histogram_chart` for frequency distributions.
- **Part-to-Whole**: Use `generate_pie_chart` or `generate_treemap_chart`.
- **Relationships & Flow**: Use `generate_scatter_chart`, `generate_sankey_chart`, or `generate_venn_chart`.
- **Maps**: Use `generate_district_map`, `generate_pin_map`, or `generate_path_map`.
- **Hierarchies & Trees**: Use `generate_organization_chart` or `generate_mind_map`.
- **Specialized**:
  - `generate_radar_chart`: Multi-dimensional comparison
  - `generate_funnel_chart`: Process stages
  - `generate_liquid_chart`: Percentage/progress
  - `generate_word_cloud_chart`: Text frequency
  - `generate_boxplot_chart` or `generate_violin_chart`: Statistical distribution
  - `generate_network_graph`: Complex node-edge relationships
  - `generate_fishbone_diagram`: Cause-effect analysis
  - `generate_flow_diagram`: Process flow
  - `generate_spreadsheet`: Tabular display or pivot-style cross-tabulation

### 2. Mandatory Reference Read Before Parameter Extraction

Once a chart type is selected, you **MUST** read the corresponding file in the `references/` directory before constructing any payload.

Examples:

- `generate_line_chart` -> `references/generate_line_chart.md`
- `generate_bar_chart` -> `references/generate_bar_chart.md`
- `generate_column_chart` -> `references/generate_column_chart.md`
- `generate_dual_axes_chart` -> `references/generate_dual_axes_chart.md`

This is a hard requirement.

After reading the reference file:

- Identify the **required** fields.
- Identify the **optional** fields actually supported.
- Convert the user's data into the exact schema required by that chart type.
- Do **not** rename fields unless the reference explicitly allows it.

### 3. Schema Normalization Rules

Use the selected reference file as the source of truth.

#### Common high-risk schema rules

- **Bar chart / Column chart**:
  - Usually require `data` records with `category` and `value`
  - Grouped or stacked variants require `group` only if supported by the reference
- **Line chart / Area chart**:
  - Usually require `data` records with `time` and `value`
  - Multi-series charts require `group` when specified by the reference
  - Do not use wide-table fields like `found`, `fixed`, `unfixed` unless the reference explicitly supports them
- **Dual axes chart**:
  - Use the `categories` + `series` structure if the reference requires it
  - Do not substitute it with `data` + `category/value` format
- **Axis titles**:
  - Use only the field names defined in the selected reference
  - Do not invent aliases such as `xAxisName` or `yAxisName` if the reference uses `axisXTitle` and `axisYTitle`


### 4. Pre-Execution Validation Gate

Before calling `scripts/generate.js`, you **MUST** verify all of the following:

1. The chart type has been selected.
2. The corresponding `references/generate_<chart_type>.md` file has been read.
3. The payload field names match that reference exactly.
4. All required fields are present.
5. The data shape matches the selected chart type.

If any of the above checks fail, **do not** execute `scripts/generate.js`.

### 5. Chart Generation

Invoke the `scripts/generate.js` script with a JSON payload only after the validation gate passes.

**Payload Format**

```json
{
  "tool": "generate_chart_type_name",
  "args": {
    "data": [...],
    "title": "...",
    "theme": "...",
    "style": { ... }
  }
}
```

**Execution Command**

```bash
node ./scripts/generate.js '<payload_json>'
```

### 6. Result Return

The script will output the URL of the generated chart image.

Return the following to the user:

- The image URL
- The complete final `args` used for generation
- A brief note describing which reference file was used


## Reference Material

Detailed specifications for each chart type are located in the `references/` directory.

You must treat those files as the authoritative schema definitions for payload construction.

## License

This `SKILL.md` is adapted from [antvis/chart-visualization-skills](https://github.com/antvis/chart-visualization-skills).
Licensed under the MIT License.