---
name: md2ipynb
description: "Convert markdown files to Jupyter notebooks (.ipynb). Splits markdown by `---` delimiters into cells, extracts code blocks (```python```, ```sql```) as code cells, and handles YAML front matter removal. Use when converting documentation, tutorials, or structured markdown into interactive Jupyter notebooks."
license: MIT
---

# Markdown to Jupyter Notebook Conversion

## Overview

Convert markdown files to Jupyter notebooks with intelligent cell splitting:
- Split by `---` horizontal rules into separate cells
- Extract fenced code blocks (`python`, `sql`) as code cells
- Automatically remove YAML front matter

## Quick Start

```bash
uvx --with nbformat python scripts/convert.py input.md output.ipynb
```

## Conversion Rules

1. **YAML Front Matter**: First `---...---` block at file start is removed
2. **Section Delimiters**: `---` splits content into separate markdown cells
3. **Code Blocks**: Fenced code blocks become code cells:
   - `python`, `sql`
4. **Other code blocks**: Non-target languages and language-less blocks remain in markdown cell (not extracted)
5. **`---` inside code blocks**: Preserved, does not split

## Example

Input:
```markdown
---
title: Tutorial
---
---
# Introduction
Welcome!
```python
print("hello")
```
---
# Data Query
```sql
SELECT * FROM users
```
---
```

Output notebook cells:
1. Markdown: `# Introduction\nWelcome!`
2. Code (python): `print("hello")`
3. Markdown: `# Data Query`
4. Code (sql): `SELECT * FROM users`

## CLI Options

```bash
uvx --with nbformat python scripts/convert.py <input.md> <output.ipynb> [options]

Options:
  --code-languages  Comma-separated languages for code cells
                    Default: python,sql
```

## Edge Cases

- **Empty sections**: Skipped
- **No `---` in file**: Entire file as single section, code blocks still extracted
- **`---` in code blocks**: Preserved as content, does not split
- **File without front matter**: First content becomes first cell

## Dependencies

Run with uvx to automatically handle dependencies:

```bash
uvx --with nbformat python scripts/convert.py ...
```
