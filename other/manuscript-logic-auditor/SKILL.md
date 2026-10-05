---
name: manuscript-logic-auditor
description: Audit a manuscript, abstract, Results/Discussion section, or figure story for logic gaps, overclaims, missing controls, selective reporting, weak novelty, and reviewer-risk points. Use for 论文逻辑审计, 投稿前检查, manuscript audit, figure story check, novelty check, claim audit, reviewer risk, or when the user asks whether a paper is convincing.
---

# Manuscript Logic Auditor

## Purpose

Review a manuscript like a strict but constructive peer reviewer. This skill focuses on scientific logic, evidence boundaries, missing controls, figure story, and reviewer risk rather than surface grammar.

## Typical Inputs

- Abstracts, Results, Discussion, or full manuscript drafts.
- Figure legends or figure storyboards.
- Reviewer-risk questions before submission.
- Bioinformatics, clinical, biomedical, pharmacy, or AI-in-medicine manuscripts.

## Core Rules

- Do not rewrite weak evidence into strong claims.
- Do not fabricate missing controls, validation cohorts, citations, results, or mechanisms.
- Flag selective reporting of only positive results.
- Distinguish discovery from validation and association from causation.
- Keep tissue, cohort, platform, species, and data-source contexts separate.
- Recommend final human review and expert review before submission.

## Workflow

Use the audit dimensions below to review the manuscript and then return prioritized risks, claim-safe wording, and reviewer-ready next steps.

## Audit Dimensions

1. Central claim:
   - Is the claim explicit?
   - Is it supported directly by the evidence?
   - Is it too broad?
2. Study design:
   - discovery vs validation
   - retrospective vs prospective
   - public data vs local cohort
   - tissue/platform/species separation
3. Methods and controls:
   - negative controls
   - sensitivity analyses
   - multiple testing
   - effect sizes and uncertainty
   - missing covariates
4. Results logic:
   - all eligible datasets reported?
   - counterexamples discussed?
   - null findings retained?
   - figures match text?
5. Mechanism:
   - enrichment vs mechanism
   - correlation vs causation
   - cell-type interpretation boundaries
6. Novelty and journal fit:
   - what is genuinely new?
   - what is incremental?
   - what tier is realistic?

## Output Format

```markdown
# Manuscript Logic Audit

## Bottom Line
[2-4 sentence judgment]

## Major Risks
1. [risk, why it matters, fix]

## Moderate Risks
1. [risk, why it matters, fix]

## Figure/Result Story
[figure-by-figure or section-by-section comments]

## Claim-Safe Rewording
[defensible alternatives]

## Reviewer-Ready Next Steps
[ranked action list]
```

## Quality Checklist

- Overclaims are clearly marked.
- Missing controls are specific.
- Counterexamples and limitations are not hidden.
- Suggestions are actionable.
- The output is advisory and requires expert review.
