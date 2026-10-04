---
name: compile-latex
description: Compile a .tex with latexmk and report ranked errors with file:line attribution across \input'd files, plus a diff against the last compile. TRIGGER on "compile this", "build my paper", "build the beamer deck", "why won't this compile", "what are the latex errors", "did my edit add warnings", or any request to build or debug a LaTeX document. TRIGGER also on polishing or debugging a TikZ or pgfplots figure whose labels overlap or that "looks wrong" (the --figures loop). Quarto .qmd decks belong to research-talk and teaching-lecture.
---

# compile-latex

Compile a `.tex`, parse the log into a ranked report with correct `file:line`
attribution, and diff it against the previous build. The default is
compile-and-report only; nothing in the source is edited unless `--figures` is
passed.

Parsing detail (package tables, log regexes, file-stack rules, box thresholds,
state schema) is in [`references/log-patterns.md`](references/log-patterns.md).
Read it before steps 3 through 5. Diff-vs-last-compile is adapted from
`compiledeck` in [scunning1975/MixtapeTools](https://github.com/scunning1975/MixtapeTools).

## Options

| Option | Default | Meaning |
|---|---|---|
| positional path | required | Master `.tex`. Absolute path, or a basename to resolve. |
| `--engine=` | `auto` | Force `pdflatex` / `xelatex` / `lualatex`. |
| `--outdir=` | `build` | Aux directory (`latexmk -outdir`). |
| `--box-threshold=` | `5pt` | Overfull reporting gate. |
| `--figures` | off | Opt-in: run the step-6 review loop on every TikZ/pgfplots figure, then splice back. |
| `--max-iter=` | 5 | Rounds per figure in the `--figures` loop. |
| `--goal=` | from caption | What a figure should communicate. Passed to the reviewer verbatim. |
| `--output=` | `$RUN/final.tex` | Where an approved standalone figure lands when there is no master to splice into. |
| `--no-bib` | off | Skip the bib run (`-bibtex-`). |
| `--force` | off | Compile even if a conflicted copy is present. |
| `--clean` / `--clean-all` | off | `latexmk -c` / `-C`, then stop. |

## Resolving the file

No config file. In order: use an absolute or cwd-relative path if given;
otherwise `Glob` `~/Library/CloudStorage/Dropbox*/Apps/Overleaf/*/**/<name>.tex` and, if a
project name was mentioned, filter to that project directory; otherwise `Glob`
`*.tex` in the cwd and pick the one with `\documentclass`. Ask only if that
leaves zero or several plausible masters.

A `.tikz` path, or an inline TikZ block pasted into the request, has no master to
compile. Take it as `--figures` on that one block: skip steps 1 through 5 and go
to step 6 with the block as the single unit, wrapped as step 6 describes. There
is nothing to splice back, so the approved source goes to `--output` (default
`$RUN/final.tex`) and the path is reported.

## Step 0, pre-flight

1. `Read` the master.
2. Conflicted-copy guard. This setup assumes these projects sync through
   Dropbox (adjust to your machine), so compiling
   next to a stale sibling means reporting errors the user already fixed
   elsewhere. `Glob` the project directory recursively for `*conflicted copy*`
   (`.tex`, `.bib`, `.sty`, `.cls`). If any exist, stop and list them with
   mtimes so the user can resolve the conflict. `--force` overrides.
3. `--clean` / `--clean-all`: run `latexmk -c -outdir=<outdir> <file>` or
   `latexmk -C -outdir=<outdir> <file>` and stop.
4. `latexmk` is at `/Library/TeX/texbin/latexmk` on a MacTeX install. If it is
   missing from `PATH`,
   prepend `/Library/TeX/texbin` before failing with `SETUP_MISSING:latexmk`.
   With `--figures`, also check `gs` (e.g. `/usr/local/bin/gs`); if absent, report
   `SETUP_MISSING:gs` and skip the figure pass, keeping the compile report.

## Step 1, detect engine and bib backend

Read the preamble plus any `\input`'d preamble file (§6 of the reference).
A `% !TEX program =` magic comment wins. Otherwise `fontspec` / `unicode-math` /
`\setmainfont` / `xeCJK` / `ctex` implies xelatex; `\directlua` / `luacode`
implies lualatex; else pdflatex. `--engine=` overrides both.

Bib backend, unless `--no-bib`: `biblatex` or `\addbibresource` means biber;
`natbib` plus `\bibliographystyle` means bibtex. Warn on a mismatch (biblatex
loaded with a leftover `\bibliographystyle`, or `\addbibresource` with no
biblatex).

Print the detection before compiling:

```
File:   <path>
Engine: xelatex  (\setmainfont in preamble)
Bib:    biber    (\addbibresource)
Outdir: build/
```

## Step 2, compile

```bash
latexmk -f "$ENGINE_FLAG" -interaction=nonstopmode -synctex=1 -outdir=<outdir> <file>
```

`ENGINE_FLAG` comes from the step-1 detection: `-pdf` (pdflatex), `-pdfxe`
(xelatex), `-pdflua` (lualatex).
`-f` matters: without it latexmk stops at the first failing pass, so the log
holds one error instead of all of them. Never pass `-halt-on-error`. Add
`-bibtex-` for `--no-bib`. A nonzero exit code is expected on a failed document
and is not a tooling failure; parse the log regardless.

## Step 3, parse the log

Read `<outdir>/<jobname>.log` and run the file-stack tracker from §3 so every
`file:line` lands on the right `\input`'d sub-file rather than the master. The
tracker must push a placeholder for non-path `(` as well, otherwise the parens
inside ordinary messages (`Overfull \hbox (15.83003pt too wide)`) pop real files
off the stack and every subsequent attribution is wrong.

Extract blocking errors (`! ...` plus the following `l.<N>`), undefined
refs/cites (§4), and boxes (§5).

## Step 4, rank and report

Lead with one verdict line, `BUILD OK` / `BUILD OK (with warnings)` /
`BUILD FAILED (N blocking)`, and the PDF path. Then, in this fixed order:

1. Blocking errors. `<file>:<line>` plus the `! ...` message. For
   `Undefined control sequence`, look the token up in §1 and suggest the
   `\usepackage`. For `Environment X undefined`, use the environment table in
   §1. For a missing `.sty`, print the `tlmgr` line from §2 for the user to run
   (MacTeX's tree is root-owned, so it needs `sudo`; never run it unprompted).
   Collapse cascades per §1: one undefined environment produces two or three
   downstream errors that vanish once the root cause is fixed.
2. Undefined refs and cites, split into two lists, keys with input lines. Only
   report what survives the final pass (§4).
3. Boxes, gated: overfull above `--box-threshold`, underfull at badness >= 5000.
   Worst 10 sorted by severity, then `+K more`.

Below-threshold and font/rerun-check noise is dropped silently.

## Step 5, diff vs last compile

State lives at `~/.claude/state/compile-latex/<hash>/last.json`, where `<hash>`
is `sha1(abspath)[:12]`. Load it, diff the new ref/cite/box sets, and report
deltas (`+2 overfull, -1 undefined ref since last compile`). Box identity is
`file:lines:kind`, not the pt value, so a reflow of the same box is not counted
as new. Write the new state atomically (tmp file plus rename); the Write tool
creates missing parent directories, but a Bash-side write needs a `mkdir -p`
first, since `~/.claude/state/` may not exist yet. With no baseline,
note `first compile (no baseline)` and just write. Schema in §8.

## Step 6, figures (opt-in, `--figures` only)

Runs only under `--figures`, and only when the build was clean and figures
exist. Extract, compile, render, review, apply, repeat, until the `tikz-reviewer`
agent answers `APPROVED` or `--max-iter` rounds are gone. The agent does the
visual judgment and it judges from pixels, never from reading source. Loop
concept borrowed from Scott Cunningham's `/tikz` collision audit in
[MixtapeTools](https://github.com/scunning1975/MixtapeTools).

### 6.1 Extract

`Grep` the master and its `\input`'d files for `\begin{tikzpicture}` and pgfplots
`\begin{axis}` / `\begin{groupplot}` blocks (§7). Treat the outermost
`tikzpicture` as the unit. For each block, record the file, the exact body text,
and `sha1(body)`.

Harvest the parent preamble's `\usepackage` / `\usetikzlibrary` /
`\usepgfplotslibrary` / `\pgfplotsset` / `\definecolor` / `\colorlet` /
`\newcommand` / `\def` / `\tikzset` lines into a `standalone` wrapper, so colors
and macros resolve and the crop is the drawing rather than a page:

```tex
\documentclass[tikz,border=4pt]{standalone}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning,calc,decorations.pathreplacing,shapes.geometric}
\usepackage{amsmath,amssymb}
% --- harvested preamble lines here ---
\begin{document}
% --- the captured block here ---
\end{document}
```

A block that has to stay in place (a figure that `\input`s a shared preamble)
compiles where it lives with the build diverted by `-outdir`. Record which case
each block is, since it sets the render DPI.

### 6.2 Compile the figure

Every round of every figure gets its own directory, so nothing is clobbered and
the history stays inspectable if the loop stalls. That also keeps `.aux` churn
out of the user's project tree and out of Dropbox sync.

```bash
export PATH="/Library/TeX/texbin:$HOME/.local/bin:$PATH"
RUN="$HOME/.claude/state/compile-latex/figures/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$RUN/fig-01/iter-01"   # and iter-NN at the top of every later round
cd "$RUN/fig-01/iter-NN" && latexmk -pdf -interaction=nonstopmode -halt-on-error diagram.tex
```

`-halt-on-error` is right here and wrong in step 2. A figure that will not build
has one error worth reading and the next round needs it now, whereas the whole
document wants every error at once. On a non-zero exit, pull the message:

```bash
grep -A2 '^! ' diagram.log | head -3
```

The `l.<N>` line follows the bang line. Do not add `-m1`: BSD grep stops reading
at the match and drops the trailing context, so you get the message with no line
number. Report `COMPILE_FAILED:<line>:<message>` for that figure and move to the
next one. If the log names a missing `.sty`, retry once with `tectonic -X compile
diagram.tex --outdir <dir>`, which fetches it; the outdir must already exist.
Never render a stale PDF from the previous round.

### 6.3 Render to PNG

```bash
gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=png16m -r200 \
   -dTextAlphaBits=4 -dGraphicsAlphaBits=4 \
   -sOutputFile=page-%d.png diagram.pdf
```

The `%d` writes one PNG per page. The alpha-bits flags are anti-aliasing; without
them thin rules and small type alias badly and the reviewer reports artifacts as
real defects. On a full document, review only the page carrying the figure.

Pick DPI from the canvas. `-r200` suits a full page (a Beamer frame lands near
1000px wide) and `-r300` a dense one, but a cropped `standalone` PDF is often two
inches across, where `-r200` yields about 390px and millimetre clearances become
unjudgeable. Start those at `-r600`, then confirm:

```bash
long=$(sips -g pixelWidth -g pixelHeight page-1.png | awk '/pixel(Width|Height)/{print $2}' | sort -rn | head -1)
```

Under 700, re-render at double the DPI; over 2400, halve it. Correct once, do not
loop. If `gs` exits non-zero or the PNG is missing or empty, surface
`RENDER_FAILED:<message>` for that figure and move on. Ghostscript is the
rasterizer here. This setup assumes no Homebrew and no poppler, so `pdftoppm`
and `pdftotext` do not exist and nothing should reach for them; adjust to your
machine.

### 6.4 Review

Launch the `tikz-reviewer` agent (`subagent_type: "tikz-reviewer"`) with
absolute paths: the PNG, the
current `.tex`, the round number against `--max-iter`, and the goal from `--goal`
or the figure's `\caption`. Tell it to read the PNG and judge from the pixels.

Its output contract is in `~/.claude/agents/tikz-reviewer.md`: either
the bare word `APPROVED`, or a numbered list of severity-tagged findings each
carrying its arithmetic and an exact search-and-replace. It already knows this,
so do not restate the contract in the prompt.

### 6.5 Apply or finish

On `APPROVED`, go to 6.6. Otherwise apply each numbered item with `Edit`, using
the exact `old_string` / `new_string` given. Surgical replacements only; never
regenerate the block. Copy the edited file into the next round's directory and
return to 6.2.

Before applying, diff the list against the previous round's. A verbatim repeat
means the loop is oscillating between two fixes, so stop early and report that
instead of burning the remaining rounds. A reply that is neither `APPROVED` nor a
parseable list earns one re-prompt ("Please respond in the required format"); on
a second drift, stop and surface the raw reply.

At `--max-iter` without approval, surface the last PNG, the outstanding
objections, and the in-progress source, and leave that block unspliced.

With several figures, launch every reviewer for the current round in one message,
then advance each figure to its next round as its own reviewer returns; do not
hold a figure for the others. A figure that approves drops out of later rounds.

### 6.6 Splice back and rebuild

Splice only on a verified anchor. Re-`Read` the source file, confirm the captured
body still appears exactly once and its `sha1` is unchanged, then `Edit` with that
body as `old_string`. If it is missing, appears more than once, or the hash moved,
skip it and report `not spliced (source changed)`. Strip the wrapper first; keep
the surrounding `figure` env, `\caption`, `\label`, `\centering`, and any
`\resizebox` / `\adjustbox`.

Recompile once. Report which blocks changed and what each round fixed, and for
every block that did not finish, the round it reached and why it stopped. To
inspect the compiled document's text, run
`~/.claude/assets/bin/pdfread.py text <outdir>/<jobname>.pdf`. This setup assumes
the Read tool cannot open a PDF (no `pdftoppm`; adjust to your machine).

## Step 7, cleanup

Aux files stay in `<outdir>/`. Mention `--clean` / `--clean-all` as the way to
wipe them; leave the PDF. For a live rebuild loop tell the user to run
`latexmk -pvc -outdir=<outdir> <file>` themselves.

## Failure modes

| Symptom | Cause | Response |
|---|---|---|
| Conflicted-copy sibling | Dropbox sync conflict | Stop in step 0, list files, offer `--force`. |
| `! ... .sty not found` | Package absent | Check `kpsewhich <file>`, then print the `tlmgr` line (§2). |
| Undefined control sequence | Missing package or user macro | §1 lookup; if it is a project macro, flag a missing `\newcommand` or an un-`\input`'d macro file. |
| Refs undefined, log says `Rerun to get cross-references right` | latexmk did not converge | Re-run once; do not report the refs (§4). |
| Stack depth goes negative | Unbalanced parens in log text | Reset to master, mark the attribution `~approx`. |
| Empty or absent `.log` | latexmk never started | Report the raw latexmk stderr; do not invent errors. |
| Figure will not converge | Hard diagram | Leave that block unspliced, report it, continue. |

## Examples

```
compile-latex main.tex
→ BUILD FAILED (1 blocking)
  sections/results.tex:212  Undefined control sequence \toprule
    fix: \usepackage{booktabs}
→ 1 undefined cite: Smith2020
→ since last compile: +0 boxes
```

```
compile-latex "Algorithmic Pricing Manuscript" --box-threshold=2pt
→ BUILD OK (with warnings) | build/main.pdf
→ 3 overfull >2pt (worst: sections/model.tex:88, 18.4pt) | +1 since last compile
```
