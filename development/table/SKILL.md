---
name: table
description: Called by /plot to upgrade regression and summary tables to top-journal standards.
---

# LaTeX Table Formatting Skill

This skill generates publication-quality regression tables, summary statistics tables, and multi-panel layouts for economics journals. Covers the major table-making tools: `pyfixest` (Python, primary), `esttab/estout` (Stata), `modelsummary/fixest::etable` (R), and `stargazer` (R/Python).

## Step 0: Workflow Interface

When called by `/plot` or another upstream command, this skill accepts a structured context block. **Do not re-ask the user for information already present in the context.**

```
table_type:       table1_descriptive | table2_balance | table3_main | table_robustness | table_heterogeneity
strategy:         DiD | RDD | IV | PanelFE | SC | OLS
model_results:    path to regression output .csv (e.g., tables/table3_main_results.csv)
software:         python | r | stata
cluster_var:      variable name or "none"
fe_list:          e.g., ["unit FE", "time FE"] or []
sample_desc:      e.g., "Firm-year panel, 2000–2015, N=12,450"
project_name:     string
```

When called standalone (not via `/plot`), prompt the user for `table_type`, `strategy`, and `software` before proceeding.

**Software → tool routing (execute only the matching section; skip all others):**

| `software` | Primary tool | Section to execute |
|---|---|---|
| `python` | `pyfixest.etable()` | [Python — pyfixest.etable()](#python--pyfixedetable-primary) |
| `r` | `modelsummary` + `fixest::etable` | [R — modelsummary](#r--modelsummary) / [R — fixest::etable](#r--fixestetable) |
| `stata` | `esttab/estout` | [Stata — esttab/estout](#stata--esttabstout) |

**Routing rules:**
1. Generate code **only** for the `software` specified in the caller context. Do not generate parallel versions in other languages unless the user explicitly requests them.
2. For `software = r`: if the upstream `/code` command used `fixest::feols`, prefer `fixest::etable()` (native, zero conversion); use `modelsummary` when the user needs `.docx` or `.html` output in addition to `.tex`.
3. For `software = python`: `pyfixest` objects (`feols`, `fepois`, `iv2sls`) pass directly to `etable()`. Do not use `statsmodels` or `pystout` unless `pyfixest` is unavailable.
4. For `software = stata`: `reghdfe` → `eststo` → `esttab` is the standard chain. Always call `ssc install estout` check at the top of the do-file.

**Output convention (always dual-format):**

Every table must be saved in two files:
- `tables/tableN_name.tex` — body-only file for `\input{}` in the paper
- `tables/tableN_name.csv` — raw numbers for manual verification

**Table type → template routing:**

| `table_type` | Template | Key Features |
|---|---|---|
| `table1_descriptive` | Descriptive stats | Variable groups, mean/sd/min/max/N, \multicolumn section headers |
| `table2_balance` | Balance test | Pre-treatment filter enforced, normalized diff column, ✅/⚠️ flag |
| `table3_main` | Main regression | Multi-column, FE rows, controls Yes/No, clustered SE note |
| `table_robustness` | Robustness | Panel layout (Panel A/B/C), same dep. var across specs |
| `table_heterogeneity` | Heterogeneity | Subgroup headers, interaction terms, p-value of difference |

## Quick Decision: Which Tool to Use

| Tool | Language | Best For |
|------|----------|----------|
| `pyfixest.etable()` | Python ⚡ | Primary tool; works with feols/fepois/iv2sls from /code |
| `esttab/estout` | Stata | Most flexible; Stata-native workflows |
| `modelsummary` | R | Modern, clean API; many output formats |
| `fixest::etable` | R | Fast tables from `fixest` regressions |
| `stargazer` | R | Classic; widely used in econ |

## Regression Tables

### Stata — esttab/estout

```stata
* Stata — multi-model regression table
ssc install estout

* Run models
eststo clear
eststo m1: reg y x1, robust
eststo m2: reg y x1 x2, robust
eststo m3: reg y x1 x2 x3, robust
eststo m4: reghdfe y x1 x2 x3, absorb(fe_var) cluster(cluster_var)

* Export to LaTeX
esttab m1 m2 m3 m4 using "results.tex", replace ///
    b(3) se(3) ///                          // 3 decimal places
    star(* 0.10 ** 0.05 *** 0.01) ///       // significance stars
    title("Main Results") ///
    mtitles("OLS" "OLS" "OLS" "FE") ///     // column titles
    label ///                                // use variable labels
    keep(x1 x2 x3) ///                      // show only key vars
    order(x1 x2 x3) ///
    stats(N r2 r2_a, fmt(%9.0fc %9.3f %9.3f) ///
          labels("Observations" "R-squared" "Adj. R-squared")) ///
    addnotes("Robust standard errors in parentheses." ///
             "*** p<0.01, ** p<0.05, * p<0.1") ///
    booktabs ///                             // professional formatting
    fragment                                 // no \begin{table} wrapper

* --- CSV dual-output (always run alongside LaTeX export) ---
* Export coefficient table as CSV for manual verification
esttab m1 m2 m3 m4 using "tables/table3_main_results.csv", replace ///
    b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    csv plain noobs

* Multi-panel table
esttab m1 m2 using "panel_a.tex", replace booktabs fragment ///
    prehead("\begin{table}[htbp]" "\centering" "\caption{Results}" ///
            "\begin{tabular}{lcc}" "\toprule" ///
            "& \multicolumn{2}{c}{\textit{Panel A: Full Sample}} \\" ///
            "\cmidrule(lr){2-3}")
esttab m3 m4 using "panel_b.tex", replace booktabs fragment ///
    prehead("\midrule" ///
            "& \multicolumn{2}{c}{\textit{Panel B: Subsample}} \\" ///
            "\cmidrule(lr){2-3}") ///
    postfoot("\bottomrule" "\end{tabular}" ///
             "\begin{tablenotes}" "\small" ///
             "\item Standard errors in parentheses." ///
             "\end{tablenotes}" "\end{table}")
```

### R — modelsummary

> **Workflow note:** `modelsummary` accepts `fixest::feols` objects directly — no conversion needed. If `/code` used `feols`, pass those objects straight into `modelsummary()` or `fixest::etable()`. Prefer `fixest::etable()` for speed; use `modelsummary()` when you need `.docx` or `.html` output alongside `.tex`.

```r
# R — modelsummary (modern, flexible)
library(modelsummary)

m1 <- lm(y ~ x1, data = df)
m2 <- lm(y ~ x1 + x2, data = df)
m3 <- lm(y ~ x1 + x2 + x3, data = df)

# LaTeX output
modelsummary(
  list("(1)" = m1, "(2)" = m2, "(3)" = m3),
  coef_map = c("x1" = "Treatment",
               "x2" = "Control 1",
               "x3" = "Control 2"),
  gof_map = c("nobs", "r.squared", "adj.r.squared"),
  stars = c('*' = .1, '**' = .05, '***' = .01),
  title = "Main Results",
  notes = "Robust standard errors in parentheses.",
  output = "tables/table3_main_results.tex"
)

# --- CSV dual-output ---
modelsummary(
  list("(1)" = m1, "(2)" = m2, "(3)" = m3),
  output = "tables/table3_main_results.csv"   # same call, different extension
)

# Add fixed effects indicators
modelsummary(
  list("(1)" = m1, "(2)" = m2, "(3)" = m3),
  add_rows = tribble(
    ~term,          ~"(1)", ~"(2)", ~"(3)",
    "Year FE",      "No",   "Yes",  "Yes",
    "Industry FE",  "No",   "No",   "Yes"
  ),
  output = "results.tex"
)
```

### R — fixest::etable

```r
# R — etable (fast, built into fixest)
library(fixest)

m1 <- feols(y ~ x1, data = df, vcov = "HC1")
m2 <- feols(y ~ x1 + x2 | year, data = df, vcov = ~cluster_var)
m3 <- feols(y ~ x1 + x2 | year + industry, data = df, vcov = ~cluster_var)

etable(m1, m2, m3,
       tex = TRUE,
       file = "results.tex",
       dict = c(x1 = "Treatment", x2 = "Control"),
       order = c("Treatment", "Control"),
       drop = "Intercept",
       fixef.group = list("Year FE" = "year",
                          "Industry FE" = "industry"),
       style.tex = style.tex("aer"),    # AER journal style
       title = "Main Results",
       notes = "Clustered standard errors in parentheses.")
```

### R — stargazer

```r
# R — stargazer (classic)
library(stargazer)

stargazer(m1, m2, m3,
          type = "latex",
          out = "results.tex",
          title = "Main Results",
          dep.var.labels = "Outcome Variable",
          covariate.labels = c("Treatment", "Control 1", "Control 2"),
          keep = c("x1", "x2", "x3"),
          add.lines = list(
            c("Year FE", "No", "Yes", "Yes"),
            c("Industry FE", "No", "No", "Yes")
          ),
          omit.stat = c("f", "ser"),
          notes = "Robust standard errors in parentheses.",
          notes.align = "l",
          star.cutoffs = c(0.1, 0.05, 0.01))
```

### Python — pyfixest.etable() (Primary)

`pyfixest` is the standard Python estimation tool used by the `/code` command. Its `etable()` function produces booktabs-ready LaTeX and a tidy DataFrame simultaneously, enabling dual-format output with no extra work.

```python
# Python — pyfixest regression table (primary workflow)
import pyfixest as pf
import pandas as pd
from pathlib import Path

TABLES_DIR = Path("tables")
TABLES_DIR.mkdir(exist_ok=True)

# Run models (mirrors /code output)
m1 = pf.feols("y ~ x1", data=df, vcov="HC3")
m2 = pf.feols("y ~ x1 + x2 | unit_id", data=df, vcov={"CRV1": "unit_id"})
m3 = pf.feols("y ~ x1 + x2 | unit_id + year", data=df, vcov={"CRV1": "unit_id"})
m4 = pf.feols("y ~ x1 + x2 | unit_id + year", data=df,
               vcov={"CRV1": "unit_id^year"})  # double-clustered

# --- LaTeX output (.tex) ---
etable_tex = pf.etable(
    [m1, m2, m3, m4],
    digits=3,
    stars=True,                        # *** 0.01, ** 0.05, * 0.10
    coef_fmt="b (se)",                 # coefficient with SE below
    dict={                             # rename variables
        "x1": "Treatment",
        "x2": "Log Income",
        "Intercept": "",               # hide intercept label
    },
    keep=["Treatment", "Log Income"],  # show only key vars
    drop_intercept=True,
    tex=True,
    # Fixed effects and controls indicators added manually below
)

# Add FE / controls indicator rows
fe_block = r"""
\midrule
Unit FE          & No  & Yes & Yes & Yes \\
Year FE          & No  & No  & Yes & Yes \\
Controls         & No  & No  & No  & Yes \\
"""

# Inject FE block before \bottomrule, then wrap in full table environment
def build_table_tex(etable_str, fe_block, caption, label, notes):
    """Wrap pyfixest etable fragment in a complete booktabs table."""
    # etable(tex=True) returns a tabular fragment; inject FE rows + wrap
    body = etable_str.replace(r"\bottomrule", fe_block + r"\bottomrule")
    return (
        r"\begin{table}[htbp]" + "\n"
        r"\centering" + "\n"
        rf"\caption{{{caption}}}" + "\n"
        rf"\label{{{label}}}" + "\n"
        + body + "\n"
        r"\begin{tablenotes}[flushleft]\footnotesize" + "\n"
        rf"\item \textit{{Notes:}} {notes}" + "\n"
        r"\end{tablenotes}" + "\n"
        r"\end{table}"
    )

notes_str = (
    "Robust standard errors in parentheses, clustered at the unit level "
    "(columns 2--4). All regressions include the controls listed in row "
    "\\textit{Controls}. Sample: {sample_desc}. "
    "*** p$<$0.01, ** p$<$0.05, * p$<$0.10."
)

full_tex = build_table_tex(
    etable_tex, fe_block,
    caption="Main Results: Effect of Treatment on Outcome",
    label="tab:main",
    notes=notes_str
)

tex_path = TABLES_DIR / "table3_main_results.tex"
tex_path.write_text(full_tex)
print(f"Saved: {tex_path}")

# --- CSV output (.csv) — always save for verification ---
coef_df = pf.etable([m1, m2, m3, m4], digits=3, type="df")
csv_path = TABLES_DIR / "table3_main_results.csv"
coef_df.to_csv(csv_path, index=False)
print(f"Saved: {csv_path}")
```

**FE indicator pattern:** Always add fixed-effects and controls indicator rows manually after `etable()` — `pyfixest` does not auto-generate these rows. The `fe_block` pattern above is the standard template.

**IV / 2SLS tables with pyfixest:**

```python
# First stage + Second stage in one table
first  = pf.feols("d ~ z + x1 | unit_id + year", data=df, vcov={"CRV1": "unit_id"})
second = pf.feols("y ~ 1 | unit_id + year | d ~ z", data=df, vcov={"CRV1": "unit_id"})
reduced = pf.feols("y ~ z + x1 | unit_id + year", data=df, vcov={"CRV1": "unit_id"})

iv_tex = pf.etable([first, second, reduced], digits=3,
                   dict={"d": "Treatment (D)", "z": "Instrument (Z)",
                         "fit_d": "Treatment (D) — IV"},
                   tex=True)
# Add first-stage F-stat row manually:
fstat = first.F_stat()  # pyfixest attribute
iv_tex = iv_tex.replace(
    r"\bottomrule",
    rf"First-stage F & {fstat:.1f} & & \\" + "\n" + r"\bottomrule"
)

## Journal-Specific Styles

### AER (American Economic Review)

```r
# fixest style
etable(m1, m2, m3, style.tex = style.tex("aer"), tex = TRUE)
```

Key conventions: booktabs rules, no vertical lines, significance noted in footnote not with stars (AER discourages stars).

### QJE / ReStud / Econometrica

```stata
* Stata — clean academic style
esttab m1 m2 m3 using "results.tex", replace ///
    b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    booktabs fragment ///
    alignment(D{.}{.}{-1}) ///
    prehead("\begin{table}[htbp]" "\centering" ///
            "\caption{Title Here}\label{tab:main}" ///
            "\begin{tabular}{l*{3}{D{.}{.}{-1}}}" "\toprule") ///
    postfoot("\bottomrule" "\end{tabular}" ///
             "\begin{tablenotes}[flushleft]\footnotesize" ///
             "\item \textit{Notes:} Standard errors in parentheses." ///
             " *** p$<$0.01, ** p$<$0.05, * p$<$0.1" ///
             "\end{tablenotes}" "\end{table}")
```

## Multi-Panel and Complex Layouts

### Side-by-Side Panels

```stata
* Panel A: OLS, Panel B: IV
esttab m_ols1 m_ols2 using "table.tex", replace booktabs fragment ///
    prehead("\begin{table}[htbp]\centering" ///
            "\caption{OLS and IV Estimates}" ///
            "\begin{tabular}{lcc}\toprule" ///
            "& \multicolumn{2}{c}{\textit{Panel A: OLS}} \\" ///
            "\cmidrule(lr){2-3}")
esttab m_iv1 m_iv2 using "table.tex", append booktabs fragment ///
    prehead("\midrule" ///
            "& \multicolumn{2}{c}{\textit{Panel B: IV/2SLS}} \\" ///
            "\cmidrule(lr){2-3}") ///
    postfoot("\bottomrule\end{tabular}\end{table}")
```

### Interaction Effects Table

```r
# R — interaction table
library(modelsummary)
m_interaction <- lm(y ~ x1 * group, data = df)
modelsummary(m_interaction,
             coef_rename = c("x1" = "Treatment",
                             "group" = "Group",
                             "x1:group" = "Treatment × Group"),
             output = "interaction.tex")
```

## Tips for Clean Tables

| Tip | Details |
|-----|---------|
| Use `booktabs` | `\toprule`, `\midrule`, `\bottomrule` instead of `\hline` |
| No vertical lines | Standard in economics journals |
| Align decimals | Use `dcolumn` package with `D{.}{.}{-1}` column type |
| Stars in notes | Clearly state significance levels in table notes |
| Variable labels | Use descriptive names, not variable codes |
| Fixed effects rows | Show Yes/No indicators for FE inclusions |
| Consistent decimals | 3 decimals for coefficients/SE; 0 for N |
| Notes placement | Below the table, left-aligned, smaller font |

## Standardized Notes Format

Every table **must** include a Notes line below the bottom rule. Notes are not optional — journals reject tables without them. Use this template, filling in the bracketed fields:

```
Notes: [SE type] in parentheses[, clustered at the [unit] level]. [FE description.]
[Sample description: unit, time period, N.] [Any variable transformation or
winsorization.] *** p<0.01, ** p<0.05, * p<0.1.
```

**Strategy-specific Notes templates:**

| Strategy | Notes Template |
|---|---|
| DiD / TWFE | "Standard errors double-clustered by unit and year in parentheses. Regressions include unit and year fixed effects. Sample: [panel, years, N]." |
| Event Study | "Standard errors clustered at the [unit] level. Reference period: t = −1. Coefficients plot relative effects; pre-period joint test p-value = [p]." |
| RDD | "Bias-corrected robust standard errors (rdrobust) in parentheses. Bandwidth h = [h] selected by MSE-optimal selector. Local linear polynomial." |
| IV / 2SLS | "Two-stage least squares. Standard errors clustered at the [unit] level. First-stage F-statistic = [F] (Stock-Yogo weak instrument critical value 10% = 16.38)." |
| Panel FE | "Standard errors clustered at the [unit] level. Hausman test p-value = [p] (favors FE over RE). Regressions include [FE list]." |
| OLS | "Heteroskedasticity-robust standard errors (HC3) in parentheses." |

**LaTeX Notes implementation:**

```latex
% Recommended: threeparttable + tablenotes (renders correctly in all TeX distributions)
\usepackage{threeparttable}

\begin{table}[htbp]
\centering
\caption{...}
\begin{threeparttable}
\begin{tabular}{...}
...
\end{tabular}
\begin{tablenotes}[flushleft]
\footnotesize
\item \textit{Notes:} Standard errors double-clustered by firm and year in
parentheses. Regressions include firm and year fixed effects. Sample covers
manufacturing firms, 2000--2015 ($N = 12{,}450$ firm-year observations).
Revenue is winsorized at the 1st and 99th percentiles.
*** $p<0.01$, ** $p<0.05$, * $p<0.1$.
\end{tablenotes}
\end{threeparttable}
\end{table}
```

**Avoid:** bare `\footnote{}` for table notes (misplaces the note); `tabular` note rows (breaks alignment); notes that only say "Standard errors in parentheses" with no clustering or FE information.

## Common Pitfalls

- **Too many decimals**: 3 is standard for coefficients; more is noise
- **Missing clustering info**: Always state what SE are clustered on
- **Forgetting FE indicators**: Reviewers need to know which FE are included
- **Stars without notes**: Always define significance levels
- **Cramming too many models**: 4–6 columns is typical maximum
- **No CSV dual-output**: Always save `.csv` alongside `.tex` for verification

## LaTeX Integration: Paper-Ready Output

When the output will be `\input{}`-ed into a compiled paper (rather than compiled standalone), three things consistently cause failures. Address them upfront.

### 1. Body-Only Files — No Document Wrapper

Tools like `esttab`, `stargazer`, and manual Python scripts often emit a standalone `.tex` file with `\documentclass...\begin{document}...\end{document}`. This breaks `\input{}` in the parent paper because LaTeX cannot nest document environments.

Always generate two versions: the full standalone file for spot-checking, and a **body-only** file stripped of the document wrapper for inclusion in the paper.

```python
# Python — strip wrapper and save body-only file
import re

def save_body_only(tex_path):
    """Strip \documentclass...\\end{document} wrapper; keep only the table content."""
    with open(tex_path) as f:
        txt = f.read()
    m = re.search(r'\\begin\{document\}(.*?)\\end\{document\}', txt, re.DOTALL)
    body = m.group(1).strip() if m else txt
    body_path = tex_path.replace('.tex', '_body.tex')
    with open(body_path, 'w') as f:
        f.write(body)
    return body_path
```

In the parent paper, include as:
```latex
\input{tables/table2_main_results_body}   % no .tex extension needed
```

Make sure each body file contains the full `\begin{table}...\end{table}` block — not just the `\begin{tabular}` fragment. A missing `\begin{table}` wrapper causes `\multicolumn` and `\caption` errors at compile time.

### 2. Avoid siunitx by Default

The `siunitx` package (used for the `S` decimal-aligned column type) is absent in many TeX distributions and causes `! LaTeX Error: File 'siunitx.sty' not found`. Prefer standard column types:

```latex
% Instead of: \begin{tabular}{l S S S}   (requires siunitx)
% Use:        \begin{tabular}{l c c c}    (always works)

% For strict decimal alignment without siunitx, use the dcolumn package:
\usepackage{dcolumn}                       % ships with every standard TeX distro
\begin{tabular}{l D{.}{.}{-1} D{.}{.}{-1}}
```

For most robustness and heterogeneity tables, `c` columns are sufficient — the numbers are clearly readable without strict decimal alignment.

Also avoid Unicode characters in Python-generated `.tex` files. Characters like `>=`, `->`, `<=` typed directly will break LaTeX. Always use their LaTeX equivalents: `$\geq$`, `$\rightarrow$`, `$\leq$`.

### 3. Overflow Prevention for Wide Tables

A table with 6 or more columns, or with a text description column, will almost certainly overflow the page width in portrait mode. Apply these fixes together:

```latex
% Rule: >=6 columns → wrap in landscape; text description column → use p{Xcm} not l

\usepackage{pdflscape}    % add to preamble

% In the body file:
\begin{landscape}
\begin{table}[ht]
\centering
\caption{...}
\begin{threeparttable}
{\footnotesize\setlength{\tabcolsep}{4pt}     % shrink font + column padding
\begin{tabular}{p{4.5cm} c c c c c c}         % p{} for text col, c for data cols
...
\end{tabular}}
\begin{tablenotes}[flushleft]\small
\item \textit{Notes}: ...
\end{tablenotes}
\end{threeparttable}
\end{table}
\end{landscape}
```

**Quick reference for portrait mode** (1.25in margins, ~16.5cm text width):

| Columns | First column | Approach |
|---------|-------------|----------|
| 3-4 | `l` | Portrait, no special treatment needed |
| 5-6 | `p{4.5cm}` + `{\footnotesize\setlength{\tabcolsep}{4pt}}` | Portrait, tight |
| 7+ | `p{Xcm}` + `\footnotesize` | Landscape always |

Keep `\begin{tablenotes}` text concise — a long inline math expression that cannot line-break (e.g., a full regression formula) will produce an `Overfull \hbox` even when the table itself fits. Summarize the spec in plain language in the note and put the equation in the methods section instead.
