---
name: sport-geography-review-bibliometric
description: "Use for external-literature review and evidence synthesis in geography + sport science, including systematic/scoping/critical/bibliometric reviews, PRISMA, literature matrices, paper-level extraction, Evidence Trace, cross-paper synthesis, conflicting evidence, heterogeneity synthesis, review gaps, and Paragraph-level Synthesis Contracts."
---

# Sport Geography Review Bibliometric

This skill supports systematic reviews, scoping reviews, critical reviews, and bibliometric/scientometric manuscripts in sport geography and urban health geography. It owns literature-evidence synthesis before manuscript prose: corpus construction, paper-level extraction, Evidence Trace, cross-paper argument mapping, and review synthesis QC. It is designed for work that combines sports facilities, parks, green/heat exposure, accessibility, equity, spatial justice, and planning implications.

Use it to move from a broad topic and paper corpus to a journal-positioned review manuscript with reproducible search logic, defensible coding, meaningful bibliometric maps, and a policy agenda.

## Core Contract

Do not treat bibliometrics as the contribution. The contribution must be one of:

- a clarified concept boundary;
- a systematic evidence map;
- a method evolution framework;
- a justice/equity coding framework;
- a journal-fit planning or policy agenda;
- a combined review + bibliometric route that explains why the field matters.

Default argument chain:

`public health and active living pressure -> unequal spatial opportunity -> exposure/accessibility measurement gap -> evidence synthesis -> method and justice framework -> planning agenda`

## Fast Workflow

1. **Position the manuscript**
   - Decide whether the paper is a systematic review, scoping review, bibliometric review, or hybrid review.
   - Choose one target route: SCS/Cities, landscape-green-space journals, health-exposure journals, or broader geography/planning journals.
   - Read `references/00_skill_design_principles.md` when updating the skill itself.
   - Read `references/01_positioning_and_journal_route.md`.

2. **Define scope and search logic**
   - Separate object terms, exposure/accessibility terms, equity/justice terms, health/activity terms, and exclusions.
   - Use WoS + Scopus by default for bibliometrics; add PubMed/SPORTDiscus/Dimensions only when the research question needs health or sport coverage.
   - Read `references/02_search_prisma_protocol.md`.

3. **Build the evidence corpus**
   - Document search date, database, query, filters, de-duplication, and screening reasons.
   - Keep OA/non-OA status, DOI, journal, partition label, and manual-download status separate from inclusion decisions.
   - Use `assets/PRISMA筛选记录模板.xlsx` and `assets/文献批判性编码模板.xlsx`.
   - Record paper-level findings in the Evidence Trace with a full-text status and source locator. `ABSTRACT_ONLY` records must not receive invented section, page, table, figure, or supplement locations.

4. **Run bibliometric analysis only after scope is stable**
   - Use bibliometrix for performance analysis and thematic evolution.
   - Use VOSviewer for co-authorship, keyword co-occurrence, citation/co-citation, and overlay maps.
   - Use CiteSpace for burst references, timeline clusters, and turning points.
   - Read `references/03_bibliometric_workflow.md`.

5. **Add critical manual coding**
   - Code facility type, exposure metric, spatial scale, method family, population group, justice dimension, health pathway, and planning implication.
   - Use coding to answer what bibliometrics cannot answer.
   - Read `references/04_critical_coding_framework.md`.

6. **Synthesize across papers before drafting**
   - Build the Cross-paper Argument Map from Evidence IDs, preserving supporting and contradictory evidence and recording methodological, population, exposure/concept, spatial-scale, and temporal heterogeneity.
   - Create a paragraph synthesis contract before drafting Results, Discussion, or review Introduction paragraphs that make factual or synthesis claims.
   - Do not use citation count, paper count, semantic similarity, bibliometric co-occurrence, RF/SHAP output, or feature importance as evidence strength or causal mechanism.

7. **Draft the manuscript**
   - Make the review argument-led, not article-by-article.
   - Use bibliometric figures as evidence for field evolution, not decoration.
   - Translate findings into planning, governance, and equity implications.
   - Read `references/05_manuscript_structure.md` and `references/06_figures_tables_policy_agenda.md`.
   - For reusable writing prompts, prompt chains, reviewer audits, and policy-agenda prompts, read `references/09_prompt_library.md`.
   - For target-journal review and bibliometric paper patterns, read `references/10_top_journal_review_patterns.md`.

8. **Audit before completion**
   - Verify every citation and DOI used in the manuscript.
   - Check whether journal partition labels are current using the user's institution access to JCR/CAS.
   - Make sure the final narrative does not overclaim health benefit from exposure or accessibility.
   - Read `references/07_quality_checks.md`.

For end-to-end projects, this skill owns literature-search reproducibility, screening, high-impact paper classification, paper-level extraction, literature matrix, Evidence Trace, Cross-paper Argument Map, evidence gap taxonomy, PRISMA records, bibliometric figures, critical coding, and review synthesis QC. Handoff stable synthesis claims and boundaries to `agent-auto-sci-methodology` and `agent-auto-sci-scicomm`; those skills do not reconstruct evidence from prose memory.

## Local Corpus

When available, use the user's curated local corpus as evidence:

- `<your-literature-library>/00_表格与清单/中文分类整理总表_含PDF匹配与下一步路线.xlsx`
- `<your-literature-library>/02_PDF文本提取与匹配索引/全文结构索引_48篇.csv`
- `<your-literature-library>/03_下一步精读与Skill建设路线.md`
- `<your-literature-library>/02_PDF文本提取与匹配索引/prompt手册_提取文本.txt`

Read `references/08_local_corpus_guide.md` before using these files.

## Scripts

- `scripts/create_review_templates.py`: create PRISMA, critical coding, Claim-Evidence Map, Evidence Trace, Cross-paper Argument Map, paragraph synthesis contract, and journal-positioning templates in a chosen output directory.
- `scripts/validate_review_templates.py`: deterministically validate workbook sheets, headers, duplicate columns, reopenability, and controlled-vocabulary bindings without judging scientific evidence.
- `scripts/audit_review_library.py`: audit a local review library folder for expected tables, PDFs, extracted text, and DOI-match counts.

## Must Not Do

- Do not use "sports park exposure" as the only topic if the corpus is actually green/open/sport space equity.
- Do not equate accessibility with actual use.
- Do not equate exposure with health benefit.
- Do not equate equality with equity or justice.
- Do not rely only on VOSviewer/CiteSpace screenshots for high-impact journals.
- Do not present JCR/CAS partition labels as confirmed unless the user has verified them from a current official source.
- Do not write a review as one-paper-at-a-time summaries; synthesize by concept, method, population, and planning implication.
