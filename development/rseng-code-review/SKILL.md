---
name: rseng-code-review
description: >-
  Covers reviewing existing code and whole projects, not just new diffs:
  structured codebase audits that produce ranked findings and then implement
  the agreed improvements, recurring project reviews after major tasks and
  milestones, review scoping by risk and tier, and turning review findings
  into tracked work and lessons. Use PROACTIVELY after major tasks and
  milestones, and when the user asks for a code review, codebase audit or
  health check of existing code, wants improvements suggested and applied,
  mentions reviewing the project after a milestone or before a release or
  submission, or when inherited or long-unreviewed code needs a structured
  pass. For diff-time pre-review of new work see rseng-pair-programming; for
  PR-time review process and rules see rseng-version-control-review.
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Code and project review

Most review attention goes to new diffs; most risk lives in the
code nobody has looked at for a year. This skill covers the
retrospective forms: reviewing the EXISTING codebase with findings
ranked and then implemented, and reviewing the PROJECT on a
cadence - after milestones, before releases and submissions.
Division of labor: rseng-pair-programming owns diff-time pre-review
of new work; rseng-version-control-review owns the review process
and rules; this skill owns review as an undertaking on what is
already there. Review-then-implement is a two-phase contract:
findings first, agreement second, changes third - never silent
rewriting under the review's flag.

## The codebase review

Scope before depth - review the code that matters most:

1. Map risk: recently churned complex modules
   (rseng-software-metrics' hotspot map), result-bearing code paths
   (what feeds published numbers), security surfaces
   (rseng-security), and anything the tests do not reach
   (rseng-testing's coverage). Review THOSE deeply; skim the rest.
2. Sweep with the pack's lenses, each producing findings with
   file:line evidence: correctness and silent-failure modes
   (rseng-defensive-coding), numerical practice
   (rseng-numerical-accuracy), design and coupling
   (rseng-software-design), performance red flags on hot paths
   (rseng-performance-profiling), hygiene and dead code
   (rseng-code-quality), reproducibility hazards - unseeded
   randomness, unpinned environments, hidden state
   (rseng-reproducibility, rseng-notebooks).
3. Rank honestly: must-fix (wrong results possible, data loss,
   security), should-fix (maintenance debt with a price), and
   nice (style beyond the linter's remit). Tier calibrates the
   bar (rseng-quality-framework): analysis code is not reviewed to
   infrastructure standards.
4. Deliver findings BEFORE changing anything: the ranked report
   with evidence is the review; the user picks what gets
   implemented (defaults offered: all must-fix, should-fix by
   effort).

## Implementing the agreed improvements

- One finding, one commit: small reviewable changes referencing
  the finding (rseng-version-control-review), tests first or
  alongside for behavior-touching fixes - and characterization
  tests BEFORE touching anything load-bearing and untested
  (rseng-legacy-code's safety net; review of legacy code IS the
  legacy workflow).
- Behavior-preserving by default: refactors keep the tests green;
  anything that changes results is flagged loudly and decided by
  the human (the science is theirs - rseng-pair-programming's
  boundary).
- Re-run the full verification after the batch: tests, linters,
  metrics delta (rseng-software-metrics shows the improvement
  measurably - report before/after numbers).
- Route the residue: declined findings recorded with reasons in
  the decision log (rseng-project-tracking), recurring patterns
  into lint rules or checklists, and the transferable insights
  into LESSONS.md (rseng-lessons-learned).

## The recurring project review

After a major task, milestone or before a release/submission,
review the PROJECT, not just the code - a lightweight standing
agenda:

- Code: the codebase review above, scoped to what changed since
  last time plus one rotating deep-dive area.
- Quality posture: indicator walk (rseng-quality-framework),
  FAIR/security assessments re-run and deltas reported
  (rseng-fairguard, rseng-security).
- Records current: README and docs truthful (rseng-documentation),
  citation and contributor records match reality
  (rseng-citation-metadata), aidecl.yaml up to date
  (rseng-ai-declaration), tracker and milestones honest
  (rseng-project-tracking).
- Reproducibility spot-check: the one-command path still works
  from clean (rseng-reproducibility).
- Close the loop: findings become tracked tasks with owners;
  the review note (date, scope, findings, actions) goes into the
  project record - and the next review starts by checking the
  last one's actions landed.

Offer this review PROACTIVELY at natural moments - a milestone
just closed, a release is near - as a short menu ("want the
post-milestone review? code, records, repro - about 20 minutes"),
respecting a decline (rseng-trainer's consensual-offer rule).

## Review craft

The comment discipline from rseng-pair-programming applies
unchanged: evidence with every claim, reasons with every request,
blocking separated from preference, praise where it is earned -
and for research code, "what does this number correspond to
physically" remains a first-class review question
(rseng-research-integrity). Reviews are of code, never of authors;
findings in inherited code especially are archaeology, not blame
(rseng-lessons-learned's blame-free wording).

## Working with this skill

This skill is source-independent: it encodes structured
code-review practice applied retrospectively to research
software. It composes the pack's lenses into one undertaking and
feeds rseng-project-tracking and rseng-lessons-learned.

Learn more (verified):
  - https://google.github.io/eng-practices/review/ - Google
    engineering review practices
  - https://bssw.io/items?topic=peer-code-review - BSSW peer
    code review resources
  - https://conventionalcomments.org - conventional comments

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-fairguard - assessment reruns during milestone reviews
- rseng-legacy-code - characterization tests before implementing fixes
- rseng-lessons-learned - findings become recorded lessons
- rseng-project-tracking - findings become tracked tasks
- rseng-quality-framework - tier calibrates the review bar
- rseng-software-metrics - hotspot map scopes the review

<!-- related-skills:end -->
