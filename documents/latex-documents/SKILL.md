---
name: LaTeX Documents
description: Professional LaTeX document generation for papers, reports, books, and presentations. Multi-agent orchestration via claude-flow. Use UK English spelling throughout.
---

# LaTeX Documents Skill

Generate publication-quality LaTeX documents with claude-flow orchestration. Covers articles, reports, books, and Beamer presentations.

**UK English spelling required** (colour, optimise, centre, behaviour).

## Quick Start

```bash
# Compile document
pdflatex document.tex

# With bibliography
pdflatex document.tex && biber document && pdflatex document.tex

# Beamer with theme
TEXINPUTS=./themes/amurmaple: pdflatex presentation.tex
```

## Agent Architecture

Five agents for document generation:

| Agent                | Role                                                    |
| -------------------- | ------------------------------------------------------- |
| **LaTeX Expert**     | Preamble design, package ordering, structure            |
| **Content Writer**   | Math, code listings, tables, figures                    |
| **Citation Checker** | Web-based citation validation, DOI/URL verification     |
| **Visual QA**        | PDF rendering check via DISPLAY=:1, layout verification |
| **Quality Checker**  | Final reference integrity, .bib validation              |

### Claude-Flow Orchestration

```bash
npx claude-flow@alpha task orchestrate \
  --task "Generate research paper on topic X" \
  --strategy sequential \
  --max-agents 5
```

### Task Tool Integration

```javascript
Task("LaTeX Expert", "Design article preamble with biblatex, amsmath", "coder");
Task("Content Writer", "Write sections with equations and code", "coder");
Task("Citation Checker", "Verify DOIs and URLs in references.bib are valid", "researcher");
Task("Visual QA", "Compile PDF, screenshot on DISPLAY=:1, check layout", "tester");
Task("Quality Checker", "Final .bib validation, orphan label check", "reviewer");
```

### Citation Checker Agent

Validates bibliography entries via web lookup:

```bash
# Verify DOI resolves
curl -sI "https://doi.org/10.1234/example" | head -1

# Check URL accessibility
curl -sI "https://example.com/paper" | head -1
```

**Checks performed:**

- DOI resolution via doi.org
- URL accessibility (HEAD request)
- Author name consistency
- Year/date validation
- Duplicate entry detection

### Visual QA Agent

Renders PDF and captures screenshot for layout verification:

```bash
# Compile document
pdflatex document.tex

# View on virtual desktop
DISPLAY=:1 evince document.pdf &
sleep 2

# Capture screenshot for analysis
DISPLAY=:1 scrot -u /tmp/pdf-qa.png

# Agent analyses screenshot for:
# - Page margins and alignment
# - Figure placement
# - Table formatting
# - Font rendering
# - Overfull/underfull boxes
```

**Visual checks:**

- Text not overflowing margins
- Figures properly placed (not floating to wrong page)
- Tables fit within page width
- Code listings properly formatted
- Headers/footers consistent

## Document Types

### Article (papers, short documents)

```latex
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,graphicx,booktabs}
\usepackage[backend=biber]{biblatex}
\addbibresource{references.bib}
\usepackage{hyperref}
```

### Report (technical reports, theses)

```latex
\documentclass[11pt,a4paper]{report}
% Same packages as article
% Adds \chapter{} level
```

### Book (multi-chapter works)

```latex
\documentclass[11pt,a4paper]{book}
% Same packages
% Front/back matter support
```

### Beamer (presentations)

```latex
\documentclass{beamer}
\usetheme{Amurmaple}  % Or: Madrid, Berlin, etc.
\usepackage[utf8]{inputenc}
```

## Package Load Order

**Mandatory sequence** (conflicts otherwise):

```latex
% 1. Encoding
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}

% 2. Layout
\usepackage[margin=1in]{geometry}

% 3. Colours (before tikz/hyperref)
\usepackage{xcolor}

% 4. Content packages
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{listings}

% 5. hyperref LAST
\usepackage{hyperref}
```

## Bibliography

The `.bib` file is the **single source of truth**. Never use inline URLs.

```latex
\usepackage[backend=biber,style=ieee]{biblatex}
\addbibresource{references.bib}

% Citation: \cite{author2024}
% Print: \printbibliography
```

**BibTeX entry for URLs:**

```bibtex
@online{example2025,
  author = {Author Name},
  title = {Page Title},
  url = {https://example.com},
  urldate = {2025-01-15},
  year = {2025}
}
```

## Label Conventions

| Type     | Prefix | Example                    |
| -------- | ------ | -------------------------- |
| Figure   | `fig:` | `\label{fig:architecture}` |
| Section  | `sec:` | `\label{sec:methods}`      |
| Equation | `eq:`  | `\label{eq:main}`          |
| Table    | `tab:` | `\label{tab:results}`      |

## AmurMaple Theme (Beamer)

```latex
\usetheme{Amurmaple}                    % Red default
\usetheme[amurmapleblue]{Amurmaple}     % Blue
\usetheme[sidebar]{Amurmaple}           % With navigation
\usetheme[sidebar,rule,amurmapleblue]{Amurmaple}  % Combined
```

**Key commands:**

- `\sepframe` — Section separator
- `\thanksframe{text}` — Closing slide
- `\framesection{title}` — Subsection within frame

## Compilation

| Engine         | Use Case                     |
| -------------- | ---------------------------- |
| `pdflatex`     | Standard documents           |
| `xelatex`      | Unicode/system fonts         |
| `lualatex`     | Advanced features (Delaunay) |
| `latexmk -pdf` | Automated multi-pass         |

**With bibliography:**

```bash
pdflatex doc.tex
biber doc
pdflatex doc.tex
pdflatex doc.tex
```

## PDF Verification

The **Visual QA agent** handles automated PDF verification. Manual verification:

```bash
# View on virtual desktop
DISPLAY=:1 evince output.pdf &

# Capture for review
DISPLAY=:1 scrot screenshot.png

# Multi-page capture (page by page)
DISPLAY=:1 pdftoppm -png output.pdf /tmp/page
# Creates /tmp/page-1.png, /tmp/page-2.png, etc.
```

Screenshot analysis checks layout, margins, figure placement, and rendering quality.

## Common Issues

| Problem             | Solution                        |
| ------------------- | ------------------------------- |
| Theme not found     | `TEXINPUTS=./themes/amurmaple:` |
| Code frame fails    | Add `[fragile]` option          |
| Bibliography empty  | Run biber, then pdflatex twice  |
| Undefined reference | Check `\label{}` exists         |

## File Structure

```text
latex-documents/
├── SKILL.md
├── templates/beamer/
│   ├── amurmaple-basic.tex
│   ├── amurmaple-academic.tex
│   └── amurmaple-technical.tex
├── examples/beamer/
│   ├── demo-presentation.tex
│   └── compile-beamer.sh
└── themes/amurmaple/
```

## Best Practices

1. **Semantic markup** — Use `\section{}`, never `\textbf{}` for headings
2. **Math** — Use `\[...\]` for display, never `$$`
3. **Tables** — Use booktabs (`\toprule`, `\midrule`, `\bottomrule`), never `\hline`
4. **Code** — Use `listings` package with `[fragile]` in Beamer
5. **UK English** — colour, optimise, centre throughout
