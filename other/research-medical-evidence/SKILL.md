---
name: research-medical-evidence
description: "Biomedical evidence search, appraisal and publication support. PubMed/PEDro, PICO/GRADE, literatür tarama and journal preparation; prefer medical-evidence-research when available."
---

# Research Medical Evidence

Original standalone scope and trigger coverage: Automatically search, retrieve, critically appraise, and synthesize biomedical, clinical, rehabilitation, and physiotherapy evidence when the user asks "bilimsel araştır", "çalışmalar ne diyor", "kanıtı var mı", "etkili mi", "literatürü tara", mentions FTR/medical evidence, or needs responsible publication support. Use for PubMed/MEDLINE, PEDro, Cochrane, Embase, CINAHL, Scopus, Web of Science, TR Dizin, DergiPark, YÖK Thesis Center; PICO/PECO/PCC, MeSH/Boolean queries, rapid/systematic reviews, evidence grading, DOI/PMID/citation verification, journal selection, reporting guidelines, manuscripts, preprints, or submission workflows. For an individual physiotherapy case, co-use physio-clinical-copilot; for ordinary nonmedical research, use quick/deep research.

## Compatibility and one-workflow routing

When `medical-evidence-research` is actually available, let its matching evidence-answer, search, appraisal or update track own that work and return one integrated answer. A named handoff is not proof that the host loaded the skill. Do not run two complete research workflows or produce duplicate outputs. If the canonical skill is unavailable, complete this skill's original standalone workflow using its local safety and method references below; do not require a paid tool or a sibling package.

For database searches, read [native search strategy](references/search-strategy.md) and [retrieval integrity](references/tool-routing.md). For paper effects and bias, read [appraisal and synthesis](references/appraisal-and-synthesis.md). For a requested evidence update/watch, read [literature watch](references/literature-watch.md). Apply independent human final eligibility for formal reviews, keep found/retrieved/reviewed counts distinct, and retain changed publication records even when an identifier was already seen. The skill itself does not schedule future runs.

Perform reproducible health-science research and publication support without confusing search databases, indexes, repositories, registries, journal platforms, or submission systems.

## Route the request

Choose one or more tracks:

1. **Evidence answer** — answer a clinical, biomedical, safety, prognosis, diagnosis, or intervention question.
2. **Literature search** — design and execute a rapid, structured, scoping, or systematic search.
3. **Paper appraisal** — evaluate supplied or retrieved studies and explain applicability.
4. **Publication support** — select a journal, apply reporting standards, prepare submission materials, or respond to reviewers.

State the track and depth when it materially affects the result. Never label an informal or single-database search a systematic review.

## Load only the needed references

- Read [references/source-map.md](references/source-map.md) before choosing databases, platforms, registries, or journal-verification tools.
- Read [references/search-strategy.md](references/search-strategy.md) when constructing, translating, documenting, or auditing a search.
- Read [references/appraisal-and-synthesis.md](references/appraisal-and-synthesis.md) when judging study quality, extracting results, or grading certainty.
- Read [references/publication-workflow.md](references/publication-workflow.md) for journal selection, reporting guidelines, ethics, preprints, or submission.

## Evidence-search workflow

### 1. Frame the question

- Define the decision the evidence must support.
- Convert the question to the best-fitting framework:
  - PICO for intervention or therapy;
  - PECO for exposure, association, or harm;
  - PCC for scoping questions;
  - SPIDER for qualitative or mixed-methods questions.
- Predefine population, setting, intervention or exposure, comparator, outcomes, follow-up, eligible designs, date range, and language restrictions.
- Ask only for missing details that could change safety, scope, or conclusions. Otherwise use explicit reasonable defaults.

### 2. Select complementary sources

- Choose sources by coverage rather than popularity.
- For detailed clinical searches, use at least two complementary databases when access permits.
- For physiotherapy or rehabilitation, normally combine PubMed/MEDLINE with PEDro, then add CINAHL, SPORTDiscus, Cochrane, or Embase as the question requires.
- For Turkish evidence, add TR Dizin, DergiPark, and YÖK Thesis Center when local publications or grey literature could matter. Do not treat these as replacements for international databases.
- Search trial and review registries when unpublished, ongoing, or selectively reported evidence could change the answer.
- Treat preprints as non-peer-reviewed and label them prominently.
- Report inaccessible subscription sources and provide database-ready queries instead of pretending they were searched.

### 3. Build database-native queries

- Split the question into concept blocks.
- Combine controlled vocabulary with free-text terms, spelling variants, acronyms, older terminology, drug brand/generic names, and Turkish/English variants where relevant.
- Build a broad sensitivity-first query and a narrower precision query.
- Translate syntax for each database; never paste PubMed syntax unchanged into every platform.
- Avoid `NOT` and restrictive filters unless clearly justified.
- Validate the strategy against known sentinel papers when available; revise if the query misses them.

### 4. Retrieve and document

- Search live sources whenever current or high-stakes accuracy matters.
- Open the record and, when necessary, the full text; do not rely on search snippets.
- Record database/platform, exact query, search date, filters, result count, and access limitations.
- Deduplicate records and perform backward citation, forward citation, similar-article, and related-review chasing when depth warrants it.
- Check publication type, peer-review status, protocol or registry record, corrections, expressions of concern, retractions, and duplicate publications.
- Prefer primary studies for claims about effects; use reviews and guidelines to map the field and locate primary evidence.

### 5. Appraise and synthesize

- Match the appraisal method to the study design; do not use a reporting checklist as a risk-of-bias tool.
- Extract population, sample, intervention/exposure, comparator, outcomes, follow-up, effect estimates, confidence intervals, attrition, adverse events, and funding/conflicts.
- Weigh risk of bias, consistency, precision, directness, and publication bias. Do not count studies as votes.
- Separate human clinical evidence from animal, in-vitro, mechanistic, surrogate, and indirect evidence.
- Distinguish association from causation and statistical significance from clinical importance.
- Say **no direct evidence found** when appropriate; do not convert it into **evidence of no effect**.

### 6. Deliver a traceable result

Lead with the answer and certainty. Then provide, as appropriate:

1. scope and last-search date;
2. databases actually searched and important sources not accessed;
3. exact search strings or a concise reproducible search log;
4. evidence table with design, sample, key result, limitations, and relevance;
5. synthesis with contradictions and applicability;
6. certainty rating and what could change the conclusion;
7. exact citations with DOI, PMID, registry ID, or stable URL when available.

Use the user's language. Keep routine answers concise; expose the full search record for systematic, academic, or explicitly detailed requests.

## Publication-support workflow

- Identify manuscript type, target readers, language, novelty, ethics approval, registration, data availability, and publication constraints.
- Select the current reporting guideline through EQUATOR and the journal's author instructions.
- Shortlist journals by scope fit first; then verify indexing, active coverage years, fees, access model, licensing, archiving, review process, and stated timelines using official sources.
- Treat DergiPark, OJS, ScholarOne, and Editorial Manager as infrastructure or workflow systems, not quality marks.
- Verify claims such as MEDLINE, Scopus, Web of Science, TR Dizin, quartile, or impact factor in the corresponding official source. Do not trust a journal logo alone.
- Screen for deceptive or predatory practices using the checks in the publication reference.
- Prepare only the materials requested: manuscript structure, abstract, cover letter, reporting checklist, title page, author contributions, conflicts, funding, ethics, consent, data statement, figures, supplements, or reviewer response.
- Never upload, submit, withdraw, accept fees, sign licenses, or contact a journal without explicit user authorization.

## Non-negotiable quality gates

- Never fabricate citations, PMIDs, DOIs, registry IDs, journal metrics, indexing status, or full-text access.
- Never claim a database was searched when only a general web result or another index was searched.
- Cite each consequential claim beside the evidence that supports it.
- Prefer official database records, publisher pages, registries, guidelines, and primary papers.
- Flag abstract-only conclusions, inaccessible full text, translation uncertainty, conflicts of interest, and post-publication concerns.
- Recheck dates, units, sample sizes, denominators, effect directions, and citation links before delivery.
- Resolve every decisive DOI, PMID, registry ID, title, author, publication year, correction, and retraction status against an authoritative record when available; a plausible-looking citation is not evidence.
- Use `$evidence-integrity-guard` for the final claim/source/citation audit when available, without treating it as a substitute for design-specific appraisal.
- For patient-specific decisions, state the evidence boundary and relevant safety escalation without replacing clinical evaluation.
