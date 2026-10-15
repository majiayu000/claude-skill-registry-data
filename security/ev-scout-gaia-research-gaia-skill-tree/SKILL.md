---
name: ev-scout
description: >-
  Broad, pre-curation evidence reconnaissance for a declared Gaia skill, intake
  batch, upstream repository, or proposed generic capability. Run before choosing
  a discovery strategy or mapping topology, to give the curator independent
  research leads and counterevidence. Context only: never scores, grades,
  ratifies, ingests, or mutates the registry. Later ev-discovery and ev-pipeline
  phases validate/promote any selected leads.
version: 1.0.0
---

# ev-scout — breadth-first pre-curation context

**Run before Phase 1 of /gaia-full-pipeline**, including an already-submitted
`gaia push` batch (Strategy F). May also run standalone, before L4 mapping.
This is a lightweight read/search pass, **not** the later /ev-discovery Phase 0
nor a substitute for /ev-pipeline. Scouting is deliberately permissive;
downstream verification and /ev-adversarial-audit are deliberately skeptical.

## Inputs

Use the declared skill URL(s), upstream `SKILL.md` or repository, intake issue,
and proposed generic concepts (if available). Keep multiple skills in a batch
distinct, especially for named-only evidence. Do not require an L4-approved
generic mapping: report tentative alternatives when topology is unresolved.

## Search widely, without grading

Explore several search angles and independent source families:
1. **Generic capability:** peer-reviewed papers, preprints, evaluations,
   general benchmark methodologies, foundational approaches, rival systems,
   and criticism or failure modes.
2. **Named implementation:** source repo, specific `SKILL.md` blobs,
   releases, tests, CI/reproduction claims, independently authored reviews,
   reported use, security findings, adoption or reproducible demonstrations.
3. **Comparison:** alternative architectures and negative findings that could
   falsify claimed benefits. Prefer disconfirming evidence when the first
   results are uniformly promotional.
4. **Evaluation opportunities:** candidate benchmark IDs, public methodology,
   datasets, harnesses and missing reproducibility details. A vendor claim is
   **never** a verified `benchmark-result`.

Try broad and narrow queries; sample independent sources rather than repeatedly
searching the same host. Favor diversity of *useful leads* over an illusion of
completeness. Do not discard a relevant lead just because it may later fail.
Do not turn mere topic relevance into implementation-specific proof.

Use available search and repository-read tools. If Firecrawl is available,
follow /ev-discovery's authentication/preflight and quoting conventions.
If not, use other available read/search tools, or report search limitations.
Absence of search is not a curation blocker: return a clearly incomplete packet.

## Output: scout packet

Produce a Markdown packet in the handoff or at
`generated-output/ev-scout/<intake-or-slug>.md` when a persistent file is
needed. Include:

- target skill(s), upstream URL(s), date, searched queries/source families,
  tools used or unavailable, and mapping status (tentative or ratified);
- a table of **leads**, with URL, title/publisher, publication date if known,
  possible canonical Gaia evidence type, generic/named/benchmark-catalog scope,
  what it might substantiate, and what a verifier must still confirm;
- a separate **counterevidence and competing approaches** section;
- likely evaluation benchmarks as **benchmark-source candidates only**,
  including proposed generic applicability and missing reproducibility fields;
- a short mapping-relevant synthesis that distinguishes architecture from
  demonstrated performance and marks uncertainty explicitly;
- suggested verification priorities and handoff to /ev-discovery, /ev-pipeline,
  and /gaia-ingest-batch *after their normal human gates*.

Use "candidate", "possible", or "unverified" until evidence is checked.
Never fabricate publication dates, citations, percentile values, peer-review
status, scores, or external adoption. Mark unavailable facts unknown.

## Non-authority and handoff

No registry mutations, evidence-lake edits, GitHub approval labels, L4
ratification, star grades, Trust Magnitude, or automatic evidence ingestion.
This packet **informs** /gaia-draft-curate, /gaia-curate[-chain/-dynamic],
and the human L4 review; it does not override their workflows.

Later /ev-discovery can investigate selected Stage-2 leads; /ev-collection
normalizes typed candidate rows; /ev-benchmark-verification and
/ev-adversarial-audit challenge them; /ev-link-validation checks links;
human review and canonical Gaia CLI ingestion remain authoritative.

If a recent scout packet for this exact source exists, reuse and refresh it
rather than rescouting blindly. Record any new material or limitations.
