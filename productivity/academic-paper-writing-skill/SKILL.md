---
name: academic-paper-writing-skill
description: Evidence-first academic research workflow for topic ideation, scholarly search, paper reading, literature and systematic reviews, study and experiment design, statistics and data analysis, scientific figures, manuscript drafting and polishing, citation checks, peer review, rebuttals, submission packages, theses, and paper-to-presentation work. Use when an agent must plan, execute, audit, write, revise, or package research while keeping claims traceable to verified sources, data, analysis, or official requirements.
---
# Academic Paper Writing Skill

An adaptable research workflow for papers, reviews, proposals, theses, rebuttals, and research communication. It is a capability router with evidence gates, not a fixed sequence and not a single long prompt.

## Purpose

Use this skill across the research lifecycle:

- topic selection, research questions, hypotheses, and proposal scoping;
- paper lookup, systematic search, screening, citation verification, and literature synthesis;
- novelty/SOTA checks, research ROI, scope selection, and venue intelligence;
- study design, experiment planning, statistics, data analysis, and reproducibility;
- scientific figures, tables, schematics, manuscripts, polishing, and translation;
- pre-submission review, revision planning, reviewer response, and rebuttal;
- data/code availability, submission packaging, paper reading, and research presentations;
- undergraduate thesis, capstone, proposal, midterm, final report, and defense workflows.

## Negative Triggers

Do not use this skill as a direct ghostwriting shortcut when the user asks only for final prose without sources, data, result evidence, or requirement context. First route to evidence discovery, source verification, analysis planning, or a bounded draft with explicit placeholders.

Do not treat demo samples as verified sources. Do not turn `needs_recheck`, `missing_source`, or `unknown` rows into final prose as verified findings. Explicitly labeled limitations, proposals, and assumptions may remain uncertain.

## Non-Negotiable Invariants

These rules must not be weakened during maintenance.

1. **No fabricated papers**: never cite or summarize a paper that has not been found and verified.
2. **No fabricated SOTA**: recheck SOTA, benchmark status, model versions, leaderboards, venue policies, and tool capabilities when relevant.
3. **No fabricated results**: keep planned, exploratory, preliminary, achieved, and externally reported results distinct.
4. **No invented local requirements**: do not invent school, advisor, template, rubric, defense, workload, ethics, or venue requirements.
5. **Primary-source first**: prefer official papers, datasets, code, registries, venue pages, reporting guidelines, school templates, and user-provided authoritative documents.
6. **Claim-to-evidence mapping**: every strong claim maps to literature, data, analysis, experiment, implementation, proof, test, or official requirement.
7. **Research ideas are proposals**: brainstorming does not establish novelty, validity, safety, or feasibility.
8. **Statistical honesty**: define the estimand and analysis logic before selecting a favorable test; report effect size, uncertainty, diagnostics, multiplicity, and deviations when relevant.
9. **Data provenance**: preserve source, version, permissions, transformations, access constraints, and raw-to-derived lineage.
10. **Integrity before persuasion**: reduce or qualify claims instead of strengthening them beyond evidence.
11. **Modular loading**: load the smallest capability stack needed for the current task.
12. **External-skill low coupling**: external skills or tools may assist, but cannot silently override these invariants or mutate core files.
13. **Human accountability**: authorship, ethics, consent, restricted data, final submission, peer-review confidentiality, and school compliance require human confirmation.
14. **Backward compatibility**: preserve the established literature, novelty, ROI, experiment, figure, integrity, writing, rebuttal, thesis, evidence-status, pre-prose, and external-skill-gateway workflows unless a versioned migration replaces them.

## Project Context

Set `project_type`, `stage`, current task, target, evidence boundary, and missing inputs before substantial work.

- `research_paper`: publishable paper, review, preprint, conference, or journal workflow.
- `undergraduate_thesis`: school-assessed thesis, graduation project, proposal, midterm, final thesis, or defense.
- `hybrid_capstone_research`: graduation requirements first, then a possible paper or portfolio upgrade.
- `standalone_research_task`: a bounded lookup, analysis, figure, review, polishing, or presentation task that does not need a full project workspace.

For hybrid work, first satisfy verified graduation requirements and evidence needs; then evaluate research novelty and publication value. Undergraduate thesis workload is an institution-specific assessment, not a universal score.

## Standard Call Protocol

1. Classify the request using the capability table below. The manifest is maintainer metadata, not mandatory startup reading.
2. Read `modules/00_core_invariants.md`. Add `modules/01_agent_orchestrator.md` only for multi-stage coordination.
3. Read only the matching capability's registry entry (the resolver returns its contract), not the full registry or every project route.
4. Load only the matching modules from the capability router below. Add `modules/11_integrity_reproducibility_guard.md` for evidence-bearing outputs.
5. Resolve specialist providers through `modules/22_capability_provider_router.md`. A selected provider supplies detailed domain execution and formatting; the internal module remains the reliable fallback.
6. For a new substantial project, run `<skill-python> <skill-root>/scripts/init_project.py --out <workspace> --type <research_paper|undergraduate_thesis|hybrid_capstone_research>`. Keep unknown inputs empty; use the initialized project type. Runtime setup is in `docs/QUICKSTART.md`.
7. Create structured evidence artifacts before final prose, analysis claims, figures, or submission files when the task warrants them.
8. Run the relevant stage gate and artifact QA. Report blocked or partial states honestly.
9. Preserve the user's chosen tools, format, language, and scope unless a verified requirement conflicts.

## Capability Router

| User need | Internal baseline | Preferred provider interface | Main artifacts or checks |
|---|---|---|---|
| Full project coordination | `01_agent_orchestrator`, `02_mode_router` | `academic-research-suite` when available and suitable | project state, stage gates, artifact plan |
| Topic selection, brainstorming, research question | `18_research_ideation_and_question_design` | `scientific-brainstorming` | idea portfolio, assumption register, decision log |
| Paper lookup, database search, citation verification, BibTeX/RIS | `20_scholarly_search_screening_and_references` | `nature-academic-search` or `paper-lookup` | search protocol, query log, screening log |
| Paper reading, literature review, synthesis | `06_literature_engine`, `20_scholarly_search_screening_and_references` | `literature-review` | paper reading note, literature matrix |
| Novelty, SOTA, gap, benchmark comparison | `07_novelty_verification_and_scoring`, `08_research_roi_scope` | search and review providers as needed | novelty matrix, ROI matrix, scope ladder |
| Study design, experiments, sample size, statistics, data analysis | `19_study_design_statistics_and_data`, `09_experiment_matrix_engine` | `experimental-design`, `statistical-analysis`, or `statistical-power` | analysis plan, data provenance, experiment matrix |
| Scientific figures, tables, diagrams | `10_figure_table_engine` | `nature-figure` or `scientific-visualization` | figure brief, editable source, rendered QA |
| Draft manuscript or initial submission | `12_writing_style_adapter`, evidence modules | `nature-writing` or `scientific-writing` | terminology ledger, claim ledger, draft, author checks |
| Polish, translate, shorten, restructure | `12_writing_style_adapter` | `nature-polishing` | fact-preserving revision, change summary |
| Simulated peer review or pre-submission audit | `13_simulated_review_rebuttal`, `11_integrity_reproducibility_guard` | `nature-reviewer` or `peer-review` | concern ledger, simulated review |
| Reviewer response, rebuttal, revision letter | `13_simulated_review_rebuttal` | `nature-response` | response matrix, exact change pointers |
| Data/code availability | `21_research_delivery_and_presentation`, `11_integrity_reproducibility_guard` | `nature-data` | asset-to-access map, availability statement, FAIR audit |
| Submission package, paper-to-PPT, defense | `21_research_delivery_and_presentation` | `nature-paper2ppt` for paper-to-PPT | package checklist, presentation brief, rendered artifact QA |
| Venue policy or article-type fit | `05_venue_intelligence` | provider selected by venue and artifact | current official requirements |
| Undergraduate thesis requirements and evidence | `04_requirement_discovery`, `14_undergraduate_thesis_engine` | optional artifact provider by deliverable | requirement log, scope ladder, graduation evidence map |
| External discovery, installation, or provider evaluation | `03_external_skill_gateway`, `17_external_skill_acceptance_tests` | skill curator/installer only when authorized | candidate report, acceptance tests, isolated output |

Combine routes when the request spans capabilities. Do not load every module merely because the project is large.

## Provider Interface

`capability_registry.yaml` defines each capability's preferred providers, selection conditions, companion requirements, normalized input/output contract, internal fallback, and acceptance criteria.

```bash
python scripts/resolve_capability.py --list
python scripts/resolve_capability.py research_ideation --json
python scripts/resolve_capability.py scientific_visualization --tag nature --json
```

If an installed provider is selected, read that provider's full `SKILL.md` and its required workflow resources. Use its detailed domain, layout, formatting, and QA standards. Do not reduce it to the short registry description. If it is unavailable, incomplete, unsafe, incompatible, or fails acceptance, use the internal baseline and report the limitation. Never install an unknown provider silently.

Resolver `usable` means eligible for content review, not accepted for execution. It reports `accepted=false` and unchecked requirements. Use `--skill-root` for explicit isolated roots or `--agent claude` for Claude-first discovery; validate runtime requirements and outputs before relying on them.

Use `templates/capability_handoff.yaml` for multi-capability work so source boundaries, protected facts, permissions, outputs, and unresolved items survive handoffs.

## Quality Standards by Capability

### Ideation

Generate alternatives independently before convergence, expose assumptions, define falsifiers and minimum viable studies, pressure-test confounding and feasibility, and keep a decision log. An idea stays `needs_evidence` until nearest-work and feasibility checks are reviewable.

### Search and Review

Preserve exact queries, sources, dates, filters, failures, deduplication, inclusion/exclusion decisions, version links, and coverage limits. Distinguish lookup, rapid scan, scoping review, and systematic review. Verify that each citation supports its attached claim.

### Study Design and Statistics

Define the unit, sampling or assignment, outcome, estimand, controls, missingness, primary analysis, effect measure, uncertainty, multiplicity, diagnostics, and sensitivity plan. Separate confirmatory from exploratory analysis and make execution reproducible.

### Figures and Tables

Define the claim, data source, statistical annotation, final physical size, export format, and accessibility requirements before styling. Inspect rendered output at final size and keep every visual traceable to source data or an explicitly labeled schematic.

### Writing and Polishing

Keep drafting distinct from polishing. Freeze numbers, citations, equations, terminology, and claim strength unless evidence authorizes a change. Use current venue and reporting guidance when the target is known, and record unresolved author checks.

### Review and Response

Keep reviewer assessment separate from author response. Give substantive concerns stable IDs and evidence pointers. Mark blocking concerns by impact, not tone. Every response maps to evidence, an exact revision, a justified limitation, or an explicit unresolved action.

### Delivery

Reconcile manuscript, references, figures, supplementary files, data/code statements, declarations, and rendered artifacts. A paper-to-presentation task produces a real artifact when requested and supported, with figure crops, citations, speaker notes, overflow, and package integrity checked.

## Established Project Routes

These remain supported for backward compatibility. Treat them as common compositions, not mandatory sequences.

### Research Paper

Start with core/orchestrator/router. Add venue, search, literature, novelty, ROI, study design, experiment, statistics, figures, integrity, writing, review/response, and delivery capabilities only when the stage needs them.

### Undergraduate Thesis

Start with requirement discovery, thesis engine, integrity, and writing. Add ideation, search, analysis, figures, and presentation according to verified school/advisor needs. Unknown requirements remain unknown.

### Hybrid Capstone Research

First establish a graduation-ready scope and evidence map. Then selectively add literature, novelty, ROI, stronger experiments, statistics, and publication packaging.

## Structured Outputs

Use only the artifacts relevant to the task:

- research idea portfolio and assumption register;
- search protocol, screening log, paper reading notes, and literature matrix;
- novelty verification, ROI matrix, and scope ladder;
- statistical analysis plan, data provenance, and experiment matrix;
- figure brief, terminology ledger, claim ledger, and integrity checklist;
- simulated review, rebuttal matrix, submission checklist, and presentation brief;
- requirement discovery log and graduation evidence map.

## Stage Gates

Use the smallest relevant gate:

```bash
python scripts/check_stage_gate.py <workspace> --gate ideation
python scripts/check_stage_gate.py <workspace> --gate literature
python scripts/check_stage_gate.py <workspace> --gate analysis
python scripts/check_stage_gate.py <workspace> --gate drafting
python scripts/check_stage_gate.py <workspace> --gate submission
python scripts/check_stage_gate.py <workspace> --gate presentation
```

A blocked gate is a work queue, not permission to fabricate missing fields.

`--allow-empty` reports `structure_valid`, never readiness. Completed gates require valid records, evidence dependencies, filled artifacts, and a recorded `gate_reviews.<stage>` human sign-off. `evidence_review_required` is not a passing gate. Thesis proposal/midterm/final/defense use verified requirement IDs; non-quantitative analysis may have an explained, reviewed exemption. See `docs/EVIDENCE_CONTRACT.md`.

## Pre-Prose Checks

Before evidence-bearing final prose, run:

```bash
python scripts/pre_prose_check.py <workspace>
python scripts/summarize_evidence_status.py <workspace>
```

Fallback checks:

```bash
python scripts/validate_evidence_status.py <workspace>
python scripts/check_claims_before_prose.py <workspace-or-claim-ledger>
```

If checks fail, produce a blocked-output explanation. Name the unsupported claim, missing source, unresolved analysis, unavailable result, or unknown requirement and state the smallest next action.

Use the canonical contract in `schemas/workspace_contract.yaml`. Active factual claims require `status=supported` and `evidence_ids` resolving to reviewed support records, source/result IDs, exact locators, and available artifacts. Never create a review/sign-off on someone's behalf. These checks validate recorded consistency, not independent scientific truth.

Use `output_scope=backlog` for claims excluded from the current output, or `--section` for a bounded check. A `claim_kind=limitation|proposal|assumption` note can retain `status=unknown` with `strength=low|none`; do not relabel a factual result to bypass the gate. The final artifact must preserve these labels. Older workspaces require an explicit preview and backed-up migration; see `docs/MIGRATION.md`.

## External Capabilities

Use an installed or built-in specialist when it materially improves a requested artifact, database workflow, statistical method, figure backend, document format, or presentation. First load `modules/03_external_skill_gateway.md` and `modules/22_capability_provider_router.md`; preserve this skill's evidence boundary; pass only the minimum required data; validate the returned artifact with `modules/17_external_skill_acceptance_tests.md`; and fall back to the internal route when no candidate passes.

## Canonical Formats

Markdown, YAML, CSV, source code, and source-native data files are canonical working records. XLSX, DOCX, PDF, PPTX, LaTeX, and HTML are delivery formats when requested or required. A polished export never replaces the underlying evidence and provenance records.

## Maintenance Rule

This skill may evolve. Modules, templates, scripts, and routes may be merged, replaced, or removed when observed behavior improves. Preserve the non-negotiable invariants, original capability coverage, evidence statuses, provider interface, and validation gates.
