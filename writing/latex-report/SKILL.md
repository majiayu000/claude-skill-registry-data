---
name: latex-report
description: Write LaTeX research reports. Use when asked to write, compile, or publish a report and save it to the dedicated reports repository.
---

# LaTeX Report Writing

## When to use

- User asks to write a report, summary, or technical document
- User asks to compile or fix a LaTeX file
- User wants a paper summary formatted as a document

## Canonical Location

- Save report sources and PDFs under `reports-repo/reports/`
- Prefer filename format: `YYYY-MM-DD-<topic>.tex` and matching `.pdf`
- If directory is missing, create it

## Workflow

### Writing a new report

1. **Clarify scope**: what topic, how detailed, who's the audience?
2. **Write the .tex file** using `\documentclass{article}` with these sections:
   - `\begin{abstract}` — 3-5 sentence summary
   - `\section{Introduction}` — context, motivation, what this report covers
   - `\section{Related Work}` — key prior work, how it connects
   - `\section{Analysis}` or `\section{Method}` — the main content
   - `\section{Discussion}` — implications, open questions
   - `\section{Conclusion}` — key takeaways, next steps
   - `\bibliography` — use BibTeX for citations

3. **Use proper LaTeX conventions**:
   - `\cite{}` for references, not inline text citations
   - `\ref{}` for cross-references to figures/tables/sections
   - `\begin{figure}`, `\begin{table}` for floats
   - `\usepackage{amsmath}` for equations
   - `\usepackage{graphicx}` for figures
   - `\usepackage{hyperref}` for clickable references

4. **Save** to `reports-repo/reports/` with a descriptive filename

5. **Compile**:
   ```bash
   pdflatex -interaction=nonstopmode -output-directory=<dir> <file>.tex
   bibtex <file>  # if bibliography used
   pdflatex -interaction=nonstopmode -output-directory=<dir> <file>.tex
   pdflatex -interaction=nonstopmode -output-directory=<dir> <file>.tex
   ```
   Run pdflatex twice (three times with bibtex) to resolve references.

6. **From `reports-repo`**, commit and push the `.tex` and `.pdf` files
   - Always commit and push so the report is accessible via GitHub
   - Do not commit generated reports to the main `internbot` repo unless user explicitly asks

7. **Post to Slack**: a brief plain-text summary (not the full LaTeX) with the direct GitHub link to the PDF

### Fixing compilation errors

- Read the .log file for the actual error (not just the first line)
- Common issues: missing `\end{}`, unescaped `_` or `%`, missing packages
- Fix the .tex and recompile

## GitHub Repository

- Reports are stored in the `reports-repo/` git subdir (separate repo with its own remote)
- To get the GitHub URL, run: `git -C reports-repo remote get-url origin`
- Direct PDF link format: `<repo-url>/blob/main/reports/<filename>.pdf` (strip any `.git` suffix and auth prefix)
- Credentials are already configured locally in the reports-repo

## Formatting for Slack

- Don't paste LaTeX source into Slack
- Give a 2-3 sentence summary of what the report covers
- Always include the direct GitHub link to the PDF
