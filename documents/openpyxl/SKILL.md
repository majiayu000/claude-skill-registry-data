---
name: openpyxl
description: Create and manipulate Microsoft Excel workbooks programmatically. Build
  spreadsheets with formulas, charts, conditional formatting, and pivot tables. Handle
  large datasets efficiently with streaming mode.
version: 1.0.0
category: data
type: skill
capabilities:
- workbook_creation
- cell_formatting
- formula_support
- chart_generation
- conditional_formatting
- pivot_tables
- large_dataset_handling
- streaming_mode
tools:
- python
- openpyxl
- pandas
tags:
- excel
- xlsx
- spreadsheet
- formulas
- charts
- data-analysis
- office-automation
platforms:
- windows
- macos
- linux
related_skills:
- pandas-data-processing
- python-docx
- plotly
requires: []
scripts_exempt: true
---

# Openpyxl

## Overview

Openpyxl is a Python library for reading and writing Excel 2010+ xlsx/xlsm files. This skill covers comprehensive patterns for spreadsheet automation including:

- **Workbook creation** with multiple worksheets
- **Cell operations** including formatting, merging, and data validation
- **Formula support** for calculations and dynamic content
- **Chart generation** for data visualization within Excel
- **Conditional formatting** for visual data analysis
- **Large dataset handling** with optimized read/write modes
- **Pivot table creation** for data summarization
- **Style management** for professional appearances

## When to Use This Skill

### USE when:

- Creating Excel reports with formulas and calculations
- Generating spreadsheets from database queries
- Automating financial reports and dashboards
- Building Excel templates with formatting
- Processing and transforming existing Excel files
- Creating charts and visualizations in Excel
- Applying conditional formatting rules
- Building data entry forms with validation
- Handling large datasets (100k+ rows)
- Creating pivot tables programmatically
### DON'T USE when:

- Only need to read data into pandas (use pandas.read_excel directly)
- Need real-time Excel manipulation (use xlwings on Windows)
- Working with .xls format (use xlrd/xlwt)
- Creating complex macros (requires VBA)
- Need Excel-specific features like Power Query

## Prerequisites

### Installation

```bash
# Basic installation
pip install openpyxl

# Using uv (recommended)
uv pip install openpyxl

# With image support
pip install openpyxl Pillow


*See sub-skills for full details.*
### Verify Installation

```python
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border
from openpyxl.chart import BarChart, LineChart, PieChart
from openpyxl.utils.dataframe import dataframe_to_rows

print("openpyxl installed successfully!")
```

## Version History

### 1.0.0 (2026-01-17)

- Initial skill creation
- Core capabilities documentation
- 6 complete code examples
- Large dataset handling patterns
- Integration with pandas

## Resources

- **Official Documentation**: https://openpyxl.readthedocs.io/
- **GitHub Repository**: https://github.com/theorchard/openpyxl
- **PyPI Package**: https://pypi.org/project/openpyxl/

## Related Skills

- **pandas-data-processing** - Data analysis and transformation
- **python-docx** - Word document generation
- **plotly** - Interactive chart generation
- **pypdf** - PDF manipulation

---

*This skill provides comprehensive patterns for Excel automation refined from production data processing systems.*

## Sub-Skills

- [1. Basic Workbook Creation](1-basic-workbook-creation/SKILL.md)
- [2. Advanced Cell Formatting](2-advanced-cell-formatting/SKILL.md)
- [3. Chart Generation](3-chart-generation/SKILL.md)
- [4. Conditional Formatting](4-conditional-formatting/SKILL.md)
- [5. Large Dataset Handling with Streaming](5-large-dataset-handling-with-streaming/SKILL.md)
- [6. Pivot Table Creation](6-pivot-table-creation/SKILL.md)
- [Pandas Integration (+1)](pandas-integration/SKILL.md)
- [1. Memory Management (+2)](1-memory-management/SKILL.md)
- [Common Issues](common-issues/SKILL.md)
