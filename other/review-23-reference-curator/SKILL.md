---
name: review-23-reference-curator
description: Curate, verify, insert, format, and audit high-quality references for medical SCI review manuscripts. Use when the user asks to find references, add citations to Chinese or English academic text, replace weak citations, enforce recent DOI/PMID-complete references, follow WJG/Nature/Science-style citation discipline, exclude low-quality journals, or build claim-citation mapping before the final review-17 citation audit.
---

# Review 23 Reference Curator

## Overview

Use this skill before `review-17-citation-audit` when references are the central task. The goal is to convert manuscript claims into a traceable, high-quality reference set that is recent, verifiable, journal-appropriate, and directly matched to the text.

This skill may borrow process standards from Nature/Science/CNS citation skills, academic search skills, citation verifier skills, and the local review workbench, but medical evidence authority always comes from verified literature and databases, not from style skills.

## Position In The Review Workbench

- Use `review-03-search-string` and `review-04-search-execution` for broad systematic searches.
- Use this skill for paragraph-level citation insertion, reference replacement, DOI/PMID completion, and reference-quality screening.
- Use `review-11-evidence-matrix` when extracted evidence needs to support manuscript arguments across sections.
- Use `review-17-citation-audit` after this skill to confirm final numbering, DOI/PMID integrity, and claim-citation alignment.
- Use `review-22-skill-router` when combining this workflow with Nature, Science, academic, PRISMA, or other external skill systems.

## Non-Negotiable Rules

- Do not invent references, DOI, PMID, author names, title, journal, year, volume, issue, pages, article number, or findings.
- Prefer 2021-2026 references. Include 2020 only when the user allows it or when it is a high-impact guideline, consensus, landmark trial, major review, or foundational method paper.
- Require both DOI and PMID for core biomedical references. If either is missing, mark it as `exception candidate` and explain why it may or may not be acceptable.
- Verify each reference through PubMed plus DOI/Crossref or publisher page when possible. Use Web of Science if available. Use Google Scholar only as a discovery aid or secondary cross-check.
- Prefer JCR Q1-Q2, CAS high-partition journals, field-defining journals, guidelines, consensus statements, high-quality systematic reviews/meta-analyses, and major original studies.
- Avoid MDPI, Frontiers, Scientific Reports, Medicine, and other user-excluded or quality-risk sources unless no credible alternative exists and the user explicitly approves the risk.
- Match each citation to the exact claim. Do not cite a paper merely because its topic is similar.
- Do not use correlation evidence to support causal language.
- Do not use basic or mechanistic evidence as direct support for clinical efficacy unless the text clearly frames it as mechanistic or hypothesis-generating.
- Do not use review articles to support precise numeric results when a primary study, guideline, or dataset is needed.

## Source Priority

Use this order for biomedical review manuscripts:

1. PubMed record and PMID.
2. Publisher page and DOI resolver/Crossref metadata.
3. Guidelines, consensus, Cochrane, major society statements, and clinical trial registrations where appropriate.
4. Web of Science, Scopus, Semantic Scholar, or OpenAlex for citation context and metadata cross-checking.
5. Google Scholar only for discovery, citation chasing, or locating otherwise missing official pages.

When using external skill layers:

- `nature-citation`: use for strict segmentation, support grading, and CNS/Nature-family candidate discovery; do not let it override the user's excluded-source list.
- `nature-polishing`: use only after evidence is settled, for prose clarity and citation discipline.
- `academic-mcp-search`: use for structured metadata, deduplication, DOI-first merging, and audit-ready tables.
- `citation-verifier`: use for local placeholder scans, duplicate keys, DOI/PMID gaps, and final bibliography hygiene.

## Workflow

### 1. Segment The Text

- Preserve the user's original paragraph order.
- Treat every substantive paragraph as needing at least one citation unless it is purely transitional.
- Split long paragraphs into focused citable claims when they contain multiple mechanisms, clinical statements, epidemiology facts, or methodological assertions.
- Assign stable IDs: `P001`, `P002` for paragraphs and `C001`, `C002` for individual claims.

### 2. Classify Each Claim

For each claim, assign one type:

- `background`
- `epidemiology`
- `mechanism`
- `clinical diagnosis`
- `clinical treatment`
- `prognosis`
- `biomarker`
- `bioinformatics method`
- `guideline or consensus`
- `review context`

Then identify population/model, disease, exposure/intervention, molecular pathway, endpoint, and whether the wording implies causality.

### 3. Search And Screen

- Translate Chinese claims into English search concepts while preserving the original scientific meaning.
- Search with precise terms first, then synonyms and broader terms.
- Prioritize recent high-quality evidence from 2021-2026.
- Keep a dropped-records log for excluded papers, especially if excluded for year, no PMID, no DOI, low-quality journal, wrong claim support, or user-excluded source.
- For clinical claims, prioritize guidelines, consensus statements, RCTs, large cohorts, systematic reviews, and meta-analyses over small retrospective studies.
- For mechanism claims, prioritize original mechanistic studies in appropriate models, supported by high-quality reviews only for context.
- For bioinformatics claims, prioritize method papers, dataset papers, benchmark studies, and reproducible workflows with stable identifiers.

### 4. Verify Each Candidate

For every retained candidate, check:

- Title matches DOI/PubMed metadata.
- DOI resolves or appears in Crossref/publisher metadata.
- PMID exists and matches title, journal, year, and authors.
- Journal is acceptable for the target review.
- Publication year fits the user's time window.
- Article type fits the claim.
- Abstract or full text supports the exact claim.
- No obvious retraction, expression of concern, or major mismatch is visible.

Support grades:

- `strong`: directly supports the exact claim.
- `partial`: supports only part of the claim or a narrower setting.
- `background`: supports field context but not the exact assertion.
- `weak`: thematically related but not adequate as direct support.
- `reject`: unverifiable, mismatched, outdated without justification, excluded source, or poor claim fit.

Only use `strong`, `partial`, or clearly labeled `background` citations in the manuscript.

### 5. Insert Citations

- Insert numeric citations in the target journal style, usually `[1]`, `[2]`.
- Keep numbering in first-appearance order.
- Use the smallest adequate number of citations per claim.
- Place citations close to the supported claim, usually at the end of the sentence or clause.
- If one paragraph contains distinct factual claims, place separate citations near each claim instead of stacking all references at the paragraph end.
- Do not change the scientific meaning while inserting citations.

### 6. Format References

- Default to the target journal's numbered style. For World Journal of Gastroenterology, use numbered references and verify the latest official author/title/journal/year/volume/page/PMID/DOI requirements at use time.
- If the user requests Nature or Science style, follow the requested journal family format after verifying current instructions.
- Preserve DOI and PMID in the output whenever allowed by the target format or in the audit table when not shown in the reference list.
- Do not fabricate missing volume, issue, page, article number, DOI, or PMID.

### 7. Produce Audit Artifacts

Always provide a compact audit table with:

- Reference number.
- Supported paragraph/claim ID.
- Claim summary.
- First author and year.
- Journal.
- Article type.
- PMID.
- DOI.
- Support grade.
- Source-quality note.
- Risk or exception.

For larger manuscripts, also recommend saving:

- `reference_candidates.csv`
- `claim_citation_check.csv`
- `citation_crossref_pubmed_check.csv`
- `citation_audit_report.md`

## Output Format

Unless the user requests otherwise, return:

For Chinese users, write the visible response in Chinese while keeping table field names stable when useful.

1. `Task decision`: reference insertion, replacement, verification, formatting, or final audit preparation.
2. `Claim analysis`: paragraph or claim IDs with claim type and citation need.
3. `Revised text with citations`: manuscript text with numeric citations.
4. `Reference list`: target journal style.
5. `Citation audit table`: DOI/PMID/year/journal/support-grade/risk table.
6. `Risks and gaps`: missing DOI/PMID, no direct evidence, old but necessary references, or excluded-source conflicts.

## Stop Conditions

- If no reference satisfies DOI, PMID, year, journal quality, and claim support requirements, state that clearly and propose a narrower search strategy.
- If a requested claim appears unsupported or overclaimed, suggest safer wording rather than forcing a citation.
- If the user asks to cite a low-quality or excluded source, flag the source risk and provide higher-quality alternatives first.

## Reference File

Read `references/reference-quality-gates.md` when the task requires strict inclusion/exclusion decisions, a reference audit table, or target-journal-ready citation insertion.
