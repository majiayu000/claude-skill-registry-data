---
name: paper-writing
description: Draft economics papers with proper structure and academic style
---

# Paper Writing Skill

## Role in Workflow

**This skill is the authoritative LaTeX template library and writing convention reference for the econometrics plugin.** It is designed to be called by the `/write` command (Phase 9) rather than invoked independently.

**Division of labor with `/write` command:**

| Responsibility | Owner |
|---------------|-------|
| Read upstream files (model-spec.md, results-memo.md, etc.) | `/write` command |
| Extract research context and build writing brief | `/write` command |
| Confirm writing scope, language, and target journal with user | `/write` command |
| Provide section-by-section content rules tied to upstream data | `/write` command |
| Provide LaTeX templates (preamble, section skeletons) | **This skill** |
| Provide causal language calibration rules | **This skill** |
| Provide writing conventions, common pitfalls, compile workflow | **This skill** |
| Assemble paper.tex, compile to PDF, export DOCX | `/write` command |

---

## Narrative Writing Principles

**An empirical economics paper is a causal story.** Every section must advance the narrative; no section should be a standalone island of results.

### The Narrative Arc

```
Introduction  →  Literature  →  Data  →  Strategy  →  Results
     ↑                                                    ↓
 (question)                                          (answer)
     ↑                                                    ↓
Conclusion  ←  Discussion  ←  Mechanisms  ←  Robustness
  (so what)                                    (credibility)
```

**Each section must:**
1. **Open** with one sentence bridging from the previous section
2. **Close** with one sentence previewing the next section (except Conclusion)

### Figure and Table Integration Rule

Every figure or table reference in the text must accomplish three things in the same paragraph:

| Step | What to do | Example |
|------|-----------|---------|
| **① Preview** | Tell the reader what they're about to see | *"Table 2 presents estimates of equation (1)."* |
| **② Extract** | Give the key number from the table/figure | *"The coefficient on D is 0.12 (s.e. = 0.04)..."* |
| **③ Interpret** | State what this means for the narrative | *"...implying a 15% increase relative to the mean."* |

**Never write**: "See Table X." or "Figure Y presents the results." without extracting and interpreting the number.

### Main Text vs. Appendix — Placement Decision

**Keep in main text** (direct support for the main causal story):
- Summary statistics table (Table 1)
- Main regression table (Table 2)
- Core identification figure (event study, RDD binscatter, IV first-stage)
- Primary heterogeneity table (if it is a core contribution)

**Move to appendix** (supporting/supplementary material):
- Full robustness table (multiple specification columns)
- Balance/pre-treatment tests (DiD, IV)
- Variable definitions table
- Additional heterogeneity subgroups
- Sample construction flowchart
- Supplementary mechanism figures

When referencing appendix items in the main text, use: *"Appendix Table A1 reports..."* or *"(see Appendix Figure A1)"*.

---

## LaTeX Preamble (Authoritative)

This is the canonical preamble for economics journal submissions. The `/write` command uses this directly — there is no separate preamble in the command file.

```latex
\documentclass[12pt]{article}
\usepackage{amsmath,amssymb}
\usepackage[margin=1.25in]{geometry}
\usepackage{setspace}
\usepackage{booktabs,caption,threeparttable,makecell}
\usepackage{pdflscape}         % landscape pages for wide tables (\begin{landscape})
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{natbib}
\usepackage[title,titletoc]{appendix}  % appendix environment with lettered sections
\usepackage{subcaption}
% \usepackage{microtype}   % enable if TeX distribution supports it

\setstretch{1.5}           % 1.5x body spacing -- standard for journal submissions
\captionsetup{labelfont=bf, labelsep=period, font=small}
\hypersetup{colorlinks=true, linkcolor=black, citecolor=black, urlcolor=blue}
\graphicspath{{../figures/}}   % relative to paper/ -- one level up to reach figures/
\bibliographystyle{aer}        % AER author-year; use chicago for other journals
```

### Front Matter (First Page)

The global `\setstretch{1.5}` inflates the title block unless overridden. Wrap front matter in `\begin{spacing}{1.0}`.

```latex
\begin{document}

\thispagestyle{empty}
\begin{spacing}{1.0}
\begin{center}
  {\large\bfseries [PAPER TITLE]}\par
  \vspace{0.7em}
  {\normalsize\bfseries [AUTHOR NAME]}\par
  {\small\textit{[AFFILIATION]} \quad \href{mailto:[EMAIL]}{[EMAIL]}}\par
  {\small [MONTH YEAR]}\par
\end{center}
\vspace{0.5em}
\input{sections/abstract}
\vspace{0.4em}
\noindent\textbf{JEL Codes:} [J23, J31, O33]
\quad\textbf{Keywords:} [keyword1, keyword2, keyword3]
\vspace{0.3em}
\noindent\footnotesize\textit{I thank [acknowledgements]. All errors are my own.}
\normalsize
\end{spacing}
\clearpage

% NO \tableofcontents -- not standard in economics journal submissions

\input{sections/introduction}
\input{sections/literature}
\input{sections/data}
\input{sections/strategy}
\input{sections/results}
\input{sections/robustness}
\input{sections/heterogeneity}
\input{sections/discussion}
\input{sections/conclusion}

\bibliography{references}

% ── Appendix ─────────────────────────────────────────────────────────────────
\begin{appendices}

% Reset counters for appendix tables and figures
\renewcommand{\thetable}{A\arabic{table}}
\renewcommand{\thefigure}{A\arabic{figure}}
\setcounter{table}{0}
\setcounter{figure}{0}

\input{sections/appendix}   % contains all supplementary tables and figures

\end{appendices}

\end{document}
```

### Key Front-Matter Conventions

- **No `\titlepage` environment** -- forces abstract to a separate page
- **No `\tableofcontents`** -- not standard in economics submissions
- **`\begin{spacing}{1.0}` for title block** -- prevents 1.5x stretch from inflating spacing
- **`\thispagestyle{empty}`** -- suppresses page number on cover page
- **Title font: `\large\bfseries`** -- `\LARGE` combined with 1.5x stretch uses too much vertical space
- **`\citet{}` vs `\citep{}`**: use `\citet{Author2020}` for "Author (2020) show that..." and `\citep{Author2020}` for parenthetical "(Author 2020)"

---

## Causal Language Calibration

**This table governs language intensity across ALL sections.** The causal language level is determined by `/write` from `results-memo.md §4` and passed to this skill. Apply consistently throughout the paper -- do not mix levels within a single draft.

| Identification credibility | Assumption framing | Verb choices |
|---------------------------|--------------------|--------------|
| **High** -- all key assumptions pass empirical tests | "The causal effect of D on Y..." | "causes", "increases", "reduces", "leads to" |
| **Medium** -- some assumptions not fully testable or show mild violations | "The effect of D on Y, as estimated by [strategy]..." | "is associated with", "predicts", "is related to" |
| **Low** -- identification assumptions not plausibly satisfied | "We document a correlation between D and Y..." | "is correlated with", "co-moves with", "we observe" |

**Cross-section enforcement**: once the level is set, apply it uniformly in the Abstract, Introduction, Results, and Conclusion. The Empirical Strategy section always describes assumptions in the formal/neutral register regardless of the level.

---

## Section Templates

### 1. Abstract

**Format**: 150-200 words, 5-6 sentences, fixed structure.

```latex
\begin{abstract}
\noindent
[RESEARCH QUESTION IN ONE SENTENCE].
Using [DATA SOURCE] covering [N] [UNITS] over [PERIOD],
we exploit [IDENTIFICATION STRATEGY] to identify
the [causal/estimated] effect of [D] on [Y].
We find that [D] [CAUSAL VERB] [Y] by [MAGNITUDE] [UNITS/PERCENT/SD]
([SIGNIFICANCE STATEMENT, e.g., significant at the 1\% level]).
[HETEROGENEITY OR ROBUSTNESS SENTENCE --
"This effect is concentrated among [SUBGROUP] and robust to [CHECKS]."]
Our results [CONTRIBUTION VERB: inform/challenge/extend]
[POLICY/THEORY IMPLICATION].
\end{abstract}
```

**Checklist**:
- Contains the main coefficient magnitude (not just direction)
- Names the identification strategy explicitly
- Causal verb consistent with the calibration table above
- Does NOT merely report statistical significance without magnitude

---

### 2. Introduction

Top-5 journal introductions are typically 4-6 pages (approx. 1,500-2,000 words). Follow the five-paragraph structure.

```latex
\section{Introduction}
\label{sec:introduction}

% -- Paragraph 1: Hook + Research Question + Main Finding (numbers required) --
% Rule: by the end of paragraph 1, the reader must know (1) what question,
% (2) what finding, (3) the magnitude. Never open with "This paper examines..."
[HOOK SENTENCE -- a striking fact, statistic, or policy puzzle].
This paper [provides causal evidence / documents] that [D] [CAUSAL VERB] [Y]:
a [UNIT CHANGE] in [D] [CAUSAL VERB] [Y] by [MAGNITUDE]
([SIGNIFICANCE]; s.e.\ = [SE]).

% -- Paragraph 2: Why is this hard to estimate? (endogeneity threats) --
Estimating the [causal / true] effect of [D] on [Y] is challenging
for [two/three] reasons.
First, [OVB THREAT -- name the omitted variable and its bias direction].
Second, [REVERSE CAUSALITY THREAT].
[Third, [MEASUREMENT ERROR / SELECTION CONCERN].]
Prior work using [OLS / cross-sectional comparisons] is likely to
[overstate/understate] the effect because [DIRECTION AND SOURCE OF BIAS].

% -- Paragraph 3: Identification strategy and data --
We address these challenges by exploiting [SOURCE OF EXOGENOUS VARIATION].
[EXPLAIN WHY THIS VARIATION IS PLAUSIBLY EXOGENOUS -- one to two sentences].
Our data come from [DATA SOURCE], covering [N UNITS] over [PERIOD],
yielding [OBS] observations.

% -- Paragraph 4: Summary of findings (magnitudes + heterogeneity + robustness) --
Our main finding is that [RESTATE MAIN RESULT WITH COEFFICIENT].
[ECONOMIC SIGNIFICANCE -- relative to mean or SD].
[HETEROGENEITY -- one sentence if applicable].
The results are robust to [ROBUSTNESS SUMMARY -- one sentence].

% -- Paragraph 5: Contribution + Roadmap --
% Rule: no more than 3 contribution statements; roadmap no more than 5 sentences.
This paper contributes to [STRAND 1] by [CONTRIBUTION 1].
[It also contributes to [STRAND 2] by [CONTRIBUTION 2].]
Unlike \citet{CLOSEST PAPER}, we [KEY DISTINCTION].
The remainder of the paper proceeds as follows.
Section~\ref{sec:literature} reviews related literature.
Section~\ref{sec:data} describes the data.
Section~\ref{sec:strategy} presents the empirical strategy.
Section~\ref{sec:results} reports main results.
Section~\ref{sec:robustness} presents robustness checks.
Section~\ref{sec:conclusion} concludes.
```

**Introduction prohibitions**:
- "This paper examines..." as the opening sentence
- Reporting significance only, no magnitude
- More than 3 contribution statements
- Roadmap paragraph longer than 5 sentences
- Any equation or technical notation in the introduction

---

### 3. Literature Review

```latex
\section{Related Literature}
\label{sec:literature}

% Organize by research STRAND (thematic), NOT chronologically.
% Typical: 2-4 strands, 1-3 paragraphs each.

% -- Strand 1: Core empirical literature --
This paper builds on [NUMBER] strands of literature.
The first strand examines [BROAD TOPIC].
\citet{Seminal1} and \citet{Seminal2} established [FOUNDATIONAL FINDING].
More recently, \citet{Recent1} show [KEY FINDING] using [DATA/METHOD],
and \citet{Recent2} document [COMPLEMENTARY RESULT] in [CONTEXT].
Unlike these papers, we [KEY DISTINCTION -- method, context, or mechanism].

% -- Strand 2: Identification approach --
The second strand uses [SIMILAR IDENTIFICATION STRATEGY] to study related questions.
\citet{Author3} exploit [INSTRUMENT/EVENT] to identify [EFFECT], finding [RESULT].
Our approach is closest to \citet{Author4}, who [BRIEF DESCRIPTION OF THEIR DESIGN].
We extend their work by [HOW WE DIFFER].

% -- Strand 3: Mechanism or theoretical background (if applicable) --

% -- Explicit contribution positioning --
This paper contributes to these literatures in two ways.
First, [CONTRIBUTION 1: the new empirical evidence you provide].
Second, [CONTRIBUTION 2: new context, method, or mechanism].
```

---

### 4. Data

```latex
\section{Data}
\label{sec:data}

\subsection{Data Sources and Sample Construction}

Our primary data come from [DATA SOURCE], which covers
[UNIT OF OBSERVATION] over the period [START YEAR]--[END YEAR].
[ONE TO TWO SENTENCES describing the data content and collection method].

We construct our analysis sample by [SAMPLE SELECTION STEPS].
We exclude [EXCLUSION CRITERIA AND REASON],
resulting in a final sample of [N] [UNITS] and [OBS] observations.

\subsection{Variable Definitions}

Our main outcome variable is [Y], defined as [PRECISE DEFINITION].
[TREATMENT VARIABLE D] takes value one if [CONDITION] and zero otherwise.
[INSTRUMENT Z] measures [DEFINITION -- for IV papers].
Variable definitions follow [REFERENCE IF STANDARD DEFINITION].

\subsection{Descriptive Statistics}

Table~\ref{tab:sumstats} reports summary statistics for the main analysis sample.
The average [Y] is [MEAN] (standard deviation [SD]).
[D PERCENT]\% of [UNITS] are [TREATED / ABOVE THRESHOLD].
[KEY OBSERVATION ABOUT DATA DISTRIBUTION OR NOTABLE PATTERN].
[IF DiD/IV: Table~\ref{tab:balance} reports pre-treatment balance.
The treatment and control groups are similar on [KEY COVARIATES],
consistent with [PARALLEL TRENDS / EXCLUSION RESTRICTION].]
```

---

### 5. Empirical Strategy

**This section receives the most scrutiny from referees.** Draw directly from `model-spec.md` and `identification-memo.md`; do not re-derive the model.

```latex
\section{Empirical Strategy}
\label{sec:strategy}

\subsection{Baseline Specification}

% Use the equation exactly as specified in model-spec.md Section 2
Our baseline specification is:

\begin{equation}
  [MAIN EQUATION FROM model-spec.md]
  \label{eq:baseline}
\end{equation}

\noindent where $[Y_{it}]$ is [OUTCOME DEFINITION],
$[D_{it}]$ is [TREATMENT DEFINITION],
$\mathbf{X}_{it}$ is a vector of controls including [CONTROL LIST],
$[FE NOTATION]$ are [ENTITY/TIME] fixed effects,
and $\varepsilon_{it}$ is the error term.
$[PARAMETER]$ is the coefficient of interest; it measures
[WHAT THE PARAMETER IDENTIFIES -- ATE/ATT/LATE and the population it applies to].
Standard errors are clustered at the [LEVEL] level to account for
[SERIAL/SPATIAL CORRELATION -- state the economic reason explicitly].

\subsection{Identification}

% State each assumption formally and in plain language.
% Always preview where you test it.
The key identifying assumption is [ASSUMPTION IN PLAIN LANGUAGE].
Formally:

\begin{equation*}
  [FORMAL STATEMENT -- e.g., parallel trends, relevance, exclusion restriction]
\end{equation*}

This assumption would be violated if [SPECIFIC, CONCRETE THREAT].
We provide evidence supporting this assumption in
Section~\ref{sec:robustness}, where we show [BRIEF PREVIEW OF TEST RESULT].

% FOR IV -- add exclusion restriction paragraph:
% The exclusion restriction requires that [Z] affects [Y] only through [D].
% This could be violated if [SPECIFIC VIOLATION SCENARIO].
% We argue this is unlikely because [ECONOMIC ARGUMENT].

% FOR RDD -- add continuity / no-manipulation paragraph
% FOR DiD -- add parallel trends + no-anticipation paragraph
```

---

### 6. Results

```latex
\section{Results}
\label{sec:results}

% Rule: Lead with the number. Never open with "Table X shows our results."

\subsection{Main Results}

[MAIN COEFFICIENT AS FIRST CLAUSE -- e.g., "A one-unit increase in D
[CAUSAL VERB] Y by [VALUE] (s.e.\ = [SE], [SIGNIFICANCE])."]
Table~\ref{tab:main} reports estimates of equation~\eqref{eq:baseline}.
Column~(1) presents the baseline specification without controls.
Adding [CONTROL SET] in column~(2) [leaves the estimate stable at /
reduces it to] [VALUE], [INTERPRETATION OF CHANGE].
Our preferred specification in column~([N]) includes [FULL CONTROLS AND FE]
and yields [FINAL ESTIMATE] ([SE], [SIGNIFICANCE]).

% Economic significance -- mandatory
To assess economic significance, note that the sample mean of [Y] is [MEAN].
Our estimate implies that [D] [CAUSAL VERB] [Y] by
[MAGNITUDE PERCENT]\% relative to the mean,
or approximately [SD-UNITS] standard deviations.
[COMPARISON: This is [larger/comparable/smaller] than
\citet{CLOSEST PAPER}'s estimate of [THEIR VALUE] using [THEIR METHOD].]

% Event study / dynamic effects (DiD papers)
[Figure~\ref{fig:eventstudy} plots event-study coefficients $\hat{\beta}_k$
for $k \in [-K, K]$ relative to the treatment date.
Pre-treatment coefficients are small and indistinguishable from zero
(joint $F$-test: $p = $ [P-VALUE]), supporting parallel trends.
Post-treatment coefficients are [positive/negative] and [growing/stable/declining],
consistent with [INTERPRETATION].]

% IMPORTANT: Tables are always in separate files under tables/
% The paper.tex structure handles \input{../tables/table_main.tex}
% Never write \begin{tabular}...\end{tabular} inline in section files
```

---

### 7. Robustness

```latex
\section{Robustness}
\label{sec:robustness}

% Open with the conclusion, then present evidence
Table~\ref{tab:robustness} presents a battery of robustness checks.
Our main finding is stable: the coefficient on [D] ranges from [MIN] to [MAX]
across all specifications, remaining statistically significant at the
[\%] level in [N of M] cases.

\subsection{Inference Robustness}
[Column~(1) replicates the preferred specification with [ALTERNATIVE SE TYPE].
The coefficient is [VALUE] ([SE]), nearly identical to the baseline.]

\subsection{Sample Robustness}
[Column~(2) excludes [GROUP / OUTLIER CRITERION].
Column~(3) restricts the sample to [SUBSAMPLE].
Estimates range from [MIN] to [MAX], consistent with the baseline.]

\subsection{Specification Robustness}
[Column~([N]) uses [ALTERNATIVE FUNCTIONAL FORM / CONTROL SET / BANDWIDTH].
The coefficient is [VALUE], [MAGNITUDE CHANGE AND INTERPRETATION].]

\subsection{Identification Checks}

% DiD: Pre-trend test
[Figure~\ref{fig:eventstudy} shows no differential pre-trends
(joint $F$-test: $p = $ [P]).]

% DiD/IV: Placebo
[Assigning treatment [one year earlier / to untreated units] yields
$\hat{\beta} = $ [NEAR-ZERO VALUE] ([SE]), confirming our result is not
driven by pre-existing trends.]

% RDD: McCrary density test
[The density of [RUNNING VARIABLE] is continuous at the threshold
($p = $ [P]), ruling out sorting around the cutoff.]

% IV: First-stage strength
[The first-stage $F$-statistic on [Z] is [F], well above the
Stock-Yogo critical value of 10, ruling out weak-instrument concerns.]

% Template for any coefficient that moves materially:
% In column ([N]), [WHAT CHANGES]. The estimate [increases/decreases] to [VALUE],
% reflecting [ECONOMIC REASON]. This does not challenge the main conclusion
% because [ARGUMENT].
```

---

### 8. Heterogeneity and Mechanisms

```latex
\section{Heterogeneity and Mechanisms}
\label{sec:heterogeneity}

\subsection{Heterogeneous Treatment Effects}

% Always: state the theory first, then show the data
[THEORETICAL REASON why heterogeneity is expected along [DIMENSION]].
If [MECHANISM], we would expect the effect to be larger among [SUBGROUP].

Table~\ref{tab:heterogeneity} reports treatment effects by [DIMENSION].
The effect is [X times larger / present only / absent] for [SUBGROUP 1]
(column~([A]): $\hat{\beta} = $ [VALUE], s.e.\ = [SE])
relative to [SUBGROUP 2]
(column~([B]): $\hat{\beta} = $ [VALUE], s.e.\ = [SE]).
[The interaction term is statistically significant ($p = $ [P]).]
[SUBGROUP 1] may respond more because [ECONOMIC REASON].

\subsection{Mechanisms}

% Language intensity follows the causal calibration table:
%   Direct mechanism evidence (externally identified) -> "provides direct evidence for"
%   Suggestive / descriptive test -> "is consistent with"
%   Ruling out alternatives -> "rules out" / "cannot be explained by"

Our results [ARE CONSISTENT WITH / PROVIDE DIRECT EVIDENCE FOR] [MAIN MECHANISM].
[We examine [INTERMEDIATE OUTCOME Z], which should [INCREASE/DECREASE]
if [MECHANISM] is operative.
Table~\ref{tab:mechanisms} shows that [D] [VERB] [Z] by [MAGNITUDE] ([SIGNIFICANCE]),
consistent with [MECHANISM].]

An alternative explanation is [COMPETING MECHANISM].
However, this predicts [TESTABLE IMPLICATION], which we do not observe in [EVIDENCE].
[We therefore rule out / cannot rule out] [ALTERNATIVE].
```

---

### 9. Discussion

```latex
\section{Discussion}
\label{sec:discussion}

\subsection{External Validity}

Our estimates apply most directly to [POPULATION / CONTEXT / TIME PERIOD].
Several factors may limit generalizability.
First, [LIMITATION 1 -- e.g., single country, specific sector].
Whether these findings generalize to [OTHER CONTEXT] is an open question.
Second, [LIMITATION 2 -- e.g., identification relies on a particular event].
Third, [LIMITATION 3 -- data quality, partial compliance, SUTVA].

\subsection{Policy Implications}

Our findings suggest that [POLICY INTERVENTION] could [EFFECT ON OUTCOME].
[BACK-OF-ENVELOPE: scaling up by [FACTOR] implies [AGGREGATE EFFECT].]
Policymakers should be cautious because [CAVEAT --
general equilibrium effects, targeting, political economy, compliance].
```

---

### 10. Conclusion

**Top-5 conclusions: 1-2 pages maximum. Do not introduce new results.**

```latex
\section{Conclusion}
\label{sec:conclusion}

% 6 elements, approx. 6-8 sentences total

% (1) Question + method (1 sentence)
This paper examined [RESEARCH QUESTION] using [IDENTIFICATION STRATEGY]
and [DATA SOURCE].

% (2) Main findings with magnitudes (2-3 sentences)
We find that [D] [CAUSAL VERB] [Y] by [MAGNITUDE] ([SIGNIFICANCE]).
[HETEROGENEITY FINDING IF APPLICABLE].
[MECHANISM FINDING IF APPLICABLE].

% (3) Robustness summary (1 sentence)
These results are robust to [ROBUSTNESS CHECKS SUMMARY].

% (4) Policy / theory implications (2-3 sentences)
For policy, our findings suggest [IMPLICATION].
For theory, they [SUPPORT / CHALLENGE / EXTEND] [THEORETICAL MECHANISM/VIEW].

% (5) Limitations (1-2 sentences)
Our analysis has limitations. [MOST IMPORTANT LIMITATION -- honest but brief].

% (6) Future directions (1-2 sentences)
Future work could [DIRECTION 1 -- natural next step].
[DIRECTION 2 -- broader question opened by this paper].
```

**Conclusion prohibitions**:
- Any result not already presented in the body of the paper
- Section-by-section recap ("In Section 2 we showed...")
- "More research is needed" without specifics
- Exceeding 2 pages

---

## Compile Workflow (Authoritative)

### Step 1 — LaTeX → PDF

Always run **four commands** in this exact sequence. Skipping BibTeX leaves all `\cite{}` commands as `[?]` in the final PDF.

```bash
cd [workspace]/paper/
pdflatex -interaction=nonstopmode paper.tex   # pass 1: build .aux file
bibtex paper                                  # resolve citations -- produces .bbl
pdflatex -interaction=nonstopmode paper.tex   # pass 2: embed bibliography
pdflatex -interaction=nonstopmode paper.tex   # pass 3: fix all cross-references

# Inspect the log
grep -i "overfull\|undefined\|missing\|error" paper.log
grep "Overfull .hbox" paper.log          # >10pt = visible overflow, fix it
grep "File.*not found" paper.log         # missing package
grep "Citation.*undefined" paper.log    # missing .bib entry
```

**Auto-fix for the four most common errors:**

| Error | Cause | Fix |
|-------|-------|-----|
| `File 'siunitx.sty' not found` | Table used `S` columns | Switch to `c` or `D{.}{.}{-1}` (dcolumn) |
| `Unicode character U+XXXX` | Python wrote symbols directly into .tex | Replace with LaTeX macros: `$\geq$`, `$\rightarrow$` |
| `Overfull \hbox (>10pt)` | Table or text overflows margin | Wrap in `\begin{landscape}...\end{landscape}` + `\footnotesize` |
| `Citation 'key' undefined` | Entry missing from references.bib | Add BibTeX entry and rerun bibtex |

### Step 2 — LaTeX → DOCX (via pandoc)

After a successful PDF compile, export DOCX for co-author review and journal submission systems that require Word format.

```bash
cd [workspace]/paper/

# Preferred: pandoc with citeproc (preserves math, citations, cross-refs)
pandoc paper.tex \
  --bibliography=references.bib \
  --citeproc \
  -o paper.docx

# Verify the output exists and has non-trivial size
ls -lh paper.docx
```

If pandoc is not installed:
```bash
# Ubuntu/Debian
apt-get install -y pandoc 2>/dev/null || true
# macOS
brew install pandoc 2>/dev/null || true
# Check version
pandoc --version | head -1
```

Fallback (lower fidelity, no pandoc needed):
```bash
libreoffice --headless --convert-to docx paper.pdf --outdir .
```

**Pandoc known limitations** — inform the user if these apply:
- Complex LaTeX tables may render as plain text in DOCX; the PDF remains the authoritative version
- `\begin{landscape}` pages convert to normal portrait pages in DOCX (landscape formatting is PDF-only)
- `\citet{}`/`\citep{}` resolve correctly only when `--citeproc` and `--bibliography` are passed

### Compile Confirmation

```
─────────────────────────────────────────────────────
✅ pdflatex pass 1-3 + bibtex: no errors
✅ No undefined references
✅ No missing citations
⚠️  Overfull \hbox (2.3pt) — minor, acceptable
✅ DOCX exported via pandoc
─────────────────────────────────────────────────────
Output: paper/paper.pdf  ([N] pages)
        paper/paper.docx
```

---

## Version Management

Every time a draft is created or revised, the `/write` command saves a versioned copy. This skill does not write files directly -- it provides templates; the command handles file output.

```
paper_v1.0_YYYYMMDD.tex   # initial draft
paper_v1.1_YYYYMMDD.tex   # first revision
paper_v2.0_YYYYMMDD.tex   # major rewrite
```

If called in Mode B (standalone) to revise a single section, always confirm: "Should I overwrite the existing file or save as a new version?" Default to saving a new version.

---

## Writing Tips

**Introductions**
- First sentence must contain a substantive claim or striking fact -- never "This paper examines..."
- State the main result with a number by the end of paragraph 1
- Limit contribution statements to 3 or fewer; more signals overselling to reviewers

**Results**
- Lead every results paragraph with the coefficient value, not "Table X shows..."
- Economic significance is mandatory: interpret magnitude relative to mean or SD
- Guide the reader column by column; explain why estimates move across specifications

**Conclusions**
- Synthesize, do not summarize -- add interpretive value, not repetition
- Be honest about limitations; reviewers will find them regardless
- End on the contribution, not a hedge

---

## Landscape Table Template (Wide Regression Tables)

Use this template whenever a table has **more than 5 columns** or produces `Overfull \hbox > 5pt` at standard page width. The table occupies its own portrait-to-landscape page and is placed in a float page (`[p]`).

```latex
% ── Wide regression table on a dedicated landscape page ──────────────────────
\begin{landscape}
\begin{table}[p]
\caption{[Table Title — e.g., Robustness Checks]}
\label{tab:robustness}
\footnotesize                        % slightly smaller font to fit more columns
\begin{threeparttable}
\begin{tabular}{l *{6}{c}}           % 1 label col + 6 numeric cols (adjust as needed)
\toprule
 & (1) & (2) & (3) & (4) & (5) & (6) \\
 & Baseline & Alt. SE & Excl. Outliers & Log Y & Alt. Controls & Preferred \\
\midrule
[D var]   & [β₁]*** & [β₂]*** & [β₃]*** & [β₄]** & [β₅]*** & \textbf{[β₆]***} \\
          & ([SE₁])  & ([SE₂])  & ([SE₃])  & ([SE₄]) & ([SE₅])  & \textbf{([SE₆])} \\
\addlinespace
Controls  & No  & No  & Yes & Yes & Alt & Yes \\
FE        & No  & Yes & Yes & Yes & Yes & Yes \\
$N$       & [N] & [N] & [N] & [N] & [N] & [N] \\
$R^2$     & [r] & [r] & [r] & [r] & [r] & [r] \\
\bottomrule
\end{tabular}
\begin{tablenotes}[flushleft]
\footnotesize
\item \textit{Notes:} [Standard error clustering. Significance: *\,p$<$0.1, **\,p$<$0.05, ***\,p$<$0.01.]
\end{tablenotes}
\end{threeparttable}
\end{table}
\end{landscape}
% ─────────────────────────────────────────────────────────────────────────────
```

**Rules for landscape tables:**
- Always use `[p]` float specifier (dedicated page, no surrounding text)
- Use `\footnotesize` (10pt) inside the table body; `\normalsize` resumes automatically after `\end{landscape}`
- `\begin{landscape}` requires `pdflscape` (already in the authoritative preamble)
- In the main text, reference the table normally: *"Table~\ref{tab:robustness} presents..."*
- DOCX export: landscape formatting is PDF-only; inform the user the DOCX version will show the table in portrait

---

## Appendix Template

```latex
% sections/appendix.tex
% Called via \input{sections/appendix} inside \begin{appendices}...\end{appendices}
% Counter resets (A1, A2, ...) are handled in paper.tex

\section{Additional Robustness Checks}
\label{sec:appendix_robustness}

[Brief narrative sentence explaining what each appendix table shows and why
it belongs in the appendix rather than the main text.]

% Wide robustness table — also use landscape here if > 5 cols
\input{../tables/table_robustness_appendix}

\section{Pre-Treatment Balance}
\label{sec:appendix_balance}

Table~\ref{tab:balance} reports balance statistics for the treatment and control groups
prior to the policy change. [One sentence summarizing the balance result.]

\input{../tables/table_balance}

\section{Variable Definitions}
\label{sec:appendix_variables}

\input{../tables/table_variable_definitions}

\section{Supplementary Figures}
\label{sec:appendix_figures}

[Brief sentence describing each supplementary figure.]

\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\textwidth]{figA1_supplementary}
  \caption{[Caption]}
  \label{fig:appendix_A1}
\end{figure}
```

---

## Common Pitfalls

- Burying the main result in the middle of the paper
- Using "significant" without specifying statistical vs. economic
- Over-claiming causality when identification is weak (see Causal Language Calibration above)
- Literature review organized chronologically rather than by research strand
- Conclusion that recaps the paper section by section
- Inline `\begin{tabular}` in section .tex files -- tables go in `tables/`, referenced via `\input`
- `\graphicspath` pointing to wrong directory (must be `../figures/` relative to `paper/`)
- Compiling without bibtex (produces `[?]` for all citations)
