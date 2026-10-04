---
name: codebase-index
version: 1.2.0
description: Automatically generate relationship and dependency maps for any component-based codebase (React, Vue, Svelte, Astro, Next.js, Angular, Solid). Auto-detects framework. Supports TOON format for 30-60% token savings. Use when indexing codebases, mapping component relationships, documenting dependencies, or understanding unfamiliar projects. Generates JSON/TOON files mapping component usage, imports, npm dependencies, utilities, CSS, and data queries.
---

# Codebase Index

Generate comprehensive, framework-agnostic relationship and dependency maps for component-based codebases with optional TOON format for token-efficient AI consumption.

## What This Skill Does

Scans any component-based codebase to automatically generate relationship maps:
- **Component relationships**: Import graph (usedBy/uses)
- **NPM dependencies**: Package usage tracking
- **Utility functions**: Shared code in lib/utils
- **Data queries**: CMS and API patterns
- **CSS structure**: Classes and design tokens

**Framework Support**: React, Vue, Svelte, Astro, Next.js, Angular, Solid (auto-detected)

**Output Formats**: 
- **TOON** (default): Token-efficient format, 30-60% smaller than JSON
- **JSON**: Standard format for tooling compatibility

## Quick Start

```bash
# Auto-detect framework, output TOON
python scripts/index_codebase.py /path/to/project

# Specify framework and format
python scripts/index_codebase.py /path/to/project --framework react --format json

# Use tab delimiters (even more token-efficient)
python scripts/index_codebase.py /path/to/project --delimiter "\t"
```

## Framework Auto-Detection

The skill automatically detects your framework from `package.json`:

| Framework | Detection | Extensions |
|-----------|-----------|------------|
| Astro | `astro` dependency | `.astro` |
| React | `react` dependency | `.jsx`, `.tsx` |
| Next.js | `next` dependency | `.jsx`, `.tsx` |
| Vue | `vue` dependency | `.vue` |
| Svelte | `svelte` dependency | `.svelte` |
| Angular | `@angular/core` | `.ts` |
| Solid | `solid-js` | `.jsx`, `.tsx` |

**Override auto-detection:**
```bash
python scripts/index_codebase.py /path/to/project --framework vue
```

## Output Formats

### TOON Format (Recommended)

**Why TOON?** 
- 30-60% fewer tokens than JSON
- Better LLM comprehension (70% vs 65% accuracy)
- Self-documenting structure with explicit lengths
- Perfect for uniform data (our use case!)

**Example TOON output:**
```toon
components[3]{name,path,type,framework,uses,usedBy}:
Button,src/components/atoms/Button.tsx,atom,react,[0]:,[2]: Card,Page
Card,src/components/molecules/Card.tsx,molecule,react,[1]: Button,[1]: Page
Page,src/pages/index.tsx,page,react,[2]: Button,Card,[0]:

statistics:
  totalComponents: 3
  atoms: 1
  molecules: 1
  pages: 1
```

**vs JSON (same data):**
```json
{
  "components": {
    "Button": {
      "path": "src/components/atoms/Button.tsx",
      "type": "atom",
      "framework": "react",
      "uses": [],
      "usedBy": ["Card", "Page"]
    },
    ...
  }
}
```

### Format Comparison

| Aspect | TOON | JSON |
|--------|------|------|
| Token count | 40-70% smaller | Baseline |
| LLM accuracy | 70.1% | 65.4% |
| Human readable | ✅ | ✅ |
| Tool compatible | ⚠️ (new format) | ✅ |
| Best for | AI consumption | Tooling |

**Recommendation**: Use TOON for AI context, JSON for tooling integration.

## Output Structure

All files generated in `src/.ai/` (or first source directory found):

```
src/.ai/
├── index.toon                      # Entry point
└── relationships/
    ├── component-usage.toon        # Component graph
    ├── dependencies.toon           # NPM + utilities + CSS
    └── data-flow.toon              # Data queries
```

## Component Type Detection

Auto-detects component types from directory structure:

| Pattern | Type |
|---------|------|
| `/atoms/` | atom |
| `/molecules/` | molecule |
| `/organisms/` | organism |
| `/templates/` | template |
| `/ui/` | ui |
| `/layouts/` | layout |
| `/pages/`, `/views/`, `/routes/` | page |
| `/hooks/` | hook |
| `/contexts/` | context |
| Other | component |

## Advanced Options

### Alternative Delimiters

For tabular data, choose delimiter for optimal tokenization:

```bash
# Comma (default) - most readable
python scripts/index_codebase.py /path/to/project --delimiter ","

# Tab - often fewer tokens
python scripts/index_codebase.py /path/to/project --delimiter "\t"

# Pipe - middle ground
python scripts/index_codebase.py /path/to/project --delimiter "|"
```

**Tab output example:**
```toon
components[2	]{name	path	type}:
Button	src/Button.tsx	atom
Card	src/Card.tsx	molecule
```

### Dual Output

Generate both formats for different use cases:

```bash
# Generate TOON for AI
python scripts/index_codebase.py /path/to/project --format toon

# Generate JSON for tools
python scripts/index_codebase.py /path/to/project --format json
```

## Reading Index Files

### For AI Assistants

After indexing, read files to understand codebase:

1. **Start with `index.toon/json`** - Overview and metadata
2. **Component relationships** - `relationships/component-usage.toon`
3. **Dependencies** - `relationships/dependencies.toon`
4. **Data flow** - `relationships/data-flow.toon`

### TOON Syntax Quick Reference

```toon
# Primitive field
name: Button

# Nested object
user:
  id: 123
  name: Ada

# Primitive array
tags[3]: react,typescript,ui

# Tabular array (uniform objects)
items[2]{id,name,price}:
1,Widget,9.99
2,Gadget,14.50

# List array (mixed)
items[3]:
- 1
- name: Item
- [2]: sub,array
```

## Framework-Specific Features

### Astro
- Detects `.astro` components
- Scans for Sanity CMS `client.fetch()` queries
- Maps layouts and pages

### React/Next.js
- Supports `.jsx`, `.tsx`
- Detects hooks, contexts
- Maps `fetch()` and `axios` patterns

### Vue
- Scans `.vue` components
- Maps views and composables

### Svelte
- Detects `.svelte` components
- Scans routes and stores

### Angular
- Scans `.component.ts` files
- Detects `http.get()` patterns

### Solid
- Supports `.jsx`, `.tsx`
- Maps Solid-specific patterns

## Project Structure Requirements

Flexible directory discovery:
- Checks framework-specific directories (e.g., `app/` for Next.js)
- Falls back to `src/` if present
- Works with various project structures

**Typical structures supported:**
```
# React/Next.js
app/
components/
pages/

# Vue
src/
  components/
  views/

# Astro
src/
  components/
  layouts/
  pages/
```

## Integration with Metadata

### Complementary Design

**Component Metadata** (manual `.metadata.json`):
- **Purpose**: "How to USE this component"
- **Contains**: Props, variants, examples, guidelines
- **Created**: Manually

**Codebase Index** (this skill):
- **Purpose**: "WHERE is this used"
- **Contains**: Relationships, dependencies, usage
- **Created**: Auto-generated

**No duplication** - These systems complement each other.

## Performance

- **Speed**: 1-5 seconds for typical projects (50-200 components)
- **Output size**: 
  - TOON: 30-150KB (typical)
  - JSON: 50-250KB (typical)
- **Memory**: Minimal (streaming processing)

**Large projects** (500+ components):
- Consider directory-specific scans
- Use tab delimiter for better tokenization
- May take 10-30 seconds

## Error Handling

The indexer is resilient:
- Skips unparseable files (logs warning)
- Handles missing directories gracefully
- Continues on errors to maximize coverage
- Reports errors in summary

## Example Usage

### First-time Index
```bash
# Let it auto-detect everything
python scripts/index_codebase.py ~/projects/my-app

# Output:
# 🔍 Scanning react codebase...
# ✅ Generated component-usage.toon
# ✅ Generated dependencies.toon
# ✅ Generated data-flow.toon
# ✅ Generated index.toon
#
# Summary:
# 🎯 Framework: react
# 📝 Format: TOON
# ✅ 42 components indexed
# ✅ 156 relationships mapped
# ✅ 8 utilities tracked
# ✅ 3 queries documented
# 💡 TOON format: 30-60% more token-efficient than JSON
```

### Re-index After Changes
```bash
# Same command - overwrites previous index
python scripts/index_codebase.py ~/projects/my-app
```

### Framework Override
```bash
# For edge cases where auto-detect fails
python scripts/index_codebase.py ~/projects/my-app --framework vue
```

## Troubleshooting

**No components found?**
- Verify source directories exist
- Check file extensions match framework
- Look for `node_modules` in exclusions

**Wrong framework detected?**
- Use `--framework` flag to override
- Check `package.json` dependencies

**Import relationships missing?**
- Verify import statements use standard ES6 format
- Dynamic imports may not be detected
- Check for path aliases (may need resolution)

**TOON parse errors?**
- File is valid - TOON is for AI consumption
- Use JSON format for tooling integration
- Check TOON spec if implementing parser

**Utilities not found?**
- Verify `lib/`, `utils/`, or `helpers/` directories exist
- Check for `.ts` files (not `.d.ts`)

## Comparison with JSON

### Example: Component Data

**JSON (123 tokens):**
```json
{
  "Button": {
    "path": "src/components/Button.tsx",
    "type": "atom",
    "framework": "react",
    "uses": [],
    "usedBy": ["Card", "Header", "Footer"]
  }
}
```

**TOON (52 tokens, 58% reduction):**
```toon
Button:
  path: src/components/Button.tsx
  type: atom
  framework: react
  uses[0]:
  usedBy[3]: Card,Header,Footer
```

**Tabular TOON (even better for multiple components):**
```toon
components[3]{name,path,type,uses,usedBy}:
Button,src/components/Button.tsx,atom,[0]:,[3]: Card,Header,Footer
Card,src/components/Card.tsx,molecule,[1]: Button,[1]: Page
Footer,src/components/Footer.tsx,organism,[2]: Button,Icon,[0]:
```

## CI/CD Integration

### Git Hook Example
```bash
# .husky/post-merge
#!/bin/sh
python scripts/index_codebase.py . --format toon
git add src/.ai/
```

### GitHub Action
```yaml
name: Update Codebase Index
on:
  push:
    branches: [main]
jobs:
  index:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Index codebase
        run: python scripts/index_codebase.py . --format toon
      - name: Commit changes
        run: |
          git add src/.ai/
          git commit -m "Update codebase index" || true
          git push
```

## Future Enhancements

Potential additions:
- Bundle size analysis
- Circular dependency detection
- Visual graph generation (mermaid)
- More CMS platforms (Contentful, Strapi)
- API route mapping
- Environment variable tracking
- Incremental updates

## Credits

- **TOON Format**: [toon-format/toon](https://github.com/toon-format/toon)
- **Token Efficiency**: 30-60% reduction vs JSON
- **LLM Accuracy**: 70.1% vs 65.4% (JSON baseline)
