---
name: goose-recipe-analysis
description: Create Goose recipes for document analysis and transformation tasks. Use when creating recipes that analyze saved reports, transform markdown files, or perform analysis on existing data without needing MCP server access.
---

# Goose Recipe Analysis Skill

Create Goose recipes for document analysis and transformation - recipes that work with saved data rather than querying live data sources.

## When to Use This Skill

Use this skill when creating recipes that:
- Analyze previously generated reports (markdown, JSON, CSV)
- Transform or enrich existing documents
- Extract insights from saved data
- Generate actionable recommendations from reports
- Perform follow-up analysis on data extracts

**Do NOT use this skill for:**
- Recipes that need to query live data sources (use `goose-recipes` skill instead)
- Recipes that require MCP server access
- Recipes that need structured JSON validation

## Quick Start

To create an analysis recipe from a spec file:

```
Use the goose-recipe-analysis skill to create a recipe for mill/spec/your-analysis-spec.md
```

The skill will:
1. Read the markdown spec file
2. Generate a simplified recipe YAML (no MCP auth, no JSON schema)
3. Create a shell script runner for easy execution
4. Save files to the appropriate locations (recipe in `mill/recipes/`, script in `scripts/mill/`)

## Recipe Creation Workflow

### 1. Read the Spec File

The skill reads from `mill/spec/*.md` files that describe document analysis workflows.

### 2. Extract Key Information

From the spec, extract:
- **Title**: Recipe name (from frontmatter)
- **Description**: What the recipe accomplishes (from frontmatter)
- **Workflow steps**: The analysis process to follow
- **Output requirements**: What the final report should include

### 3. Generate Recipe YAML

Create a simplified recipe with:

```yaml
version: "1.0.0"
title: "Recipe Title from Spec"
description: "Description from spec frontmatter"

parameters:
  - key: input_file
    input_type: file
    requirement: required
    description: "Path to the report file to analyze"

  - key: output_file
    input_type: string
    requirement: optional
    default: "analysis-output.md"
    description: "Path where analysis report should be saved"

instructions: |
  # Analysis Instructions

  You are analyzing a saved fundraising report to extract actionable insights.

  ## Input
  The report to analyze:
  {{ input_file }}

  ## Analysis Framework
  [Include framework from spec - sections, steps, validations]

  ## Output Requirements
  Create a comprehensive analysis report including:
  [Include output structure from spec]

  Save the analysis to: {{ output_file }}

prompt: "Analyze the fundraising report and generate actionable recommendations following the framework above."

settings:
  goose_provider: "anthropic"
  goose_model: "claude-sonnet-4-20250514"
  temperature: 0.5
```

### 4. Generate Shell Script Runner

Create a convenient runner script:

```bash
#!/bin/bash
# run-[recipe-name].sh

RECIPE_NAME="recipe-name"
RECIPE_PATH="mill/recipes/${RECIPE_NAME}.yaml"

# Default values
INPUT_FILE=""
OUTPUT_FILE="analysis-output.md"

# Usage function
usage() {
  cat <<EOF
Usage: $0 [OPTIONS]

Analyze a saved fundraising report using Goose.

OPTIONS:
  --input FILE      Path to the report file to analyze (required)
  --output FILE     Path where analysis should be saved (default: analysis-output.md)
  -h, --help        Show this help message

EXAMPLES:
  # Analyze a report
  $0 --input reports/q4-2024/report.md

  # Analyze with custom output
  $0 --input reports/q4-2024/report.md --output analysis/q4-insights.md
EOF
  exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --input)
      INPUT_FILE="$2"
      shift 2
      ;;
    --output)
      OUTPUT_FILE="$2"
      shift 2
      ;;
    -h|--help)
      usage
      ;;
    *)
      echo "Unknown option: $1"
      usage
      ;;
  esac
done

# Validate required parameters
if [ -z "$INPUT_FILE" ]; then
  echo "Error: --input is required"
  usage
fi

if [ ! -f "$INPUT_FILE" ]; then
  echo "Error: Input file does not exist: $INPUT_FILE"
  exit 1
fi

# Run the recipe
echo "Analyzing report: $INPUT_FILE"
echo "Output will be saved to: $OUTPUT_FILE"
echo ""

goose run --recipe "$RECIPE_PATH" \
  --params input_file="$INPUT_FILE" \
  --params output_file="$OUTPUT_FILE"
```

## Key Differences from goose-recipes Skill

| Feature | goose-recipes | goose-recipe-analysis |
|---------|---------------|----------------------|
| **Purpose** | Query live data sources | Analyze saved documents |
| **MCP Authentication** | ✅ Included | ❌ Not needed |
| **JSON Schema** | ✅ For validation | ❌ Not needed |
| **Input Type** | Parameters + MCP tools | File input parameters |
| **Output** | Structured JSON | Markdown analysis |
| **Retry Logic** | Complex validation | Simple completion check |
| **Use Case** | Data extraction | Data analysis |

## Common Patterns for Analysis Recipes

### Pattern 1: Report Analysis

Analyze a previously generated report:

```yaml
parameters:
  - key: report_file
    input_type: file
    requirement: required
    description: "The report markdown file to analyze"

instructions: |
  Analyze the following report:
  {{ report_file }}

  Extract key metrics, identify trends, and provide recommendations.
```

### Pattern 2: Multi-File Analysis

Compare or combine multiple documents:

```yaml
parameters:
  - key: current_report
    input_type: file
    requirement: required
    description: "Current period report"

  - key: previous_report
    input_type: file
    requirement: required
    description: "Previous period report"

instructions: |
  Compare these two reports:

  Current: {{ current_report }}
  Previous: {{ previous_report }}

  Identify changes, trends, and provide comparative analysis.
```

### Pattern 3: Data Enrichment

Add context or recommendations to existing data:

```yaml
parameters:
  - key: base_data
    input_type: file
    requirement: required
    description: "Base data file to enrich"

  - key: context_info
    input_type: string
    requirement: optional
    default: ""
    description: "Additional context to consider"

instructions: |
  Enrich this data with actionable recommendations:
  {{ base_data }}

  Additional context: {{ context_info }}
```

### Pattern 4: Time-Sensitive Analysis

Include current date context for time-aware recommendations:

```yaml
instructions: |
  Today's date: $(date +%Y-%m-%d)
  Current quarter: Q$(( ($(date +%-m)-1)/3+1 ))

  Analyze the report with time-sensitive recommendations:
  {{ report_file }}

  Consider the current fiscal position when prioritizing actions.
```

## Validation and Testing

### Test Your Recipe

```bash
# Preview the recipe
goose run --recipe mill/recipes/your-recipe.yaml --explain

# Test with sample data
goose run --recipe mill/recipes/your-recipe.yaml \
  --params input_file="test-data.md" \
  --params output_file="test-output.md"
```

### Common Issues

| Issue | Solution |
|-------|----------|
| "File not found" | Check input_file path is correct, use absolute paths if needed |
| "No output generated" | Ensure instructions are clear about saving to output_file |
| "Analysis too generic" | Add more specific framework sections in instructions |
| "Missing context" | Include current date, period info, or other context in instructions |

## File Organization

Analysis recipes follow this structure:

```
mill/
├── spec/
│   └── your-analysis-spec.md          # Markdown spec describing analysis
└── recipes/
    └── your-analysis-recipe.yaml      # Generated recipe file

scripts/mill/
└── run-your-analysis.sh                # Shell script runner
```

## Usage Philosophy

**CLI for Production, Desktop for Development**

- **Use CLI** (via shell scripts or `goose run`) for running analysis recipes
- **Use Desktop** for ad-hoc exploration, testing, and development
- Analysis recipes are meant to be repeatable and scriptable

## Reference Documentation

For complete Goose recipe field reference, see the goose-recipes skill:
- `.claude/skills/goose-recipes/references/recipe-structure.md`

## Example: Creating a Follow-Up Analysis Recipe

Given a spec `mill/spec/fundraising-data-analysis-followup.md`:

```markdown
---
title: fundraising-data-analysis-followup
description: Analyze saved fundraising report with actionable recommendations
---

# Fundraising Report Analysis Recipe

## Workflow
Analyze report to extract insights and generate action items...

## Output Structure
- Executive Summary
- Actionable Intelligence
- Performance Benchmarks
```

Run the skill:

```
Use the goose-recipe-analysis skill to create a recipe for mill/spec/fundraising-data-analysis-followup.md
```

This generates:
- `mill/recipes/fundraising-data-analysis-followup.yaml`
- `scripts/mill/run-fundraising-followup.sh`

Then run it:

```bash
./scripts/mill/run-fundraising-followup.sh \
  --input reports/fundraising-data-analysis/2024-10-31-1400/report.md \
  --output reports/fundraising-data-analysis/2024-10-31-1400/analysis.md
```

## Best Practices

1. **Clear input requirements**: Specify exactly what format the input file should be
2. **Structured instructions**: Break analysis framework into clear sections
3. **Output specifications**: Define exactly what the analysis should include
4. **Time context**: Include current date/quarter for time-sensitive recommendations
5. **Validation steps**: Include data quality checks in the analysis framework
6. **Actionable output**: Ensure recommendations are specific and executable

## Integration with Data Extraction Recipes

Analysis recipes are designed to work as follow-ups to data extraction recipes:

```
Workflow 1 (Data Extraction):
  goose-recipes skill → fundraising-data-analysis.yaml
  Queries Salesforce → Generates report.md

Workflow 2 (Analysis):
  goose-recipe-analysis skill → fundraising-data-analysis-followup.yaml
  Reads report.md → Generates analysis.md with recommendations
```

This separation allows:
- Reusable data extracts that can be analyzed multiple ways
- Fast re-analysis without re-querying live data
- Different analysis frameworks on the same base data
