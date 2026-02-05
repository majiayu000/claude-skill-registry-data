---
name: figma-design-tokens
description: Extracts design tokens from Figma files and generates production-ready CSS, SCSS, JSON, TypeScript, and W3C DTCG format files using the Figma MCP server
version: 0.2.0
---

# Figma Design Tokens Generator

## Overview

This skill enables extraction of design tokens (colors, typography, spacing, etc.) from Figma designs through the Figma MCP server and transforms them into production-ready format files. Generate CSS custom properties, SCSS variables, JSON, W3C Design Tokens Format, TypeScript types, and documentation from Figma variables.

## Prerequisites

**Required:**
- Figma MCP server installed and configured in `~/.claude/config.json`
- Figma file with design variables (or elements with styles for fallback extraction)
- View or edit access to the Figma file

**Setup verification:**
- If user reports MCP connection issues, consult `references/troubleshooting.md`
- For installation help, direct user to README.md

## Workflow Decision Tree

Choose the appropriate workflow based on the user's goal:

**A. Selection-Based Extraction**
- User has specific frames/components to extract
- Working with subset of design system
- Quick extraction for specific use case

**B. Full Design System Extraction**
- User wants all tokens from entire file
- Building comprehensive design system
- Multiple themes/modes to handle

## Selection-Based Extraction Workflow

### Step 1: Extract Variables from Figma

Use the `get_variable_defs` MCP tool to extract Figma variables:

```
Use the Figma MCP get_variable_defs tool with:
- file_url: <figma-file-url>
- node_ids: <comma-separated-node-ids> (optional, extracts all if omitted)
```

**Returns:** JSON with variable definitions including names, values, types, modes, and references.

**Fallback:** If no variables exist, the extraction script automatically extracts tokens from node styles (fills, strokes, typography, spacing) with duplicate detection.

### Step 2: Apply Core Token Generation Workflow

Proceed to "Core Token Generation Workflow" section below.

## Full Design System Workflow

### Step 1: Get File Metadata (Optional)

Use `get_metadata` MCP tool to understand file structure:

```
Use the Figma MCP get_metadata tool with:
- file_url: <figma-file-url>
```

This returns layer IDs, names, types, and hierarchy.

### Step 2: Extract All Variables

Use `get_variable_defs` without node_ids:

```
Use the Figma MCP get_variable_defs tool with:
- file_url: <figma-file-url>
```

### Step 3: Apply Core Token Generation Workflow

Proceed to "Core Token Generation Workflow" section below.

## Core Token Generation Workflow

This workflow applies to both extraction approaches above.

### Step 1: Transform to W3C DTCG Format

Use the bundled `extract_tokens.py` script to transform Figma data:

```bash
python figma-design-tokens/scripts/extract_tokens.py \
  --figma-data <path-to-mcp-output.json> \
  --output-path <output-tokens.json> \
  --token-types colors,typography,spacing
```

**Key Transformations:**
- Figma COLOR → W3C `color` tokens (sRGB color space)
- Figma FLOAT → W3C `dimension` or `number` tokens
- Figma STRING → W3C `fontFamily` or custom tokens
- Variable references → W3C alias syntax `{token.name}`
- Variable modes → Organized token groups or separate files

**Token Types:**
- `colors` - Color variables
- `typography` - Font families, sizes, weights, line heights
- `spacing` - Spacing, margins, padding, dimensions
- `all` - All available token types (default)

### Step 2: Generate Output Formats

Use the bundled `transform_tokens.py` script:

```bash
python figma-design-tokens/scripts/transform_tokens.py \
  --input <tokens.json> \
  --format css,scss,json,typescript,documentation \
  --naming-convention kebab-case \
  --output-dir <output-directory>
```

**Available Formats:**
1. **CSS Custom Properties** - `:root { --color-primary: #0066cc; }`
2. **SCSS Variables** - `$color-primary: #0066cc;`
3. **JSON** - Style Dictionary compatible
4. **TypeScript** - Type-safe definitions with `as const`
5. **Documentation** - Markdown tables and usage examples

**Naming Conventions:**
- `kebab-case` (default) - `color-primary-500`
- `camelCase` - `colorPrimary500`
- `snake_case` - `color_primary_500`
- `bem` - `color__primary--500`

### Step 3: Validate Output

Use the bundled `validate_tokens.py` script:

```bash
python figma-design-tokens/scripts/validate_tokens.py \
  --input <output-tokens.json> \
  --report <validation-report.md>
```

**Validation Checks:**
- W3C DTCG specification compliance
- Required properties presence (`$value`)
- Token type consistency
- Circular reference detection
- Value format correctness

### Step 4: Organize Files (Optional)

For category-specific files:

```bash
python figma-design-tokens/scripts/transform_tokens.py \
  --input <tokens.json> \
  --format css,scss,json \
  --organize-by-category \
  --output-dir <output-directory>
```

**Generated structure:**
```
output/
├── colors.tokens.json
├── colors.css
├── colors.scss
├── spacing.tokens.json
├── spacing.css
├── spacing.scss
├── typography.tokens.json
├── typography.css
└── typography.scss
```

## Multi-Theme Handling

If Figma file contains variable modes (light/dark themes):

### Option A: Separate Files Per Theme

```bash
# Extract each mode separately
python figma-design-tokens/scripts/extract_tokens.py \
  --figma-data <mcp-output.json> \
  --mode light \
  --output-path <tokens-light.json>

python figma-design-tokens/scripts/extract_tokens.py \
  --figma-data <mcp-output.json> \
  --mode dark \
  --output-path <tokens-dark.json>
```

### Option B: Token References

Generate base tokens with mode-specific tokens referencing base:

```json
{
  "color": {
    "blue-500": {
      "$type": "color",
      "$value": "rgb(0, 102, 204)"
    },
    "primary": {
      "$value": "{color.blue-500}"
    }
  }
}
```

Then create theme files that override references.

## Token Naming Conventions

### Default (kebab-case)
```
color-primary-500
spacing-medium
font-family-body
```

### Custom Prefixes

Use `--category-prefix` to add category prefixes:

```bash
--category-prefix color:clr,spacing:sp,typography:type
```

Results in: `clr-primary-500`, `sp-medium`, `type-body`

### Semantic Name Standardization (NEW)

Automatically standardize Figma token names to industry-standard semantic conventions:

```bash
python figma-design-tokens/scripts/extract_tokens.py \
  --figma-data <mcp-output.json> \
  --output-path <tokens.json> \
  --standardize-names
```

**What It Does:**

1. **Color Name Standardization**
   - Maps Figma color names to semantic standards
   - `Brand Blue` → `primary`
   - `Red` or `Danger` → `error`
   - `Green` or `Positive` → `success`
   - `Yellow` or `Alert` → `warning`
   - Supports: primary, secondary, tertiary, success, warning, error, info, neutral, background, foreground, accent, link

2. **Size Standardization (T-shirt Sizing)**
   - Normalizes dimensions to t-shirt scale: xs, sm, md, lg, xl, 2xl, 3xl, 4xl
   - Applies to spacing, width, height, border-radius, font-size
   - Name-based: `Small` → `sm`, `Extra Large` → `xl`
   - Value-based: `4px` → `xs`, `16px` → `md`, `64px` → `2xl`

**Custom Mappings:**

Create a JSON file with custom semantic mappings:

```json
{
  "colors": {
    "brand": ["brand", "company", "corporate"],
    "disabled": ["disabled", "inactive", "muted"]
  },
  "sizes": {
    "tiny": ["tiny", "micro", "mini"],
    "huge": ["huge", "jumbo", "massive"]
  }
}
```

Use with `--name-mappings`:

```bash
python figma-design-tokens/scripts/extract_tokens.py \
  --figma-data <mcp-output.json> \
  --output-path <tokens.json> \
  --standardize-names \
  --name-mappings <custom-mappings.json>
```

**Benefits:**
- Consistent naming across projects
- Easier onboarding for developers
- Better integration with component libraries
- Semantic clarity (intent over appearance)

## Token Organization Patterns

### Primitive vs Semantic Tokens

**Primitive Tokens** (base values):
```json
{
  "blue": {
    "500": { "$value": "#0066cc" }
  }
}
```

**Semantic Tokens** (context-specific):
```json
{
  "color": {
    "primary": { "$value": "{blue.500}" }
  }
}
```

The scripts automatically identify primitive vs semantic based on variable references.

### File Organization Strategies

Use `--organization-strategy` or `--organize-by-category` flag:

- **Single File** - All tokens in one `tokens.json` (simple projects)
- **Category Files** - Separate files per category (medium projects)
- **Primitive + Semantic Split** - Advanced organization (large design systems)

## Script Usage Reference

### extract_tokens.py

**Purpose:** Transform Figma MCP data to W3C DTCG format

**Key Arguments:**
- `--figma-data` - Path to Figma MCP JSON output (required)
- `--output-path` - Output file path (required)
- `--token-types` - Comma-separated types: colors, typography, spacing, all
- `--mode` - Figma variable mode (e.g., light, dark)
- `--pretty` - Pretty-print JSON output
- `--standardize-names` - Enable semantic name standardization (optional)
- `--name-mappings` - Path to custom mappings JSON file (optional)

**Help:** `python extract_tokens.py --help`

### transform_tokens.py

**Purpose:** Generate CSS, SCSS, JSON, TypeScript, documentation from W3C tokens

**Key Arguments:**
- `--input` - W3C DTCG JSON file (required)
- `--format` - Output formats: css, scss, json, typescript, documentation
- `--naming-convention` - Token naming style
- `--output-dir` - Output directory (required)
- `--organize-by-category` - Generate separate files per category

**Help:** `python transform_tokens.py --help`

### validate_tokens.py

**Purpose:** Validate W3C DTCG compliance

**Key Arguments:**
- `--input` - W3C DTCG JSON file (required)
- `--report` - Validation report path (markdown)
- `--strict` - Treat warnings as errors

**Help:** `python validate_tokens.py --help`

## Common Use Cases

### Extract Brand Colors
1. Select brand color frames in Figma
2. Extract using `get_variable_defs`
3. Transform to CSS custom properties
4. Import into global stylesheet

### Build Multi-Theme System
1. Define light/dark modes in Figma variables
2. Extract both modes separately
3. Generate theme-specific CSS files
4. Switch themes with CSS class toggling

### Create Component Library Tokens
1. Extract component-specific spacing/sizing
2. Generate TypeScript definitions
3. Import into React/Vue components
4. Use type-safe token access

### Generate Design System Documentation
1. Extract all design tokens
2. Generate documentation markdown
3. Include in design system site
4. Maintain single source of truth

### Extract from Files Without Variables
1. Open Figma file (only has styles, no variables)
2. Select frames/components with design elements
3. Use extraction script (auto-falls back to node extraction)
4. Script extracts colors, typography, spacing from properties
5. Duplicates automatically skipped

## Bundled Resources

### Scripts

- **`scripts/extract_tokens.py`** - Transform Figma → W3C DTCG
- **`scripts/transform_tokens.py`** - W3C → Multiple formats
- **`scripts/validate_tokens.py`** - Validate W3C compliance

All scripts include `--help` for detailed usage.

### References

- **`references/w3c-dtcg-spec.md`** - Complete W3C Design Tokens specification
- **`references/figma-mcp-tools.md`** - Figma MCP server tools documentation
- **`references/token-naming-conventions.md`** - Naming patterns and best practices
- **`references/troubleshooting.md`** - Error handling and solutions
- **`references/integration-examples.md`** - Build tool integration (Style Dictionary, PostCSS, React, Vue, etc.)
- **`references/advanced-usage.md`** - Custom types, batch processing, automation

Load these references when detailed information is needed.

### Templates

- **`templates/w3c-tokens.template.json`** - W3C DTCG structure template
- **`templates/css-variables.template.css`** - CSS custom properties template
- **`templates/scss-variables.template.scss`** - SCSS variables template
- **`templates/typescript-types.template.ts`** - TypeScript definitions template
- **`templates/documentation.template.md`** - Documentation generation template

## Quick Decision Guide

**User says:** "Extract design tokens from Figma"
→ Ask: Full file or specific selection?
→ Guide to appropriate workflow

**User says:** "No variables found"
→ Explain: Automatic fallback extracts from node styles
→ Verify: File has accessible elements with fills/text/spacing

**User reports:** "MCP server error"
→ Direct to: `references/troubleshooting.md`

**User asks:** "How to integrate with [tool]"
→ Direct to: `references/integration-examples.md`

**User needs:** Advanced features
→ Direct to: `references/advanced-usage.md`

## Expected Output

When using this skill, deliver:

1. **W3C DTCG JSON File** - Specification-compliant design tokens
2. **CSS Custom Properties** - Ready for browser usage
3. **SCSS Variables** - For Sass-based projects
4. **TypeScript Definitions** - Type-safe token access
5. **Documentation** - Auto-generated reference guide
6. **Validation Report** - Compliance and quality checks

All files are production-ready and can be integrated directly into projects.

---

For detailed information, consult the bundled reference documentation in the `references/` directory.
