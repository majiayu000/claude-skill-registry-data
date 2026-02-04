---
name: Seongjin_Book-Prep
description: Prepares PDF books for LLM analysis. Creates analysis-ready chunks through TOC-based splitting and markdown conversion while preventing Context Overflow. Use when you need PDF book analysis, chapter-based splitting, or markdown conversion.
allowed-tools: Read, Bash, Glob, Grep
version: 1.1.0
status: active
updated: 2026-01-01
---

# Book-Prep: PDF Book LLM Analysis Preparation Skill

Prepares PDF books in an optimized format for LLM analysis. Provides TOC-based splitting and markdown conversion with AI image descriptions.

## Quick Reference

### Script Locations

All scripts are located in a single directory within the skill folder:

- Script Directory: `.claude/skills/Seongjin_Book-Prep/Scripts/`
- Contains: `check_toc.py`, `split_pdf.py`, `pdf_to_md.py`, `prompt_book.md`, `.env`

### Core Workflow

1. TOC Analysis: Run check_toc.py to generate toc.json
2. Level Selection: Analyze TOC structure to select optimal level
3. PDF Splitting: Run split_pdf.py --level N
4. Markdown Conversion: Convert each split PDF with pdf_to_md.py

### Basic Commands

All commands use the Scripts directory. Use absolute path or set SCRIPTS_DIR variable:

```bash
SCRIPTS_DIR="/path/to/vault/.claude/skills/Seongjin_Book-Prep/Scripts"
```

TOC Analysis:

```bash
cd "$SCRIPTS_DIR"
source .venv/bin/activate
python3 check_toc.py "/path/to/book.pdf"
```

PDF Splitting:

```bash
python3 "$SCRIPTS_DIR/split_pdf.py" --level 1 "/path/to/book.pdf"
```

Markdown Conversion:

```bash
python3 "$SCRIPTS_DIR/pdf_to_md.py" -p "/path/to/split/chapter.pdf"
```

Alternative (direct venv python execution):

```bash
"$SCRIPTS_DIR/.venv/bin/python" "$SCRIPTS_DIR/pdf_to_md.py" -p "/path/to/chapter.pdf"
```

Note: Use `-m gemini` or `-m gpt` only when user explicitly requests a specific model.

### Output Structure

```
book.pdf (original)
book/
  toc.json (TOC analysis result)
  1. Chapter One.pdf (split PDF)
  1. Chapter One.md (markdown)
  image-cache_1. Chapter One.json (image cache)
  2. Chapter Two.pdf
  2. Chapter Two.md
  image-cache_2. Chapter Two.json
  images/ (shared image folder)
```

---

## Environment Setup

### Prerequisites

- Python 3.10+ (use `python3`, not `python` on macOS)
- Virtual environment in Scripts directory

### Initial Setup

```bash
SCRIPTS_DIR="/path/to/vault/.claude/skills/Seongjin_Book-Prep/Scripts"
cd "$SCRIPTS_DIR"
python3 -m venv .venv
source .venv/bin/activate
pip install pymupdf pymupdf4llm google-generativeai openai Pillow python-dotenv
```

### API Keys Configuration

Create or edit `.env` file in Scripts directory:

```
OPENAI_API_KEY=your-key
OPENAI_MODEL=gpt-4.1-mini
GOOGLE_API_KEY=your-key
GOOGLE_MODEL=gemini-3-flash-preview
```

---

## Implementation Guide

### Step 1: TOC Analysis

Analyzes the PDF's table of contents structure and saves it as JSON.

```bash
SCRIPTS_DIR="/path/to/vault/.claude/skills/Seongjin_Book-Prep/Scripts"
"$SCRIPTS_DIR/.venv/bin/python" "$SCRIPTS_DIR/check_toc.py" "/path/to/book.pdf"
```

Generated toc.json structure:

```json
{
  "pdf_name": "Value.pdf",
  "total_pages": 561,
  "summary": {
    "max_level": 4,
    "levels": {
      "level_1": {
        "count": 6,
        "total_pages": 380,
        "avg_pages": 89.7,
        "min_pages": 1,
        "max_pages": 505,
        "total_characters": 770597,
        "avg_characters": 77059.7,
        "min_characters": 0,
        "max_characters": 330635
      },
      "level_2": {
        "count": 5,
        "total_pages": 342,
        "avg_pages": 101.0,
        "min_pages": 30,
        "max_pages": 152,
        "total_characters": 711232,
        "avg_characters": 79025.8,
        "min_characters": 66422,
        "max_characters": 107262
      }
    }
  },
  "toc": [
    {
      "level": 1,
      "title": "Part I",
      "start_page": 20,
      "end_page": 161,
      "page_count": 142,
      "characters": 236255,
      "has_children": true
    }
  ]
}
```

#### TOC Fields

| Field | Description |
|-------|-------------|
| `level` | TOC hierarchy level (1 = top level) |
| `title` | Section title |
| `start_page` | First page (1-based) |
| `end_page` | Last page (1-based) |
| `page_count` | Number of pages |
| `characters` | Total text characters in page range |
| `has_children` | Whether this entry has sub-entries |

#### Summary Level Statistics

| Field | Description |
|-------|-------------|
| `count` | Number of entries at this level |
| `total_pages` | Sum of all page counts |
| `avg_pages` / `min_pages` / `max_pages` | Page statistics |
| `total_characters` | Sum of all character counts |
| `avg_characters` / `min_characters` / `max_characters` | Character statistics |

### Step 2: Split Level Decision

Split level decision is the core of this skill. Wrong level selection creates chunks that are too large (Context Overflow) or too small (insufficient context).

#### Decision Rules

Default rule: Use level=1 when it represents the top-level of main body content

Exception rule: Use level=2 when level=1 contains a single entry encompassing the entire body

#### Judgment Criteria

Use level=2 when ALL of the following conditions are met:
- A specific level_1 entry occupies 70% or more of total pages
- That entry has has_children: true

Use level=1 when:
- level_1 entries are relatively evenly distributed
- Each entry is an independent Part or Section

#### Real Analysis Examples

Example 1 - Value.pdf (use level=1):

toc.json analysis:
- level_1: Part I (142p), Part II (205p), Part III (140p)
- Each Part occupies 25-37% of total
- Even distribution, so level=1 is appropriate

Example 2 - The Idea of Justice.pdf (use level=2):

toc.json analysis:
- level_1: Preface (6p), Acknowledgements (5p), ... , "The Idea of Justice" (505p)
- "The Idea of Justice" entry occupies 93% (505/543)
- has_children: true
- Using level=1 creates a single 505-page chunk
- Using level=2 properly splits into Introduction, PART ONE~FOUR

Example 3 - Outclassed.pdf (use level=1):

toc.json analysis:
- level_1: Part I, Part II, Part III, Part IV
- Each Part is appropriately sized
- level=1 is appropriate

### Step 3: PDF Splitting

Split the PDF with the determined level.

```bash
"$SCRIPTS_DIR/.venv/bin/python" "$SCRIPTS_DIR/split_pdf.py" --level 2 "/path/to/book.pdf"
```

Split result:

```
The Idea of Justice/
  1. Introduction.pdf
  2. PART ONE The Demands of Justice.pdf
  3. PART TWO Forms of Reasoning.pdf
  4. PART THREE The Materials of Justice.pdf
  5. PART FOUR Public Reasoning and Democracy.pdf
```

#### Split Options

- --level 1: Top-level TOC (Part level)
- --level 2: Second-level TOC (Chapter level)
- --level 3: Third-level TOC (Section level)

### Step 4: Markdown Conversion

Convert each split PDF to markdown.

```bash
"$SCRIPTS_DIR/.venv/bin/python" "$SCRIPTS_DIR/pdf_to_md.py" -p "/path/to/chapter.pdf"
```

Conversion result (files created in same folder as PDF):

```
folder/
  Chapter.pdf (input)
  Chapter.md (markdown)
  Chapter.md.backup (backup)
  image-cache_Chapter.json (image cache)
  images/
    Chapter.pdf-0-0.png
    Chapter.pdf-1-0.png
```

#### Model Selection

- -m gpt: Use OpenAI GPT (default)
- -m gemini: Use Google Gemini

---

## Advanced Patterns

### Batch Processing

Process multiple PDFs sequentially:

```bash
for pdf in "/path/to/split/folder"/*.pdf; do
  "$SCRIPTS_DIR/.venv/bin/python" "$SCRIPTS_DIR/pdf_to_md.py" -p "$pdf"
done
```

### Parallel Processing

Run multiple conversions in parallel (background jobs):

```bash
"$SCRIPTS_DIR/.venv/bin/python" "$SCRIPTS_DIR/pdf_to_md.py" -p "chapter1.pdf" &
"$SCRIPTS_DIR/.venv/bin/python" "$SCRIPTS_DIR/pdf_to_md.py" -p "chapter2.pdf" &
"$SCRIPTS_DIR/.venv/bin/python" "$SCRIPTS_DIR/pdf_to_md.py" -p "chapter3.pdf" &
wait
```

### Large Book Processing Strategy

For books over 500 pages:

1. Understand structure with check_toc.py
2. Consider more granular splitting with level_2 or level_3
3. Adjust so each chunk is around 100-200 pages

### Prompt Customization

Modify prompt_book.md file to change image description style:

```markdown
# Available placeholders
{context_before} - Text before image
{context_after} - Text after image
{image_path} - Image path
```

### Caching Utilization

`image-cache_[name].json` caches image descriptions:
- Located in the output directory alongside markdown file
- Skips already processed images on re-run
- Delete cache and re-run to refresh descriptions

---

## Troubleshooting

### Command not found: python

Error: `command not found: python`

Cause: macOS uses `python3` instead of `python`

Solution: Always use `python3` or activate virtual environment first

### Module not found: pymupdf

Error: `ModuleNotFoundError: No module named 'pymupdf'`

Cause: Virtual environment not activated or packages not installed

Solution:
```bash
cd "$SCRIPTS_DIR"
source .venv/bin/activate
pip install pymupdf pymupdf4llm google-generativeai openai Pillow python-dotenv
```

### Externally managed environment

Error: `externally-managed-environment`

Cause: Attempting to install packages outside of virtual environment

Solution: Always use virtual environment pip:
```bash
"$SCRIPTS_DIR/.venv/bin/pip" install pymupdf pymupdf4llm google-generativeai openai Pillow python-dotenv
```

### Corrupted Virtual Environment

Error: `No such file or directory: .../python3.14`

Cause: venv references a Python path that no longer exists (moved or deleted)

Solution: Recreate the virtual environment:
```bash
cd "$SCRIPTS_DIR"
rm -rf .venv
python3 -m venv .venv
./.venv/bin/pip install pymupdf pymupdf4llm google-generativeai openai Pillow python-dotenv
```

### PDF Without TOC

Error message: "No TOC found"

Solution:
- Verify TOC exists in PDF viewer
- If no TOC, manual page range specification required
- Add TOC with Adobe Acrobat and retry

### Invalid Page Reference

Error message: "Excluded items (invalid page reference)"

Cause: Some TOC entries in PDF reference incorrect page numbers

Solution: Automatically filtered, can be ignored

### API Call Failure

Error message: "API call failed"

Check:
- Verify API key in .env file
- Check API quota
- Verify network connection

### Missing Image File

Error message: "Image file not found"

Cause: Image extraction failed during PDF conversion

Solution: Adjust DPI setting or change image format

---

## Dependencies

Required packages:
- Python 3.10+
- PyMuPDF 1.26.7+
- pymupdf4llm
- google-generativeai
- openai
- Pillow
- python-dotenv

Installation (within virtual environment):

```bash
pip install pymupdf pymupdf4llm google-generativeai openai Pillow python-dotenv
```

---

## Works Well With

- pdf skill: PDF manipulation and form processing
- pptx skill: Presentation creation
- Seongjin:Knowledge-Architect: Restructure extracted markdown
