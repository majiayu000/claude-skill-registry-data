---
name: paper-review
description: Review an author's manuscript, its argument and paragraph structure, analyze reviewer comments, draft rebuttals, and verify revisions. Use for self-review, structural edit plans, simulated reviewer objections, author responses, revision closure, and submission-readiness assessment. Formal assigned peer review is outside this skill; manuscript edits and final figures/tables use their owning skills.
---

# Paper Review

Support the author in improving a manuscript and answering its reviewers.
Produce evidence-anchored findings, usable responses, or verified revision
status according to the request. Author preferences remain editorial guidance.
Formal assigned peer review is outside this skill and awaits a separate workflow.
Do not treat an author's request for self-review as a formal reviewer assignment.

## Select the Work

| Request | Needed inputs | Deliverable | References |
|---|---|---|---|
| Check a paragraph, section, or selected concern | Supplied text and available supporting material | Located issues, what can stay, and exact replacements when useful | Relevant dimensions in `references/pre-submission-audit.md` |
| Audit the author's manuscript | Current manuscript and requested focus | Prioritized findings with support and bounded fixes | `references/pre-submission-audit.md`; `references/issue-board.md` for substantial issue sets |
| Review paragraph necessity, argument order, or cross-section repetition | Draft and available supporting evidence | Argument map, located paragraph decisions and information destinations | `references/argument-structure.md` |
| Simulate reviewer objections | Current draft and supplied evidence | Clearly labeled simulated perspectives and actionable synthesis | `references/reviewer-panel.md` |
| Analyze external reviews | Actual comments and manuscript where available | Concern-to-evidence mapping, priorities, and response options | `references/issue-board.md`, `references/rebuttal-strategy.md` |
| Draft or polish an author response | Comments, available evidence, approved decisions, length limit if known | Response draft, unresolved evidence, and honest commitment status | `references/rebuttal-drafting.md`; `references/revision-plan.md` for promised edits |
| Verify a revision | Relevant comments/promises and current revised files/results | Completed, pending, deferred, or unsupported items with locations | `references/revision-plan.md` |
| Decide whether further revision is warranted | Inspected manuscript, remaining issues and prior attempted fixes | Scoped closure judgment and any concrete remaining work | `references/revision-closure.md` |
| Assess submission readiness | Current manuscript, verified requirements, available compliance evidence | Evidence-backed readiness result and remaining blockers | `references/policy-compliance.md`, `references/quality-gates.md` |

Read `references/review-modes.md` for ambiguous modes or structured context
values. Load `references/citation-and-evidence-policy.md` when source access or
citation support needs resolution. Load only the quality checks relevant to the
requested deliverable; a local critique does not require a full policy audit.

When substantial structure is in question, inspect it before line-level prose
cleanup. After a substantial review or revision, use `references/revision-closure.md`
to explain whether further work is needed. Scope the conclusion to the inspected
material; editorial closure does not establish submission readiness.

For over-defensive or formulaic prose, read the applicable
`../paper-writing/references/over-defensive-writing.md` or
`../paper-writing/references/prose-pattern-audit.md`. Assess what can stay as well
as what needs changing; style findings remain contextual suggestions.

## Review Discipline

- Anchor criticisms to the manuscript, a reviewer comment, supplied evidence, or
  a precisely described absence. Distinguish an observed defect from a concern
  that cannot be assessed with the available material.
- Prioritize scientific substance, evidence boundaries, and reader misunderstanding.
  Do not prescribe experiments for issues resolved by clearer or narrower claims.
- Preserve numbers, uncertainty, causal status, terminology, material limitations,
  and distinct evidence roles. A supported bias direction must remain explicit;
  use indeterminacy when its direction cannot be established.
- Check novelty against identified comparators; missing access does not establish
  absence of prior work. Follow existing local/closed-corpus boundaries; scoped
  public source verification is permitted when the request includes it. Keep
  confidential text out of external services.
- Distinguish substantive findings from adaptable structure or style advice.
  A comparison table, traditional heading, or specific typography is not required
  solely by personal preference. Never infer authorship from style or detector scores.
- For responses, cover every supplied concern, including deferred items and reasons.
  Do not invent reviewer comments, evidence, experiments, or completed revisions.
  Use `scripts/count_rebuttal_limit.py` when an actual word/character limit applies.
- For revision verification, inspect the current source or artifact for every
  claimed completed change. A plan or response promise is not completion evidence.
- Simulated perspectives do not establish independent reviewer agreement or real
  editorial outcomes. Use additional agents only when separately authorized.

## Scope, Policy, and Handoffs

Ordinary self-review returns findings without assigning global readiness. Run
`references/policy-compliance.md` for an explicit compliance/readiness judgment
or when that validation is part of the requested delivery. An existing context
file or a manuscript's submission stage does not itself expand a local task.

Formal compliance assesses applicable manuscript requirements. Keep missing
semantic/manual evidence `UNVERIFIED`; agent semantic PASS requires source-bound
evidence, and manual checks retain their human/user/venue boundary. Deterministic
FAIL takes precedence. See `../paper-policy/references/compliance-schema.md`.

An audit-only request is read-only. A request to fix the identified issues
already authorizes necessary scoped edits: load `paper-writing` for manuscript
prose or `paper-figures-tables` for artifacts and complete them in this task.
This skill owns rebuttal prose. Use
`../paper-policy/references/authority-model.md` for authorization conflicts.
Draft delivery does not authorize external submission, contact, or publication.

## Delivery

Return the requested critique, response, or verification result. A small task
may use a short list; a large review can use issue cards. Include exact locations,
priorities, concrete fixes, evidence gaps, and relevant checks. State what was
actually inspected. Avoid mandatory empty ledgers, simulated scores unless
requested, or a policy-status dump for an ordinary prose review.
