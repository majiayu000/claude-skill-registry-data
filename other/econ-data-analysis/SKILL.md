---
name: econ-data-analysis
description: Economic data-analysis discipline. Use for importing, cleaning, merging, filtering, variables, aggregation, summary stats, regressions, or figures on economic, financial, or panel data.
user-invocable: true
---

# Economic Data Analysis

## Stage-Scoped References

Load per stage, not all at once:

| Reference | Load when |
|---|---|
| `references/planning.md` | PLAN phase — data inventory and sensitivity analysis design. |
| `references/data-robustness-checklist.md` | PLAN (design) and IMPLEMENT (execution of sensitivity tasks) — menu of robustness checks. |
| `references/integrate-drift-tests.md` | protection stage — data-analysis key-result identification, econ-specific tolerances, data-analysis failure modes for drift/regression tests. |
| `references/integration.md` | INTEGRATE stage — data-specific refactor-integrity gates. |
| `references/notebook-format.md` | IMPLEMENT stage (for implementer) — cell organization, narrative, output idioms, Python jupytext / Julia Quarto rendering. Companions: `jupytext-guide.md`, `julia-quarto-guide.md`. |

## The Iron Law

```
NO TRANSFORMATION WITHOUT PRIOR DESCRIPTION
```

Transformed without describing first? Undo it and describe fresh from the current data state — not from a previous session, not "later at the end."

---

## Three Concurrent Disciplines: Describe–Analyze–Validate

**Concurrent, not sequential** — every analysis step exercises all three, with documentation alongside.

Shared checklist: implementer before DONE, reviewer within its focus. These items apply to every analysis task; operation-conditional items live in §Pitfalls.

- `[BLOCKING]` — must fix to earn APPROVE.
- `[ADVISORY]` — recorded; never blocks APPROVE.

**Committed diagnostics, row-count logs, and output files are the evidence.** A missing diagnostic is a finding, not a prompt to generate it yourself. When fixing, re-run the changed step and its downstream dependents; unaffected upstream outputs stand as committed.

### Describe

Describe before and after every transformation. The post-transformation describe feeds Sanity checks below.

**After loading any dataset:**

- `[BLOCKING]` Every input described before the first transformation on it.
- `[BLOCKING]` **Panel structure** — first priority for panel/longitudinal data, the common case. Pure cross-section: note it, skip these.
  - **IDs identified** — panel ID (firm, fund, country, individual) and time ID (year, quarter, month, day).
  - **Counts verified** — unique IDs and unique time periods, against expectations.
  - **Date range** — min and max noted.
  - **Balancedness characterized** — periods-per-unit distribution (mean, median, min, max) and balanced ratio (actual rows / N_ids × T_periods).
    - Unbalanced: pattern characterized — entry/exit, mid-panel gaps, expanding coverage.
- `[BLOCKING]` **Variable diagnostics** on key variables — do NOT blanket-`describe()` all columns:
  - Continuous (returns, prices, GDP, weights): mean, median, std, min, max, tail percentiles (p1, p5, p95, p99).
  - Categorical/binary (sector codes, indicators, country): value counts and shares; check unexpected categories or near-zero frequencies.
  - Identifiers: panel ID × time uniquely identifies rows; check duplicates.
- `[BLOCKING]` **Data types and missing values**:
  - Column types correct — dates as dates, numerics as numerics, not object/string.
  - Missing values counted, and share per variable.
  - Missingness pattern noted — random vs systematic. Interpretation: §Validate §Missing-data as signal.

Data already imported and validated upstream: read the existing diagnostics instead of re-running full validation.

**Outlier flagging:**

- `[BLOCKING]` Observations beyond p1/p99 flagged and assessed.
  - Data error vs genuine extreme — naturally skewed variables (firm size, wealth, trade volumes) have real extremes.
  - Keep/winsorize/trim decision documented.
- `[ADVISORY]` If winsorizing, cutoff documented; robustness with alternatives considered (see `references/data-robustness-checklist.md`).

**After every major transformation (re-describe):**

- `[BLOCKING]` Descriptive statistics re-run on affected variables, compared against pre-transformation values.
  - Applies after merges, filters, variable construction, aggregations, reshaping, deduplication.
  - An unexplained distribution shift is silent corruption — nothing downstream uses the variable until it is understood.

**Visualization for key variables** — plot what summary statistics hide:

- `[BLOCKING]` **A companion figure wherever visualization is feasible**, which covers most analyses. A key variable carried through the analysis without one is a finding.
  - **Continuous variable**, before transforming, winsorizing, or filtering it — histogram.
  - **Time-series variable** — line plot against time, where structural breaks and seasonality live.
  - **A correlation you are about to rely on** — scatter plot.
- `[ADVISORY]` Visualization not feasible — a lone scalar, too many series to plot individually, a figure that would not clarify: say which and move on.

### Analyze

Transform data with integrity. Operation-specific traps: §Pitfalls.

- `[BLOCKING]` **One logical operation per step.** One verb per step — merge, filter, construct, aggregate, reshape, deduplicate. No chaining merge + filter + construct.
- `[BLOCKING]` **Row-count logging at every sample-changing operation.** Print `before → after` for every merge, filter, drop, deduplication, or sample restriction.
  - Major operations warrant their own cell; minor ones can share a cell as long as the count is printed.

### Validate

Numbers must make economic sense — checked against priors, literature, cross-variable relationships, and alternative specifications. Runs on the output of every Analyze step, not at the end.

**Sanity checks** (after every Analyze step; minimum bar before proceeding):

- `[BLOCKING]` **Row count matches a stated expectation**, not just logged.
  - Left join: matches the left table when the right side is m:1.
  - Inner join and filter: drop counts explained, drop rate defensible.
- `[BLOCKING]` **Economic sense.**
  - Magnitudes plausible — GDP growth of 300% is wrong.
  - Signs correct; correlations match known stylized facts.
  - Constructed variables and growth rates spot-checked by hand on a few observations.
- `[BLOCKING]` **Task objective expectations comparison.** Task objective states Expected Results or Hypotheses: compare findings explicitly, flag divergences before moving on.

Anything unexpected: STOP and investigate.

**Multi-source validation** (key variables and headline numbers):

- `[BLOCKING]` Every key variable and headline number checked against **at least one external reference**, for scale, sign, and relationship.
  - References: a published benchmark (IMF WEO, World Bank, central-bank data), prior literature, or a known related measure.
  - Two proxies for the same construct should correlate.
  - Conditional means across obvious subgroups (developed vs emerging, pre/post crisis) should behave as expected.
  - A surprising relationship is a signal to investigate, not to explain away.

**Missing-data as signal** (interrogate before handling — how-to in §Pitfalls §Missing data handling):

- `[BLOCKING]` **Systematic missingness** (concentrated in time, geography, or correlated with other variables) investigated — true absence vs construction error.
- `[BLOCKING]` **"Missing" meaning disambiguated.** No position (→ zero) vs didn't report (→ truly missing). Missing returns treated as zero is almost always wrong.

**Sensitivity analysis** (design in `references/planning.md`; menu in `references/data-robustness-checklist.md`):

- `[ADVISORY]` Sensitivity checks run on robustness-sensitive tasks, one alternative specification at a time — sample cutoff, variable definition, winsorization, leave-one-out.
  - "Robust enough" is an economic judgment: a coefficient moving 5% is usually fine, one that flips sign is not.
  - The question is whether the researcher tells the same story under the alternative.
- `[BLOCKING]` **Divergence escalated.** A sensitivity check with a meaningfully different result: STOP and `AskUserQuestion`.
  - Meaningfully different — sign flip, lost significance on a headline coefficient, magnitude change large enough to change the interpretation.
  - Divergence is a methodology question, not an RA decision.

### Implementation standards

- `[BLOCKING]` Analysis scripts follow the notebook-compatible format per `references/notebook-format.md`.
- `[BLOCKING]` Major decisions (filter threshold, join type, variable definition, sample period) carry a markdown-cell justification; minor decisions carry an inline comment.
- `[BLOCKING]` Outputs (tables, figures) are generated from committed code, not ad-hoc REPL state.

### Documentation and handoff

- `[BLOCKING]` In a superRA task, task-specific result-producing code follows `using-superra/references/task-companion-files.md`.
- `[BLOCKING]` Markdown cells explain what each block does and why.
- `[BLOCKING]` **Headline findings presented visually.** Each headline result as a figure — a distribution, a relationship, or a time path.
  - Exception: a figure would not clarify it — a lone scalar, a small table that already reads clearly.
- `[BLOCKING]` Figures saved under the task's `attachments/` directory and embedded in task `## Results` as `attachments/fig.png` per `superRA:communicate`.

### Stage-scoped discipline (not walked at every implementation dispatch)

- **`integration` stage** — `references/integration.md` (codebase consistency, data discipline preserved through refactoring, utility reuse, documented deviations).
- **End-of-workflow completion verification** — orchestrator-owned, not dispatched. In superRA, `superimplement/references/completion.md` §Verify Pipeline and Reproducibility.

## Pitfalls

Operation-conditional — walk a subsection only when the task performs that operation. Severity markers match the main checklist.

### Merges and joins

- `[BLOCKING]` **Before — describe both sides.** Row counts and unique join-key values in both tables; key overlap and type compatibility.
  - A merge without join-key inspection on both sides is an Iron Law violation.
- `[BLOCKING]` **Join type declared.** Decide 1:1, m:1, or 1:m before writing the merge; confirm the post-merge row count against it.
  - Many-to-many is almost always a bug — a Cartesian product that silently inflates row counts, and the reason a left join can come back longer than its left table.
- `[BLOCKING]` **Unmatched rows logged.** How many rows from each side did not match; whether non-matching is random or systematic.

### Time-series operations (lag, lead, diff, cumsum, fill)

- `[BLOCKING]` **Sort first.** By panel ID + time, before any lag, lead, diff, or cumsum. Joins destroy sort order — re-sort after every merge.
- `[BLOCKING]` **Check for gaps** before lags/leads/diffs.
  - If unit `i` is missing period `t`, a naive `shift(1)` treats period `t+1`'s lag as `t-1`'s value — silently wrong.
  - Diagnose gaps per unit first, then spot-check a few units after the shift, especially near panel entry and exit.
- `[BLOCKING]` **Use time-aware operators when available.**
  - Julia: `PanelShift.jl` handles gaps.
  - Python: merge on lagged time index, or `reindex` to a full time grid before shifting.
  - Positional-shift-only framework: verify no gaps, or fill gaps explicitly — with NaN, not interpolation.

### Reshaping

- `[BLOCKING]` After pivot: unique IDs × unique time periods should match original shape.
- `[BLOCKING]` Check for unintended NAs from unbalanced panels going wide.

### Aggregations

- `[BLOCKING]` **Function matches content.** Sum dollar amounts, average rates — never the reverse.
- `[BLOCKING]` **Group-by keys match intended level** (country-year, not country-month).
- `[BLOCKING]` **Weights verified.** Weighted average: weights sum to expected values.
- `[BLOCKING]` **Duplicates handled before aggregating** — dupes cause double-counting.

### Deduplication

- `[BLOCKING]` Uniqueness checked before operations that assume it (merges, index-setting).
- `[BLOCKING]` Which duplicate kept, and why (first, last, highest value).

### Filtering

- `[BLOCKING]` Rows dropped logged — count, reason, before/after.
- `[BLOCKING]` **Non-randomness of drops checked.** Drops concentrated in certain countries, periods, or variable ranges are sample-selection-bias risk.
- `[BLOCKING]` **Boolean logic verified.** `&` vs `|` is a common silent bug; chained filters compound.

### Variable construction

- `[BLOCKING]` **Transformation order:** log → winsorize → standardize. Log after standardize fails on negative standardized values.
- `[BLOCKING]` **Ratio denominators checked** for zero/near-zero; extreme ratios often come from small denominators.
- `[BLOCKING]` **Growth rates:** spot-checked against published benchmarks; first differences amplify measurement error — inspect for implausible spikes.
- `[BLOCKING]` **Standardization:** mean ≈ 0, std ≈ 1 within the relevant sample; cross-sectional vs time-series vs pooled stated.

### Missing data handling

*Handling* missingness (for *interpretation*, §Validate §Missing-data as signal):

- `[BLOCKING]` **Handling is visible and auditable** — `.fillna(0)`, `.dropna()`, and filters explicit; package defaults that silently ignore NaN in aggregations checked against the analytical objective.
- `[BLOCKING]` **Prefer passing missing through the pipeline** over filling silently; fill or coalesce only with explicit justification.

## Common Rationalizations

Excuses that precede Iron Law violations. Catch yourself forming one: undo the transformation and describe first.

| Excuse | Reality |
|--------|---------|
| "Already know this data" / "Same as last session" | Your memory ≠ current state. Files and upstream code change. Describe fresh. |
| "Just a simple merge, I can skip the describe" | Simple merges create the worst silent bugs. |
| "Quick exploration, not formal analysis" | If results inform a decision, they need validation. |
| "I'll validate at the end" | Can't isolate which step caused the problem. |
| "Only filtering, not transforming" | Filters change your sample. Log what you're losing. |

## Key References

- Gentzkow & Shapiro (2014), "Code and Data for the Social Sciences"
- AEA Data Editor, "Guidance for Replication Packages"
