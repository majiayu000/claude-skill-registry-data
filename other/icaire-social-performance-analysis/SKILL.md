---
name: icaire-social-performance-analysis
description: Analyze ICAIRE post-level snapshots when evidence-bounded social performance patterns are needed for the Audience Growth Engine.
---

# ICAIRE Social Performance Analysis

Analyze validated ICAIRE LinkedIn and X observations using the canonical Brain protocol and clearly bounded evidence.

## Contract Checklist

- Read the canonical ICAIRE Brain page `protocol/icaire-social-performance-analysis` before analysis and follow its current instructions.
- Use validated post-level snapshots from the Audience Growth Engine, not aggregate summaries as the primary evidence.
- Confirm platform, date, post, metric, language, format, visual, and topic coverage before comparing cohorts.
- Preserve metric definitions and separate observed facts, calculated values, analyst labels, and hypotheses.
- Do not claim causation from observational performance data.
- Label sparse, incomplete, signed-out, or non-comparable data prominently.
- Save analysis artifacts under `/Users/hq/projects/ICAIRE/Audience Growth Engine/` without altering raw data.
- Do not draft, publish, message, or optimize content in this skill.

## Workflow

1. Load the governing protocol and inputs:
   - Read the live ICAIRE Brain protocol `protocol/icaire-social-performance-analysis` and any linked metric definitions.
   - Locate the latest validated normalized snapshots and the analysis workbook.
   - Record exact run IDs, collection times, platform coverage, and analysis window.
   - Stop if the protocol is unavailable or the selected data cannot be traced to immutable raw artifacts.
   - Anti-patterns: relying on remembered protocol text, analyzing an unvalidated workbook, treating Reem's aggregate report as post-level evidence
2. Audit comparability and completeness:
   - Quantify posts and observations by platform, date, language, topic, format, and visual status.
   - Identify duplicate snapshots and select the intended observation time without deleting history.
   - Check metric availability and definitions by platform. Keep non-equivalent metrics separate.
   - Decide whether cross-platform analysis is supportable; otherwise analyze each platform separately.
   - Anti-patterns: pooling unlike metrics, comparing unequal windows without disclosure, treating null metrics as zero
3. Produce descriptive baselines:
   - Calculate transparent post-level summaries allowed by the protocol, including distribution and median as well as totals and means where suitable.
   - Normalize only with defensible denominators and show the exact formula.
   - Identify outliers without allowing a single post to define a general pattern.
   - Anti-patterns: rank-ordering on raw totals alone, hiding sample sizes, inventing follower counts or reach denominators
4. Test content dimensions:
   - Examine topic, observed language, posting time, platform, post format, and visual presence when sample sizes permit.
   - Use matched or stratified comparisons where practical to reduce obvious confounding.
   - Record each result with cohort definition, sample size, metric, effect direction, uncertainty, and counterexamples.
   - Anti-patterns: claiming that visuals caused engagement, interpreting one or two examples as a trend, retrofitting topic labels to performance
5. Synthesize evidence-bounded patterns:
   - Classify findings as observed pattern, weak signal, insufficient evidence, or data-quality issue.
   - Distinguish cross-cutting patterns from platform-specific observations.
   - State plausible alternative explanations and the next data needed to strengthen each finding.
   - Do not convert patterns into next-week actions here; hand validated findings to the optimization skill.
   - Anti-patterns: causal language, cherry-picking winners, hiding contradictory posts, mixing recommendations into analysis
6. Validate and hand off:
   - Reconcile analysis tables to source row counts and spot-check calculations against the workbook.
   - Save reproducible tables, formulas or scripts, and a concise analysis section with exact source run IDs.
   - Report what can and cannot be concluded, plus any blocker to cross-platform interpretation.
   - Anti-patterns: reporting without source traceability, omitting calculation checks, presenting incomplete X data as definitive

## Evidence Labels

- **Observed pattern:** repeated, traceable association with adequate cohort coverage.
- **Weak signal:** suggestive direction with limited sample or confounding.
- **Insufficient evidence:** too little or incomparable data.
- **Data-quality issue:** missing, stale, ambiguous, or inconsistent measurement.

## Anti-Patterns

- Treating correlation as causation.
- Using aggregate summaries in place of raw post-level observations.
- Combining LinkedIn and X metrics that are named similarly but measured differently.
- Hiding nulls, missing periods, small cohorts, outliers, or failed comparisons.
- Turning the analysis into copywriting, content approval, or publishing.

## Output

Produce a reproducible analysis artifact with scope, source run IDs, coverage audit, methods, descriptive baselines, evidence-labeled patterns, counterexamples, limitations, and handoff findings. Report exact paths and validation checks, and state that optimization and publishing were not performed.
