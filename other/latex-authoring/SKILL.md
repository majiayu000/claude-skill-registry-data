---
name: latex-authoring
description: >-
  Write or revise LaTeX source for articles and technical documents: document class,
  math, tables, citations, semantic macros, and package selection. Use when the
  requested change is in .tex content or preamble. NOT for compiling or diagnosing
  build failures (latex-build-diagnostics), Beamer slides
  (latex-beamer-presentations), TikZ figures (tikz-figure-engineering), or
  repository PDF publication (latex-whitepaper-engineering).
license: Apache-2.0
metadata:
  category: Writing
  tags: [latex, typesetting, math, tables, bibliography]
  pairs-with: [latex-build-diagnostics, latex-beamer-presentations, tikz-figure-engineering]
---

# LaTeX Authoring

Write source that expresses the document's structure and mathematics clearly.
Choose the document class and bibliography backend before adding packages;
follow a venue template when one is required. The source change is complete
only when the relevant build and rendered pages have been checked with
`latex-build-diagnostics` or the repository's publication skill.

## Choose the source structure

| Document | Starting point |
|---|---|
| Article or preprint | `article`, unless the venue requires its class |
| Book or thesis | The existing institutional class; otherwise `book`, `memoir`, or KOMA-Script |
| Letter | `scrlttr2` |
| Slides | `latex-beamer-presentations` |
| Standalone figure | `tikz-figure-engineering` |

Use a small preamble. `mathtools`, `amssymb`, `amsthm`, `microtype`,
`booktabs`, `siunitx`, `graphicx`, and `hyperref` have distinct jobs; add each
only when the source uses it. Load `hyperref` near the end and `cleveref`
after it. The current article skeleton is `templates/article.tex`.

## Mathematics

- Use `\[...\]` for display math, `align` for aligned derivations, `gather`
  for separate centered equations, and `multline` for one long equation.
- Put words in math with `\text{...}` and define repeated operators with
  `\DeclareMathOperator`. Define semantic macros once in the preamble.
- Put units through `siunitx` and distinguish a differential from a variable,
  for example `\,\mathrm{d}x`.
- Avoid `$$...$$`, `eqnarray`, and manual line breaks to end paragraphs.

Read `references/math-typesetting.md` for theorem environments, equations,
and common math-mode errors.

## Tables and figures in prose

Use `booktabs` rules without vertical grid lines. Use `siunitx` `S` columns
for comparable numeric values and `tabularx` when width is constrained.
Captions normally precede tables and follow figures. Size included figures
relative to `\linewidth` inside columns or minipages. Use vector output for
plots and raster output for photographs. For a figure drawn in TikZ, hand off
to `tikz-figure-engineering`; choose the semantic form before coordinates.

## Bibliography

| Context | Backend |
|---|---|
| Venue supplies `.bst` or requires `natbib` | BibTeX and `natbib` |
| New document with a controlled toolchain | `biblatex` and Biber |
| Repository has an established inline bibliography | Follow that repository convention |

Never mix `natbib` and `biblatex` in one document. Keep citation keys stable,
check that each cited source supports its sentence, and follow the venue's
bibliography instructions. Read `references/bibliography.md` for backend
options and `.bib` hygiene.

## Source review

- Every label and citation has a matching definition or entry.
- Every macro name describes a role, not a one-off visual tweak.
- Package order is deliberate; avoid obsolete `epsfig`, `subfigure`, and
  `eqnarray` patterns.
- Tables and math can be read at final page width.
- Pass the source to the build skill or repository pipeline and inspect the
  rendered pages that changed.

## References

- `references/math-typesetting.md`: load for equations and theorem structure.
- `references/bibliography.md`: load for citation backend and entries.
- `templates/article.tex`: starting article source.
