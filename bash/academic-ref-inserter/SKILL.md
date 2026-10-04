---
name: academic-ref-inserter
description: Insert, format, and cross-reference academic citations in Word (.docx) documents. Supports GB/T 7714-2015 (Chinese), IEEE, and APA 7th.
---

# Academic Reference Inserter

Insert, format, and cross-reference academic citations in Word (.docx) documents.

## When to Use

Use this skill when the user asks to:
- Insert or format academic citations in a .docx paper
- Change citation style (e.g., to IEEE, GB/T 7714, or APA)
- Add clickable cross-reference hyperlinks for citations
- Validate reference formatting
- Reorder references to match citation order

## CLI Reference

All commands support `--json` for structured output.

```bash
# Full pipeline (recommended)
python scripts/insert_refs.py fix --input paper.docx --format gbt7714

# Analyze current state
python scripts/insert_refs.py analyze --input paper.docx --json

# Change format
python scripts/insert_refs.py reformat --input paper.docx --format ieee

# Reorder references
python scripts/insert_refs.py reorder --input paper.docx

# Add hyperlinks
python scripts/insert_refs.py hyperlink --input paper.docx

# Validate
python scripts/insert_refs.py validate --input paper.docx --format gbt7714 --json
```

## Supported Formats

| Format | Flag | Ordering |
|--------|------|----------|
| GB/T 7714-2015 (Chinese) | `gbt7714` | Sequential [1] |
| IEEE (Engineering/CS) | `ieee` | Sequential [1] |
| APA 7th (Social Sciences) | `apa7` | Author-Year alphabetical |

## Workflow

1. Always run `analyze --json` first to understand the document state
2. Choose format based on user's target journal
3. Run `fix --format <name>` for the full pipeline
4. Validate with `validate --json`
5. Report summary to user

## File Locations

- Main script: `scripts/insert_refs.py`
- Format implementations: `scripts/formats/`
- Utilities: `scripts/utils/`
- Full skill definition: `.trae/skills/academic-ref-inserter/SKILL.md`

## Requirements

```bash
pip install python-docx
```

Python 3.8+ required.
