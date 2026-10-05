---
name: review-22-skill-router
description: Route, merge, and validate review-writing skills for a medical literature review workbench. Use when the user asks to combine local review skills, Nature/Science-style skills, GitHub skill repositories, PRISMA/systematic-review skills, citation-checking skills, or external academic-writing workflows into the existing review workbench without losing traceability, evidence boundaries, or step-by-step folder validation.
---

# Review Skill Router

Use this skill after the core review pipeline exists and the user wants to add, compare, or reuse other skill systems. The goal is not to copy every external skill into the workbench. The goal is to decide which external skill should inform which review step, keep the original source visible, and avoid importing unverified or incompatible instructions.

## Routing Rules

1. Start from the current review step, not from the external skill name.
2. Prefer the local `review-00` to `review-28` skills for the main workflow.
3. Use external skills as reference layers:
   - Nature or Science style: argument architecture, figure standards, citation discipline, editorial polish.
   - PRISMA/systematic review: protocol, search, screening, reporting checklist, flow diagram.
   - Academic research suites: research planning, literature synthesis, writing, review, revision.
   - Scientific agent skills: database access, citation verification, biomedical workflows, reproducible outputs.
4. Never treat a GitHub skill as authoritative medical evidence. It can guide process, not replace PubMed, Embase, Web of Science, Cochrane, guidelines, or primary literature.
5. Check license/source notes before copying content. If unsure, summarize the workflow pattern and link the source instead of copying the text.
6. Every routed decision must leave a small artifact in `19_skill_library` or the relevant step folder.

## Decision Workflow

1. Identify the user's task type: six-step workbench setup, topic design, search, screening, full-text reading, Zotero/PDF handoff, evidence matrix, section-chain writing, manuscript drafting, figures/tables, GitHub archive, citation audit, journal match, submission, response, or final QC.
2. Map the task to the native review skill.
3. Select at most three external references that add value for that step.
4. State what is adopted, what is rejected, and why.
5. Write the result into the workbench using the existing folder structure.
6. If the task affects medical claims, add an evidence-boundary reminder.

## Default Routing Map

| Task | Native skill | External references to consider | Guardrail |
|---|---|---|---|
| Review protocol or PICO/PECO/PCC | `review-01`, `review-02` | PRISMA, academic research suite | Do not finalize until scope and population are explicit |
| Six-step public workflow or course demo | `review-28` | GitHub skills, Nature skills, academic skills, Xiaohongshu/video workflows | Compress long workflow into six auditable steps; plugins optional |
| Search strategy | `review-03`, `review-04` | systematic literature review skills, biomedical database skills | Record database, date, full string, and result count |
| Screening and PRISMA | `review-08` | PRISMA-focused skills | Keep exclusion reasons auditable |
| Benchmark review reading | `review-07`, `review-10` | Nature reader, academic paper reviewer | Separate article structure learning from evidence extraction |
| Evidence matrix | `review-11` | citation verifier, scientific agent skills | No claim without source, DOI/PMID, and evidence level |
| Reference search and insertion | `review-23` | academic MCP search, Nature citation, citation verifier | Recent high-quality DOI/PMID references only; avoid user-excluded journals |
| Section-chain writing | `review-24` | Nature writing, academic writing, manuscript optimizer | Advance one manuscript stage at a time; stop if evidence is missing |
| Zotero and PDF handoff | `review-25` | Zotero MCP, PubMed export, fulltext retrieval tools | Search hits are not usable evidence until PDF/full-text status is known |
| Outline and manuscript | `review-12` to `review-16` | Nature writing, scientific writing, manuscript optimizer | Improve logic and style without adding unsupported mechanisms |
| Figures and tables | `review-13`, `review-26` | Nature figure, Figma, BioRender, SVG, Excel | Track source, permission, caption, and manuscript callout |
| GitHub archive and versioning | `review-27` | GitHub workflow, project templates, reproducibility notes | Do not publish PDFs, patient data, licensed assets, or active drafts publicly |
| Citation audit | `review-17` | citation verifier, Nature citation, review-23 outputs | Verify every key citation against source text |
| Journal and submission | `review-18`, `review-19` | Nature portfolio playbook, submission audit | Match article type, scope, limits, fees, and policies |
| Revision response | `review-20` | rebuttal response, peer review | Respond point by point and cite revised locations |
| Final QC | `review-21` | all relevant external checks | Evidence, numbers, causality, ethics, declarations, and journal fit must pass |

## Reference Files

Read `references/mainstream-skill-index.md` when the user asks what external or mainstream skills are available.

Read `references/review-skill-routing.md` when selecting which external skill layer to combine with a specific review step.

When the local 490 SCI review package is present (`00-SCI综述专家` to `20-审稿人意见回复器`), do not treat it as a generic external reference by default. Read `references/490-sci-workflow-integration.md` and apply the best-of-both routing: native `review-*` skills keep medical evidence gates and final audit, while stronger 490 modules may become execution submodules for search export, Zotero/PDF handling, benchmark learning, target-journal learning, permissions, cover letter, submission guidance, and reviewer response.

## Required Output

When this skill is used, return or update:

- A routing decision: current step, native skill, external skills considered, selected references.
- A merge decision: what is adopted, what is only noted, what is rejected.
- A validation note: what artifact proves this step is complete.
- A source note for any GitHub or external repository referenced.
