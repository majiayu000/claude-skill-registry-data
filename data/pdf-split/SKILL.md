---
name: pdf-split
description: |
  This skill should be used when the user asks to "split PDF by chapters", "divide book into chapters", "extract chapters from PDF", or "break PDF into sections". Splits PDF documents based on table of contents or text patterns using pypdf.
context: fork
---

# PDF Chapter Splitting

Split PDF documents into individual chapter files based on table of contents or text pattern detection.

## Overview

This skill handles PDF splitting when:
- A book or document needs to be divided by chapters
- The PDF has embedded bookmarks/outlines, OR
- Chapter boundaries can be detected from text patterns (e.g., "Chapter 1:", "Part One")

## Prerequisites

Install pypdf via uv inline script dependency:
```python
# /// script
# dependencies = ["pypdf"]
# ///
```

## Workflow

### Phase 1: Analyze PDF Structure

Run `scripts/extract_toc.py` to analyze the PDF:

```bash
uv run ~/.claude/skills/pdf-split/scripts/extract_toc.py <pdf_path>
```

Output includes:
- Total page count
- Embedded bookmarks/outline (if present)
- Detected chapter patterns from text

### Phase 2: Define Chapter Boundaries

Based on Phase 1 output, define chapter boundaries as a list of tuples:
```python
chapters = [
    (start_page, end_page, "chapter_name"),
    # ...
]
```

**If bookmarks exist**: Use bookmark page numbers directly.

**If no bookmarks**:
1. Search for chapter heading patterns in text
2. Verify boundaries by checking page content
3. Present proposed boundaries for user confirmation

### Phase 3: Execute Split

Run `scripts/split_by_chapters.py` with the chapter definitions:

```bash
uv run ~/.claude/skills/pdf-split/scripts/split_by_chapters.py <pdf_path> <output_dir> --chapters '<json_chapters>'
```

Example:
```bash
uv run ~/.claude/skills/pdf-split/scripts/split_by_chapters.py \
  ~/book.pdf \
  ~/book_chapters \
  --chapters '[[1,22,"00_Intro"],[23,45,"01_Chapter1"]]'
```

## Common Chapter Patterns

| Pattern | Regex | Example |
|---------|-------|---------|
| Numbered | `Chapter\s+\d+` | "Chapter 1", "Chapter 12" |
| Part + Chapter | `Part\s+\w+.*Chapter` | "Part One: Chapter 1" |
| Section | `Section\s+\d+` | "Section 1.1" |
| Roman numerals | `Chapter\s+[IVXLC]+` | "Chapter IV" |

## Edge Cases

### Large Chapter Detection (100+ pages)
When a detected chapter exceeds 100 pages, verify the boundary:
- Check if appendix content is included
- Look for sub-sections that should be separate files

### Missing TOC
When no bookmarks or clear patterns exist:
1. Extract first 20 pages of text
2. Look for manual TOC listing
3. Parse page numbers from TOC text

### Duplicate Pattern Matches
Filter results to keep only actual chapter starts:
- Chapter headings typically appear at page top
- Ignore references to chapters in body text (e.g., "see Chapter 3")

## Output Structure

```
output_dir/
├── 00_Front_Matter.pdf
├── 01_Chapter_Name.pdf
├── 02_Chapter_Name.pdf
├── ...
└── Appendix.pdf
```

Naming convention: `{index:02d}_{sanitized_name}.pdf`

## Integration Notes

### For NotebookLM Upload
Split PDFs are suitable for NotebookLM sources:
- Each chapter as separate source enables targeted queries
- Recommended: Keep files under 500KB when possible
- Large chapters may need further splitting

### For RAG Systems
Chapter-level splitting provides natural semantic boundaries for:
- Document chunking
- Retrieval granularity
- Citation accuracy

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `scripts/extract_toc.py` | Analyze PDF, extract bookmarks and detect chapter patterns |
| `scripts/split_by_chapters.py` | Execute split with provided chapter definitions |

## Additional Resources

- **`references/pypdf-guide.md`** - pypdf API quick reference for custom operations
