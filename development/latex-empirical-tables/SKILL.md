---
name: latex-empirical-tables
description: >-
  Set up, format, fix, and clean up LaTeX regression and estimation tables in empirical
  economics or finance papers. Use when (a) creating a .tex, results.tex, main.tex, or
  preamble to display regression or estimation output from Python (pyfixest), Stata, or R
  — including any mention of estout, esttab, estauto, estwide, or table fragments;
  (b) formatting or repairing estout-style regression tables that overflow the right margin,
  have cramped or boxed notes, misaligned columns, or poor significance stars, or when asked
  to match a reference paper, make the note fill the table width, or choose among \estwide,
  \estauto, and landscape layouts; (c) diagnosing "Misplaced \omit" errors from \input-ed
  table fragments inside tabular environments. Covers \@@input, \estwide, \estauto, \estautoLT,
  \specialcell, \sym, minipage notes below tabulars, and the convert-and-verify workflow.
  Do NOT trigger for general LaTeX documents like beamer presentations, problem sets, letters,
  or CVs.
metadata:
  author: Claude Code
  version: 1.1.0
  date: 2026-07-20
  consolidates: Merges estout-table-formatting, latex-results-preamble, and latex-input-multicolumn-omit-fix into one skill.
---

# LaTeX Empirical Tables

Empirical economics and finance papers export regression and estimation output as estout/esttab "body fragments" — rows of `\multicolumn` headers, coefficients with `\sym` stars, and parenthesised p-values or SEs, with no `\toprule`/`\bottomrule` — pulled into the manuscript through a wrapper macro (`\estauto`/`\estwide`/`\estautoLT`). Done well this reads like a top-journal table. Done naively it looks broken: wide tables spill past the right margin, the note legend is jammed inside the tabular as a boxed cell, columns sit at uneven widths, and `\input`-ed fragments throw "Misplaced \omit". This skill sets a results `.tex` up from scratch, converts ugly estout tables to the gold-standard pattern, and diagnoses the `\omit` error. The reasoning behind each choice is given so you can adapt rather than copy blindly.

## Routing

| You want to... | Go to |
|----------------|-------|
| Set up `results.tex`/`main.tex` and its preamble from scratch | Section A |
| Fix or reformat existing estout tables (overflow, cramped notes, stars, alignment) | Section B |
| Diagnose a "Misplaced `\omit`" error from an `\input`-ed fragment | Section C |
| Merge several self-compiling block `results.tex` files into one master document | Section D |
| Fix skipped table numbers (Table 1, Table 3, ...) when `\captionof` + `longtable` are combined | Section D |

---

# Section A — Build a results document from scratch

When producing regression or estimation tables, follow this workflow to create a
compilable LaTeX document with a standard empirical-economics preamble and estout macros.

## Directory structure

All output lives under `outline/` relative to the project root:

```
outline/
├── preamble/
│   └── preamble.tex    ← LaTeX preamble (no \begin{document})
├── Tables/
│   ├── table_01.tex    ← table fragments (auto-increment)
│   ├── table_02.tex
│   └── ...
├── Figures/
│   └── ...             ← figures (.pdf, .png, etc.)
└── results.tex         ← master document (created on first table)
```

## Step-by-step workflow

### 1. Ensure directories exist

Create `outline/preamble/` and `outline/Tables/` if they don't already exist. Also
create `outline/Figures/` if figures will be produced.

### 2. Save the preamble

Copy `references/preamble.tex` from this skill's directory to
`outline/preamble/preamble.tex`. This file contains everything up to but NOT including
`\begin{document}` — the document class, all packages, and the estout macro definitions
(`\estauto`, `\estwide`, `\estautoLT`, `\sym`, `\specialcell`). The macros are defined
there in full; Section B lists a minimal subset if you only need to graft them onto an
existing preamble.

Do NOT create `outline/results.tex` yet — it gets created automatically when the first
table is generated.

### 3. When producing a table

Each time a regression or summary table is generated:

1. Save the table fragment to `outline/Tables/table_XX.tex` with auto-incrementing
   numbering (01, 02, 03, ...).

2. If `outline/results.tex` does **not** exist, create it:
   ```latex
   \input{preamble/preamble}

   \begin{document}

   \section{Tables}

   \subsection{Descriptive Title}
   \begin{table}[H]
   \caption{Descriptive Title}
   \centering
   \estauto{Tables/table_01.tex}{N}{D{.}{.}{-1}}
   \end{table}
   \FloatBarrier

   \end{document}
   ```

3. If `outline/results.tex` **already exists**, insert the following block BEFORE
   `\end{document}`:
   ```latex
   \subsection{Descriptive Title}
   \begin{table}[H]
   \caption{Descriptive Title}
   \centering
   \estauto{Tables/table_XX.tex}{N}{D{.}{.}{-1}}
   \end{table}
   \FloatBarrier
   ```

Where `N` = number of data columns in the fragment (excluding the label column).

## Estout table macros

Three macros are defined in the preamble for including table fragments generated by any
tool (pyfixest, esttab, R, etc.). All use the TeX primitive `\@@input` to avoid
`\multicolumn`/`\omit` errors (Section C explains why this matters).

| Macro | Use case | Environment |
|-------|----------|-------------|
| `\estauto{file}{ncols}{colspec}` | Standard-width tables | `tabular` |
| `\estwide{file}{ncols}{colspec}` | Full-page-width tables | `tabular*` |
| `\estautoLT{file}{ncols}{colspec}` | Multi-page tables | `longtable` |

The default column spec is `D{.}{.}{-1}` (decimal-aligned via `dcolumn`). Use `c` only
when columns contain non-numeric content.

## Table fragment format

Fragments must follow these conventions — the wrapper macros add `\toprule` and
`\bottomrule`, so fragments should NOT include them.

### Structure:
- Column headers: `\multicolumn{1}{c}{(1)}` style
- Group headers: `\multicolumn{N}{c}{Group Name}` with `\cmidrule(lr){start-end}`
- Coefficients right-aligned, p-values in parentheses on the next line
- Significance: `\sym{*}` p<0.10, `\sym{**}` p<0.05, `\sym{***}` p<0.01
- Multi-line variable names: `\specialcell{Line1 \\ Line2}`
- `\addlinespace` between variable blocks
- `\midrule` before summary statistics
- Yes/No rows: `\multicolumn{1}{c}{Yes}`
- Numeric summary stats: raw numbers, no `\multicolumn` wrapper
- Do NOT end with a trailing `\\` (the macro appends `\\ \bottomrule`)

Because the wrapper expands the TeX primitive `\@@input` rather than `\input`, a fragment
may begin with `\multicolumn` spanning all columns without error; Section C explains why
that matters and what to do if a house preamble expands plain `\input` instead.

### Example fragment:

```latex
                    &\multicolumn{2}{c}{OLS}                    &\multicolumn{2}{c}{IV}                     \\\cmidrule(lr){2-3}\cmidrule(lr){4-5}
                    &\multicolumn{1}{c}{(1)}         &\multicolumn{1}{c}{(2)}         &\multicolumn{1}{c}{(3)}         &\multicolumn{1}{c}{(4)}         \\
\midrule
Treatment           &       0.245\sym{**} &       0.312\sym{***}&       0.198\sym{*}  &       0.267\sym{**} \\
                    &     (0.024)         &     (0.003)         &     (0.087)         &     (0.041)         \\
\addlinespace
Control Variable    &      -0.031         &      -0.045         &      -0.028         &      -0.039         \\
                    &     (0.542)         &     (0.388)         &     (0.601)         &     (0.452)         \\
\midrule
Observations        &        1500         &        1500         &        1500         &        1500         \\
Firm FE             &\multicolumn{1}{c}{Yes}         &\multicolumn{1}{c}{No}          &\multicolumn{1}{c}{Yes}         &\multicolumn{1}{c}{No}          \\
Year FE             &\multicolumn{1}{c}{Yes}         &\multicolumn{1}{c}{Yes}         &\multicolumn{1}{c}{Yes}         &\multicolumn{1}{c}{Yes}         \\
Adjusted R-Sq       &       0.342         &       0.215         &                     &                     \\
F Statistic         &      12.450         &       8.320         &                     &                     \\
```

## Optional: Bibliography support

If the document needs references, add this to `outline/preamble/preamble.tex` (before the
end of the file):

```latex
% --- References (biblatex + biber, APA) ---
\usepackage[numbib]{tocbibind}
\usepackage[
  backend=biber,
  style=apa,
  backref=true,
]{biblatex}
\addbibresource{references.bib}
\renewcommand*{\bibfont}{\setstretch{1.2}}
\setlength\bibitemsep{1em}
```

---

# Section B — Fix or reformat existing tables

The gold-standard pattern and the procedure to convert an ugly set of estout tables to
it. Read `references/conversion-example.md` for a full before/after.

## What good looks like (the four practices)

1. **Wrapper macros use the TeX primitive `\@@input`, not `\input`.** estout fragments typically start with `\multicolumn{...}`, whose internal `\omit` must be the first token in the cell; LaTeX's `\input` wraps the file read in non-expandable file-existence checks that execute *in that first cell*, so the fragment throws **"Misplaced \omit"**. The primitive `\@@input` (inside `\makeatletter … \makeatother`) does not, so the fragment renders. Section C gives the full root cause and the before/after fix.

2. **Wide tables fill `\textwidth` via `\estwide` (a `tabular*`).** A plain `\begin{tabular}` sizes to its natural content width — fine for 2–3 narrow columns, but a 5–6 column regression table overflows the margin (you see `Overfull \hbox` on the table rows and the right edge runs off the page). `\estwide` uses `\begin{tabular*}{\textwidth}{@{\hskip\tabcolsep\extracolsep\fill}l*{N}{c}}` so the inter-column glue (`\extracolsep\fill`) spreads the columns to exactly `\textwidth`. The table now fits and the columns are evenly distributed.

3. **Notes live OUTSIDE the tabular, in a `\minipage` below it.** This is the single most common defect. Putting the legend inside the fragment as a `\multicolumn{N}{l}{\footnotesize ...}` row makes the note part of the ruled box, clamps it to the table's width, and breaks awkwardly. Instead, strip those rows out of the fragment and place the note in a `\begin{minipage}{\textwidth}\footnotesize{Note: ...}\end{minipage}` *below* the `\estwide`/`\estauto` call. The note then spans the text block, wraps cleanly, and reads like a journal table note. If the float wraps the table in `\resizebox{..\textwidth}{!}{...}`, the `\minipage` note goes *outside* that box — a note left inside is scaled with the table to a tiny font and clamped to the table width (the "the note doesn't fill the page" complaint). See "Special case" below.

4. **Each table float is consistent:** `\begin{table}[!htbp]` (or `[H]`), `\caption{...}`, `\label{...}`, `\centering`, the `\estwide`/`\estauto` call, then the `\minipage` note, then `\end{table}`. Multi-line column headers use `\specialcell{...}`; grouped columns get `\cmidrule(lr){a-b}`.

## The macros (minimal block to add to an existing preamble)

Add these once to an existing preamble. They require `booktabs` (for
`\toprule`/`\midrule`/`\bottomrule`/`\cmidrule`). `\estwide` and `\estauto` are siblings;
keep BOTH so you can pick per table. (Section A's `references/preamble.tex` already
contains these plus `\estautoLT`.)

```latex
\makeatletter
% Natural-width estout table. \@@input (TeX primitive) lets a fragment that
% starts with \multicolumn render without a "Misplaced \omit" error.
\newcommand{\estauto}[3]{%
  \vspace{.75ex}{%
    \begin{tabular}{l*{#2}{#3}}\toprule\@@input #1 %
    \\ \bottomrule
    \addlinespace[.75ex]
    \end{tabular}%
  }%
}
% Full-\textwidth estout table: a tabular* whose \extracolsep\fill spreads the
% columns to fill the page, so a wide table stops overflowing the margin.
\newcommand{\estwide}[3]{%
  \vspace{.75ex}{%
    \begin{tabular*}{\textwidth}{@{\hskip\tabcolsep\extracolsep\fill}l*{#2}{#3}}\toprule\@@input #1 %
    \\ \bottomrule
    \addlinespace[.75ex]
    \end{tabular*}%
  }%
}
\makeatother
% Multi-line column headers inside a single cell: \specialcell{line1\\line2}.
\newcommand{\specialcell}[2][c]{\begin{tabular}[#1]{@{}c@{}}#2\end{tabular}}
% Significance stars that don't widen the column (overlap to the right).
\newcommand{\sym}[1]{\rlap{#1}}
```

`#1` = fragment path, `#2` = number of data columns, `#3` = column type (`c`, or a
`dcolumn` `D{.}{.}{-1}` spec for decimal alignment). The second argument MUST equal the
fragment's data-column count.

## The table float pattern

```latex
\begin{table}[!htbp]
\caption{Difference-in-Differences: Board Independence}
\label{tab:h1_did}
\centering
\estwide{Tables/table_02.tex}{4}{c}
\begin{minipage}{\textwidth}
\footnotesize{Note: \sym{***} $p<0.01$, \sym{**} $p<0.05$, \sym{*} $p<0.10$. Values in parentheses are $p$-values. The panel estimates difference-in-differences effects on board independence across sample windows, with controls, firm and year fixed effects, and firm-clustered inference.}
\end{minipage}
\end{table}
```

For a table that should occupy its own page, follow `\end{table}` with `\vspace*{\fill}`
then `\clearpage`. For a table too wide even for `\estwide`, wrap the call in
`\begin{landscape} ... \resizebox{1.0\linewidth}{!}{\estauto{...}} ... \end{landscape}`
(landscape needs `pdflscape`/`lscape`).

## Choosing the wrapper

- **`\estwide`** — the default for regression and summary tables with **≥4 data
  columns**, or any table that overflows the margin. Fills `\textwidth`.
- **`\estauto`** — genuinely **narrow** tables (2–3 columns, e.g. a year-by-year event
  study), where stretching to full width would leave absurd gaps.
- **landscape + `\resizebox`** — very wide tables (many columns / long headers) that
  won't fit even rotated at natural size. `\resizebox` scales the font, so prefer
  `\estwide` whenever it fits; reserve `\resizebox` for the genuinely huge.

## Special case: a self-contained tabular `\input`-ed with its note inside

The worst-formatted table in a paper is often the one that escaped the `\estauto`/`\estwide` convention entirely: a fragment that is a *complete* `tabular` — its own `\begin{tabular}{...}`, `\toprule`, `\bottomrule`, `\end{tabular}`, **and** the note baked in as a final `\multicolumn{N}{p{...}}{\footnotesize ...}` row — pulled into the manuscript with a plain `\input{...}`, frequently wrapped in `\resizebox{0.99\textwidth}{!}{ \input{...} }`.

**Detection** (grep the manuscript for `\input{Tables/` or `\input{Online Appendix/`, then open the fragment): the fragment contains `\begin{tabular}`…`\end{tabular}` with `\toprule`/`\bottomrule`, its last content row is a `\multicolumn{N}{...}{\footnotesize ...}` note, and the float wraps it in `\resizebox{...}{!}{ \input{...} }`. Every *other* regression table in the same paper instead uses `\estauto{...}{N}{c}` (or `\estwide`) with the note in a `\minipage` — so this one is the outlier.

**Why it looks broken:** `\resizebox` scales the *whole* box, so a note living inside the tabular is shrunk to a tiny font **and** clamped to the tabular's width — it no longer matches the table that fills the page. That is exactly the "the note doesn't adhere to / doesn't fill the page" complaint. (Even without `\resizebox`, an in-tabular `\multicolumn{N}{p{0.97\linewidth}}` note is a ruled-box cell — practice 3.)

**Fix — convert it to the house pattern, matching a sibling table in the SAME manuscript**
(read one sibling's float and its fragment first, to copy the column count, note wording,
and trailing convention):

1. **Make the fragment body-only.** Delete `\begin{tabular}{...}`, `\toprule`, the `\bottomrule`, `\end{tabular}`, and the `\multicolumn{N}{...}{...}` note row. Keep the column-header rows, `\cmidrule`s, `\midrule`s, data rows, and the scalar rows (Observations, $R^2$, control-indicator rows). Match the sibling fragments' trailing convention — in many house preambles the last data row ends with `\\` and the wrapper appends its own `\\ \bottomrule`, so a trailing `\\` is correct *there* even though a bare body fragment usually omits it. (If you generate the fragment from a script, edit the emitter to stop writing the wrapper and the note, not the manuscript by hand.)
2. **Switch the manuscript call** from `\input{Tables/X.tex}` to `\estauto{Tables/X.tex}{N}{c}` (or `\estwide`), with `N` = the fragment's data-column count. Keep any surrounding `\resizebox`.
3. **Move the note into a `\minipage`** placed *below* and *outside* the `\resizebox{...}{!}{...}` so it renders at full `\footnotesize`/`\textwidth`, copying the wording style (and the "* significant at the 10\% level; … We cluster standard-errors at …" closing) of a sibling table's note. State the winsorization and any sample restriction here if the project requires it.
4. Recompile and verify (below); confirm no `Misplaced \omit` and that the note now spans the page under the table.

**The `\input` vs `\@@input` caveat.** If the wrapper expands `\input` / `\estinput` (some house preambles do `\let\estinput=\input`) rather than `\@@input`, the body fragment **must start with an empty leading cell** — ` & \multicolumn{...}` — so the first token after `\toprule` is not `\multicolumn`'s `\omit`; otherwise the wrapper throws "Misplaced \omit" and you must switch it to `\@@input` (practice 1). estout's own output already starts with that empty cell, which is why these fragments compile under a plain-`\input` wrapper.

## Conversion procedure (ugly estout tables → gold standard)

This is the exact sequence that works. Read `references/conversion-example.md` for a full
before/after.

1. **Find a gold-standard reference if the user names one** (a prior paper of theirs that is formatted well). Read its preamble macros and a couple of its `\begin{table}` blocks to match house style (note wording, column-group rules, header style). If none is named, use the pattern above.
2. **Add `\estwide` and `\specialcell` to the preamble**, keeping `\@@input` (do not "simplify" to `\input` — it reintroduces the `\omit` error). Confirm `booktabs` and (if using decimal alignment) `dcolumn` are loaded.
3. **Switch wide `\estauto{...}` calls to `\estwide{...}`** in the manuscript, per the decision rule. Keep the second argument (column count) unchanged.
4. **Relocate the notes.** In each fragment, delete the explanatory legend rows — the `\midrule` + `\multicolumn{N}{l}{\footnotesize ... $p$-values ... \sym ...}` lines and any other purely-descriptive `\multicolumn{...}{\footnotesize ...}` rows. Keep panel headers (`\multicolumn{N}{l}{\textbf{Panel A: ...}}`), data rows, `\midrule`s, and column-header rows. Then add a `\minipage` note below each table in the manuscript, folding the deleted legend plus **one accurate descriptive sentence** (DV, controls, fixed effects, clustering, sample) into it. Pull the description from the deleted note and the surrounding prose — never invent a result.
5. **Add `\centering` and a `\label`** to any float missing them (prose `\ref`s depend on existing label names — keep them).
6. **Freeze every number.** Do not touch a coefficient, SE, p-value, significance star, sample size, or panel. Formatting only.
7. **Compile and verify** (below).

## Verification (do not claim done until these pass)

Run `pdflatex → bibtex → pdflatex → pdflatex`, then confirm:

- **0 errors:** `grep -E "^!|:[0-9]+:" main.log` is empty (in particular no "Misplaced
  \omit", which means a fragment is being `\input` not `\@@input`).
- **0 undefined references/citations.**
- **No large table overflow:** the `Overfull \hbox` warnings on table rows are gone (a
  few-pt overfull on a prose line is fine; tens of pt on a table row is not).
  `grep -cE "Overfull \\\\hbox \\([2-9][0-9]" main.log` should be ~0 for table lines.
- **Numbers unchanged:** if the project has a star/p-value validator (e.g.
  `scripts/validate_stars.py`), it must still report ALL PASS. Otherwise diff each fragment
  against a backup and confirm the only removed lines are the legend rows.

Always back up `main.tex` and the `Tables/` fragments before editing, since the edits touch
many files.

---

# Section C — Diagnose "Misplaced \omit"

## Problem

When using `\input` (or a macro aliased to `\input`) to include table fragment files inside a `tabular` environment, LaTeX throws `! Misplaced \omit` errors if the fragment file starts with `\multicolumn`. The same table content works perfectly when written inline (without `\input`). This commonly occurs with estout-style table macros (e.g., `\estauto`) that wrap `\input`-ed fragments in `\begin{tabular}...\toprule...\input{file}...\bottomrule...\end{tabular}`.

## Context / Trigger Conditions

- **Error message**: `! Misplaced \omit.` followed by `\multispan ->\omit`
- **Scenario**: A tabular environment uses `\input{file.tex}` where the file starts with
  `\multicolumn{N}{...}{...}`
- **Pattern**: Multi-panel tables with `\multicolumn{N}{l}{\textbf{Panel A:...}}` as the
  first content line fail, while single-panel tables starting with
  ` & \multicolumn{1}{c}{(1)} & ...` succeed (because `\omit` is in the second cell, not
  the first)
- **Key diagnostic**: The exact same table content compiles without error when pasted
  inline instead of `\input`-ed

## Root Cause

LaTeX's `\input` command is NOT the TeX primitive. LaTeX redefines `\input` to wrap the
primitive (`\@@input`) with:
- File existence checks (`\InputIfFileExists`)
- Path resolution
- Nested input tracking

These wrapper operations are **non-expandable** and execute as content in the first table cell. Once any content has been processed in a cell, `\multicolumn`'s internal `\omit` command (which must be the absolute first token in a cell) is rejected by TeX's alignment mechanism.

**Why some tables work**: Fragments starting with ` & \multicolumn{1}{c}{...}` put `\omit` in the *second* cell (after `&`), where it IS the first token. Only fragments where `\multicolumn` spanning all columns is the very first token trigger the error.

## Solution

Replace LaTeX's `\input` with the TeX primitive `\@@input` in the table macro. The
primitive is fully expandable and injects no tokens before the file content.

### Before (broken):

```latex
\newcommand{\estauto}[3]{
    \vspace{.75ex}{
        \begin{tabular}{l*{#2}{#3}}
        \toprule
        \estinput{#1}
        \\ \bottomrule
        \addlinespace[.75ex]
        \end{tabular}
    }
}
\let\estinput=\input
```

### After (fixed):

```latex
\makeatletter
\newcommand{\estauto}[3]{%
    \vspace{.75ex}{%
        \begin{tabular}{l*{#2}{#3}}\toprule\@@input #1 %
        \\ \bottomrule
        \addlinespace[.75ex]
        \end{tabular}%
    }%
}
\makeatother
```

### Key details of the fix:

1. **`\@@input` instead of `\input`**: The TeX primitive is fully expandable, so it
   injects no tokens before the file content. Requires `\makeatletter` / `\makeatother`
   since the name contains `@`.

2. **Syntax**: `\@@input #1 ` (space-terminated filename, no braces). The trailing space
   after `#1` is the filename terminator for the primitive.

3. **Same line**: `\toprule\@@input #1 %` keeps everything on one line with `%` eating the
   trailing newline, preventing whitespace tokens between `\toprule` and the file content.

4. **`%` after lines**: Add `%` at end of macro definition lines to prevent newline-generated
   space tokens from entering the tabular cells.

## Also fix: trailing `\\` in fragments

When using an `\estauto`-style macro that appends `\\ \bottomrule` after the input, ensure
table fragment files do NOT end with `\\` on their last line. Double `\\` before
`\bottomrule` creates an empty row where `\bottomrule`'s internal `\omit`/`\multispan` also
fails.

## Verification

1. Compile with `pdflatex -interaction=nonstopmode`
2. Check log: `grep "^!" results.log` should return nothing
3. Previously failing multi-panel tables now compile cleanly
4. PDF output should be visually identical

## Notes

- This is a fundamental TeX/LaTeX interaction issue, not specific to any particular package
  or document class
- The `booktabs` package (`\toprule`, `\midrule`, `\bottomrule`) is NOT the cause, though
  it commonly appears in the error context
- The issue affects ANY `\input` inside a tabular where `\multicolumn` is the first token,
  regardless of `\toprule`
- MiKTeX, TeX Live, and other distributions are all affected
- `\let\estinput=\input` does NOT help because it aliases LaTeX's redefined `\input`, not
  the primitive
- In nonstopmode, TeX ignores the error and produces correct output, but the errors halt
  compilation in interactive/scrollmode (the default)

---

# Section D — Assemble a master document from self-compiling block folders

Verified 2026-07-20 assembling seven exhibit blocks (each a self-compiling `results.tex` +
`Tables\` + `Figures\` + block-local `preamble\`) into one `exhibits.tex`. A small script
(`make_master.py`) extracts each block's body and concatenates them under one shared preamble.
Three pitfalls bit in practice; all three fixes below are load-bearing.

## The extraction recipe

For each block, take the text between `\begin{document}` and `\end{document}`, then rewrite
resource paths into the block subfolder. THREE rewrites are required, not two:

```python
body = body.replace("{Tables/",  "{" + block + "/Tables/")
body = body.replace("{Figures/", "{" + block + "/Figures/")
# bare \@@input (hand-rolled tabulars outside the est* macros have no brace before the path)
body = body.replace("\@@input Tables/", "\@@input " + block + "/Tables/")
```

The third line matters because a block that needs text columns often bypasses `\estwide` and
writes `\begin{tabular*}...\@@input Tables/frag.tex...` directly — the path has no preceding
`{`, so the brace-based rewrite misses it and the master fails with "I can't find file".

## Hoist block-local preamble macros

A block's `results.tex` may define macros between `\input{preamble/preamble}` and
`\begin{document}` (e.g. a bespoke table wrapper). Body-only extraction silently drops them and
the master dies with "Undefined control sequence". Capture that pre-document chunk per block
(minus the `\input{preamble/preamble}` line) and emit it into the master before
`\begin{document}`. Block-named macros avoid cross-block collisions.

## The `\captionof` + `longtable` counter double-advance

Symptom: tables number 1, 3, 5... (standalone or in the master). Cause: a longtable wrapper
(`\estautoLT`) used under `\captionof{table}` advances `\c@table` TWICE — `\captionof` steps it
and the `longtable` environment steps it again on its own. Fix inside the wrapper, so exactly
one mechanism advances the counter:

```latex
\newcommand{\estautoLT}[3]{%
  \edef\est@savedtable{\arabic{table}}%   % save before longtable
  \begin{longtable}{l*{#2}{#3}} ... \end{longtable}%
  \setcounter{table}{\est@savedtable}%    % undo longtable's own step
}
```

Apply the patch in EVERY preamble that compiles the content — the block-local one AND the
master's shared copy (the master never reads block preambles, so a fix living only there
silently vanishes when the body is hoisted).

## Parallel-fixer discipline

When several agents fix different blocks concurrently, exactly one process may own the master
(`make_master.py` + its `pdflatex`) — block fixers rebuild only their own folder, and the
orchestrator reassembles once at the end. Two concurrent master compiles race on
`exhibits.aux`/`.pdf` and produce corrupt or interleaved output.
