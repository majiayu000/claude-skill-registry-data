---
name: pbir-visual-creator
description: Create Power BI PBIR visuals from templates. Use when users need to add visuals (cards, charts, tables, slicers, maps) to Power BI Enhanced Report Format projects. Handles template selection, placeholder substitution, measure/column binding, and visual.json generation.
---

# PBIR Visual Creator

Create Power BI visuals for PBIR (.Report folder) projects using validated templates.

## When to Use This Skill

Use when the user wants to:
- Add a new visual to a Power BI report page
- Create a card, chart, table, matrix, slicer, or map visual
- Generate visual.json files for PBIR projects
- Bind measures or columns to visuals

## Available Templates

Search `visual-templates/` in this plugin for available templates:

| Template | Visual Type | Use Case |
|----------|-------------|----------|
| `card-single-measure.json` | Card | Single KPI display |
| `line-chart-category-y.json` | Line Chart | Trend over category |
| `line-chart-multi-y.json` | Line Chart | Multiple measures on Y |
| `line-chart-with-series.json` | Line Chart | Category + legend series |
| `bar-chart-category-y.json` | Bar Chart | Horizontal bars |
| `bar-chart-with-series.json` | Bar Chart | Grouped/stacked bars |
| `clustered-column-multi-measure.json` | Column Chart | Side-by-side columns |
| `table-basic.json` | Table | Columnar data |
| `matrix-basic.json` | Matrix | Pivot table |
| `pie-chart.json` | Pie Chart | Part-to-whole |
| `scatter-bubble-chart.json` | Scatter/Bubble | X-Y relationship |
| `azure-map-gradient.json` | Azure Map | Filled regions |
| `azure-map-bubble.json` | Azure Map | Bubble markers |
| `slicer-between-date.json` | Slicer | Date range filter |
| `slicer-dropdown.json` | Slicer | Dropdown selection |
| `slicer-list-multiselect.json` | Slicer | Multi-select list |
| `image-static.json` | Image | Static logo/image |

## Workflow

### Step 1: Gather Requirements

Ask the user:
1. **Visual type** - What kind of visual? (card, bar chart, line chart, etc.)
2. **Data bindings** - Which measures/columns?
3. **Position** - Where on the page? (or use layout defaults)
4. **Title** - Visual title text
5. **Target page** - Which report page folder?

### Step 2: Select Template

```
# Find matching template
Glob: visual-templates/*.json

# Read template
Read: visual-templates/[selected-template].json
```

### Step 3: Substitute Placeholders

Replace `{{PLACEHOLDER}}` values:

**Common:**
- `{{VISUAL_NAME}}` - Unique identifier (e.g., `TotalSalesCard`)
- `{{X}}`, `{{Y}}` - Position coordinates
- `{{WIDTH}}`, `{{HEIGHT}}` - Dimensions
- `{{Z}}` - Z-order (typically 2000+)
- `{{TAB_ORDER}}` - Keyboard navigation order
- `{{TITLE}}` - Visual title text
- `{{FILTER_GUID}}` - Generate with `secrets.token_hex(10)`

**Data Bindings:**
- `{{TABLE_NAME}}`, `{{MEASURE_NAME}}` - Primary measure
- `{{CATEGORY_TABLE}}`, `{{CATEGORY_COLUMN}}` - X-axis dimension
- `{{SERIES_TABLE}}`, `{{SERIES_COLUMN}}` - Legend/series

### Step 4: Generate visual.json

Create folder structure:
```
.Report/definition/pages/[PageGUID]/visuals/[VisualGUID]/visual.json
```

Generate GUID: `VisualContainer` + 8 random hex digits

### Step 5: Validate Output

Before writing, verify:
- [ ] JSON is well-formed
- [ ] All placeholders replaced
- [ ] Measure/column references are correct
- [ ] Position within canvas (1600x900)

## Example: Create a Card Visual

**User request:** "Add a Total Sales card to the Dashboard page"

**Process:**
1. Read `visual-templates/card-single-measure.json`
2. Replace placeholders:
   ```
   {{VISUAL_NAME}} → "TotalSalesCard"
   {{TABLE_NAME}} → "Fact_Sales"
   {{MEASURE_NAME}} → "Total Sales"
   {{TITLE}} → "Total Sales"
   {{X}} → "24"
   {{Y}} → "80"
   {{WIDTH}} → "300"
   {{HEIGHT}} → "180"
   {{Z}} → "2000"
   {{TAB_ORDER}} → "0"
   {{FILTER_GUID}} → "a1b2c3d4e5f6789012ab"
   {{FONT_SIZE}} → "32"
   {{DISPLAY_UNITS}} → "1"
   ```
3. Write to `.Report/definition/pages/ReportSection.../visuals/VisualContainerABCD1234/visual.json`

## Data Binding Patterns

**Measure reference:**
```json
{
  "field": {
    "Measure": {
      "Expression": { "SourceRef": { "Entity": "TableName" } },
      "Property": "Measure Name"
    }
  },
  "queryRef": "TableName.Measure Name",
  "nativeQueryRef": "Measure Name"
}
```

**Column reference:**
```json
{
  "field": {
    "Column": {
      "Expression": { "SourceRef": { "Entity": "TableName" } },
      "Property": "column_name"
    }
  },
  "queryRef": "TableName.column_name",
  "nativeQueryRef": "column_name",
  "active": true
}
```

## Schema Version

All templates use PBIR schema version **2.4.0**:
```
https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json
```

## Constraints

- Templates are read-only (don't modify originals)
- Always generate unique visual GUIDs
- Validate JSON before writing
- Use `queryState/projections` structure (not legacy config blobs)
