---
name: rseng-research-integrity
description: >-
  Covers integrity checks on research outputs before submission or release:
  statcheck/GRIM-style consistency of reported statistics, agreement between
  manuscript numbers and pipeline outputs, retraction screening of cited work,
  sanity checks on tables and figures against the data, and an auditable
  pre-submission checklist. Use PROACTIVELY before manuscript submission or
  release of result-bearing reports, when reported numbers are transcribed
  from analysis outputs, and when the user asks to check a paper's numbers,
  mentions statcheck, GRIM or integrity checks, or suspects a mismatch between
  code outputs and text. (Reference existence and retractions:
  rseng-citation-hygiene; claim-source support: rseng-fact-checking; concealment
  requests: rseng-honesty.)
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Research integrity checks

Most integrity failures in the literature are not fraud - they are
transcription errors, stale numbers from an earlier analysis run,
rounding inconsistencies and copy-paste slips that nobody checked
because checking by hand is tedious. That is exactly what makes
this agent work: the checks are mechanical, the cost of running
them is minutes, and finding an error BEFORE submission converts a
potential correction notice into an edit. Frame every finding
accordingly: this is proofreading for numbers, not accusation.

## Internal consistency of reported statistics

Checks that need only the manuscript text:

- statcheck-style recomputation: for every reported test statistic
  with degrees of freedom and p-value (t, F, chi-square, r...),
  recompute the p from the statistic and df and flag mismatches -
  the classic detectable error class in psychology and beyond
  (the statcheck R package automates this for standard reporting
  formats; the same arithmetic can be applied directly).
- GRIM-style granularity: reported means of integer data with
  known sample size are only possible on a discrete grid. With
  n=25 the grid is multiples of 1/25, so a reported mean of 3.47
  is impossible (3.47 x 25 = 86.75, and 25 integer responses
  cannot sum to that) while the neighbouring 3.48 is attainable.
  Work out the grid before calling a value impossible - the
  near-miss is the whole point of the test. The same applies to
  percentages, with one extra step: a reported percentage is
  usually rounded, so test the whole interval it could have come
  from, not the point value. 34% of n=170 gives 57.8, but 57 and
  58 both round to 34%, so 34% is perfectly reportable; 34% of
  n=3 is not, because no count rounds there. The scrutiny R
  package implements these granularity tests.
- Arithmetic on the page: totals that sum, percentages that reach
  100 within rounding, subgroup Ns that add to the total N,
  confidence intervals consistent with the point estimate and SE.

## The stronger check: manuscript vs pipeline

When the analysis code is available (it should be -
rseng-reproducibility), do not settle for internal consistency:

- Regenerate the numbers: run the pipeline and compare every
  reported statistic, table cell and figure value against the
  fresh outputs, within stated rounding. Mismatches usually mean
  the text cites an OLDER run - exactly the silent staleness that
  one-command reproducibility (rseng-reproducibility) and
  generated-not-transcribed reporting prevent.
- Kill transcription at the source where feasible: propose
  generating tables and inline statistics from the pipeline
  outputs rather than retyping them; every hand-copied number is
  a defect opportunity.
- Check the figure data too: axis ranges, group counts and
  plotted Ns against the data files (a figure from the wrong CSV
  survives visual review easily).

## Citations and provenance

- Retraction screen of the bibliography, and verification that
  every reference is real and correctly attributed - delegated to
  rseng-citation-hygiene; run it as part of this battery.
- Provenance completeness: data sources identified with versions
  and access dates (rseng-data-management), software versions and
  seeds recorded (rseng-reproducibility), AI contributions declared
  honestly in aidecl.yaml and manuscript disclosure sections
  (rseng-ai-declaration) - venues increasingly ask, and the honest
  record is the one that already exists.

## The pre-submission battery

Run as one auditable pass and write the report into the project:

1. Statistics: statcheck-style + granularity checks over the
   manuscript.
2. Regeneration: pipeline outputs vs reported numbers, tables,
   figures.
3. Citations: existence, attribution, retraction screen
   (rseng-citation-hygiene).
4. Data/code availability statements true in practice: links
   resolve, the deposit exists, the archive matches the text
   (rseng-archiving, rseng-reproducibility).
5. Declarations complete: contributions, AI use, conflicts as the
   venue requires.

Report findings with locations and severities; fix-and-rerun until
clean, and keep the final report with the submission record - it is
evidence of diligence, and the checklist for the revision round.

## Boundaries

An agent flags inconsistencies; it does not adjudicate misconduct.
If checks surface a pattern that looks deliberate in someone
ELSE's work, the route is the venue's editorial process and COPE-
style guidance, via the user and the responsible institutional
channels - not a public accusation from a tool report. For the
user's own work, everything found is simply fixed before
submission, which is the point of checking first.

## Working with this skill

This skill is source-independent: its authority is the published
consistency-check methods (statcheck, GRIM and granularity
testing) and the services linked below.

Learn more (verified):
  - https://github.com/MicheleNuijten/statcheck - statcheck
  - https://github.com/lhdjung/scrutiny - scrutiny (GRIM and
    granularity tests)
  - https://gitlab.com/crossref/retraction-watch-data - Retraction
    Watch database
  - https://help.openalex.org - OpenAlex API

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-ai-declaration - declarations complete at submission
- rseng-archiving - availability statements must resolve
- rseng-citation-hygiene - reference existence and retraction screens
- rseng-fact-checking - do sources support the claims
- rseng-numerical-accuracy - numeric mismatches may be float issues
- rseng-reproducibility - regenerate numbers from the pipeline

<!-- related-skills:end -->
