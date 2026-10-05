---
name: generating-writeup
description: Generates academic/technical writeups with IEEE citations and pandoc PDF output. Use when creating research papers, technical reports, or documentation with references.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch
  argument-hint: "[topic] [template] [citation-style]"
  stability: stable
  content-hash: sha256:9e500bc5e5b4c840c55fdb360e80ad198953af3b1be65784df0f00ae22cbf5ad
  last-verified-cc-version: 1.0.34
---

# Writeup Generation

**Target**: $ARGUMENTS

Generates **structured academic/technical writeups** as markdown with citation
support. IEEE `[1]` style by default. PDF export via pandoc is optional.

## Workflow

1. **Parse arguments** - Extract topic, template (default: `project-report-IMRaD`), and citation style
2. **Create directory** - `docs/write-up/<topic>/`
3. **Copy template** - Copy from `templates/` to `docs/write-up/<topic>/`:
   - `project-report-IMRaD` — scientific/academic (Introduction, Methods, Results, Discussion)
   - `technical-doc` — software documentation (Overview, Architecture, API, Config, Deployment)
4. **Fill sections** - Replace TODO comments in each chapter file
5. **Setup bibliography** - Add entries to `09a_bibliography.bib`
6. **Run markdownlint** - `npx markdownlint-cli docs/write-up/<topic>/*.md`
7. **Generate PDF** (optional) - If pandoc is available, run `make pandoc_run`

## Additional Resources

- Templates: [project-report-IMRaD/](templates/project-report-IMRaD/) | [technical-doc/](templates/technical-doc/)
- Setup help: `make -f $CLAUDE_PLUGIN_ROOT/Makefile setup_pdf_converter HELP`
- Pandoc help: `make -f $CLAUDE_PLUGIN_ROOT/Makefile pandoc_run HELP=1`

## Citation Styles

| Style | CSL File | Notes |
| ----- | -------- | ----- |
| IEEE (default) | Bundled (`scripts/writeup/citation-styles/ieee.csl`) | Numeric `[1]` |
| APA | Bundled (`scripts/writeup/citation-styles/apa.csl`) | Author-date `(Smith, 2024)` |
| Chicago | Bundled (`scripts/writeup/citation-styles/chicago-author-date.csl`) | Author-date `(Smith 2024)` |

Additional CSL files are available from the
[Zotero Style Repository](https://www.zotero.org/styles).

## PDF Export (Optional)

If pandoc and LaTeX are installed, generate PDF using the bundled Makefile:

```bash
dir=docs/write-up/<topic> && \
make -f $CLAUDE_PLUGIN_ROOT/Makefile pandoc_run \
  INPUT_FILES="$$(printf '%s\036' $$dir/*.md)" \
  OUTPUT_FILE="$$dir/output.pdf" \
  BIBLIOGRAPHY="$$dir/09a_bibliography.bib"
```

With custom citation style:

```bash
dir=docs/write-up/<topic> && \
make -f $CLAUDE_PLUGIN_ROOT/Makefile pandoc_run \
  INPUT_FILES="$$(printf '%s\036' $$dir/*.md)" \
  OUTPUT_FILE="$$dir/output.pdf" \
  BIBLIOGRAPHY="$$dir/09a_bibliography.bib" \
  CSL="$CLAUDE_PLUGIN_ROOT/scripts/writeup/citation-styles/apa.csl"
```

Full writeup build (content generation + PDF):

```bash
make -f $CLAUDE_PLUGIN_ROOT/Makefile writeup \
  WRITEUP_DIR=docs/write-up/<topic>
```

## Section Numbering (MANDATORY)

**NEVER add manual section numbers to headings.** Pandoc `--number-sections`
handles all numbering automatically.

- **Wrong**: `# 2. Projektvorstellung`, `## 2.1 Motivation`, `### 2.1.1 Details`
- **Correct**: `# Projektvorstellung`, `## Motivation`, `### Details`

Manual numbers in markdown headings conflict with pandoc auto-numbering and
produce duplicated numbers in the PDF output.

## Quality Checks

Before completing:

1. **No manual section numbers** - Headings must not contain `N.`, `N.N`, `N.N.N` prefixes
2. **Markdownlint** - `npx markdownlint-cli docs/write-up/<topic>/*.md`
3. **Citation validation** - Verify all `[@key]` references exist in `.bib` file
4. **PDF generation** (optional) - If pandoc available, run `make pandoc_run`

## Further Reading

- [Pandoc User's Guide](https://pandoc.org/MANUAL.html)
- [Zotero Style Repository](https://www.zotero.org/styles)
- [Citation Style Language Specification](https://citationstyles.org/)
- [BibTeX Entry Types](https://www.bibtex.org/Format/)
