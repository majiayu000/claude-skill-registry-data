---
name: latex-architect
version: 1.0.0
description: LaTeX document standards on TeX Live 2026 — latexmk-only builds, preamble and package-order discipline, biblatex + biber bibliographies, semantic cross-references (cleveref, siunitx, booktabs), float and math conventions, chktex/latexindent gates. Use when writing, building, structuring, or reviewing LaTeX documents, papers, reports, or theses.
---

# LaTeX Architect

LaTeX conventions for documents you control — papers, reports, theses, preprints. Targets **TeX Live 2026** with **pdfLaTeX** as the default engine and **latexmk** as the only build entry point. Full skeletons (project tree, `.latexmkrc`, preamble, CI workflow, `.gitignore`) live in [RECIPES.md](RECIPES.md); pinned versions in [STACK.md](STACK.md).

Venue-specific formatting (page limits, anonymization, conference style files) is **not** this skill's job — see [ml-conference-paper-architect](../../academic/ml-conference-paper-architect/SKILL.md).

## 1. Scope & defaults

| Decision | Default | Switch when |
|---|---|---|
| Distribution | TeX Live 2026 | Never for CI. Use Tectonic for hermetic/reproducible builds where package coverage allows |
| Engine | `pdflatex` | `lualatex` when you need system fonts, real Unicode input, or microtype-heavy typography. `xelatex` only for legacy font pipelines |
| Build driver | `latexmk` | Never |
| Bibliography | `biblatex` + `biber` | Venue templates that ship `natbib` — see [§8](#8-bibliography) |
| Document classes | `article`, `report`, `book`, institutional thesis classes | — |

**Never hand-run `pdflatex` twice.** Rerun logic (cross-refs, bibliography, ToC convergence) is exactly what `latexmk` exists to solve. A build recipe that calls `pdflatex && biber && pdflatex && pdflatex` is a bug waiting to happen — it silently under-runs on the documents that need a fourth pass.

## 2. Project layout

One file per chapter or section, assembled by `\input` from a thin root file. The root holds the preamble and the `\input` list and nothing else — this keeps merge conflicts confined and lets you comment out a chapter with one line while drafting.

- `main.tex` — documentclass, preamble, `\input` list only.
- `sections/` (or `chapters/`) — one `.tex` per unit, no preamble, no `\documentclass`.
- `figures/` — source images. `tables/` if tables are large enough to warrant their own files.
- `refs.bib` — one bibliography database. Split only past ~200 entries.
- `preamble/` — split the preamble into `packages.tex` + `macros.tex` once it passes ~100 lines.

Rules that make this survive collaborators:

- **`\input` over `\include`** unless you specifically need `\includeonly` and per-chapter `.aux` files (long theses). `\include` forces a page break; `\input` does not.
- **No file extensions in `\includegraphics`** — `\includegraphics{figures/plot}` lets the engine pick `.pdf` over `.png`. Hardcoding `.png` locks you out of vector output.
- **Forward slashes and relative paths only.** `C:\Users\...` or `\graphicspath` with absolute paths breaks every other machine, including CI.
- **Vector figures (PDF/EPS) for anything plotted.** Raster only for photographs, at 300 dpi minimum.

Tree and root-file skeleton in [RECIPES §1](RECIPES.md#1-project-tree--root-file).

## 3. Build

`.latexmkrc` committed at the repo root is the contract — it encodes the engine, the bibliography backend, and the output directory so that `latexmk` alone reproduces the build on any machine and in CI. Nobody should need to remember flags.

- Build into `build/` (`$out_dir`), never the source tree. Keeps `git status` clean and makes cleanup a directory delete.
- Set `$pdf_mode` and `$bibtex_use` explicitly rather than relying on latexmk's defaults.
- `latexmk -C` for a full clean; `-c` leaves the PDF.
- Commit `.latexmkrc`; gitignore `build/` and every generated artifact (`.aux`, `.bbl`, `.fls`, `.synctex.gz`, …). **Exception:** journals that demand a `.bbl` in the submission tarball — generate it at submission time, don't track it.

`.latexmkrc` and `.gitignore` in [RECIPES §2](RECIPES.md#2-latexmkrc--gitignore).

## 4. Preamble discipline

**Package order is load-bearing**, not stylistic. The canonical order:

1. Encoding/font: `fontenc` (`T1`) + `lmodern`, or `fontspec` under lua/xelatex.
2. Layout: `geometry`, `setspace`.
3. Math: `amsmath`, `amssymb`, then `mathtools` (which patches amsmath and must follow it).
4. Content: `graphicx`, `booktabs`, `siunitx`, `listings`/`minted`.
5. Bibliography: `biblatex`.
6. **`hyperref` second-to-last** — it redefines a large surface of internal commands and must see the final versions.
7. **`cleveref` last** — it must load after `hyperref`. This one ordering constraint causes more silent breakage than any other.

Additional rules:

- **`microtype` always.** One line, measurably better justification and fewer overfull boxes. There is no reason to skip it.
- **Define semantic macros, not visual ones.** `\newcommand{\model}{\textsc{Orion}}` survives a rename; `\newcommand{\bs}{\boldsymbol}` just aliases a primitive and buys nothing.
- **`\newcommand` over `\def`** — it errors on redefinition instead of silently clobbering a package's internals.
- **No `\usepackage{times}`, `{mathptmx}`, `{pslatex}`** — obsolete font packages. Use `newtxtext`/`newtxmath` if a Times clone is mandated.
- Don't load `inputenc` under LuaLaTeX/XeLaTeX (UTF-8 is native), and don't load `subfigure` ever — it has been deprecated for two decades in favor of `subcaption`.

Preamble skeleton in [RECIPES §3](RECIPES.md#3-preamble-skeleton).

## 5. Semantic markup

The rule underneath all of these: **write meaning, let packages render it.** Anything you type as literal formatting becomes a manual-update liability when the document is restructured.

- **`\cref`/`\Cref` (cleveref) over hand-written `Figure~\ref{...}`.** The package emits the right word and the right capitalization, and `\cref{fig:a,fig:b}` handles ranges and lists automatically. Never write the word "Figure" next to a `\ref` by hand.
- **`\label` immediately after `\caption`**, never before — a label placed before the caption picks up the enclosing section's counter instead of the float's, producing references to the wrong number with no error.
- **Label prefixes by type**: `fig:`, `tab:`, `eq:`, `sec:`, `alg:`, `app:`. Makes `\cref` misuse visible on sight.
- **`siunitx` for every number with a unit** — `\SI{9.8}{\meter\per\second\squared}`, `\num{1e-3}`. Consistent spacing, correct minus signs, and one place to switch decimal separator.
- **`booktabs` rules only** (`\toprule`, `\midrule`, `\bottomrule`). No `\hline`, no vertical rules — vertical rules in tables are a typographic error, not a preference.
- **`~` before every reference and citation** (`Figure~\ref`, `Smith~\cite{x}`) to prevent a line break between the word and its number.
- Quotes: `` `single' `` and ` ``double'' `` — never the `"` character, which renders as two right-quotes.
- Dashes: `-` hyphen, `--` numeric range, `---` em dash.

## 6. Floats

- **Placement specifier `[t]` or `[tb]`.** Never `[h]` alone (LaTeX may ignore it entirely) and never `[H]` unless `float` is loaded and you have a real reason — forcing exact placement fights the algorithm and produces half-empty pages.
- **Reference every float in the text** before it appears. A float nothing points to has no defined position in the reading order.
- **Caption above tables, below figures.** This is convention, not taste; follow it unless a venue's style file overrides.
- **One `\centering` inside the float environment**, not `\begin{center}` — the latter adds vertical space that misaligns the float.
- Fighting float placement at draft stage is wasted effort. Write first; place at the end, when the text is final.

## 7. Math

- **`\[ ... \]` or `equation`/`align`. Never `$$`** — plain-TeX `$$` breaks `amsmath` spacing and `fleqn`.
- **`eqnarray` is banned** — broken spacing, known bug. Use `align`.
- `align` for multi-line, `split` inside `equation` for one numbered equation across lines, `gather` for unrelated centered lines.
- **Don't number equations you never reference.** Use the starred forms (`align*`, `equation*`).
- `\text{}` (amsmath) for words inside math, not `\mbox` or bare italics.
- Operator names: `\newcommand{\argmax}{\operatorname*{arg\,max}}`, not `\text{argmax}` — spacing and limit placement differ.

## 8. Bibliography

**Default: `biblatex` + `biber`.** Unicode-correct sorting, real field handling, `\autocite` and friends, no `.bst` archaeology. Set `backend=biber` explicitly.

- One `.bib` file, entries keyed consistently (`author-year-keyword`), exported from a manager (Zotero/JabRef) rather than hand-typed.
- **Clean the exported entries.** Publisher exports carry wrong-cased titles, missing DOIs, and arXiv preprints for papers that were later published in a venue — cite the published version.
- **Protect capitals with braces** in titles: `{B}ayesian`, `{L}aTeX`. Style files that lowercase titles will mangle proper nouns otherwise.
- `\autocite` for the common case; `\textcite` when the author is part of the sentence.

**natbib carve-out.** Conference and journal templates ship their own `.sty` with `natbib` wired in and a matching `.bst`. **Do not convert them to biblatex** — you break the venue's citation rendering and risk desk rejection. In that case: keep `natbib`, use `\citep`/`\citet`, and run `bibtex` (set `$bibtex_use = 2` in `.latexmkrc`). The rule is scoped by ownership: your document, biblatex; their template, whatever it ships. See [ml-conference-paper-architect](../../academic/ml-conference-paper-architect/SKILL.md) for the venue side.

biblatex config and both `.latexmkrc` variants in [RECIPES §4](RECIPES.md#4-bibliography-configuration).

## 9. Quality gates

- **`chktex`** — lints for the mechanical errors above (missing `~`, `$$`, bad quotes, space after abbreviations). Run it in CI; suppress specific warnings with a committed `.chktexrc`, never by disabling the tool.
- **`latexindent`** — deterministic formatting. Commit `.latexindent.yaml` and run in pre-commit so diffs stay reviewable.
- **Zero tolerance for `Overfull \hbox` over ~5pt** in the final pass. Fix by rewording, not by `\sloppy`.
- **`\usepackage[l2tabu, orthodox]{nag}`** while drafting — warns on obsolete commands directly during compilation. Remove before submission.
- **CI builds the PDF on every push** and uploads it as an artifact. A LaTeX repo where `main` doesn't compile is worse than useless, and it's a 20-line workflow.
- **One sentence per line** in source. Line-level diffs become sentence-level diffs, making review and merges tractable. Never reflow paragraphs — it produces diffs nobody can read.

CI workflow and `latexindent` config in [RECIPES §5](RECIPES.md#5-quality-gates--ci).

## 10. Banned constructs

Each of these has a correct replacement and no legitimate use in a new document:

| Never | Instead | Why |
|---|---|---|
| `\\` to end a paragraph | blank line | `\\` breaks the line without paragraph spacing or indentation logic |
| `$$ ... $$` | `\[ ... \]` | Breaks amsmath spacing |
| `eqnarray` | `align` | Known-broken spacing |
| `\hline` in tables | `booktabs` rules | Cramped, no vertical padding control |
| `subfigure` | `subcaption` | Deprecated, conflicts with `caption` |
| `\bf`, `\it`, `\rm`, `\sc` | `\textbf`, `\textit`, … | LaTeX 2.09 syntax; doesn't nest |
| `\vspace` / `\hspace` for layout | fix the underlying spacing | Hand-tuned space breaks on any reflow |
| `\centerline` | `\centering` | Plain TeX; ignores paragraph parameters |
| `\sloppy` to fix overfull boxes | reword the sentence | Trades one visible defect for worse inter-word spacing |
| Absolute paths in `\includegraphics` | relative paths | Breaks on every other machine |

## 11. Out of scope

- **Venue formatting** (page limits, anonymization, camera-ready toggles, conference `.sty` files) → [ml-conference-paper-architect](../../academic/ml-conference-paper-architect/SKILL.md)
- **Presentations / beamer** → [demo-presentation-architect](../../personal/demo-presentation-architect/SKILL.md) for deck content design, [reveal-js-architect](../../frameworks/reveal-js-architect/SKILL.md) for HTML decks
- **URU institutional formats** (Word-targeted `.md` specs) → [uru-thesis-architect](../../personal/uru-thesis-architect/SKILL.md), [uru-scientific-paper-architect](../../personal/uru-scientific-paper-architect/SKILL.md)
- **Repo tooling** (task runner, pre-commit wiring, version pinning) → [repo-tooling-architect](../../tooling/repo-tooling-architect/SKILL.md)
- **CI pipeline design** beyond the build job → [ci-cd-architect](../../infra/ci-cd-architect/SKILL.md)
