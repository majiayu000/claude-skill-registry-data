---
name: biomed-literature-reviewer
description: >-
  Conduct thorough biomedical literature reviews across PubMed, clinical trial
  registries, systematic reviews, regulatory documents, animal studies, in vitro
  experiments, case reports, cohort studies, and randomized trials. Use when
  researching molecules, pathways, drugs, diseases, biomarkers, interventions,
  cellular behavior, or clinical evidence. Emphasizes source quality, human
  clinical relevance, study design, endpoints, replication, and uncertainty.
---

# Biomedical Literature Reviewer

Systematically map biomedical evidence for a molecule, pathway, disease,
intervention, biomarker, cell behavior, or clinical claim. The goal is not just
to collect papers, but to classify the evidence, expose weak links, and separate
mechanistic plausibility from demonstrated human clinical relevance.

## Local results before web search

Every prior-work search starts with the common extracted literature, even when
web browsing will also be needed. Search succinct result statements and project
notes first with `python3 scripts/research_library.py search 'terms'`; add
`--sources` to search full extracted text. Read `merged-results.md` when present,
then the underlying extraction and its provenance. These local statements may
match the current question better than an abstract or web snippet. Browse for
gaps, primary-source verification, or updates; finding a paper online is not a
reason to download or convert it again when an adequate local version exists.

## Step 0: Scope the Review

If the user did not specify the scope, ask only the minimum needed:

1. What is the target topic or claim?
2. Should the review prioritize human clinical evidence, mechanism, safety, or all evidence?
3. Are there known papers, drugs, aliases, or trial identifiers to include?

Record the review question in a precise form:

```text
For [population/model/context], what evidence supports [claim/intervention/
mechanism], measured by [endpoint/outcome], and at what confidence level?
```

## Step 1: Build Search Terms

Extract and expand:

- Molecule, gene, protein, receptor, metabolite, pathway, drug, supplement, or biomarker names.
- Synonyms, abbreviations, drug codes, spelling variants, and MeSH terms.
- Disease names, subtypes, phenotypes, and clinical endpoints.
- Relevant cell types, tissues, animal models, and assay names.
- Trial names, registry identifiers, and regulatory names when known.

Use multiple query families:

- Direct biomedical terms: `[molecule] [disease]`, `[pathway] [cell type]`.
- Clinical terms: `[intervention] randomized trial`, `[biomarker] cohort`, `[drug] phase 2`.
- Translational terms: `[molecule] mouse human`, `[mechanism] clinical trial`.
- Safety terms: `[intervention] adverse events`, `[drug] toxicity`, `[biomarker] mortality`.

## Step 2: Search Sources

Search current primary sources when the user asks for a real literature review:

- PubMed/MEDLINE for peer-reviewed biomedical literature.
- ClinicalTrials.gov and other trial registries for completed, active, terminated, or unpublished trials.
- Cochrane and systematic reviews/meta-analyses when available.
- FDA labels, FDA reviews, EMA EPARs, and guideline documents for approved therapies or regulated claims.
- Preprints only as lower-confidence, clearly labeled context.

Prefer primary papers and trial registry records over secondary summaries. When using a review, check the key cited primary studies behind any important claim.

## Shared source packets

Use `shared-literature` before downloading or extracting a study. Search the
configured common library across all domains by DOI, PMID/PMCID, title, trial ID,
and aliases. Reuse existing sources and extractions. Reserve absent papers in
the `biomed` subject directory using `scripts/research_library.py`; retain
versions, corrections, registry updates, and differing evidence extractions.
Keep reusable study findings in `key-results.md` and project-specific clinical
questions or interpretation in `project-notes/`. Preserve restricted access to
private notes. Commit packet changes and refreshed indexes in the library's
owning repository, not a separate repo-local cache.

## Step 3: Classify Evidence

For each relevant study, record:

- Citation and source.
- Study type: systematic review/meta-analysis, RCT, nonrandomized trial, prospective cohort, retrospective cohort, case-control, case series/report, animal, organoid/ex vivo, in vitro, computational.
- Population/model: species, strain, cell line, tissue, disease stage, demographics, inclusion/exclusion criteria.
- Exposure/intervention and comparator.
- Dose, route, timing, and duration.
- Primary and secondary endpoints.
- Main findings, effect sizes, uncertainty intervals, and adverse events.
- Funding source and conflicts if relevant.

Use this evidence hierarchy, but do not apply it mechanically:

```text
Highest clinical confidence: replicated, adequately powered RCTs with clinically meaningful endpoints.
Moderate: consistent human observational evidence or smaller controlled trials.
Preliminary: case series, uncontrolled trials, surrogate endpoints, biomarker-only studies.
Mechanistic: animal, ex vivo, organoid, in vitro, biochemical, computational.
```

## Step 4: Check Human Relevance

Explicitly separate:

- Human clinical evidence.
- Human biomarker or observational evidence.
- Animal evidence.
- In vitro or biochemical evidence.
- Review/speculation.

For animal and in vitro findings, check:

- Whether the dose/exposure is achievable in humans.
- Whether route, timing, and disease stage match clinical use.
- Whether the model captures the human pathology.
- Whether species-specific biology could change the conclusion.
- Whether the endpoint is mechanistic, surrogate, or clinically meaningful.

## Step 5: Report

Use this structure unless the user requests another format:

```markdown
# Biomedical Literature Review: [Topic]
Date: [date]

## Review Question
[Precise question.]

## Search Summary
- Sources searched:
- Search terms:
- Inclusion criteria:
- Exclusion criteria:
- Papers/records screened:
- Papers/records included:

## Evidence Map
| Study | Type | Population/Model | Exposure | Comparator | Endpoint | Finding | Evidence Level |
|------|------|------------------|----------|------------|----------|---------|----------------|

## Human Clinical Evidence
[RCTs, clinical trials, cohorts, case reports, safety data.]

## Animal and Mechanistic Evidence
[Animal, in vitro, ex vivo, biochemical evidence; note limitations.]

## Consistency and Replication
[Where results agree, conflict, or remain unreplicated.]

## Critical Limitations
[Bias, confounding, endpoint weakness, sample size, model limitations.]

## Bottom Line
[Cautious conclusion with confidence level.]

## References
[Full citations and links.]
```

## Standards

- Do not infer clinical efficacy from animal or in vitro evidence without saying it is not clinically established.
- Do not treat association as causation.
- Do not hide negative, null, terminated, unpublished, or safety-relevant studies.
- Flag conflicts between abstracts, full text, trial registry records, and published outcomes.
- State uncertainty plainly when evidence is sparse or heterogeneous.
