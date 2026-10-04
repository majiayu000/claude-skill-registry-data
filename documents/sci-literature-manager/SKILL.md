---
name: sci-literature-manager
description: Manage a reusable academic source library independently from project experiment evidence. Use when discovering papers, assigning stable source identities, organizing source packets, maintaining global indexes and reading routes, tracking bibliographic verification and versions, deduplicating sources, or returning a source-grounded handback for project adoption. Use sci-paper-reader for deep reading; leave project tags, LiteratureClaim state, experiment decisions, and evidence promotion to sci-research-manager.
---

# SCI Literature Manager

Make literature discoverable and reusable without mixing it with experiment records. Follow project-local rules and the ownership boundary in `sci-research-manager`.

## Classify the task

- `literature_discovery`: find candidate papers from primary/official sources.
- `literature_indexing`: organize global PDFs, source packets, notes, and indexes.
- `deep_reading`: hand the located source to `sci-paper-reader`.
- `route_synthesis`: return source-grounded options for a project question and competing causes.
- `citation_verification`: verify title, author, venue, year, DOI/arXiv, code, and exact claims.
- `experiment_support`: return verified source material for a literature-to-experiment brief.
- `maintenance`: deduplicate, repair links, or archive superseded notes.

## Retrieve before reading broadly

Read the relevant global query route/index, then matching records, then decisive primary-source sections. Reuse unchanged source IDs, notes, manifests, and tool capabilities already read in this task; inspect deltas on resumption. Do not batch-read the entire library unless the user asks for a full audit. Context reuse never replaces exact claim verification.

For a known paper, resolve its supplied DOI/arXiv/Source ID or exact title, check identity/version/duplicates, verify missing metadata, and register only the requested delta. Do not restart domain discovery, create project claims, or deep-read every section as an intake prerequisite. Reuse an existing record; preserve preprint/publication and alias relations rather than deleting them as duplicates.

For discovery, state the question and start with the mechanism, synonyms, and closest citation neighbors. Expand only to resolve a named uncertainty. Stop when another expansion no longer changes the nearest overlap, consequential protocol difference, or next evidence-needed action; report coverage and unresolved sources, not an exhaustive novelty claim. Access failures are not evidence of absence. Reuse valid results, retry only for a diagnosed recoverable cause or useful authorized alternate source, and stop retrying unchanged failures.

Request identifiers, selected metadata, exact sections, page/table anchors, or short relevant passages from tools. Keep full text and large catalogs on disk when available. Mark incomplete/truncated output; do not repeatedly fetch the same full response or treat an abstract as proof of mechanism or exact results. Use deterministic lookup, extraction, deduplication, and verification scripts before considering bounded delegation; no particular provider, model, or notification tool is required.

## Keep a portable paper packet

Only when a reusable reading packet is requested, prefer:

```text
<category>/<paper-slug>/
  paper.pdf
  paper_understanding_YYYYMMDD.md
  paper_visual_YYYYMMDD.html
  assets/
  README.md
```

Use library-relative paths and existing conventions. Generate only requested artifacts; ordinary intake needs a verified source record and available source location, not Markdown/HTML/PPT/Word derivatives. For a reading packet, keep Markdown canonical. Return candidate project relevance to `sci-research-manager` only when project adoption or state is in scope; do not embed it in global identity or reusable understanding artifacts.

## Maintain verification states

Use clear labels such as:

- `verified`;
- `cached_pdf`;
- `needs_download`;
- `needs_bibliographic_verification`;
- `needs_metric_verification`;
- `paywalled_or_access_limited`.

Do not invent bibliographic fields or exact metrics. Record page/table/figure anchors for numerical claims. Distinguish preprints from accepted publications.

## Build problem-driven reading routes

Use:

`problem -> competing causes -> paper groups -> variables/controls -> evidence limits -> validation implication -> next question`

Do not turn a mature framework or paper module into the project's contribution by default.

## Return a typed source handback

For intake or a narrow lookup, return only the source ID/location, verified fields, changed records, and unresolved gaps. For a project decision or experiment-support request, return a compact typed source handback with the relevant fields below; do not create a second plan or registry:

- stable source identities, canonical locations, versions, and bibliographic verification status;
- bounded source claims with exact locations and protocol limits;
- theoretical motivation separated from any proposed project hypothesis;
- variables/cues and required controls;
- success/failure criteria;
- likely confounds and non-transferable assumptions;
- do-not-overclaim/do-not-do-next;
- unresolved identity, access, or citation gaps.

Include the nearest substantive overlap, remaining testable difference, decisive source locations actually read, and search coverage. A close precedent may make a method a reproduction or baseline; it does not automatically invalidate the whole direction. Do not invent novelty from a new name, benchmark, or untested condition. The research owner integrates the decision before proposal-specific asset preparation or costly execution.

Return to the current requester. Use `sci-research-manager` only when project adoption, tags, LiteratureClaim verification, experiment allocation, or downstream state actually enters scope; a direct lookup or intake can finish without a coordinator call. Literature-only items never enter the experiment index or claim map as project evidence.
