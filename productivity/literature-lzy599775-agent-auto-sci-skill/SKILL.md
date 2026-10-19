---
name: literature
description: Route and execute evidence-traceable literature research for papers, references, citations, DOI/metadata verification, Zotero library use, reviews, source synthesis, and citation-support questions. Use when Codex must search, deduplicate, verify, extract, audit, or synthesize scholarly sources; do not use as a substitute for direct data analysis or manuscript drafting when literature evidence is not the primary task.
---

# Literature Workflow V0

Use a manual, reviewable workflow before adding automation.

## Route the request

Choose the primary route:

- Corpus discovery or review -> literature review pipeline.
- One-paper understanding -> structured paper note plus evidence records.
- Citation supports a sentence -> citation-claim audit.
- Reproduction planning -> extract methods, data, parameters, and assets, then hand off to the reproduction workflow.
- Current research landscape -> search current authoritative scholarly sources and record the search date.

Read [references/contracts.md](references/contracts.md) for input and output contracts.

## Follow the pipeline

1. Define the research question, scope, eligibility, and expected output.
2. Inspect existing Zotero and local sources before duplicating discovery work.
3. Search authoritative scholarly sources when the corpus is incomplete or current information matters.
   - Automatically apply [Paper Artifact Availability Protocol V1](../../docs/workflows/PAPER_ARTIFACT_AVAILABILITY_PROTOCOL_V1.md) to every paper surfaced to the user, shortlisted, entered into an evidence table, considered as an exemplar, used in method comparison, or included in synthesis. Check publisher/supplement and data/code statements plus bounded repository searches; the user need not separately request code/data. For monitors, defer Level 1 until qualification and Level 2 until reading/exemplar/reproduction use.
4. Deduplicate by DOI or authoritative identifier, then title/author/year evidence.
5. Verify metadata and full-text availability.
6. Extract only source-supported fields.
7. Create claim-level evidence traces.
8. Run metadata, method, numeric, and claim-support quality checks.
9. Synthesize agreements, differences, limitations, and uncertainty without erasing study context.

Repository identity, licenses, and code/data availability are separate verified fields. Search/retrieval failures remain `NOT_VERIFIED_DUE_TO_NETWORK`; do not call them absent. Artifact availability affects reproducibility utility, not scientific relevance, causal credibility, result validity, or journal quality.

Use the detailed pipeline in `docs/workflows/literature_review.md` and the evidence schema in `docs/standards/evidence_trace.md`.

## Apply source hierarchy

Prefer:

1. original paper, supplement, dataset, or code;
2. publisher or authoritative metadata;
3. verified structured extraction;
4. secondary synthesis;
5. snippets only for discovery.

Do not use a Research Vault summary as a substitute for the source paper.

## Use Zotero safely

Use Zotero for bibliographic parent metadata, citation keys, attachments, PDFs, and indexed full text. Store derived notes and evidence records in the Research Vault.

Read [references/zotero-integration.md](references/zotero-integration.md) before using Zotero. Treat imports and library changes as explicit write actions.

## Preserve missingness and uncertainty

Use `NOT_REPORTED`, `NOT_APPLICABLE`, or `NOT_VERIFIED` for unsupported fields. Use `KNOWN`, `SUPPORTED`, `INFERRED`, `UNKNOWN`, `NOT_AVAILABLE`, or `CONFLICTING_EVIDENCE` for epistemic state.

Never invent citations, DOI values, URLs, metadata, sample sizes, methods, results, or full-text content.

## Handle failures

Read [references/failure-and-qc.md](references/failure-and-qc.md) for inaccessible full text, ambiguous duplicates, conflicting metadata, temporary retrieval failures, and required quality gates.

Retry safe technical failures. Stop only when human credentials, paid access, legal/licensing decisions, destructive writes, or materially different scientific choices require user judgment.

## Return

Report:

- route selected;
- sources searched or inspected;
- verified corpus or paper identity;
- full-text availability;
- derived artifacts created;
- evidence and uncertainty status;
- quality-control results;
- unresolved blockers.
