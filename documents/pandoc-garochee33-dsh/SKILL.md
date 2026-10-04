---
name: "pandoc"
description: "Universal document conversion with Pandoc. Use when converting between document formats (Markdown, DOCX, HTML, LaTeX, PDF, EPUB, PPTX, reveal.js, CSV, RST, Org), generating polished deliverables from plain text, batch-converting files, applying custom templates or Lua filters, or producing slide decks from Markdown."
---

# Pandoc Skill

Universal document converter — transforms content between 40+ formats while preserving structure, metadata, and styling.

## When to Use

- Convert Markdown → DOCX, PDF, HTML, EPUB, PPTX, or slides
- Convert DOCX/HTML → Markdown (for ingestion into repos or KBs)
- Batch-convert multiple files in one pass
- Generate professional reports with custom templates
- Build reveal.js slide decks from Markdown
- Extract structured content from HTML or EPUB
- Apply Lua filters for custom transformations (citation rewriting, heading renumbering, metadata injection)
- Produce camera-ready LaTeX or PDF from Markdown drafts

## Core Commands

```bash
# Markdown → Word
pandoc input.md -o output.docx

# Markdown → PDF (requires LaTeX engine)
pandoc input.md -o output.pdf --pdf-engine=lualatex

# Markdown → PDF (no LaTeX — use HTML intermediate)
pandoc input.md -t html5 -o output.pdf --pdf-engine=wkhtmltopdf

# Markdown → reveal.js slides
pandoc slides.md -t revealjs -s -o slides.html

# Markdown → PowerPoint
pandoc input.md -o output.pptx

# Markdown → EPUB
pandoc input.md --metadata title="My Book" -o output.epub

# Word → Markdown (for repo ingestion)
pandoc input.docx -t markdown -o output.md

# HTML → Markdown
pandoc input.html -t markdown -o output.md

# CSV → HTML table
pandoc input.csv -f csv -t html -o table.html

# With custom template
pandoc input.md --template=template.tex -o output.pdf

# With Lua filter
pandoc input.md --lua-filter=filter.lua -o output.docx

# Batch convert (all .md in directory)
for f in *.md; do pandoc "$f" -o "${f%.md}.docx"; done
```

## Workflow

1. **Identify source and target formats** — determine the conversion path.
2. **Check if extras are needed:**
   - PDF output → needs a LaTeX engine (`lualatex`, `xelatex`) or `wkhtmltopdf`
   - Styled DOCX → use `--reference-doc=reference.docx`
   - Slides → choose `revealjs` (HTML) or `pptx` (PowerPoint)
   - Citations → use `--citeproc` with a `.bib` file
3. **Run the conversion** — use the simplest command that achieves the goal.
4. **Verify output:**
   - For DOCX/PPTX: open or use the `doc`/`pptx` skill for visual QA
   - For PDF: use the `pdf` skill to render pages and inspect
   - For HTML: open in browser or use `agent-browser` skill
5. **Iterate** — adjust metadata, templates, or filters as needed.
6. **Clean up** — remove intermediate files.

## Key Options

| Flag | Purpose |
|------|---------|
| `-f FORMAT` | Input format (auto-detected from extension if omitted) |
| `-t FORMAT` | Output format (auto-detected from extension if omitted) |
| `-s` / `--standalone` | Produce complete document (not fragment) |
| `--template=FILE` | Custom template for output |
| `--reference-doc=FILE` | Style reference for DOCX/PPTX output |
| `--pdf-engine=ENGINE` | PDF engine: `lualatex`, `xelatex`, `wkhtmltopdf`, `weasyprint` |
| `--toc` | Generate table of contents |
| `--number-sections` | Number headings |
| `--metadata KEY=VAL` | Set metadata (title, author, date) |
| `--lua-filter=FILE` | Apply Lua filter for custom transforms |
| `--citeproc` | Process citations from bibliography |
| `--bibliography=FILE` | BibTeX/CSL JSON bibliography |
| `--highlight-style=STYLE` | Code syntax highlighting theme |
| `--columns=N` | Line wrap width for plain text output |
| `--wrap=none` | No line wrapping (useful for Markdown output) |
| `--extract-media=DIR` | Extract images to directory |

## YAML Metadata Block

Place at the top of Markdown files for rich output:

```yaml
---
title: "Document Title"
author: "Author Name"
date: 2026-05-16
abstract: "Brief summary"
lang: en
toc: true
number-sections: true
geometry: margin=1in
fontsize: 12pt
---
```

## Lua Filters (Advanced)

Pandoc supports Lua scripting for custom transformations. Save as `.lua`:

```lua
-- uppercase-headings.lua — capitalize all headings
function Header(el)
  el.content = pandoc.walk_inline(el.content, {
    Str = function(s) return pandoc.Str(s.text:upper()) end
  })
  return el
end
```

Use with: `pandoc input.md --lua-filter=uppercase-headings.lua -o output.docx`

## Temp and Output Conventions

- Intermediate files: `tmp/pandoc/` — delete when done
- Final deliverables: `output/pandoc/` or alongside source file
- Templates: store in `~/.pandoc/templates/` or project-local `templates/`
- Lua filters: store in `~/.pandoc/filters/` or project-local `filters/`

## Dependencies

Pandoc is installed via the system package manager (`brew install pandoc` on macOS, `apt install pandoc` on Linux).

For PDF output, one of:
```bash
# LaTeX (full — large install ~4GB)
brew install --cask mactex

# LaTeX (minimal — recommended)
brew install basictex
# then: sudo tlmgr install collection-fontsrecommended

# No LaTeX alternative
brew install wkhtmltopdf
# or: pip install weasyprint
```

## Format Quick Reference

| Input | Best Output Targets |
|-------|-------------------|
| Markdown | docx, pdf, html, epub, pptx, revealjs, latex |
| DOCX | markdown, html, plain |
| HTML | markdown, docx, epub, pdf |
| LaTeX | pdf, html, docx |
| CSV | html (tables), markdown |
| EPUB | markdown, html, docx |
| Org-mode | markdown, html, docx, pdf |
| RST | markdown, html, docx, pdf |

## Integration with Other Skills

- **doc/docx skill** — use pandoc to generate DOCX, then `doc` skill for visual QA
- **pdf skill** — use pandoc for PDF generation, then `pdf` skill to render and verify
- **pptx skill** — use pandoc for slide generation, then `pptx` skill for refinement
- **deep-research** — convert research outputs to polished deliverables
- **hyperframes** — convert Markdown scripts to HTML for video compositions
