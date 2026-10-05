---
name: paper-review-panel
description: Use when independently reviewing a research-paper draft before submission, running a mock top-conference panel, assessing readiness or accept/reject risk, or predicting reviewer concerns for venues such as CVPR, ICCV, ECCV, ICLR, NeurIPS, and AAAI. Does not draft or audit author responses after official reviews arrive.
license: MIT
---

# Paper Review Panel

## Core Rule

This skill owns pre-submission paper review and readiness assessment. Review by
default. Do not edit the paper, mutate LaTeX, change figures, rerun experiments,
or patch files unless the user separately asks for implementation. The output
is an official-review-style synthesis plus compact revision priorities.

Once official reviews arrive, stop using this skill as the workflow owner. Use
`$rebuttal-response-skills` for exact concern mapping, evidence integration,
author-response drafting, and response audits.

## Workflow

1. Ground the review in artifacts.
   - Prefer the compiled PDF first when available; inspect layout, figures,
     tables, appendix, and references as a reviewer would see them.
   - Read the source text, bibliography, figure/table sources, logs, or result
     artifacts only as needed to verify claims and locate concrete anchors.
   - Use `$research-evidence` for citation/reference sanity checks or literature
     positioning when a review finding depends on external evidence.
   - For novelty, related-work, score-prediction, reviewer-risk,
     submission-readiness, or final-submission reviews, run a recent-literature
     audit through `$research-evidence` before finalizing novelty or acceptance
     risk. Do not require this extra pass for casual local or prose-only reviews
     unless novelty or missing citations are part of the ask.
   - If that audit is incomplete or source coverage is weak, state the coverage
     limit before assigning novelty confidence or acceptance risk.
   - If only a section is provided, label the result as a partial review and do
     not score the full paper as if all sections were available.

2. Apply the three-reviewer lens in the main review.
   - Reviewer 1: contribution, novelty, positioning, motivation, venue fit.
   - Reviewer 2: method, technical correctness, experiments, metrics, evidence.
   - Reviewer 3: writing, figures, tables, consistency, reproducibility,
     appendix, reviewer readability.
   - Read `references/reviewer-roles.md` for detailed role prompts.

3. Synthesize rather than concatenate.
   - Do not list reviewer lenses separately unless that helps diagnose the
     paper's risks.
   - Judge each concern independently: valid issue, clarity-induced
     misunderstanding, unsupported or incorrect reviewer claim, or optional
     polish.
   - Preserve concrete anchors such as section, page, table, figure, equation,
     appendix item, or source location whenever available.

4. Run a complexity and readability audit.
   - Check whether a reviewer can identify the central claim and its main table
     before encountering secondary ablations or diagnostics.
   - Require every non-standard metric and delta to define its measured
     quantity, aggregation population, unit, direction, and reference.
   - Treat duplicate terminology, opaque metric names, and diagnostic overload
     as acceptance risks when they make the evidence harder to verify.

5. Report in official-review style.
   - Use English by default.
   - Use venue-aware scoring when the venue is known. If unknown, use
     `Overall score 1-10` and `Confidence 1-5`.
   - End with score, confidence, acceptance risk, and compact revision
     priorities.
   - Read `references/output-format.md` before drafting the final synthesis.

## Review Standards

- Treat unsupported claims, weak baselines, missing ablations, protocol leakage,
  metric ambiguity, and inconsistent appendix/main-paper numbers as high-risk
  issues.
- Do not mechanically require repeated training seeds for expensive tasks.
  Accept single-run training when comparisons use the same budget, evaluation,
  and checkpoint-selection policy; request repeated seeds only when variance
  could change a central claim, the margin is small, runs are inexpensive, or
  the venue requires them.
- In work-in-progress reviews, treat `--` cells as structure only and do not
  credit them as evidence. In submission-readiness reviews, report unresolved
  placeholders as incomplete evidence and verify that no result claim depends
  on them.
- For dataset and benchmark papers, separate dataset contribution, protocol
  validity, reference baseline strength, and evidence that the benchmark tests
  the claimed capability.
- For method papers, separate novelty, technical correctness, implementation
  plausibility, ablation quality, and comparison fairness.
- Do not fabricate citations or assume experiments exist. If evidence is
  missing, mark the concern as a risk or requested evidence.
- For high-risk novelty or readiness judgments, do not rely on memory or the
  paper's current bibliography alone. Use `$research-evidence` to test direct
  and adjacent recent work, terminology variants, and source-coverage limits.
- If the literature check is partial, make the score or risk estimate
  conditional on that search coverage instead of presenting it as final.
- If a novelty, related-work, or citation-authenticity concern remains
  uncertain after checking, report the uncertainty as reviewer risk rather than
  treating the concern as proven.
- Read `references/review-checklist.md` for the full audit checklist.

## Reference Routing

- Read `references/reviewer-roles.md` for role-specific prompts and review
  lenses.
- Read `references/output-format.md` before writing the final review.
- Read `references/review-checklist.md` for deep or high-stakes readiness
  audits.
