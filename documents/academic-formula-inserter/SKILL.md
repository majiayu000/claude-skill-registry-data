---
name: "academic-formula-inserter"
description: "Insert, format, and number math formulas in Word and LaTeX academic papers. Supports Chinese core journals and international journal formats. Invoke when user needs to insert LaTeX formulas into Word (OMML), validate formula formats per journal standards, or auto-number equations."
---

# Academic Formula Inserter

Insert, format, number, and validate math formulas in academic papers. Supports **Word (.docx)** with native OMML equations and **LaTeX (.tex)** output, with automatic formatting per journal standards.

## Supported Journal Formats

| Category | Formats | Examples |
|----------|---------|---------|
| **Chinese Core** | GB/T 7714 formula style | 中文核心、CSCD、CSSCI |
| **International** | IEEE, APA, Nature, Science | Elsevier, Springer, Taylor & Francis |
| **General Academic** | Custom numbering & style | Thesis, dissertation, report |

## Formula Numbering Styles

| Style | Example | Used By |
|-------|---------|---------|
| `chinese` | `式(1)` `式(2)` | Chinese core journals |
| `parentheses` | `(1)` `(2)` | IEEE, general |
| `brackets` | `[1]` `[2]` | Some physics journals |
| `section` | `(1.1)` `(2.3)` | Thesis with section-based numbering |
| `latex-tag` | `\tag{1}` `\label{eq:1}` | LaTeX native |

## Commands

### `insert-formula` — Insert LaTeX formula into Word document

Converts LaTeX string to native Word OMML equation and inserts at cursor or specified location.

**Usage:**
```bash
python insert_formula.py insert-formula <docx_path> --latex "<formula>" [--display] [--style <style>] [--number <num>]
```

**Options:**
| Argument | Description |
|----------|-------------|
| `<docx_path>` | Path to .docx file |
| `--latex` | LaTeX formula string (e.g. "E=mc^2") |
| `--display` | Display equation (centered, default: inline) |
| `--style` | Numbering style: `chinese`, `parentheses`, `brackets`, `section`, `none` |
| `--number` | Specific number for the equation |
| `--position` | Paragraph index to insert at |
| `--label` | Equation label for cross-reference |
| `--interactive` | Interactive mode: prompt to choose numbering style from a menu |

### `batch-convert` — Batch convert all LaTeX in document

Scans the document for `$...$` and `$$...$$` patterns and converts them to native OMML equations.

**Usage:**
```bash
python insert_formula.py batch-convert <docx_path> [--backup] [--mode quick|safe|full]
```

### `number-formulas` — Auto-number all equations

Detects all equations in the document and numbers them sequentially according to the specified style.

**Usage:**
```bash
# 指定编号风格
python insert_formula.py number-formulas <docx_path> --style parentheses

# 交互模式: 程序提示用户选择编号风格
python insert_formula.py number-formulas <docx_path> --interactive
```

**支持编号风格 (交互提示):**
```
  编号   名称          示例              说明
  ----------------------------------------------
    1    中文核心      式(1)             适用于中文核心期刊
    2    圆括号        (1)               适用于 IEEE、Elsevier 等国际期刊
    3    方括号        [1]               适用于部分物理/数学期刊
    4    章节编号      (1.1)             适用于学位论文/多章节文档
    5    LaTeX标签     \tag{1}           LaTeX 原生格式
    6    中文+括号     式(1)             中文括号组合
    7    无编号        无                不添加编号
  ----------------------------------------------
  输入编号 (1-7)，或按 Enter 使用默认 [2-圆括号]
```

### `validate-format` — Validate formula format for journal

Checks if all formulas in the document conform to the target journal's style requirements.

**Usage:**
```bash
python insert_formula.py validate-format <docx_path> --journal <journal>
```

### `export-latex` — Export formulas as LaTeX

Extracts all OMML equations from a Word document and exports them as LaTeX code.

**Usage:**
```bash
python insert_formula.py export-latex <docx_path> [--output <output.tex>]
```

### `list-styles` — List all supported journal styles

```bash
python insert_formula.py list-styles
```

## Conversion Pipeline

```
LaTeX string
    │
    ▼
latex2mathml ──── LaTeX → MathML
    │
    ▼
pandoc/mml2omml ── MathML → OMML (Office Math Markup Language)
    │
    ▼
python-docx ────── Insert OMML into .docx paragraph
    │
    ▼
Word native equation (editable, scalable)
```

## Architecture

```
academic-formula-inserter/
├── SKILL.md                           # Skill definition
├── scripts/
│   ├── formula_inserter.py            # Main entry (CLI)
│   ├── latex_omml_converter.py        # LaTeX ↔ OMML conversion
│   ├── formula_numbering.py           # Auto-numbering engine
│   ├── format_validator.py            # Journal format validation
│   └── utils/
│       ├── docx_utils.py              # Word document utilities
│       ├── journal_profiles.py        # Journal format definitions
│       └── omml_builder.py            # Low-level OMML XML building
```

## Requirements

- Python 3.8+
- python-docx
- latex2mathml
- lxml

Optional:
- pandoc (for advanced MathML→OMML conversion)
- pylatex (for LaTeX export)

## Examples

### Insert a display equation with Chinese numbering
```python
python insert_formula.py insert-formula paper.docx ^
    --latex "\sum_{i=1}^{n} x_i = \mu" ^
    --display --style chinese --number 5
```
Result: centered equation with `式(5)` right-aligned

### Batch convert for IEEE submission
```bash
python insert_formula.py batch-convert paper.docx --backup
python insert_formula.py number-formulas paper.docx --style parentheses
python insert_formula.py validate-format paper.docx --journal ieee
```

### Export to LaTeX
```bash
python insert_formula.py export-latex paper.docx --output formulas.tex
```
