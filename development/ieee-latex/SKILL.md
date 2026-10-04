---
name: ieee-latex
description: >-
  Compile, diagnose, and fix IEEEtran LaTeX manuscripts for JSAC, TWC, TCOM, WCL, CL, and related
  IEEE journals: documentclass options, BibTeX/IEEEtran bibliography, undefined citations/refs,
  overfull hboxes, figure/table placement, algorithm/equation numbering, Index Terms, EDICS,
  biographies, and final PDF checks. Use this when the user asks to "compile IEEEtran", "fix LaTeX",
  "overfull hbox", "undefined references", "BibTeX error", "IEEE LaTeX", "latex编译", "参考文献不显示",
  or prepare a manuscript PDF for IEEE submission. Use latex-compile when available for raw build
  execution; this skill adds IEEE-specific diagnosis.
---

# IEEEtran LaTeX Build and Diagnosis

Use this skill to compile and repair IEEE journal manuscripts while preserving IEEEtran conventions.
It complements generic LaTeX compilation skills by focusing on IEEE-specific structure, bibliography,
floats, captions, and submission checks.

## Core stance

- **Compile before guessing.** Read the `.log`, `.blg`, and warnings; fix the first real error
  before cosmetic warnings.
- **Use IEEEtran conventions.** Do not "fix" by switching classes, bibliography styles, caption
  packages, or section styles away from IEEE unless the template requires it.
- **Keep source changes minimal.** Prefer small fixes to packages/macros over broad template rewrites.
- **Do not hide warnings.** Overfull boxes, undefined refs, missing fonts, and BibTeX failures need
  diagnosis, not suppression.
- **Check final PDF surface.** A successful compile is not enough if figures are unreadable,
  references are `??`, or captions violate IEEE style.

## When to open extra files

| File | Open when |
|---|---|
| [references/build-diagnosis.md](references/build-diagnosis.md) | Running compile commands, reading `.log`/`.blg`, fixing undefined refs/citations, overfull boxes, package conflicts, and BibTeX problems |
| [references/ieeetran-checklist.md](references/ieeetran-checklist.md) | Auditing IEEEtran class options, abstract/Index Terms, floats/captions, equations, references, biographies, WCL/CL page constraints, and submission readiness |

Use `ieee-citation` for reference formatting, `ieee-figure` for figure generation, and
`ieee-letter` for WCL/CL page strategy.

## Workflow

1. **Locate the root file** and build system: `main.tex`, `latexmkrc`, Makefile, arara, or IDE log.
2. **Run or inspect the build** with an IEEE-safe sequence: LaTeX -> BibTeX -> LaTeX -> LaTeX, or
   `latexmk` when configured.
3. **Classify failures:** fatal compile error, bibliography failure, undefined references, float
   problems, overfull boxes, missing fonts/figures, or page-limit issue.
4. **Patch minimally:** fix paths, labels, citations, packages, fragile macros, caption syntax, and
   bibliography style without rewriting the manuscript.
5. **Rebuild and verify:** no fatal errors; no unresolved `??`; bibliography generated; PDF opens;
   critical warnings explained.
6. **Run IEEE-specific checks:** documentclass, Index Terms, section headings, figure/table captions,
   equation numbering, appendices, biographies, page budget, and vector figures.

## Output format

1. `Diagnosis:` root cause, files involved, and the first failing log lines or warning classes.
2. `Commands run:` exact compile/check commands and results.
3. `Fixes applied:` concise list of source changes.
4. `PDF status:` output PDF path, unresolved refs/cites count, major warnings, page count if known.
5. `Remaining actions:` any author decisions, missing figures, metadata, or journal-specific checks.
