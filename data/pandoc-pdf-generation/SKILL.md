---
name: pandoc-pdf-generation
description: Generates professional PDFs from Markdown using Pandoc with XeLaTeX. Use when creating PDFs, needing section numbering, table of contents, bibliography, or custom LaTeX styling.
---

# Pandoc PDF Generation

## Overview

Generate professional PDF documents from Markdown using Pandoc with the XeLaTeX engine. This skill covers automatic section numbering, table of contents, bibliography management, LaTeX customization, and common troubleshooting patterns learned through production use.

## When to Use This Skill

Use this skill when:
- Converting Markdown to PDF with professional formatting requirements
- Needing automatic section numbering and table of contents
- Managing citations and bibliographies without manual duplication
- Controlling table formatting and page breaks in LaTeX output
- Building automated PDF generation workflows

## Quick Start: Universal Build Script

### Single Source of Truth Pattern

This skill provides production-proven assets in `~/.claude/skills/pandoc-pdf-generation/assets/`:
- `table-spacing-template.tex` - Production-tuned LaTeX preamble (booktabs, colortbl, ToC fixes)
- `build-pdf.sh` - Universal auto-detecting build script

### From Any Project

```bash
# Create symlink once per project (git-friendly)
ln -s ~/.claude/skills/pandoc-pdf-generation/assets/build-pdf.sh build-pdf.sh

# Auto-detect single .md file in directory
./build-pdf.sh

# Or specify explicitly
./build-pdf.sh input.md output.pdf
```

**Features:**
- ✅ Auto-detects input file (if single .md exists)
- ✅ Auto-detects bibliography (`references.bib`) and CSL files
- ✅ Always uses production-proven LaTeX preamble from skill
- ✅ Pre-flight checks (pandoc, xelatex, files exist)
- ✅ Post-build validation (file size, page count)

### Manual Command (For Reference)

```bash
pandoc document.md \
  -o document.pdf \
  --pdf-engine=xelatex \
  --toc \
  --toc-depth=3 \
  --number-sections \
  -V geometry:margin=1in \
  -V mainfont="DejaVu Sans" \
  -H ~/.claude/skills/pandoc-pdf-generation/assets/table-spacing-template.tex
```


______________________________________________________________________

## Reference Documentation

For detailed information, see:
- [Core Development Principles](/Users/terryli/.claude/skills/pandoc-pdf-generation/references/core-principles.md) - **START HERE** - Universal principles learned from production failures
- [YAML Front Matter Structure](/Users/terryli/.claude/skills/pandoc-pdf-generation/references/yaml-structure.md) - YAML metadata patterns
- [LaTeX Customization](/Users/terryli/.claude/skills/pandoc-pdf-generation/references/latex-parameters.md) - Preamble and table formatting
- [Bibliography & Citations](/Users/terryli/.claude/skills/pandoc-pdf-generation/references/bibliography-citations.md) - BibTeX and CSL styles
- [Document Patterns](/Users/terryli/.claude/skills/pandoc-pdf-generation/references/document-patterns.md) - Document type templates
- [Troubleshooting](/Users/terryli/.claude/skills/pandoc-pdf-generation/references/troubleshooting-pandoc.md) - Common issues and fixes
