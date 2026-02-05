---
name: pbir-template-extractor
description: Extract Power BI PBIR visuals into reusable templates. Use when users want to save an existing visual configuration as a template, standardize visual formats across projects, or add new visual types to the template library.
---

# PBIR Template Extractor

Extract existing PBIR visuals and convert them to reusable templates with placeholders.

## When to Use This Skill

Use when the user wants to:
- Save an existing visual as a reusable template
- Create a new template type not in the library
- Standardize a visual configuration for reuse
- Extract a well-formatted visual from Power BI Desktop
- Add to the visual-templates library

## Workflow

### Step 1: Locate Source Visual

Find the visual.json file to extract:

```
# List pages in the report
Glob: .Report/definition/pages/*/page.json

# List visuals on a page
Glob: .Report/definition/pages/[PageGUID]/visuals/*/visual.json

# Read specific visual
Read: .Report/definition/pages/[PageGUID]/visuals/[VisualGUID]/visual.json
```

### Step 2: Analyze Visual Structure

Identify:
1. **Visual type** - `visualType` property (card, barChart, lineChart, etc.)
2. **Data roles** - Query projections (Values, Category, Y, Series, etc.)
3. **Formatting** - Objects in `visualContainerObjects` and `visual.objects`
4. **Special features** - Interactions, drill-through, conditional formatting

### Step 3: Create Placeholders

Replace specific values with `{{PLACEHOLDER}}` syntax:

**Always Replace:**

| Value | Placeholder |
|-------|-------------|
| Visual GUID (name) | `{{VISUAL_NAME}}` |
| Position x | `{{X}}` |
| Position y | `{{Y}}` |
| Position z | `{{Z}}` |
| Width | `{{WIDTH}}` |
| Height | `{{HEIGHT}}` |
| Tab order | `{{TAB_ORDER}}` |
| Title text | `{{TITLE}}` |
| Filter names (GUIDs) | `{{FILTER_GUID}}` |

**Data Binding Replacements:**

| Binding | Placeholders |
|---------|--------------|
| Primary measure | `{{TABLE_NAME}}`, `{{MEASURE_NAME}}` |
| Multiple measures | `{{MEASURE_1_TABLE}}`, `{{MEASURE_1_NAME}}`, etc. |
| Category axis | `{{CATEGORY_TABLE}}`, `{{CATEGORY_COLUMN}}` |
| Series/Legend | `{{SERIES_TABLE}}`, `{{SERIES_COLUMN}}` |
| Matrix rows | `{{ROW_TABLE}}`, `{{ROW_COLUMN}}` |
| Matrix columns | `{{COLUMN_TABLE}}`, `{{COLUMN_COLUMN}}` |
| Map location | `{{LOCATION_TABLE}}`, `{{LOCATION_COLUMN}}` |
| Scatter X/Y | `{{X_MEASURE_TABLE}}`, `{{Y_MEASURE_TABLE}}`, etc. |

**Formatting Replacements (Optional):**

| Property | Placeholder |
|----------|-------------|
| Font size | `{{FONT_SIZE}}` |
| Display units | `{{DISPLAY_UNITS}}` |
| Colors | `{{MEASURE_1_COLOR}}`, etc. |
| Legend position | `{{LEGEND_POSITION}}` |

### Step 4: Validate Template

Before saving, verify:
- [ ] JSON is well-formed
- [ ] All specific values replaced with placeholders
- [ ] Schema reference preserved (`$schema`)
- [ ] No hardcoded table/column names remain
- [ ] No hardcoded visual names remain

### Step 5: Name and Save Template

**Naming Convention:**
```
[visual-type]-[variant].json

Examples:
- card-single-measure.json
- line-chart-with-series.json
- slicer-dropdown.json
- azure-map-bubble.json
```

**Save Location:**
```
visual-templates/[template-name].json
```

### Step 6: Update Documentation

Add entry to `visual-templates/README.md`:

```markdown
| `[template-name].json` | [Visual Type] | [Description] |
```

Document any unique placeholders for this template.

## Example: Extract a Bar Chart

**Source visual.json:**
```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
  "name": "SalesByRegionBar",
  "position": {
    "x": "100",
    "y": "200",
    "z": "2000",
    "height": "300",
    "width": "400",
    "tabOrder": "1"
  },
  "visual": {
    "visualType": "barChart",
    "query": {
      "queryState": {
        "Category": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "dim_region" } },
                  "Property": "region_name"
                }
              },
              "queryRef": "dim_region.region_name",
              "nativeQueryRef": "region_name",
              "active": true
            }
          ]
        },
        "Y": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "Fact_Sales" } },
                  "Property": "Total Sales"
                }
              },
              "queryRef": "Fact_Sales.Total Sales",
              "nativeQueryRef": "Total Sales"
            }
          ]
        }
      }
    }
  }
}
```

**Extracted template:**
```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
  "name": "{{VISUAL_NAME}}",
  "position": {
    "x": "{{X}}",
    "y": "{{Y}}",
    "z": "{{Z}}",
    "height": "{{HEIGHT}}",
    "width": "{{WIDTH}}",
    "tabOrder": "{{TAB_ORDER}}"
  },
  "visual": {
    "visualType": "barChart",
    "query": {
      "queryState": {
        "Category": {
          "projections": [
            {
              "field": {
                "Column": {
                  "Expression": { "SourceRef": { "Entity": "{{CATEGORY_TABLE}}" } },
                  "Property": "{{CATEGORY_COLUMN}}"
                }
              },
              "queryRef": "{{CATEGORY_TABLE}}.{{CATEGORY_COLUMN}}",
              "nativeQueryRef": "{{CATEGORY_COLUMN}}",
              "active": true
            }
          ]
        },
        "Y": {
          "projections": [
            {
              "field": {
                "Measure": {
                  "Expression": { "SourceRef": { "Entity": "{{TABLE_NAME}}" } },
                  "Property": "{{MEASURE_NAME}}"
                }
              },
              "queryRef": "{{TABLE_NAME}}.{{MEASURE_NAME}}",
              "nativeQueryRef": "{{MEASURE_NAME}}"
            }
          ]
        }
      }
    }
  }
}
```

## Handling Complex Visuals

### Multiple Measures

For visuals with multiple Y values, use numbered placeholders:
```
{{MEASURE_1_TABLE}}, {{MEASURE_1_NAME}}
{{MEASURE_2_TABLE}}, {{MEASURE_2_NAME}}
{{MEASURE_3_TABLE}}, {{MEASURE_3_NAME}}
```

### Conditional Formatting

Keep conditional formatting rules but placeholder the references:
```json
"rules": [
  {
    "field": {
      "Measure": {
        "Expression": { "SourceRef": { "Entity": "{{TABLE_NAME}}" } },
        "Property": "{{MEASURE_NAME}}"
      }
    }
  }
]
```

### Default Values

Some formatting values should remain hardcoded (good defaults):
- Font family: Keep as-is (e.g., "Segoe UI")
- Default colors: Keep unless user wants custom
- Axis show/hide: Keep as-is

## Quality Checklist

Before finalizing template:
- [ ] `$schema` property preserved at top
- [ ] `name` → `{{VISUAL_NAME}}`
- [ ] All position values → placeholders
- [ ] All table names → placeholders
- [ ] All column/measure names → placeholders
- [ ] Filter GUIDs → `{{FILTER_GUID}}`
- [ ] Title text → `{{TITLE}}`
- [ ] JSON validates successfully
- [ ] Template follows naming convention

## Contribution to Template Library

When adding new templates:

1. Test the template by creating a visual with it
2. Verify it opens correctly in Power BI Desktop
3. Add to `visual-templates/README.md`
4. Document any unique placeholders
5. Add to the "Available Templates" table

## Constraints

- Never modify the source visual.json
- Always preserve the schema version
- Use consistent placeholder naming
- Test templates before adding to library
