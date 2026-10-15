---
name: paper
description: Work with research papers and TeX documents -- read, edit, compile, review.
version: 0.1.0
execution-mode: advisory
argument-hint: "[read FILE | compile FILE | review FILE | cite \"QUERY\"]"
category: fleet-ops
status: candidate
---
# Paper

Work with research papers, TeX/LaTeX documents, and academic writing.

## Operations

### read
Read a PDF or TeX file:
```bash
# PDF (Claude can read PDFs directly via the Read tool)
# Just provide the path -- Claude will render it visually

# TeX source
cat docs/publications/PAPER.tex
```

### compile
Compile a TeX document to PDF:
```bash
cd docs/publications
pdflatex PAPER.tex
# Run twice for references:
pdflatex PAPER.tex
```

If using bibliography:
```bash
pdflatex PAPER.tex
bibtex PAPER
pdflatex PAPER.tex
pdflatex PAPER.tex
```

### review
Review a paper for:
- **Accuracy**: Are claims supported by evidence?
- **Clarity**: Is the writing clear and unambiguous?
- **Completeness**: Are there missing sections or arguments?
- **Numbers**: Are statistics, counts, and citations accurate?
- **Formatting**: TeX errors, missing references, layout issues

### cite
Search for papers to cite:
- Use `[web-research]` to find relevant papers
- Check arxiv, Google Scholar, Semantic Scholar
- Verify the paper exists before citing

## Current Papers
- `docs/publications/CRAI_2026_TYPED_TUPLE_PROFILE.tex` -- CRAI 2026 paper on typed tuple profiles
- `docs/publications/CRAI_2026_TYPED_TUPLE_PROFILE.pdf` -- Compiled PDF

## TeX Tips
- Use `\cite{key}` for citations (requires .bib file)
- Use `\ref{label}` for cross-references
- Check for overfull hboxes in compile output
- Keep line length < 80 chars for readable diffs

## Skill Chains
- For OpenAlex citation search for paper research -> `[free-apis]` (`python ~/bin/free_apis.py openalex search --query <query>`)
