---
name: nist-stat-handbook
description: "Knowledge base from the NIST/SEMATECH e-Handbook of Statistical Methods (NIST HB 151) — the practical statistics reference for engineering, metrology, and quality. Use for: exploratory data analysis and the four univariate assumptions (4-plot); measurement process characterization including bias/precision, calibration designs, gauge R&R, and ISO/GUM uncertainty budgets; production process characterization (stability vs. capability); process modeling and regression (LS/WLS/NLS/LOESS); design of experiments (screening, fractional/factorial, response-surface, Taguchi); statistical process control (Shewhart/CUSUM/EWMA charts, capability indices, acceptance sampling); product/process comparisons (hypothesis tests and confidence intervals for 1/2/3+ groups, ANOVA, multiple comparisons); and reliability (lifetime & repair-rate models, accelerated testing, reliability growth). Scope limits: this is applied frequentist statistics for measurement and quality — it does NOT reproduce the per-distribution formula galleries, worked case studies, datasets, plot images, or Dataplot/R code of the original web Handbook (those are described, not copied); it is thin on modern machine learning, Bayesian methods beyond conjugate reliability priors, time-series/forecasting, and Bayesian experimental design."
---

<!-- argument-hint: [statistical task: EDA/4-plot, uncertainty/GUM, calibration, gauge R&R, DOE/screening/response-surface, control chart, hypothesis test/ANOVA, reliability/Weibull/acceleration, capability, chapter number] -->

# NIST/SEMATECH e-Handbook of Statistical Methods (NIST HB 151)
**Source**: NIST/SEMATECH (US Government work, public domain) | **Chapters**: 8

## When to use
Use this skill when you need applied frequentist statistics for engineering, metrology, or quality work, drawing from the NIST/SEMATECH e-Handbook of Statistical Methods (NIST HB 151). It is the right pack for exploratory data analysis and the four univariate assumptions (4-plot), measurement process characterization including bias/precision, calibration designs, gauge R&R, and ISO/GUM uncertainty budgets, production process characterization covering stability vs. capability, process modeling and regression (LS/WLS/NLS/LOESS), design of experiments (screening, fractional/factorial, response-surface, Taguchi), statistical process control (Shewhart/CUSUM/EWMA charts, capability indices, acceptance sampling), product/process comparisons (hypothesis tests and confidence intervals for one, two, or more groups, ANOVA, multiple comparisons), and reliability (lifetime and repair-rate models, accelerated testing, reliability growth).

**Prerequisites:** none, plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the Core Frameworks below: the EDA mindset, the
  characterization→modeling→improvement→control→comparison→reliability arc, and the
  routing rules for picking a method.
- **With a statistical task** — route to the right chapter and pattern. Examples:
  "is my data in control?" → ch01 (4-plot); "state the uncertainty of this result" →
  ch02 (GUM budget); "design an experiment to optimize yield" → ch05 (DOE);
  "which control chart for small drifts?" → ch06 (CUSUM/EWMA); "compare three machines"
  → ch07 (ANOVA + multiple comparisons); "fit a life distribution" → ch08 (Weibull).
- **With a chapter** — `ch01` EDA · `ch02` measurement/uncertainty · `ch03` process
  characterization · `ch04` regression · `ch05` DOE · `ch06` SPC · `ch07` comparisons ·
  `ch08` reliability.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or runtime licence needed.

> **What this Handbook is.** A practitioner's reference for *engineering statistics* —
> measurement, process, and quality work — not a mathematical-statistics textbook. Its
> through-line is the **engineering scientific method**: characterize a process, model it,
> improve it by experiment, hold the gains with control charts, compare alternatives with
> the right test, and predict how long it will last. The signature attitude (from ch01)
> is **look at the data before imposing a model.**

## Core Frameworks & Mental Models

### The EDA stance — let the data reveal the model (ch01)
Classical analysis imposes a model (normality, linearity), then estimates and tests it.
**Exploratory Data Analysis (EDA)** holds that decision back: plot the data first and let
its structure surface. The unifying baseline is the **univariate model** `Y = c + ε` and
its **four assumptions** — the data have (1) fixed location, (2) fixed scale, (3) randomness
(no autocorrelation), and (4) a fixed distribution. The **4-Plot** (run-sequence, lag,
histogram, normal-probability) tests all four at a glance. Pass all four ⇒ the process is
"in statistical control" and predictable. A failed panel is a *diagnostic* pointing at a
physical cause. **Residuals** are the universal diagnostic: an adequate model leaves
structureless residuals.

### Characterizing a measurement process — goodness decomposed (ch02)
Treat measurements as the output of a process and ask how *good* they are. Goodness splits
into **bias** (quantitative offset from the reference/true value), **short-term variability
/ precision** (level-1), **long-term / day-to-day variability** (level-2, often *larger*
than precision for very precise instruments), and **uncertainty**. The engine is the
**check standard** — a database of repeated measurements on a stable surrogate — monitored
by an **individuals Shewhart chart** (and **EWMA** for small shifts). **Calibration designs**
are redundant least-squares intercomparison schedules (anchored by a **restraint** = the
known reference value) that assign values while cancelling constant **left-right bias** and
linear **drift**. **Gauge R&R** nested designs separate repeatability, reproducibility, and
stability. Uncertainty follows the **ISO/GUM** framework: every component a standard
deviation, grouped by **Type A** (from statistical analysis) vs. **Type B** (other means),
combined by **root-sum-squares** with **sensitivity coefficients**, expanded by a coverage
factor `U = k·u` (k≈2 ⇒ ~95%), with **Welch-Satterthwaite** for unknown degrees of freedom.

### Characterizing a production process — stability before capability (ch03)
Frame the process as a **black box** (inputs / controlled factors / uncontrolled noise /
output), then expand drivers with a **fishbone** diagram. Distribution = **location +
spread + shape**. Models span the **Continuous Linear Model (CLM)**, **ANOVA**, and
**discrete (contingency/chi-square)** forms. Two rules dominate: **add variances, never
standard deviations** when combining error; and **establish stability before claiming
capability** — Cp/Cpk on an out-of-control process are meaningless. Interpret graphically,
then confirm numerically. The most expensive mistake is skimping on planning.

### Modeling a process — function plus error (ch04)
The general statistical model is `y = f(x; β) + ε`: a deterministic function of the factors
plus random error. Four method families build it — **linear least squares**, **nonlinear
least squares**, **weighted least squares (WLS)** for non-constant variance, and **LOESS**
for local, assumption-light smoothing. A model is used to **estimate, predict, calibrate,
and optimize**. Six standard assumptions (random errors, mean zero, constant variance,
known distribution, independence, correct functional form) are checked through **residual
analysis** — the same look-at-the-residuals discipline as EDA.

### Improving by experiment — sequential DOE (ch05)
**Design of Experiments** varies factors *together* to estimate effects efficiently; its
four objective classes are **comparative, screening, response-surface, and regression**.
The strategy is a **staircase**, not one big experiment: screen many factors cheaply with
**fractional factorial / Plackett-Burman** designs, test curvature with **center points**,
**foldover** to de-alias, then spend three-level **response-surface** runs (**CCD**,
**Box-Behnken**) near the optimum. **Resolution** (III/IV/V) is the confounding dial; the
**defining relation** and **generators** set the **aliasing**. **One-factor-at-a-time is a
trap** — it misses interactions. **Taguchi** robust design (parameter design via inner/outer
arrays, then tolerance design) minimizes sensitivity to noise. Always randomize; finish with
**confirmation runs**.

### Holding the gains — statistical process control (ch06)
**SPC/SQC** uses control charts to separate common-cause from special-cause variation.
**Phase I** builds and validates limits from history; **Phase II** monitors new data.
Chart families: **Shewhart** (X-bar & R/s, individuals) for large shifts; **CUSUM** (V-mask)
and **EWMA** (memory depth λ) for small sustained drifts; **attributes** charts for counts;
**Hotelling's T²** for correlated multivariate data. **Control limits ≠ specification
limits** (voice of the process vs. voice of the customer). Compare charts by **Average Run
Length (ARL)**: sensitivity is bought with false alarms (**WECO rules**). Decide the response
in advance with an **OCAP**. **Acceptance sampling** (OC curve, AQL/LTPD, producer's/
consumer's risk, AOQ/AOQL) governs lot accept/reject decisions.

### Comparing alternatives — the right test (ch07)
Route by **how many processes**: one (t/z, chi-square, exact-binomial/Wilson), two
(two-sample/paired t, F-test, two-proportion z / Fisher exact), or three-plus (**ANOVA**
then a **multiple-comparison** procedure — Tukey, Scheffé, Bonferroni, Tukey-Kramer,
Marascuilo; **Kruskal-Wallis** if non-normal). The spine is **test ⇔ interval duality**:
reject exactly when the hypothesized value falls outside the matching confidence interval.
ANOVA **analyzes variances to draw conclusions about means**; fixed vs. random effects
changes the inferential target. Use **exact** methods for small samples, **approximations**
(with their validity gates) for large; **"failure to reject" is not proof of equality.**

### Predicting how long it lasts — reliability (ch08)
**Reliability is quality over time** — R(t) = probability of surviving past t. The first
fork is **non-repairable vs. repairable**. Non-repairable units get a **lifetime
distribution** (Weibull, lognormal, exponential, gamma, extreme value, Birnbaum-Saunders),
reasoned about via the **hazard rate** h(t) (a *speedometer*) and the **bathtub curve**;
data are **censored** (Type I by time, Type II by count) and information scales with the
number of **failures**. Repairable systems get a **repair-rate** model (HPP; **NHPP Power
Law / Duane-AMSAA** for **reliability growth** under **TAAF**) reasoned about via N(t), M(t),
m(t) — they have *no single failure rate*. **System reliability** is built **bottom-up**
from series/parallel/k-of-n/standby blocks (series = product of part reliabilities).
**Accelerated testing** needs a justified **acceleration model** (Arrhenius, Eyring,
Coffin-Manson) that rescales time.

---

## Chapter Index

| # | Chapter file | Topic | Key content |
|---|---|---|---|
| 1 | [ch01](chapters/ch01-nist-stat-handbook-exploratory-data-analysis.md) | Exploratory Data Analysis | EDA philosophy, univariate model, four assumptions, the 4-plot, residuals, problem categories |
| 2 | [ch02](chapters/ch02-nist-stat-handbook-measurement-process-characterization.md) | Measurement Process Characterization | Bias/precision/uncertainty, check standards, Level-1/2/3 model, calibration designs, gauge R&R, **ISO/GUM uncertainty budgets** |
| 3 | [ch03](chapters/ch03-nist-stat-handbook-production-process-characterization.md) | Production Process Characterization | Black-box & fishbone framing, CLM/ANOVA/discrete models, error propagation, stability vs. capability |
| 4 | [ch04](chapters/ch04-nist-stat-handbook-process-modeling.md) | Process Modeling | `y = f(x;β)+ε`, LS/WLS/NLS/LOESS, four uses of a model, six assumptions, residual analysis |
| 5 | [ch05](chapters/ch05-nist-stat-handbook-process-improvement-doe.md) | Process Improvement (DOE) | Design objective classes, factorial/fractional/Plackett-Burman, resolution & confounding, response surface (CCD/Box-Behnken), Taguchi |
| 6 | [ch06](chapters/ch06-nist-stat-handbook-process-monitoring-and-control.md) | Process Monitoring & Control | SPC, Shewhart/CUSUM/EWMA/attributes/multivariate charts, Phase I/II, ARL, capability, acceptance sampling |
| 7 | [ch07](chapters/ch07-nist-stat-handbook-product-and-process-comparisons.md) | Product & Process Comparisons | Hypothesis tests & intervals for 1/2/3+ groups, test/interval duality, ANOVA, multiple comparisons, goodness-of-fit |
| 8 | [ch08](chapters/ch08-nist-stat-handbook-assessing-product-reliability.md) | Assessing Product Reliability | Lifetime & repair-rate models, bathtub curve, censoring, acceleration models, system reliability, reliability growth, Bayesian |

## Topic Index

- **4-Plot / four univariate assumptions** → ch01, cheatsheet
- **Acceleration models (Arrhenius/Eyring/Coffin-Manson)** → ch08
- **Acceptance sampling / OC curve / AQL / LTPD** → ch06, cheatsheet
- **ANOVA (one-way / two-way / fixed-random effects)** → ch07, ch03, ch05
- **Average Run Length (ARL)** → ch06
- **Bathtub curve / hazard rate** → ch08
- **Bias / accuracy (measurement)** → ch02
- **Black-box & fishbone (cause-and-effect) diagram** → ch03
- **Calibration designs / restraint / drift & left-right bias** → ch02
- **Capability (Cp, Cpk) / stability vs. capability** → ch06, ch03, cheatsheet
- **Censoring (Type I / Type II)** → ch08
- **Check standard** → ch02, patterns
- **Confidence intervals / test–interval duality** → ch07, cheatsheet
- **Confounding / aliasing / resolution (III/IV/V)** → ch05
- **Control charts (Shewhart / CUSUM / EWMA / attributes / T²)** → ch06, cheatsheet
- **Design of Experiments (DOE) / objective classes** → ch05, patterns
- **EDA (exploratory data analysis) philosophy** → ch01
- **Error propagation / add variances / sensitivity coefficients** → ch02, ch03, patterns
- **Factorial & fractional factorial / Plackett-Burman** → ch05
- **Foldover / center points** → ch05
- **Gauge R&R (repeatability / reproducibility / stability)** → ch02
- **Goodness-of-fit (Anderson-Darling, K-S, chi-square, Shapiro-Wilk)** → ch07, ch08
- **Hotelling's T² (multivariate SPC)** → ch06
- **Hypothesis tests by group count (1/2/3+)** → ch07, cheatsheet
- **ISO/GUM uncertainty / Type A & Type B / expanded uncertainty** → ch02, patterns, cheatsheet
- **Lifetime distributions (Weibull / lognormal / exponential / gamma)** → ch08, glossary
- **LOESS / local regression** → ch04
- **Multiple-comparison procedures (Tukey / Scheffé / Bonferroni)** → ch07
- **Out-of-Control Action Plan (OCAP)** → ch06
- **Phase I vs. Phase II (SPC)** → ch06
- **Process model `y = f(x;β)+ε` / regression (LS/WLS/NLS)** → ch04
- **Randomized block / completely randomized designs** → ch05
- **Reliability R(t) / non-repairable vs. repairable** → ch08, patterns
- **Reliability growth / Duane / AMSAA / TAAF** → ch08
- **Residual analysis** → ch04, ch01
- **Response surface (CCD / Box-Behnken / RSM)** → ch05
- **Run-sequence / lag / histogram / normal-probability plots** → ch01
- **Sampling / stratification / sample size** → ch03
- **Sequential experimentation strategy** → ch05, patterns
- **Series / parallel / k-of-n / standby system models** → ch08
- **Statistical Process Control (SPC / SQC)** → ch06
- **Taguchi / parameter & tolerance design** → ch05
- **Three-level standard-deviation model (Level 1/2/3)** → ch02
- **Uncertainty budgets / Welch-Satterthwaite** → ch02, cheatsheet
- **WECO rules / control vs. specification limits** → ch06

## Supporting Files

- [glossary.md](glossary.md) — key statistical, metrology, DOE, SPC, and reliability terms, alphabetical, with chapter references
- [patterns.md](patterns.md) — ten reusable techniques (4-plot gate, black-box framing, GUM uncertainty budget, stability-before-capability, chart selection, sequential DOE, comparison-test routing, reliability fork, check-standard control) with When/How/Trade-offs
- [cheatsheet.md](cheatsheet.md) — chapter map, the four assumptions, comparison-test selector, control-chart selector, DOE & reliability decision tables, uncertainty-in-one-screen, and tells & smells

---

## Scope & Limits

**Covers**: applied (frequentist) statistics for engineering, metrology, and quality across
the eight Handbook chapters — exploratory data analysis; measurement-process characterization
and ISO/GUM uncertainty; production-process characterization; process modeling and
regression; design of experiments; statistical process control and acceptance sampling;
hypothesis testing, confidence intervals, ANOVA and multiple comparisons; and product
reliability (lifetime models, accelerated testing, reliability growth, basic Bayesian
reliability).

**Does not cover / thin on**: the original web Handbook is an HTML/web-native reference of
many short interlinked pages with extensive **per-distribution formula galleries, worked
case studies, datasets, plot/figure images, and Dataplot/R code blocks** — this pack
**synthesizes the concepts and method-selection logic in original words and deliberately
does not reproduce** those galleries, case studies, datasets, images, or code (they are
described, not copied — a quality and licence-safety choice). It is also **thin on**: modern
machine learning / statistical learning; Bayesian methods beyond conjugate reliability
priors; time-series analysis and forecasting; Bayesian/optimal experimental design;
survey/causal-inference methodology; and software-specific how-tos. For SE-process context
see `sebok`, `dau-se-guidebook`, `nasa-npr-7123`; this pack is the quantitative-methods
companion to those.

**Source version**: NIST/SEMATECH e-Handbook of Statistical Methods, **NIST Handbook 151**
(2012 edition, last updated October 2022). **Public domain** — a work of the U.S. Government
(17 U.S.C. 105); free to reproduce, transform, and redistribute, including commercially.
SEMATECH co-developed the content; attribution to NIST/SEMATECH is a courtesy, not an
obligation, and neither endorses this pack.
