---
name: write-lab-report
description: Use when writing a biology lab report in academic or research contexts following scientific reporting standards
source: Nature Methods reporting standards, IMRaD format (ICMJE guidelines), APA Publication Manual 7th edition (biological sciences)
tags: [science, biology, lab-report, imrad, scientific-writing, statistics, academic]
verified: true
---

# Write Lab Report

Write a complete biology lab report using the IMRaD structure with correct statistical reporting and reproducible methods.

## Why This Is Best Practice

**Adopted by:** Nature, Science, PLOS Biology, and all major peer-reviewed journals use IMRaD format; ICMJE (International Committee of Medical Journal Editors) provides the global standard
**Impact:** Nature Methods' 2013 analysis found that incomplete methods reporting is the leading cause of failed replication attempts in biology — the reproducibility crisis that prompted new reporting standards

**Why best:** IMRaD (Introduction, Methods, Results, Discussion) is not bureaucratic convention — it is the structure that allows independent scientists to evaluate, replicate, and build on findings. Each section serves a distinct epistemic function: why the question matters, how the answer was obtained, what was observed, and what it means. Omitting detail from Methods is the single most common reason biology experiments cannot be reproduced.

## Steps

1. **Write the Methods section first** — Methods are written while the experiment is fresh. Include: organism/strain details (species, supplier, passage number), reagent specifications (catalog number, concentration, lot number), equipment (make, model, settings), sample sizes, statistical tests, and any deviations from the planned protocol.
2. **Compile raw data and run statistics** — Organize raw data in a spreadsheet. Identify the appropriate statistical test (t-test for 2 groups, ANOVA for 3+, Chi-square for categorical, regression for continuous). Calculate means, SD or SEM, n, and p-values. Determine significance threshold (α = 0.05 is standard).
3. **Write the Results section** — Present findings in logical order, not chronological. Each result requires: a figure or table, a figure legend that is self-sufficient (reader can understand without the text), and a paragraph that states what the data show (not what they mean). Refer to all figures by number. Report exact p-values (p = 0.032, not p < 0.05).
4. **Write the Discussion section** — Interpret the results in the context of the hypothesis. Address: Does the data support or refute the hypothesis? How do results compare to prior literature (cite specific papers)? What are the limitations (sample size, assay sensitivity, confounders)? What are the next logical experiments?
5. **Write the Introduction section last** — Introduce the biological question, provide the relevant background literature (cited), state the gap this experiment addresses, and end with an explicit statement of the hypothesis and experimental approach.
6. **Write the Abstract** — 250-word summary of the entire report: background (1-2 sentences), objective (1 sentence), methods (2-3 sentences), key results with statistics (2-3 sentences), conclusion (1 sentence). The abstract must be accurate and self-contained.
7. **Compile references** — Use a consistent citation format (APA, Vancouver, or journal-specific). Every citation in the text must appear in the reference list; every reference must be cited in the text. Use reference management software (Zotero, Mendeley).
8. **Review for completeness using a reporting checklist** — Use ARRIVE (animal research), CONSORT (clinical trials), or MIQE (qPCR) guidelines as applicable. Any required element not present is a revision before submission.

## Rules

- Methods must be sufficiently detailed that an independent researcher with standard lab equipment can replicate the experiment without contacting the authors.
- Results section reports observations only — interpretation belongs in the Discussion.
- Every p-value must be accompanied by n (sample size) and the statistical test used; without these, the p-value is uninterpretable.
- Never use "significant" to mean "notable" — reserve the word for statistical significance with a reported p-value.

## Examples

Results section example: "Treatment with 10μM inhibitor X reduced cell viability by 42% compared to vehicle control (Figure 2A; p = 0.003, unpaired t-test, n = 6 biological replicates). This effect was dose-dependent, with 1μM treatment producing a non-significant 8% reduction (p = 0.21). Western blot analysis confirmed that inhibitor X reduced phospho-ERK levels by 67% at 10μM (Figure 2B)."

Contrast with incorrect Discussion mixed in: "Treatment with inhibitor X significantly reduced cell viability (Figure 2A), demonstrating that this pathway is essential for cell survival in this context..." (This belongs in Discussion, not Results.)

## Common Mistakes

- Insufficient Methods detail — "cells were treated with the drug and incubated" is not reproducible; concentration, volume, duration, and cell density are all required.
- Interpreting results in the Results section — results present data; discussion interprets it. Mixing the two obscures the difference between observation and inference.
- Reporting "p < 0.05" instead of exact p-value — exact p-values allow readers to apply their own significance thresholds and are required by Nature and most major journals.
- Writing the Introduction as a literature review instead of a funnel — Introduction should narrow from broad biology → specific gap → this experiment's hypothesis, not provide a general review of the field.

## When NOT to Use

- When the output is a research proposal or grant application — those formats require specific sections (Aims, Significance, Innovation, Approach) that do not map to IMRaD and are evaluated by different criteria than a completed experiment report.
- When the work is a methods development or protocol paper where the primary contribution is the technique itself — these use an alternative structure that foregrounds validation benchmarks, comparison to prior methods, and step-by-step protocol tables rather than hypothesis-driven IMRaD flow.
- When summarizing secondary literature or writing a review article — review papers synthesize existing findings across many studies and follow a distinct structure (scope, search strategy, synthesis, limitations) that differs fundamentally from a single-experiment lab report.
