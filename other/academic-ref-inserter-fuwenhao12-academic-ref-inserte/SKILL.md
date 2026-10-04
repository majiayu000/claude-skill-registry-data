---
name: academic-ref-inserter
description: Insert, format, and cross-reference academic citations in Word (.docx) documents. Supports GB/T 7714-2015, IEEE, APA 7th.
---

# Academic Reference Inserter

Insert, format, and cross-reference academic citations in Word documents.

## When to Use

Use this skill when the user asks about:
- Inserting or formatting academic citations/references
- Changing citation style to GB/T 7714, IEEE, or APA
- Adding clickable hyperlinks for cross-references in Word
- Validating or reordering references

## CLI Commands

All commands accept `--json` for structured output.

```bash
python scripts/insert_refs.py analyze   --input paper.docx --json
python scripts/insert_refs.py fix       --input paper.docx --format gbt7714
python scripts/insert_refs.py reformat  --input paper.docx --format ieee
python scripts/insert_refs.py validate  --input paper.docx --format apa7 --json
python scripts/insert_refs.py reorder   --input paper.docx
python scripts/insert_refs.py hyperlink --input paper.docx
```

## Formats

| Flag | Style | Ordering |
|------|-------|----------|
| `gbt7714` | GB/T 7714-2015 (Chinese) | Sequential [1] |
| `ieee` | IEEE (Engineering/CS) | Sequential [1] |
| `apa7` | APA 7th (Social Sciences) | Author-Year alphabetical |

## Requirements

```bash
pip install python-docx
```

Python 3.8+ required. See `.trae/skills/academic-ref-inserter/SKILL.md` for full documentation.
