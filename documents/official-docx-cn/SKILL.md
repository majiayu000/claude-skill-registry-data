---
name: official-docx-cn
description: Create or revise Chinese official-style Word documents from Markdown or DOCX content, using stable formal-document formatting rules such as title hierarchy recognition, Founder GBK Chinese fonts, Times New Roman for Latin text and digits, fixed 28 pt line spacing, and standard odd/even page number layout. Use when the user asks for 公文格式, 按公文格式排版, 转成公文格式 Word, 正式公文排版, 整理不规范的 Word, 述职述廉报告, 述责述廉, 汇报材料, 领导讲话稿, 正式机关文稿, or wants a Markdown or Word file converted into a compliant .docx.
---

# Official DOCX CN

## Overview

Use this skill when the user wants a Chinese formal-style `.docx`, not just a generic Word export.

This skill is intentionally strict. Prefer the bundled script over ad-hoc formatting so repeated outputs stay consistent.

## When To Use

Use this skill when the user asks for any of the following:

- Convert Markdown to Chinese formal document format
- Rebuild an existing `.docx` into Chinese formal document format
- Reformat a report, speech, summary, or statement into formal Chinese document style
- Apply stable fonts, line spacing, title hierarchy, and page numbers for formal materials
- Diagnose whether headings and body text are misclassified before generating a `.docx`

Do not use this skill for:

- ordinary business memos with no formal-format requirement
- rich collaborative editing with tracked changes
- complex original `.docx` surgery where the existing file must be preserved exactly

For tracked changes or editing someone else's Word file in place, use the general `docx` skill instead.

## Workflow

### 1. Check the source structure

If the source is Markdown, inspect the heading structure first.

This skill assumes:

- `# ` main title
- first `## ` after the main title is the author/signature/date line when it looks like a name or date
- later `## ` lines are second-level headings such as `一、……`
- paragraphs beginning with `一是 / 二是 / 三是 ...` are candidate third-level items

If the source structure is inconsistent, fix the source or explain the mismatch before generating.

If the source is `.docx`, this skill extracts paragraph text and rebuilds the structure heuristically:

- first non-empty paragraph => main title
- next short name-like or date-like paragraph => author/signature/date line
- lines beginning with `一、二、三……` => second-level headings
- lines beginning with `一是 / 二是 / 三是 ...` => third-level items
- everything else => body paragraphs

This is intended for restyling non-standard Word files. It does not preserve the source file's original styles.

### 2. Use the bundled script

Run the script in `scripts/build_official_doc.py`.

Typical usage:

```bash
python3 build_official_doc.py \
  --src "/path/source.md" \
  --out "/path/output.docx"
```

DOCX input:

```bash
python3 build_official_doc.py \
  --src "/path/source.docx" \
  --out "/path/output.docx"
```

Optional desktop copy:

```bash
python3 build_official_doc.py \
  --src "/path/source.md" \
  --out "/path/output.docx" \
  --desktop-copy "/Users/you/Desktop/output.docx"
```

### 3. Formatting defaults

The script applies these defaults:

- A4 paper
- top margin `3.7 cm`
- bottom margin `3.5 cm`
- left margin `2.8 cm`
- right margin `2.6 cm`
- fixed line spacing `28 pt`
- Chinese title and body fonts from the Founder GBK series
- Latin letters and digits in `Times New Roman`
- odd pages: page number on right
- even pages: page number on left
- page number style: `— 1 —`
- if an author/signature/date line exists below the main title, do not insert a blank line between them
- keep one blank line between the author/signature/date line and the body

### 4. Heading mapping

The script maps structure as follows:

- main title: `方正小标宋_GBK`
- author/signature/date line: centered `方正楷体_GBK`
- second-level headings such as `一、……`: indented `方正黑体_GBK`
- third-level lead-in such as `一是在……方面。`: `方正楷体_GBK`
- body text after that lead-in in the same paragraph: `方正仿宋_GBK`
- ordinary body paragraphs: `方正仿宋_GBK`

If the preferred fonts are unavailable, Word may fall back to locally available fonts. The content remains usable, but the final page-level appearance may differ.

### 5. Validate output pragmatically

After generating:

- confirm the `.docx` file exists and was updated
- if the machine supports visual conversion, optionally convert to PDF for inspection
- if the user reports a layout defect, patch the script instead of manually restyling by hand

## References

If you need the stable conventions or the heading rules, read:

- `references/format-rules.md`

## Resources

### scripts/

- `scripts/build_official_doc.py`: generate formal-style `.docx` from Markdown or DOCX

### references/

- `references/format-rules.md`: the formatting and classification rules this skill follows

