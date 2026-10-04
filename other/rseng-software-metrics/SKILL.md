---
name: rseng-software-metrics
description: >-
  Covers measuring code health quantitatively: cyclomatic complexity, code
  duplication, coupling and cohesion, code churn, maintainability index, size
  conventions and documentation coverage - running radon, lizard, jscpd,
  interrogate and SonarQube-class tools, interpreting numbers against
  community conventions and the software's tier, wiring metric gates into CI,
  and avoiding metric gaming. Use when the user asks how healthy, complex or
  maintainable their code is, wants metrics or duplication measured, mentions
  cyclomatic complexity, churn, coupling or maintainability index, or when a
  quality assessment (rseng-quality-framework) needs the quantitative half. For
  style and linting see rseng-code-quality; for runtime performance measurement
  see rseng-performance-profiling.
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Software metrics for research code

Quality talk stays opinion until something is measured. A cluster
of the community research software quality indicators is explicitly
quantitative - complexity, duplication, cohesion/coupling, churn,
maintainability index, size and documentation coverage "within
community conventions" - and all of it is measurable in minutes
with free tools. The discipline is in the interpretation: metrics
LOCATE problems, humans judge them; a number out of convention is
a place to look, not a verdict. And Goodhart's law is the standing
hazard - when a metric becomes a target, it stops measuring
(the gaming section below is as important as the tools).

## The metrics and what they actually indicate

- Cyclomatic complexity (independent paths per function): high
  values mean hard-to-test, hard-to-reason code; each point is
  roughly one more test case needed (rseng-testing). Look at the
  per-function outliers, never the average.
- Duplication ratio: copy-pasted blocks that must be fixed twice;
  research code's most common debt (the "second copy-paste" signal
  from rseng-software-design's extraction rule, made measurable).
- Coupling and cohesion: how tangled modules are (CBO-style
  counts) and how single-purpose they are internally - the
  quantitative face of rseng-software-design's change-cost test.
- Code churn (change frequency per file): files that change
  constantly are either active development or a design hotspot;
  churn x complexity is the best bug-risk locator in the set.
- Maintainability index: a composite; useful for trend and
  worst-file ranking, meaningless as an absolute grade.
- Size conventions (LOC per function/module): long functions
  correlate with everything bad; community conventions vary by
  language (rseng-language-guides).
- Documentation coverage: fraction of public functions/classes
  with docstrings (interrogate-style) - the measurable slice of
  rseng-documentation, and an explicit quality indicator.

## Measuring: the tool layer

- Python: radon (complexity, maintainability index, raw metrics),
  interrogate (docstring coverage); lizard covers complexity
  across a dozen languages (C/C++, Java, JS, Fortran-adjacent
  stacks) with no setup.
- Duplication: jscpd scans mixed-language repositories quickly.
- Churn: git itself (`git log --format= --name-only | sort |
  uniq -c`) - no tool needed; join with complexity for the
  hotspot map.
- Platform-scale: SonarQube-class services aggregate all of the
  above with history when a team wants dashboards; overkill for a
  single analysis repo (match the tier).

Run measurements read-only first and report: worst five functions
by complexity, duplication clusters, hotspot files (churn x
complexity), doc-coverage percentage - with file:line locations
so every number is actionable.

## Interpreting against conventions and tier

"Community conventions" is the catalog phrasing for a reason -
absolute thresholds are folklore, but working defaults exist:
complexity warnings commonly start around 10 per function,
duplication tolerance a few percent, doc coverage expectations
scale with audience. Calibrate by tier (rseng-quality-framework):
analysis code earns attention only for egregious outliers;
shared libraries justify gates; infrastructure justifies trend
tracking. State the convention being applied and why - an
unexplained threshold is just a different opinion.

## Gates and trends in CI

- Ratchet, do not ambush: set gates at the CURRENT values so
  metrics cannot regress, then tighten deliberately - a strict
  gate on a legacy codebase blocks all work and gets disabled
  within a week (the same start-where-you-are rule as
  rseng-fairguard's quality gates).
- Fail on new debt only where possible (changed-files scope), and
  keep the full-repo numbers as a tracked report, not a blocker
  (rseng-ci-cd).
- Trends beat snapshots: rising churn in a complex module is a
  refactoring signal (rseng-legacy-code, rseng-software-design)
  worth an issue, even when every absolute number still passes.

## Metric gaming, named

Every metric can be satisfied without improving anything:
splitting functions mechanically to duck a complexity gate,
deleting docstring checks instead of writing docstrings,
suppressing duplication detection with trivial edits. Flag the
pattern when reviewing (rseng-pair-programming's pre-review pass),
and keep metrics plural - a basket is harder to game than a
single number. The metric serves the change-cost reality, never
the reverse; when a metric and good judgment disagree, judgment
wins and the exception gets a comment.

## Working with this skill

This skill is source-independent: its authority is the tool
documentation and the published indicator definitions linked below.
It supplies the quantitative half of rseng-quality-framework
assessments; rseng-code-quality owns style and linting,
rseng-performance-profiling owns runtime measurement.

Learn more (verified):
  - https://radon.readthedocs.io - radon (Python complexity and
    maintainability)
  - https://github.com/terryyin/lizard - lizard multi-language
    complexity
  - https://github.com/kucherenko/jscpd - jscpd duplication
    detection
  - https://interrogate.readthedocs.io - interrogate docstring
    coverage

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-community-metrics - project-level counterpart to code metrics
- rseng-documentation - doc-coverage is its measurable slice
- rseng-legacy-code - hotspot map targets refactoring
- rseng-maintenance-sustainability - trend tracking signals sustainability risk
- rseng-quality-framework - supplies the quantitative half of assessments
- rseng-software-design - coupling numbers test the design

<!-- related-skills:end -->
