---
name: lexfolio
description: Typeset legal documents from Markdown to print-ready PDF with CJK-aware layout. Supports four document templates (legal opinion / memo / contract review / analysis), three brand color schemes, and eight typography presets. Triggers when the user needs to typeset legal documents, generate legal PDFs, format legal writing, or mentions "lexfolio" or "md-to-pdf".
---

# LexFolio — Legal Markdown-to-PDF Typesetting

LexFolio renders Markdown-formatted legal documents into professionally typeset PDF files. Built on ReportLab, it ships with a Noto Serif SC / Noto Sans SC / EB Garamond font stack, three brand color schemes, eight typography presets, and four document templates tuned for common legal deliverables.

> **Dual identity.** LexFolio is both a WorkBuddy skill (this file) and an open-source Python project (Apache-2.0). The codebase is identical; this `SKILL.md` simply teaches WorkBuddy how to discover and invoke it. When distributed on GitHub, this file is harmless and can be kept.

## Project layout

```
{SKILL_DIR}/
├── SKILL.md              This file (WorkBuddy discovery descriptor)
├── run.py                CLI entry point (--demo / --list-presets / ...)
├── _demo.md              Built-in sample document
├── theme.json            Main config (colors / fonts / presets / page / cover / i18n)
├── engine/               Typesetting engine
│   ├── api.py            Public API: md_to_pdf(input, output, **opts)
│   ├── parser.py         Markdown -> Block list
│   ├── renderer.py       Block -> PDF (two-pass render for page numbering)
│   ├── styles.py         ParagraphStyle factory
│   ├── fonts.py          Font registration + CJK/Latin mixed-text formatting
│   ├── theme.py          theme.json loader
│   ├── cover.py          Cover page builder
│   └── chrome.py         Header / footer drawing
├── templates/            4 document template JSONs
│   ├── opinion.json      Legal opinion (full cover)
│   ├── memo.json         Legal memo (header table)
│   ├── review.json       Contract review (no cover)
│   └── analysis.json     Legal analysis (no cover)
└── fonts/                Font files (Noto SC + EB Garamond, OFL)
```

`{SKILL_DIR}` refers to the absolute path of the directory containing this `SKILL.md`.

## Setup

Requires `reportlab` and `pyyaml`. Install before first use:

```bash
pip install reportlab pyyaml
```

## Invocation

### Option 1: Python API (recommended)

```python
import sys
sys.path.insert(0, "{SKILL_DIR}")
from engine.api import md_to_pdf

# Basic call
md_to_pdf("input.md", "output.pdf")

# With template
md_to_pdf("input.md", template="opinion")

# With color scheme + font provider + preset
md_to_pdf("input.md", color_scheme="B", font_provider="noto", preset="executive")
```

### Option 2: CLI

```bash
cd {SKILL_DIR}
python run.py input.md -t opinion               # legal opinion template
python run.py input.md -t memo                  # memo template
python run.py input.md -s C                     # color scheme C
python run.py input.md --preset executive       # executive preset
python run.py --demo -t opinion                 # built-in demo
python run.py --list-templates                  # list templates
python run.py --list-presets                    # list presets
```

## Document templates

| Template | Label | Default preset | Default scheme | Cover |
|---|---|---|---|---|
| `opinion` | Legal Opinion | standard | B (teal + amber) | Full cover |
| `memo` | Legal Memo | executive | A (indigo) | Memo header table |
| `review` | Contract Review | redline | B (teal + amber) | None |
| `analysis` | Legal Analysis | deep | B (teal + amber) | None |

Resolution priority: CLI args > front matter > template defaults > theme.json baseline.

## Brand color schemes

| Scheme | Name | Fit |
|---|---|---|
| A | Indigo + Periwinkle | Traditional firms, finance, government |
| B | Teal + Amber | Tech, data platforms, cross-border compliance |
| C | Graphite + Cobalt | Internet, AI startups |

## Typography presets

`standard`, `executive`, `mobile`, `editorial`, `academic`, `deep`, `matrix` (landscape), `redline`.

## Markdown authoring

### Front matter (YAML)

```yaml
---
doc_type: opinion              # required: opinion / memo / review / analysis
title: Legal Opinion on XX     # cover title
firm_name_cn: XX Law Firm      # cover firm name (CN); overrides theme.json default
firm_name_en: XX LAW FIRM      # cover firm name (EN); opinion cover only
author: Jane Doe               # author / issuing attorney
date: June 15, 2026            # date
ref_no: LEGAL-OP-2026-015      # reference number (header right side)
addressee: XX Corp.            # addressee
confidential: true             # cover bottom confidential marker
cover_style: standard          # standard (white) or color (brand full-bleed)
color_scheme: B                # A / B / C
font_provider: noto            # noto (founder is kept as an alias of noto)
layout_preset: standard        # typography preset
---
```

**Key constraints:**
- `doc_type` is required; it determines the cover type and default typography.
- `firm_name_cn` / `firm_name_en` override the theme.json defaults. **Set these when deploying to a new firm.**
- `cover_style: color` enables a brand-color full-bleed cover (white text + accent line); default is `standard` (white background).
- The `founder` provider is kept as a backward-compatible alias of `noto`. The original Founder (FZ) commercial fonts were removed for licensing reasons; both providers now resolve to the same open-source Noto fonts (OFL). Configure custom fonts via `theme.json` paths.

### Supported syntax

| Syntax | Behavior |
|---|---|
| `# H1` / `## H2` / `### H3` | Three heading levels (H1 gets a brand-color decoration line; H4+ degrades to H3) |
| `> quote text` | Block quote (auto-detects case / statute / general) |
| `**Analysis**: ...` | Opinion paragraph (brand-color top bar) |
| `**bold**` / `*italic*` / `` `code` `` | Inline formatting |
| `\| header \| ... \|` | Three-line table (zebra striping + right-aligned numeric columns) |
| `---` | Horizontal rule |
| `<!-- pagebreak -->` | Forced page break |
| `<!-- sigfooter -->` | Signature-page footer ornament (brand line + confidential marker + firm name) |
| `>right text` | Right-aligned paragraph (signature blocks, attribution) |
| `^[n]^` | Footnote superscript (auto-placed before preceding punctuation, e.g. `item^[4]^.` -> `item⁴.`) |
| `[^n]: text` | Footnote definition (rendered as `[n] text` inline paragraph) |

**Limitations:**
- Ordered (`1.`) and unordered (`-`) lists are not rendered with indentation; use "First / Second" or paragraph form instead.
- Footnotes render as inline paragraphs (not page-bottom); the superscript is visual only.

## Signature page

The signature page must occupy its own page at the document end. Fixed structure:

```markdown
<!-- pagebreak -->

## Signature Page

>right **Issuing firm:** XX Law Firm

>right **Issuing attorney:** Jane Doe

>right **Date:** June 15, 2026

*Disclaimer text.*

<!-- sigfooter -->
```

**Key constraints:**
- Leave one blank line before and after `<!-- pagebreak -->`.
- `>right` lines must **not** be separated by blank lines (blank lines parse as separate paragraphs).
- `<!-- sigfooter -->` must be the last non-empty line in the document.
- Use `## Signature Page` (H2) for the heading, not H1.

## Full document skeleton

```markdown
---
doc_type: opinion
title: Legal Opinion on XX Matter
firm_name_cn: XX Law Firm
firm_name_en: XX LAW FIRM
author: Jane Doe
date: June 15, 2026
ref_no: LEGAL-OP-2026-001
addressee: XX Corp.
confidential: true
---

# Legal Opinion on XX Matter

**Client:** XX Corp.

**Issuing firm:** XX Law Firm

**Issuing attorney:** Jane Doe

---

## I. Background

(Body text...)

## II. Legal Analysis

(Body text...)

## III. Conclusion and Recommendations

(Body text...)

<!-- pagebreak -->

## Signature Page

>right **Issuing firm:** XX Law Firm

>right **Issuing attorney:** Jane Doe

>right **Date:** June 15, 2026

*Disclaimer text.*

<!-- sigfooter -->
```
