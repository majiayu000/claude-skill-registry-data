---
name: Aggregation and Export
description: Aggregate flat building elements into hierarchical construction documents with 4-level cost breakdown structure.
---

# Aggregation and Export

Maps flat JSON input to hierarchical DocumentConstructionDashboard schema with automatic parent section generation and total calculations.

## When to Use This Skill

Use this skill when the user asks about:
- Saving estimation results
- Generating final construction documents
- Creating cost breakdowns
- Exporting project summaries
- Organizing elements into construction sections

## Workflow Overview

This is the **final step** in the estimation pipeline:

```
Ingestion → Estimation Strategy → Aggregation & Export
```

**Purpose**: Take flat pricing results and:
1. Parse building IDs and hierarchical structure
2. Generate missing parent sections automatically
3. Calculate totals bottom-up through the hierarchy
4. Create DocumentConstructionDashboard with pricing lines
5. Save final output to JSON file

## Processing Architecture

### Hierarchy Building
The script analyzes building IDs (e.g., "1", "1.1", "1.1.1", "1.1.1.1") to:
- Extract parent sections that need to be created
- Determine element types (titre, section, subsection, line)
- Calculate indent levels based on depth
- Build section title mapping from Roman numerals

### Type Determination
Based on indent level and whether an element has children:
- **Level 0** ("1", "2"): titre or line
- **Level 1** ("1.1", "2.1"): section or line
- **Level 2** ("1.1.1"): subsection or line
- **Level 3+** ("1.1.1.1"): line

### Total Calculation
Calculates totals bottom-up:
1. Start with leaf elements (actual building elements)
2. Sum direct children for each parent
3. Propagate totals up through hierarchy

## Usage

### CLI Command

```bash
python aggregation_and_export.py --path_temp_file /path/to/input.json --project_id project_123
```

**Arguments:**
- `--path_temp_file` (required): Path to input JSON file
- `--project_id` (optional): Project ID to use in output (overrides project.id from input JSON)

**Output**: `aggregation_ui_<uuid>.json` saved in same directory as input file

The script will print the output path and format information when complete.

## Input Format

Flat array of building elements with project information:

```json
{
  "project": {
    "name": "Building A",
    "id": "project_123"
  },
  "elements": [
    {
      "building_id": "1.1.1",
      "building_name": "External Wall - North",
      "building_elm_section": "I - Préparation de chantier",
      "building_elm_unit": "m²",
      "building_elm_quantity": 50.0,
      "building_elm_unit_price": 150.0,
      "building_elm_total_ht": 7500.0,
      "project_id": "project_123",
      "project_name": "Building A"
    }
  ]
}
```

**Key Fields:**
- `building_id`: Hierarchical ID (e.g., "1", "1.1", "1.1.1")
- `building_name`: Element description
- `building_elm_section`: Section title with Roman numeral (e.g., "I - Title")
- `building_elm_unit`, `building_elm_quantity`, `building_elm_unit_price`, `building_elm_total_ht`: Pricing data

## Output Format

Dashboard-ready JSON with hierarchical pricing lines:

**Structure:**
- `projectId`: Project identifier
- `projectName`: Project name
- `pricingLines`: Array of pricing lines in hierarchical order

**Pricing Line Types:**
- `titre`: Top-level section (indent 0)
- `section`: Second-level section (indent 1)
- `subsection`: Third-level section (indent 2)
- `line`: Leaf element with pricing details (indent 3+)

**Parent Lines** (titre, section, subsection):
- No unit, quantity, or unitPrice
- totalPrice calculated from children
- isExpanded = true (collapsible UI)
- confidence = null

**Leaf Lines:**
- Full pricing details (unit, quantity, unitPrice, totalPrice)
- Confidence level based on data completeness
- isExpanded = null (not collapsible)

The script will print the output file path when complete.

## Schema Validation

All outputs follow Pydantic schemas defined in [schemas.py](./schemas.py):

- **DocumentConstructionDashboard**: Dashboard format with pricing lines
- **PricingLine**: Individual line with type, indentLevel, and optional pricing
- **PricingLineType**: "titre" | "section" | "subsection" | "line"
- **ConfidenceLevel**: "low" | "medium" | "high"

## Confidence Calculation

Confidence level is determined by pricing data completeness:
- **Low**: unit_price or quantity is None, or total_ht is 0.0
- **Medium**: All pricing data present and valid

## Error Handling

- Missing input file → Error and exit
- Invalid JSON → Error and exit with traceback
- Processing errors → Logged with full traceback

## Key Features

- **Automatic Hierarchy**: Generates parent sections from building IDs
- **Bottom-up Totals**: Calculates totals by summing children
- **Roman Numeral Parsing**: Extracts section titles from input data
- **Type Detection**: Determines element type based on hierarchy position
- **Confidence Scoring**: Evaluates pricing data completeness
- **Unique IDs**: Generates stable IDs for each pricing line

## Related Files

- [schemas.py](./schemas.py): Pydantic model definitions
- [aggregation_and_export.py](./aggregation_and_export.py): Main script

---

**Version:** 2.0 (Simplified - No LLM)
**Last Updated:** November 2025
