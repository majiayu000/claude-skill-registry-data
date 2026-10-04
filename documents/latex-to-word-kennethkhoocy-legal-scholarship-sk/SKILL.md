---
name: latex-to-word
description: >-
  Convert between LaTeX and Microsoft Word for academic manuscripts in either
  direction, and assemble .tex from mixed sources. Fires on: converting
  .tex/LaTeX to Word/.docx ("tex to docx", "latex to word", "tex2docx", "convert
  to word", "pandoc convert"); converting .docx manuscripts to LaTeX for editing
  and back ("convert to latex", "manuscript", "footnotes", "reference doc", the
  docx-to-tex-to-docx round-trip / academic paper editing pipeline); high-fidelity
  delivery where plain pandoc loses tables, mangles cross-references, or fails on
  custom macros — booktabs/regression tables, OMML equations, cleveref, \estauto,
  \@@input, \thanks, TikZ, native Word tables, longtable, siunitx; and building
  .tex from mixed PDF/docx/LLM-generated sources. Replaces and reroutes the
  retired skills manuscript-editing-template-latex, latex-to-docx-fidelity,
  tex2docx, and latex-from-mixed-sources.
metadata:
  author: Claude Code
  date: 2026-07-03
  version: 1.0.0
---

# LaTeX ↔ Word

This skill moves academic manuscripts between LaTeX and Microsoft Word and
assembles `.tex` from heterogeneous sources. It consolidates four former skills
into three workflows: a footnote-preserving **round-trip** for co-author editing
cycles, a high-fidelity **one-way** `.tex → .docx` engine for delivering finished
papers to Word-only journals or coauthors, and a set of **knowledge patterns**
for building a single `.tex` from PDF/docx/LLM-generated content. Read the deep
doc for the workflow you need before running anything.

## Routing

| User intent | Workflow | Entry point | Deep doc |
|---|---|---|---|
| Deliver a finished LaTeX paper as high-fidelity Word (regression tables, math, cross-references must survive) | **B — one-way tex→docx** | `scripts/convert.py` | `references/tex-to-docx-engine.md` |
| Iterate on a manuscript with Word-based co-authors while editing in LaTeX (docx→tex→docx, footnotes preserved) | **A — round-trip** | `gui.py`, or `scripts/docx_to_tex.py` + `scripts/tex_to_docx.py` | `references/roundtrip.md` |
| Build a `.tex` from PDF / .docx / LLM-generated text | **C — assemble from mixed sources** | knowledge patterns (no scripts) | `references/mixed-sources.md` |

## Which workflow

- **B is the default for "deliver my LaTeX paper as Word."** The fidelity engine
  builds native Word tables, OMML equations, real footnotes, embedded figures,
  and resolves `\cref`/`\Cref`/`\eqref` from the `.aux`. Use B whenever the paper
  has regression/booktabs tables, math, or cross-references that must survive —
  plain pandoc drops or mangles all of these.
- **A is for iterating with Word-based co-authors** while you edit in LaTeX. Its
  `tex → docx` step is plain pandoc plus a style-templated `scripts/reference.docx`
  (fast, formatting-only), so it does not build native tables or resolve crefs.
  Choose A when the exchange is prose and footnotes and speed matters; switch to
  B once the document depends on tables/math/cross-references.
- **C is knowledge-only** — patterns for a pipeline that emits `.tex`, applied
  when you author the pipeline. No script to invoke.

## Quick start

Workflow B (one-way, high fidelity) — compile the source once so a current `.aux`
exists, then:

```bash
python scripts/convert.py path/to/main.tex --out main.docx
# optional: --aux main.aux --tables-dir tables --figures-dir figures \
#           --font "Linux Libertine G" --no-render
```

Workflow A (round-trip) — either launch the GUI:

```bash
python gui.py
```

or drive the two version-aware helpers (they wrap pandoc + reference.docx and run
the footnote-count sanity check), using the `input/ intermediate/ output/` layout:

```bash
python scripts/docx_to_tex.py v1     # input/input_v1.docx  -> intermediate/intermediate_v1.tex
# edit intermediate/intermediate_v2.tex ...
python scripts/tex_to_docx.py v2     # intermediate/intermediate_v2.tex -> output/output_v2.docx
```

Workflow C — no command; read `references/mixed-sources.md` and apply the
two-track escaping / code-fence-stripping / `\DeclareUnicodeCharacter` patterns
in your own generator.

## Tool requirements

- **pandoc** (3.x for the engine; ≥ 2.11 for the round-trip).
- **xelatex / latexmk** (TeX Live or MiKTeX) — required to produce the `.aux` the
  engine reads, and for TikZ/PGFPlots/algorithm rendering.
- **python-docx**, **lxml** — native table and OOXML construction.
- Optional **PyMuPDF** (fitz) + **Pillow** — QA rasterization and image rendering.
- Optional **Microsoft Word** (COM, via `win32com`) or **LibreOffice** (`soffice`)
  — final render-to-PDF check.
- `scripts/toolcheck.py` resolves the pandoc / latexmk / xelatex executable
  locations for `scripts/convert.py`, `scripts/render_latex_env.py`, and
  `scripts/gen_reference.py`; `gui.py`, the round-trip helpers, and
  `tests/run_tests.py` still call bare `pandoc`/`xelatex`/`latexmk` from PATH.

## Consolidation notes

This skill merges four predecessors; their old names route here via the
description above:

- **manuscript-editing-template-latex** → workflow A (`references/roundtrip.md`).
- **latex-to-docx-fidelity** → workflow B (`references/tex-to-docx-engine.md`).
- **latex-from-mixed-sources** → workflow C (`references/mixed-sources.md`).
- **tex2docx** (retired). Its pandoc-postprocessing fix registry was diffed
  against the fidelity engine: six of seven fixes were already subsumed
  architecturally, because the engine prevents upstream what tex2docx patched
  after the fact — tables, figures, and captions never pass through pandoc, so
  the damage tex2docx repaired downstream never occurs. The two genuine gaps were
  ported INTO the engine: the **notes-punctuation normalizer**
  (`normalize_note_text`, applied to table-notes text in both table engines) and
  **`\include{}` expansion** (in `expand_latex_inputs`). See the
  "Ported from tex2docx" section of `references/tex-to-docx-engine.md`.

`tests/` holds the 46-fixture (`t01`–`t46`) regression harness driven by
`tests/run_tests.py` and scored by `tests/qa_metrics.py`. It ships **source `.tex`
fixtures only** — compiled PDFs, rendered PNGs, and `.docx` artifacts regenerate
on each run. Fix the converter under `scripts/`, never the fixtures.

## Caution: gui.py bypasses permission prompts

`gui.py` invokes the Claude CLI with `--dangerously-skip-permissions` for its
auto-edit and auto-fix loops (the "Edits" box and the automatic XeLaTeX-error
repair). This bypasses the normal permission prompts, so any tool call Claude
makes in those loops runs without confirmation. Review `gui.py` (see the two
`--dangerously-skip-permissions` invocations) and understand what the auto loops
can do before enabling that path.
