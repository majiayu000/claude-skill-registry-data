---
name: modern-doc
description: >
  Create, improve, and debug professional LuaLaTeX documents using KOMA-Script + the moderndoc package (and the legacy modern-doc shim). Use for: generating new documents from a goal, improving typography/layout, producing PDF/A-4-friendly output, setting up minted/biblatex/tabularray/tikz, converting Mermaid → TikZ, and debugging compilation logs.


triggers:
  - "File extension: .tex"
  - "Uses \\usepackage{moderndoc} or \\usepackage{modern-doc}"
  - "Uses KOMA classes: scrartcl/scrreprt/scrbook/scrlttr2"
  - "Mentions: lualatex, latexmk, tlmgr, biber, biblatex, minted, tabularray, tikz, luatexja"
success_criteria:
  - "Generated LaTeX compiles with LuaLaTeX (and biber/minted if enabled)."
  - "Typography: no fake small caps by default, consistent paragraph style, widow/orphan control enabled."
  - "When debugging: identify the first real error, provide exact fix and recompile command."
principles:
  - "Make minimal, safe diffs. Do not introduce packages without a concrete reason."
  - "When adding bibliography data: verify citation metadata via web search (DOI/arXiv/ISBN) when possible."
  - "Prefer semantic markup over manual styling (\\term, \\foreign, \\software, \\acronym, etc.)."
---

# ModernDoc Skill

This skill helps users (beginners and advanced) produce high‑quality PDFs using:

- **LuaLaTeX** (Unicode + OpenType fonts)
- **KOMA‑Script** for layout and headings
- **moderndoc** style package

## Workflow

### 0) If the user wants “a beautiful document fast”

Use the **Template Picker** below, then generate a complete, compilable template.

### 1) Template picker (choose the best starting point)

**Ask only if missing:**

- What are you writing? (paper/report/book/letter/etc.)
- Single vs two‑column?
- Any institutional constraints? (margin rules, spacing rules, required styles)
- Need code highlighting? (minted)
- Need bibliography? (biblatex)

**Mapping:**

| User goal                     | KOMA class               | moderndoc doctype |
| ----------------------------- | ------------------------ | ----------------- |
| Short article / documentation | `scrartcl`               | `article`         |
| Conference paper (two‑column) | `scrartcl` + `twocolumn` | `paper`           |
| Technical/business report     | `scrreprt`               | `report`          |
| Thesis / dissertation         | `scrbook` (preferred)    | `thesis`          |
| Book / long-form              | `scrbook`                | `book`            |
| Formal letter                 | `scrlttr2`               | `letter`          |

Then generate from: `references/templates.md`.

### 2) Configure options safely

- Keep defaults unless the user asks.
- Use `references/options.md` to select: language, font, CJK strategy, citations, minted.

### 3) Add content features

- Bibliography: see `references/bibliography.md`
- Code: see `references/code-minted.md`
- Tables: see `references/tables-tabularray.md`
- Diagrams: see `references/diagrams-tikz.md` (+ Mermaid conversion in `references/mermaid.md`)

### 4) Typography improvement pass (when editing existing LaTeX)

Must check:

- **Paragraph style**: indent OR skip (not both)
- **Widows/orphans** penalties enabled
- Two-column layout: KOMA typearea aware (`twocolumn=true` before `\recalctypearea`)
- No fake small caps by default (fallback to letterspaced caps)

### 5) Build and verify

Preferred build:

- `latexmk -lualatex --shell-escape main.tex`

If minted disabled:

- `latexmk -lualatex main.tex`

## Debugging protocol (LaTeX compilation issues)

When user provides logs, follow this exact order:

1. Identify the _first real_ error in `.log` (ignore cascaded errors).
2. Classify:
   - Missing package (`*.sty not found`)
   - Wrong engine (pdfTeX vs LuaLaTeX)
   - Minted issue (shell escape / latexminted / pygmentize)
   - Biber/biblatex mismatch
   - Font not found (fontspec)
3. Provide:
   - Root cause (1–2 lines)
   - Exact fix command(s)
   - Exact rebuild command(s)

If logs are not provided:

- Ask for `build/*.log` or the terminal error output.
- Suggest: `latexmk -lualatex -interaction=nonstopmode -file-line-error ...`

## Output style rules

- Provide complete, compilable snippets when generating documents.
- Prefer short patches (diff-style) when improving existing code.
- Explain _why_ a change improves readability/robustness (1–2 sentences per change).

## References index

- `references/templates.md`
- `references/options.md`
- `references/project-structure.md`
- `references/luatex-koma.md`
- `references/bibliography.md`
- `references/code-minted.md`
- `references/tables-tabularray.md`
- `references/diagrams-tikz.md`
- `references/mermaid.md`
- `references/install-and-troubleshooting.md`
