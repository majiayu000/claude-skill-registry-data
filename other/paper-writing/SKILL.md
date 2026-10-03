---
name: paper-writing
description: Draft and revise evidence-grounded academic manuscripts with adaptable author preferences. Use for section writing, implementing structural edits, claim calibration, citation-integrated prose, prose cleanup, standalone review excerpts, and LaTeX template migration. Use paper-review for critique or author responses, and paper-figures-tables for final visual artifacts.
---

# Paper Writing

Produce the requested manuscript text or revision. Begin at the task's actual
scope: a supplied paragraph needs a local edit; a full paper needs a coherent
argument grounded in its available evidence. Apply relevant manuscript requirements
and choose editorial guidance for the task; author preferences remain adaptable.

## Select the Work

| Request | Start with | Return | Load when needed |
|---|---|---|---|
| Rewrite, shorten, translate, or polish supplied prose | The passage and requested change | Revised text; explain only material changes or unresolved facts | `references/academic-prose.md`; `references/prose-pattern-audit.md` for explicit formulaic-prose cleanup |
| Reduce over-defensive writing or self-undermining | The passage and available claim context | Direct, scoped prose retaining necessary qualifications | `references/over-defensive-writing.md` |
| Draft a section or contribution list | Section purpose, supplied findings/notes, surrounding claims | A usable section with evidence-bounded claims and explicit factual gaps | `references/section-drafting.md`; `references/introduction-framing.md` for gap/RQs |
| Organize an outline or revise several sections | Research question, evidence, existing manuscript if any | Argument outline or revised sections, according to the request | `references/writing-workflow.md`, `references/section-architecture.md` |
| Review or implement paragraph placement and cross-section structure | Draft, available evidence, requested scope or review plan | Located structural findings or completed edits, as requested | `../paper-review/references/argument-structure.md`; continue through `paper-review` for audit |
| Turn repository results into manuscript text | Relevant results, configurations, analysis records and outline | Evidence-supported Results and requested artifacts | `references/evidence-to-results.md` |
| Draft or revise a full paper | Available sources and intended contribution | Supported manuscript draft; track unresolved evidence and cross-section changes | `references/writing-workflow.md`, applicable section references |
| Write Related Work or repair citations | Allowed source corpus and comparison purpose | Source-supported synthesis or scoped citation repair | `references/related-work.md`, `references/citation-integration.md` |
| Prepare final manuscript prose | Current manuscript and verified submission requirements | Revised source plus relevant validation results and remaining blockers | `references/policy-integration.md`, `references/venue-adaptation.md` |
| Compile a standalone section for coauthor review | Main source, selected section, desired preview or portable package | Working excerpt PDF and necessary sources | `references/review-excerpts.md` |
| Prepare a template, migrate venues or package sources | Source manuscript/template and target requirements | Migrated source, compiled output and build notes | `references/template-migration.md` |
| Learn writing techniques from reference papers | Supplied papers and learning focus | Source-located decisions and applicable examples | `references/learning-from-papers.md` |
| Need a finished figure or table as part of writing | Claim and supplied data/content | Completed artifact through its owning skill, plus prose integration | `references/artifact-handoffs.md`, then `paper-figures-tables` |

Read `references/style-profile.md` when composing prose. Read
`references/priority-model.md` when sources or requirements conflict. The workflow
reference describes evidence handoffs and completion criteria for substantial
writing; it is not a checklist to load for every sentence edit.

## Evidence and Scope

- Preserve numbers, technical meaning, claim strength, causal status, terminology,
  citation attachment, and material limitations. Never invent results or support.
- Ground contributions in new knowledge or concrete artifacts; measurements,
  replications, negative results, and systematic syntheses can be contributions.
- Apply the existing source boundary: local polish uses existing evidence;
  an explicit closed corpus stays closed; literature completion or verification
  permits scoped public primary-source lookup and supported bibliography edits.
  Use `references/citation-integration.md` for that work.
- Keep missing facts explicit and continue the supported parts. Ask only when a
  missing decision controls the requested work; do not invent an author position.
- Preserve LaTeX commands, labels, citations, math, and macros unless their change
  is within scope. Keep internal paths and validation logs outside paper prose.
- Improve clarity without detector scores, invented human signals, or claims
  about authorship inferred from style. Check semantic drift after cleanup.
- For characterized systematic bias, preserve its supported direction or explicit
  indeterminacy. Keep distinct evidence roles from silently supporting stronger
  claims. Read the method/results guidance when those issues apply.

## Policy and Validation

Use `references/policy-integration.md` to choose the validation depth. Ordinary
writing applies the relevant constraints without requiring a context file,
registry run, or readiness assessment. Resolve machine-readable policy for an
explicit policy task, a complex rule conflict, or formal submission validation.
An existing policy context can be reused after checking that it describes the
current task; its existence alone does not require a full audit.

Check the changed claims, values, citations, and local context before delivery.
Compile modified LaTeX when a buildable project is available and inspect the
render where the edit can affect layout. A text-only edit cannot establish PDF
readiness. A formal submission-ready claim requires `paper-policy` evidence
assessment, including its source-snapshot and manual-check boundaries.

## Authorized Work and Workspace

A writing request authorizes its necessary reversible local edits. Internal
handoffs continue in the same task; a spec is the endpoint only when the user
asked for a spec. Audit-only requests remain read-only. Use
`../paper-policy/references/authority-model.md` for authorization conflicts.

Before persistent manuscript edits, check for `PROJECT-WORKSPACE.md` at the
selected research-project root. Inside an independent paper Git repository,
resolve `.research-workspace.yml` without searching beyond its Git boundary.
If a valid contract resolves, use its declared paper repository and keep
experiment records and data in their designated locations. Otherwise use the
normal writing workflow; a prose task does not require workspace initialization.

## Delivery

Return the requested prose or files, relevant verification, and material gaps.
For revisions, identify substantive claim or structure changes; for audit-only
requests, provide exact suggested replacements without applying them. Keep
ordinary preference choices out of a per-rule compliance report. Reuse existing
notes when continuity matters; do not manufacture empty workflow documents.
