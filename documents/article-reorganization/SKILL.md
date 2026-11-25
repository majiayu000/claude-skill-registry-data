---
name: article-reorganization
description: >
  Reorganize a long, scattered Markdown article into a clean hierarchy of
  Parts and Chapters, then regenerate its PDF with Pandoc
  (--top-level-division=part).
  Use when asked to "reorganize an article", "restructure into parts and
  chapters", "fix article structure and regenerate PDF", or invokes
  /article-reorganization.
---

# article-reorganization

Reorganize a long, scattered Markdown article into a clean hierarchy of **Parts** and **Chapters**, then regenerate its PDF.

## When to use

Use this skill when an article has:
- Flat or scattered section structure
- Related topics split across non-consecutive sections (e.g., "Section 2" and "Section 2 (Extended)" far apart)
- A need for print/PDF output with Parts, Chapters, Table of Contents, and Index

## Method

### 1. Analyze the current structure

Read the source Markdown and list all top-level headers. Identify logical groups, such as:
- Foundations
- Training and alignment
- Ecosystem and tooling
- Systems and applications
- Interpretability, limits, and evaluation
- Appendices and references

### 2. Propose a Part / Chapter plan

Map existing sections into a hierarchy. Keep related sections consecutive and remove "Extended" markers by promoting the content to its own chapter.

Example:

| Old | New |
| --- | --- |
| Section 1 — Introduction | Part I — Foundations → Chapter 1 — Introduction |
| Section 2 — What LLMs Actually Learn | Chapter 2 — What LLMs Actually Learn |
| Section 2 (Extended) — Transformer Architecture | Chapter 3 — Transformer Architecture |
| Section 3 — Pre-training | Chapter 4 — Pre-training |
| Section 3 (Extended) — Pre-training Deep Dive | Chapter 5 — Pre-training Deep Dive |

### 3. Rewrite the Markdown

- Use `#` for **Parts**.
- Use `##` for **Chapters**.
- Shift all internal headings down by one level (`##` → `###`, `###` → `####`).
- Place the Preface as an unnumbered chapter before Part I: `## Preface {.unnumbered}`.
- Add an **Index of Parts and Chapters** after the Preface as an unnumbered chapter.

### 4. Generate the PDF

Use Pandoc with `--top-level-division=part` so `#` becomes a LaTeX `\part{}`, `##` becomes `\chapter{}`, and `###` becomes `\section{}`.

```bash
pandoc article.md -o pdf/article.pdf \
  --toc --toc-depth=3 --number-sections \
  --pdf-engine=xelatex \
  -f markdown+hard_line_breaks \
  -V geometry:margin=1in \
  -V colorlinks=true \
  -V documentclass=report \
  --top-level-division=part \
  -V mainfont="DejaVu Serif" \
  -V sansfont="DejaVu Sans" \
  -V monofont="DejaVu Sans Mono" \
  -V mathfont="DejaVu Math TeX Gyre"
```

DejaVu fonts are recommended so box-drawing characters in ASCII diagrams render correctly.

### 5. Verify and commit

- Confirm the PDF contains the Parts, Chapters, Table of Contents, and Index.
- Commit the reorganized Markdown and regenerated PDF.
- Remove any temporary helper files; the original content remains in Git history.

## Output structure

```markdown
---
title: Article Title
---

## Preface: How to Read This Article {.unnumbered}
...

## Index of Parts and Chapters {.unnumbered}
- Part I — Foundations
  - Chapter 1 — ...
  - Chapter 2 — ...

# Part I — Foundations
## Chapter 1 — Introduction
### Section
...

# Part II — ...
...
```
