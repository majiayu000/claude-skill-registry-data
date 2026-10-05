---
name: runpro
description: Execute a project from a folder of raw materials. Use when the user drops messages, screenshots, documents, drafts, and references into a project directory and wants Codex to identify the real goal, build a plan, do the work, drive the project to a submission-ready state, verify completion, and return a clear final summary of what was required, what was completed, and how it was done.
---

# Project Folder Executor

## Mission

Turn a messy project folder into a finished, reviewable, or submittable result. RunPro owns intake, requirement reconstruction, feasibility, requirement lock, execution, remediation, actual-file validation, clean delivery, and final reporting. It is not a summary-only skill.

Default interaction:

1. infer everything safely recoverable from the folder
2. ask only about high-impact ambiguity
3. lock requirements with the user before full execution
4. execute the complete locked scope
5. continue until every applicable gate passes or a true blocker remains
6. return the result by default, with concise evidence

## Non-Negotiable Quality Contract

Quality gates may be consolidated, but never weakened, skipped, converted to a one-line self-approval, or marked not applicable merely to save time or tokens.

The following invariants always control:

- complete all required parts; do not trade coverage for polish
- preserve exact local rules, templates, rubrics, prohibitions, output format, and submission mechanics
- validate claims, sources, citations, calculations, layout, native files, and student-facing residue in visible final text whenever relevant
- use the actual final artifact for layout-sensitive and residue checks
- remediate every fixable failure, then rerun affected checks
- use the lower credible score estimate when plausible estimates conflict
- separate verified fact, inference, and untested limitation
- never claim an external grade is guaranteed
- never hand off with a stale or missing quality receipt in strict mode

For high-achievement work, the target is a submission plausibly capable of `90+` under the real grading standard. `90+ plausible` is allowed only when the conservative lower bound is at least 90, all central criteria pass, and no fixable weakness remains. Otherwise continue remediation or report a true blocker.

## Exact Local Rules

For school, university, course, workplace, client, funding-body, journal, conference, or platform submissions, local sources override generic conventions. Inspect assignment briefs, rubrics, marking grids, handbooks, module guides, tutor feedback, lecture slides, examples, templates, citation guides, word-count policies, academic-integrity rules, portal instructions, screenshots, filenames, and user comments when present.

Extract each local requirement separately into `requirement-ledger.md`, including task wording, learning outcomes, topic boundaries, structure, section order, word-count inclusions/exclusions, citation variant, source limits, voice, format, template behavior, integrity declarations, filenames, export type, and package contents. Use the newest assignment-specific source first, then course/module authority, institutional authority, and only then generic convention.

For cohort topic selection, also check collision risk with class examples, classmates, previous work, assignment-suggested defaults, and likely generic-AI choices. Prefer a specific, source-sufficient, locally relevant, analytically rich topic. Record rejected defaults and reasons; never sacrifice evidence or requirement fit merely to be unusual.

Read [academic-format-policy.md](./references/academic-format-policy.md) for any graded academic, source-backed, citation-sensitive, or local-rule-bound assignment.

## Strict Mode

Enter strict mode automatically when any of these apply:

- graded essay, paper, proposal, literature review, formal report, or similar submission
- source-backed or literature-backed work
- explicit rubric, template, form, format, or local rule
- `90+` or comparable high-achievement target
- native `.docx`, `.pptx`, PDF, spreadsheet, code, data, or exported-file correctness matters
- a false readiness claim would materially harm the user

Standard mode is only for genuinely low-risk work. It still requires relevant checks.

Strict mode is fail-closed:

- skipped, unknown, stale, unsupported, or narrative-only gates do not pass
- failed validators trigger remediation, not handoff
- unavailable material checks become explicit limitations or blockers
- central requirements need item-level evidence, not “covered overall”
- audit sections must be substantive; one-line “pass” statements are invalid
- after any final artifact or control-file change, final validation must run again

## Context-Efficient Operating Model

Reduce repeated context, not verification depth.

- Read this file once per invocation.
- Bootstrap once. Rebuild inventory/routing only if source files or scope changed.
- After approval, treat `approval-gate.md`, `requirement-ledger.md`, and route-specific ledgers as the active contract; do not repeatedly reload unchanged general rules.
- Load only the references selected by the route map below. Do not reload a reference unless the route, source, failure, or locked requirement changed.
- Update state on phase transitions, requirement changes, meaningful repairs, and final validation—not after every micro-action.
- Batch independent inspections and use concise tool output. Save detailed evidence in project state files.
- Use one planned create/render/inspect/repair cycle, then rerun only affected checks, followed by the final centralized chain.
- Reuse a current hash-bound quality receipt for handoff verification. Never reuse it after any hashed file or validator changes.

Efficiency never authorizes shallower research, fewer rubric checks, weaker source validation, skipped visual inspection, omitted deliverables, or optimistic score claims.

## Reference Routing

Load references progressively:

| Situation | Required reference |
|---|---|
| phase status or stop condition | [execution-gates.md](./references/execution-gates.md) |
| state-file purpose/schema | [project-state-files.md](./references/project-state-files.md) |
| document or written artifact | [document-branch.md](./references/document-branch.md) |
| graded/source-backed/citation/local-rule work | [academic-format-policy.md](./references/academic-format-policy.md) |
| slide deck or presentation | [presentation-branch.md](./references/presentation-branch.md) |
| code/software | [code-branch.md](./references/code-branch.md) |
| data/spreadsheet/analysis | [data-branch.md](./references/data-branch.md) |
| mixed deliverables | [mixed-branch.md](./references/mixed-branch.md) plus each applicable branch |
| uncertain route | [adaptive-branch.md](./references/adaptive-branch.md) |
| final failure/remediation | [remediation-loop.md](./references/remediation-loop.md) |
| final manual audit | [final-checklist.md](./references/final-checklist.md) |
| truth/status language | [truthfulness-policy.md](./references/truthfulness-policy.md) |
| collaboration or output mode needed | [collaboration-framework.md](./references/collaboration-framework.md), [output-modes.md](./references/output-modes.md) |

Use [efficiency-policy.md](./references/efficiency-policy.md) only when choosing between equally reliable execution paths. Use [routing-matrix.md](./references/routing-matrix.md) only if generated routing is ambiguous.

## Required Workspace

Run:

```bash
python3 <runpro-skill>/scripts/bootstrap_project.py <project-root>
```

Keep all RunPro process files under `runpro_workspace/`. Keep only actual required final submission files in `runpro_workspace/submission/`. Drafts, source materials, audits, templates, previews, helper exports, and duplicates stay outside `submission/`. If a written final format is not specified, default to `.docx`. Missing submitter identity fields remain blank unless the user supplied them.

The existing state-file set remains the compatibility contract. Do not delete state files to reduce context. Use them selectively as described in [project-state-files.md](./references/project-state-files.md).

## Gate 1 — Reconstruct and Inventory

1. Inventory the folder, including screenshots and attached images.
2. Identify authoritative instructions, rubrics, templates, source material, drafts, exemplars, and final-output expectations.
3. Classify each important file by purpose; do not assume all images or documents belong to the same assignment part.
4. Separate confirmed facts, safe inferences, unsupported assumptions, and missing inputs.
5. Build `requirement-ledger.md` with one item per content, structure, format, prohibition, local-rule, and submission requirement.
6. For graded written work, build `rubric-ledger.md` before full drafting. If no rubric exists, mark it `rubric-inferred` and record the limitation.
7. For source-backed work, begin `source-log.md`; for source-backed written work, maintain `source-claim-audit.md`; for source-backed presentations, create `source-visual-inventory.md` before final slide drafting.

## Gate 2 — Feasibility and Requirement Lock

Write `feasibility-check.md` with one verdict:

- `Can Complete`
- `Can Complete With Recoverable Gaps`
- `Cannot Complete Yet`

Do not call missing essential instructions, templates, data, forms, or core sources recoverable when they are not. Missing identity fields alone are not blockers.

Populate `approval-gate.md`, including the full `Validation Profile` generated by bootstrap. Every profile key must be explicit; no `pending` value may remain. The profile is a machine-checked list of all applicable gates and their parameters. Do not set a gate to `no` merely because it is costly. The centralized validator rejects contradictions such as `90+` with no 90+ gate, graded written work without rubric/academic/CheckPro checks, source-backed work without source gates, local submissions without local-rule audit, or polished presentations without PPTPro.

Before requesting confirmation, run:

```bash
python3 <runpro-skill>/scripts/validate_requirement_lock.py \
  runpro_workspace/10_analysis/approval-gate.md \
  --require-validation-profile
```

Ask for confirmation only when the user has not already explicitly approved the reconstructed plan. Confirmation must cover scope, required parts, format/template, quality target, strict/standard mode, allowed inference, and unresolved material choices. After confirmation, record it and run with `--require-approved --require-validation-profile`.

If the locked direction changes materially, stop, update the lock/profile, and obtain renewed confirmation.

## Gate 3 — Execute the Complete Scope

Create an early skeleton, then a complete usable version, then polish. Work against the locked ledgers, not memory. Preserve supplied templates and partial-scope boundaries exactly.

Apply every relevant route branch. For formal graded academic writing, invoke `checkpro` before final handoff and record substantive evidence in `CheckPro Execution Evidence`; if unavailable, perform the equivalent audit and state that limitation. The audit must cover prompt/rubric alignment, analytical purpose, evidence quality, synthesis, limitations/counterarguments, source-claim integrity, empirical precision, theory/framework application, visual/table integration, repetition control, citation specificity, academic register, and conclusion discipline.

For presentations requiring high visual quality, invoke `pptpro`, preserve template and partial-scope boundaries, inspect rendered previews, and run its strict native deck audit. Source-backed decks require verified source logs, source-visual candidates with selection/rejection rationale and provenance, human-facing source language, and slide/script correspondence when a script exists.

Use native authoring tools for native deliverables. Validate the real output, not only source text or generation code.

## Gate 4 — Route-Specific Validation

Run route checks during execution when they give useful repair feedback:

- documents: content completeness, word count, headings, citations, references, tables/figures, pagination, headers/footers, template rules, and actual rendered layout
- academic work: rubric, exact local citation authority, academic standards, source claims, argument quality, citation micro-defects, local rules, and conservative score risk
- presentations: slide count/order, overflow, overlap, typography, visual hierarchy, provenance, references/source separation, preview inspection, script mapping, and final native deck
- code: build, tests, lint/type checks, key runtime flows, configuration, and documented untested limits
- data: schema, row counts, formulas, joins, missingness, units, outliers, reproducibility, and output integrity
- mixed work: cross-file consistency, naming, references, package completeness, and each component's native checks

Passing a validator does not replace human judgement or visual inspection. Human judgement does not replace a deterministic validator when one exists.

## Gate 5 — Final Audit and Central Validation

Complete `final-audit.md` with evidence-bearing sections required by the locked profile. Every requirement verdict must have a final status and location/evidence. `Estimated Score Band` must use the conservative lower reading. `Ready to submit` is forbidden while any central item is partial, failed, not assessable, unresolved, pending, stale, or still has a fixable remediation action.

Complete `final-summary.md` before centralized validation. Because strict validation hashes the state and submission files, do not edit either after a PASS unless you rerun validation.

Run the single final entry point after the last content, format, export, or package change:

```bash
python3 <runpro-skill>/scripts/runpro_validate.py <project-root>
```

This command fail-closes and consolidates:

- approved requirement lock and complete validation profile
- final requirement-ledger statuses
- 90+ threshold enforcement
- rubric, academic standards, source-claim, academic-quality, citation, local-rule, presentation-source, CheckPro-evidence, and residue audit sections as applicable
- source-log and source-visual validators as applicable
- actual supported submission-artifact residue scanning
- PPTPro `--render --strict` audit as applicable
- SHA-256 binding of control files, final artifacts, and validator versions into `quality-receipt.json`

After any later change, rerun the full command. Immediately before handoff, verify freshness:

```bash
python3 <runpro-skill>/scripts/runpro_validate.py <project-root> --check-receipt
```

Do not manually create, edit, or claim a passing quality receipt.

## Gate 6 — Remediation

When a check fails:

1. record the exact issue, impact, and affected requirement
2. choose the smallest repair that preserves all locked requirements
3. repair the source and regenerate the actual artifact when needed
4. rerun affected route checks
5. rerun centralized final validation after the last change

Do not endlessly rewrite unaffected content. Do not stop because the first draft is acceptable. Stop only when all applicable gates pass or further progress requires new authority/material and a true blocker is recorded.

## Gate 7 — Clean Handoff

Before handoff:

- review [final-checklist.md](./references/final-checklist.md)
- confirm `submission/` contains only required final files
- verify the quality receipt is current
- confirm `final-summary.md` was completed before the last centralized PASS
- state exactly one status: `Ready to submit`, `Ready for review`, or `Blocked`
- name the deliverables and summarize validation performed
- state remaining limitations without overstating certainty

Do not expose process files as deliverables. Keep the final response concise; the workspace contains the detailed evidence.

## Script Map

- `bootstrap_project.py`: initialize workspace, inventory, routing, and state templates
- `validate_requirement_lock.py`: validate lock, approval, and validation profile
- `validate_requirement_ledger.py`: require final item-level statuses and evidence
- `validate_final_audit.py`: enforce substantive audit sections and score/readiness logic
- `validate_source_log.py`: validate source count and optional recency ratio
- `validate_source_visual_inventory.py`: validate presentation visual candidates and provenance
- `scan_student_facing_residue.py`: inspect supported final artifacts for workflow/tool/prompt/prior-task residue
- `runpro_validate.py`: centralized final gate and hash-bound quality receipt

The scripts enforce minimum evidence. They do not authorize shallow work that merely contains marker words.
