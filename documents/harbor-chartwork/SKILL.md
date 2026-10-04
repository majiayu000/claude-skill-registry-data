---
name: harbor-chartwork
description: "Chartwork for the Harbor library: choosing the diagram kind that fits an idea and drawing it in TikZ to the house style, with mechanical figure QA. Use when drafting, redesigning, auditing or QA-ing any figure in the chapters or research papers. NOT for matplotlib/raster plots, web SVG components, slide decks, or prose exposition."
license: FSL-1.1-MIT
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  category: Writing
  tags: [latex, tikz, figure-qa, whitepaper, harbor-research]
  pairs-with: [tikz-figure-engineering, whitepaper-figure-system]
  provenance:
    kind: first-party
---

# Harbor Chartwork

Three TikZ figure corpora feed the Harbor library: `website-v2/public/whitepaper/figures/`
and `whitepaper/figures/` (the seven chapter whitepapers, `hh*`-palette house style), and
`docs/harbor-research/figures/` (the seven research papers, `harborblue`/`shipred`/`seagreen`
palette). Every fragment is a bare `.tex` file `\input` at point of use -- none carries its
own `\documentclass` (six orphaned `website-v2/figures/diag-*.tex` files excepted), so none
compiles or previews on its own without help.

This skill is the toolsmith's half of chartwork: deterministic scripts that compile a lone
fragment, lint its source, inspect its rendered geometry, and lay a batch out for review. It
does not decide what a figure should say, and it does not redesign one -- that is craft and
editorial judgment, kept in `references/craft-rules.md` and `references/taxonomy.md` (both
pending, see below) for the book's author to write.

## When to use

Use this skill whenever you are drafting a new figure, revising an existing one, or auditing
the corpus for compile/lint/geometry problems -- in any of the three directories above.

Do **not** use it for matplotlib/raster plots, web/SVG UI components, slide decks, or prose
exposition. For choosing a figure's *semantic form* in the whitepaper corpus specifically
(relation vs. plot vs. state machine vs. ...), see `whitepaper-figure-system` first; for TikZ
layout craft, typography, and render-review discipline once the form is chosen, see
`tikz-figure-engineering`. Both predate this skill and own real, non-overlapping ground --
see "Relationship to other skills" below.

## The QA loop: precheck -> compile -> figcheck -> contact sheet

```bash
# 1. Source lint, no TeX needed -- fast, run this first and on every edit.
python3 scripts/tikz_precheck.py path/to/fig-whatever.tex

# 2. Compile it standalone, wrapped in the real chapter/paper preamble.
scripts/compile_fragment.sh path/to/fig-whatever.tex --out /tmp/chartwork/fig-whatever

# 3. Geometry QA on the compiled PDF: minimum text size, overflow, overlap,
#    a line through text, off-page content, dead canvas, overwidth content.
python3 scripts/figcheck.py /tmp/chartwork/fig-whatever/fig-whatever.pdf

# 4. Reviewing several figures together: one contact sheet, captioned by file.
python3 scripts/contact_sheet.py /tmp/chartwork/*/*.pdf --out /tmp/chartwork/sheet.png
```

A fragment passes this skill's QA when steps 1-3 all pass (step 3's T6/T7 are warn-only).
None of these tools rewrites a fragment; they only report. `scripts/build_corpus_audit.py`
runs the whole loop over every fragment in all three corpora at once and regenerates
`references/corpus-audit.md` -- re-run it after any figure change to refresh that inventory.

## Scripts

| Script | What it does |
|---|---|
| `scripts/tikz_precheck.py FRAGMENT.tex...` | Source lint, no TeX: missing provenance comment, `\tiny`, an off-palette color, an unwrapped multi-word node, an internal result label (`R\d+`/`CR-\d`/`B6`) in a title; P10 `\tiny`, P11 `\scriptsize` in a fragment, P13 a bare low-alpha fill with no edge (errors); P12 `\resizebox` below 0.85 and P14 `\scriptsize` row labels (warnings). P15 a caption promising a styling word the drawing never draws, P16 one identifier spelled two ways (errors), P17 a caption naming an identifier no label carries (warning). P18-P25 enforce the typographic law in `figures/pd-figure-language.tex`: a node carrying a `pd *` style AND its own `font=` (P18), any `font=` naming a size command (P19), a house ink painted on a path with no `pd *` style in its option list (P20), any `font=` naming a type family (P21 -- figure type inherits the document's face; an edition substitutes it in one place, a fragment never), `\pdfigmath` on math with no sub/superscript (P22), a `dotted`/`densely dotted`/`loosely dotted` key (P23 -- its on-length is `\pgflinewidth`, read when the key is processed, so a later `line width=` silently changes the stroke and not the dash), and a family-selection command in a node's TEXT rather than its `font=` (P24 -- `\normalfont` resets to the DOCUMENT's family, which is the door P21 does not watch; `\mathrm`/`\text` are math and are not flagged), and a `font=` built from anything but the house handles (P25 -- the general rule, because a node's `font=` replaces the PICTURE-level `font=` that carries the family, so even `font=\bfseries` loses the edition's face). P18-P25 are errors, chapter corpus only, except P23 which also applies to the style files because that is where the defect was. JSON/markdown via `--json`/`--md`. Exit 0 clean, 1 on a hard finding. |
| `scripts/compile_fragment.sh FRAGMENT.tex [--preamble chapter\|research\|book] [--out DIR]` | Wraps the fragment in the real chapter/paper preamble (read from the real source at run time, not hand-copied) and compiles it: tectonic when one is present, otherwise a local TeX Live through `latexmk -xelatex` (see *Local TeX Live* below). Writes `DIR/<stem>.pdf` + `.log`. **Exit 0** a PDF was produced; **1** a real TeX error (the first `!` line is printed); **2** usage error, or neither tectonic nor a local LaTeX engine can be found; **3** nothing to draw -- LaTeX reported no error and no pages, which is what a style or apparatus file under `figures/` does, and which a caller must not read as a compile failure. |
| `scripts/figcheck.py PDF [--json OUT] [--md OUT] [--min-font-pt 7] [--textwidth-cm 16.3] [--dash-dpi 150]` | Ten PyMuPDF checks (T1-T10) on a compiled fragment PDF; T6/T7 are warn-only, T8 (drawing or text colliding with the caption) and T9 (a dash whose on-length, gap or stroke falls under a device pixel at `--dash-dpi`) fail. T9 is the one check that answers a question no source linter can: whether a dash pattern present in the source and named in the caption actually arrives on the page. T10 fails when the drawing itself uses more than one text family (the caption, the identifier face and math excluded) -- the one check that looks at the thing a reader notices first, and the one that caught a figure passing T1-T9 clean while setting two labels in the body serif and the rest in grotesk. T10 is NOT in the CI gate's failing set; the condition for adding it is in check_figure_gate_results.py. Exit 0 clean, 1 on a T1-T5, T8, T9 or T10 failure. |
| `scripts/contact_sheet.py PDF... --out sheet.png [--cols 4] [--dpi 150]` | Renders page 0 of each PDF to a captioned thumbnail grid (Pillow). A missing/broken PDF becomes a labeled placeholder cell. |
| `scripts/build_corpus_audit.py [--out PATH] [--skip-compile]` | Runs the whole loop over all three corpora and (re)writes `references/corpus-audit.md`. `--skip-compile` runs precheck only, for a fast pass. |

## Local TeX Live (when there is no tectonic)

tectonic is the reference engine: CI installs it, and the committed PDFs are judged
against it. It is also a single self-contained binary that fetches its own packages, so
for a long time a sandbox without network egress could not compile anything at all and
every figure had to be judged from CI. That is no longer necessary. `compile_fragment.sh`
and `scripts/build-whitepapers.sh` both run on a stock Debian/Ubuntu TeX Live when no
tectonic is on `PATH`, and the whole Book — all three editions — builds locally in about
ninety seconds per edition.

**One command to set the machine up.** Run this in a fresh container before touching a
figure or the Book:

```bash
sudo apt-get update && sudo apt-get install -y --no-install-recommends \
  texlive-xetex texlive-latex-base texlive-latex-recommended texlive-latex-extra \
  texlive-pictures texlive-fonts-recommended texlive-fonts-extra \
  texlive-plain-generic texlive-science texlive-lang-greek \
  latexmk lmodern fonts-texgyre poppler-utils

# The Book binds its faces BY NAME through fontspec (TeX Gyre Pagella, TeX Gyre Heros,
# Source Code Pro), so fontconfig — not kpathsea — has to be able to find them. The
# Debian packages drop the OpenType/TrueType trees under texmf-dist without registering
# them with fontconfig, so without this file every \setmainfont in the preamble fails
# with "The font ... cannot be found" and no edition builds.
sudo tee /etc/fonts/conf.d/09-texlive-fonts.conf >/dev/null <<'XML'
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <dir>/usr/share/texlive/texmf-dist/fonts/opentype</dir>
  <dir>/usr/share/texlive/texmf-dist/fonts/truetype</dir>
</fontconfig>
XML
sudo fc-cache -f
```

Verify before trusting it — each of these must print a non-zero count:

```bash
fc-list | grep -ci 'source code pro'    # Source Code Pro: the Book's mono face
fc-list | grep -ci 'tex gyre pagella'   # Palatino: the Book's text face
fc-list | grep -ci 'tex gyre heros'     # Helvetica: \textsf and \mathsf
kpsewhich algpseudocode.sty             # texlive-science; the pseudocode listings
```

Then a real end-to-end probe, which exercises fontspec, TikZ (`matrix`,
`patterns.meta`, `decorations.pathreplacing`, `calc`, `arrows.meta`, `positioning`,
`fit`), pgfplots, mdframed, answers, standalone, sidenotes, marginnote, algpseudocode,
listings, hyperref and cleveref in one document:

```bash
skills/harbor-chartwork/scripts/compile_fragment.sh \
  website-v2/public/whitepaper/figures/fig-swk-stack-map.tex --preamble book \
  --out /tmp/chartwork/probe
```

**What the local engine does and does not give you.**

| | tectonic | local TeX Live |
|---|---|---|
| Missing `.sty` | downloaded from the bundle | hard error; `apt-get install` the TeX Live package |
| Reruns | to a fixed point | to a fixed point under `latexmk`; a fixed 3 passes without it |
| Network | needed once to warm the cache | none |
| Byte-for-byte agreement with CI | yes (same bundle) | no — see below |

The local build is a *geometry* oracle, not a *bytes* oracle. TeX Live 2023 from apt and
tectonic's bundle are different package sets with different font metrics, so the same
source can break pages differently. Judge a figure's fit, its overflow and its overlaps
locally; quote page numbers, digests and sizes from the CI PDFs. `CHARTWORK_FORCE_LOCAL_TEX=1`
takes the local branch even on a machine that has tectonic, which is how you compare the two.

## Relationship to other skills

`tikz-figure-engineering` owns TikZ source craft, typography, spacing, and its own
render-review loop (`render_tikz_figure.py`) for the whitepaper corpus specifically; its
renderer and this skill's `compile_fragment.sh`/`figcheck.py` both compile-and-inspect a
figure but answer different questions (page-fit/warnings vs. seven specific rendered-geometry
checks with a JSON/markdown contract) and neither replaces the other today. `whitepaper-figure-
system` owns semantic form (what a whitepaper figure should be) and its own atlas-coverage
checker; it does not reach the research corpus or run any of the checks here. This skill adds
what neither had: a script that actually compiles a bare fragment standalone (required before
either of the other two's renderers can run against a whitepaper fragment in isolation), a
source lint pass, and one inventory spanning all three corpora together.

## References

| File | Consult when |
|---|---|
| `references/corpus-audit.md` | You need the current compile/lint/geometry status of a specific fragment, or corpus-wide totals. Regenerate with `build_corpus_audit.py` after any figure change. |
| `references/taxonomy.md` | You are choosing the diagram kind for an idea: the idea shape → kind → TikZ idiom table (Mermaid-inspired inventory), with the figure each kind replaced in the Book. |
| `references/craft-rules.md` | You are drawing or reviewing a figure: the brief-and-atlas gate, the five-point legibility rubric, page role, per-kind rules, mechanics table, caption grammar and typography, and §7's claims/notation/convention rules (caption-drawing integrity, one notation per entity, show data variation not design variation, use the convention before inventing, encode the boundary, termination padding, edition type). |
| `references/research-notes.md` | You need the source behind a rule: the design research (Bertin, Cleveland–McGill, Tufte, Wilke, Few, Munzner) and the print-legibility measurements, with citations. |

## Validation

`tests/test_figcheck.py` and `tests/test_tikz_precheck.py` cover the two Python checkers
against fixture PDFs/fixture strings; `tests/test_figcheck_t8.py` covers the caption-collision
check (T8), `tests/test_tikz_precheck_new_rules.py` covers the legibility rules P10–P14, and
`tests/test_tikz_precheck_typography.py` covers the typographic-law rules P18–P25, the apparatus-prefix rule and the rule-id registry; `tests/test_figcheck_typeface.py` covers T9, T10 and the font-family helpers — a passing
and a failing fixture per rule, plus the exemptions (the style-definition file itself, the
research corpus, `hhpaper` as the page ground)
(see each script's own `--help` for CLI details):

```bash
python3 -m unittest discover -s skills/harbor-chartwork/tests -p 'test_*.py' -v
```
