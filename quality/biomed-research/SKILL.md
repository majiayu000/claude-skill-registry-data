---
name: biomed-research
description: >-
  Umbrella skill for biomedical and medicine research sessions. Load at the
  beginning of a session involving diseases, drugs, supplements, molecules,
  pathways, biomarkers, clinical trials, animal studies, in vitro experiments,
  case reports, longitudinal studies, or translational claims. Routes work to
  specialized skills for literature review, study appraisal, evidence synthesis,
  and clinical translation checks while emphasizing rigorous source quality,
  human clinical relevance, safety, and uncertainty.
---

# Biomedical Research Umbrella

Use this at the beginning of a biomedical or medicine research session to set
the operating standard and choose the right specialized skill. This file should
stay light: it routes the work and enforces shared principles; the detailed
workflows live in the specialized skills.

## Local results before web search

Every prior-work search starts with the common extracted literature, even when
web browsing will also be needed. Search succinct result statements and project
notes first with `python3 scripts/research_library.py search 'terms'`; add
`--sources` to search full extracted text. Read `merged-results.md` when present,
then the underlying extraction and its provenance. These local statements may
match the current question better than an abstract or web snippet. Browse for
gaps, primary-source verification, or updates; finding a paper online is not a
reason to download or convert it again when an adequate local version exists.

## Shared literature source

Before acquiring or extracting papers, use `shared-literature` to search and
reuse the configured common library. Store new source packets in its `biomed`
section, with project interpretation in separate notes. Do not start a new
per-project download cache.

## Specialized Skills

Load the relevant skill before doing the task:

- `biomed-literature-reviewer`: broad literature searches across PubMed,
  trial registries, systematic reviews, regulatory documents, animal studies,
  in vitro studies, case reports, cohorts, and randomized trials.
- `biomed-study-appraiser`: close critical appraisal of one paper, trial record,
  case report, cohort, animal experiment, or in vitro study.
- `biomed-evidence-synthesizer`: compare and integrate multiple studies,
  especially when results conflict or evidence types differ.
- `clinical-translational-checker`: determine whether mechanistic, animal,
  biomarker, or in vitro claims have credible human clinical support.

## Routing

Use this routing table:

| User Need | Load |
|----------|------|
| "Find the literature on X" | `biomed-literature-reviewer` |
| "What does this paper show?" | `biomed-study-appraiser` |
| "Compare these studies" | `biomed-evidence-synthesizer` |
| "Is this clinically proven in humans?" | `clinical-translational-checker` |
| "This molecule/pathway may affect disease Y" | `biomed-literature-reviewer` plus `clinical-translational-checker` |
| "The animal data look strong; does it translate?" | `clinical-translational-checker` |
| "The papers disagree" | `biomed-evidence-synthesizer` |
| "Can we cite this study?" | `biomed-study-appraiser` |

When multiple apply, load the minimum set that covers the task.

## Shared Standards

Always distinguish:

- Human clinical evidence.
- Human observational or biomarker evidence.
- Animal evidence.
- Ex vivo, organoid, in vitro, biochemical, or computational evidence.
- Review articles, editorials, hypotheses, and speculation.

Always check:

- Study design and control quality.
- Sample size, power, attrition, and missing data.
- Endpoint relevance: clinical outcome, validated surrogate, exploratory biomarker, or mechanistic assay.
- Dose, route, timing, duration, and follow-up.
- Population/model fit and species differences.
- Safety, adverse events, toxicity, and drug interactions.
- Replication, negative studies, unpublished completed trials, and terminated trials.
- Funding source, sponsor role, and conflicts of interest when relevant.

## Evidence Language

Use cautious evidence labels:

- Clinically established.
- Clinically supported but incomplete.
- Preliminary human evidence.
- Human association only.
- Mechanistically plausible but clinically unproven.
- Animal-only.
- In vitro only.
- Mixed or inconclusive.
- Unsupported.
- Contradicted by stronger evidence.

Do not use clinical efficacy language for animal-only or in vitro-only findings.
Do not equate biomarker movement with patient benefit unless the biomarker is a
validated surrogate for that clinical context.

## Session Workflow

1. Clarify the exact claim or research question.
2. Identify whether the task is search, appraisal, synthesis, translation, or a combination.
3. Load the specialized skill(s).
4. Search or evaluate primary sources when the user asks for current evidence.
5. Separate evidence by tier and model.
6. Produce a concise bottom line plus the evidence table or appraisal details needed to audit it.

## Safety Boundary

Biomedical research support is not medical advice. For clinical decisions,
diagnosis, treatment, dosing, medication changes, or urgent symptoms, tell the
user to consult an appropriate licensed clinician. Still provide rigorous
research analysis when requested, clearly framed as evidence review.
