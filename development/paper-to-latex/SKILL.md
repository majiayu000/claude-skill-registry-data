---
description: >
  Convert the finalized paper (final/paper.md + bibliography.jsonl) into
  LaTeX using the bundled template, and compile to PDF when a LaTeX
  toolchain is available. Optional post-processing after /verify-claims.
argument-hint: "[--run <run-id>] [--keep-tags]"
disable-model-invocation: true
allowed-tools: Bash(which:*), Read, Write, Glob
---

# /paper-to-latex — optional .tex / PDF rendering

Arguments: `$ARGUMENTS`

LaTeX availability: !`which pdflatex latexmk 2>/dev/null || echo "no LaTeX toolchain found"`

Preconditions: resolve the run (`--run` or ACTIVE_RUN); `final/paper.md`
must exist — otherwise point to `/verify-claims`.

1. Read `final/paper.md`, `bibliography.jsonl`, and the template
   `${CLAUDE_SKILL_DIR}/templates/paper.tex.tmpl`.
2. Write `final/paper.tex`:
   - Map markdown sections → `\section{}`, bold/italic/code accordingly.
   - Strip evidence tags from the prose UNLESS `--keep-tags` was passed
     (then render them as `\footnote{\texttt{EV:...}}`). Stripping tags is a
     RENDERING step only — never touch final/paper.md itself.
   - Replace `[EV:cite:key]` with `\cite{key}` and generate
     `final/references.bib` from bibliography.jsonl (BibTeX entries; use
     `@misc` with `howpublished={\url{...}}` when venue data is thin).
   - Escape LaTeX specials (%, &, _, #) in text.
3. If pdflatex/latexmk exists: compile in `final/`
   (`latexmk -pdf -interaction=nonstopmode paper.tex` or two pdflatex +
   bibtex passes), report `final/paper.pdf`. Clean aux files.
4. If no toolchain: stop at `final/paper.tex` + `final/references.bib` and
   tell the user they compile anywhere (e.g. Overleaf) — do NOT attempt to
   install texlive.
