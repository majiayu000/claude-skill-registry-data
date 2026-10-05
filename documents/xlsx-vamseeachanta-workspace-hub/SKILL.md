---
name: xlsx
description: Excel spreadsheet toolkit for creating, reading, and manipulating .xlsx
  files. Supports formulas, formatting, charts, and financial modeling with industry-standard
  conventions. Use for data analysis, financial models, reports, and spreadsheet automation.
type: reference
version: 1.1.0
last_updated: 2026-01-02
category: data
related_skills:
- docx
- pptx
- pdf
capabilities: []
requires: []
tags: []
freedom: medium
---

# Xlsx

## Overview

Comprehensive Excel manipulation using pandas for data analysis and openpyxl for formulas, formatting, and Excel-specific features.

## Quick Start

```python
import pandas as pd
from openpyxl import Workbook

# Read with pandas
df = pd.read_excel("data.xlsx")
print(df.head())

# Create with openpyxl
wb = Workbook()
ws = wb.active
ws["A1"] = "Hello"
ws["B1"] = "World"
wb.save("output.xlsx")
```

## When to Use

- Reading and analyzing Excel data with pandas
- Creating formatted spreadsheets programmatically
- Building financial models with formulas
- Generating reports with charts and graphs
- Automating data entry and updates
- Converting between Excel and other formats
- Batch processing multiple spreadsheets
- Creating templates for repeated use

## Version History

- **1.1.0** (2026-01-02): Added Quick Start, When to Use, Execution Checklist, Error Handling, Metrics sections; updated frontmatter with version, category, related_skills
- **1.0.0** (2024-10-15): Initial release with pandas, openpyxl, financial model standards

## Sub-Skills

- [Execution Checklist](execution-checklist/SKILL.md)
- [Error Handling](error-handling/SKILL.md)
- [Metrics](metrics/SKILL.md)
- [Quick Reference](quick-reference/SKILL.md)
- [Dependencies](dependencies/SKILL.md)

## Sub-Skills

- [Financial Model Color Standards (+1)](financial-model-color-standards/SKILL.md)
- [With Pandas (+1)](with-pandas/SKILL.md)
- [With Pandas (+1)](with-pandas/SKILL.md)
- [Cell Styles (+1)](cell-styles/SKILL.md)
- [Charts](charts/SKILL.md)
- [Check for Errors (+1)](check-for-errors/SKILL.md)
- [Workflow](workflow/SKILL.md)
