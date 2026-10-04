---
name: rseng-citation-hygiene
description: >-
  Covers verifying that every citation is real, correct and current: checking
  references in manuscripts, READMEs, references files and code metadata
  against Crossref and OpenAlex, screening cited DOIs against the Retraction
  Watch database, catching fabricated or mis-attributed citations (a
  documented AI failure mode), and keeping bibliographies and CITATION.cff
  files resolvable. Use PROACTIVELY before any bibliography, reference list or
  citation metadata is finalized or published, whenever the agent itself has
  produced citations, and when the user asks to check references, mentions
  broken DOIs, retracted papers or citation verification, or prepares a
  manuscript, README or software paper with references. (Making your own
  software citable is rseng-citation-metadata.)
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Citation hygiene

A citation is a checkable claim: this work exists, says what I say
it says, and stands unretracted. All three parts fail routinely -
and AI assistance has made the first failure mode systematic:
language models fabricate plausible references with confident DOIs.
An agent that produces or touches citations therefore has a special
duty here, stated plainly: VERIFY EVERY CITATION YOU GENERATE
against an authoritative source before handing it to the user, and
say which were verified. No unverified reference should survive to
a published artifact. rseng-citation-metadata covers making YOUR
software citable; this skill covers the references you cite.

## Verify existence and metadata (Crossref, OpenAlex)

For each reference with a DOI:

- Resolve it: `curl -sI https://doi.org/<DOI>` - a failing DOI is
  either a typo or a fabrication; both are findings.
- Fetch the registered metadata and compare with the citation as
  written: `https://api.crossref.org/works/<DOI>` (or the OpenAlex
  record at `https://api.openalex.org/works/doi:<DOI>` - open,
  keyless APIs). Title, authors, venue and year must match; a DOI
  that resolves to a DIFFERENT paper than the citation claims is
  the classic fabrication signature and worse than a dead link.
- References without DOIs: search Crossref/OpenAlex by title and
  authors; if nothing plausible exists, flag it - books and grey
  literature can be legitimate, but only a human can vouch for
  them.
- Batch the work: extract all references (BibTeX, CSL JSON,
  CITATION.cff references, markdown bibliographies), verify each,
  and report a table: verified / metadata-mismatch / unresolvable /
  no-DOI-needs-human.

## Screen for retractions (Retraction Watch)

The Retraction Watch database is public, CC-BY, updated every
working day, and Crossref-distributed - screening is one step:

- Per DOI: query Crossref and inspect `message.updated-by`, keeping
  entries whose `type` is retraction, correction or
  expression_of_concern. Mind the direction: `update-to` points the
  opposite way, from a notice to the work it corrects, so querying
  it against a retracted paper returns nothing and the paper reads
  as clean. Or check against the full CSV (public git repository at
  gitlab.com/crossref/retraction-watch-data).
- Screen at these moments: finalizing a bibliography, submitting a
  manuscript (rseng-research-integrity runs the fuller pre-submission
  battery), and citing a paper as the FOUNDATION of a method -
  building on a retracted result is the costliest citation failure.
- A retraction hit is information, not automatic removal: report
  it with the retraction reason and let the author decide - citing
  retracted work knowingly (e.g. to discuss the retraction) is
  legitimate; citing it unknowingly is the failure.

## Where citations hide in code projects

Manuscripts are not the only bibliography. Check:

- CITATION.cff `references` and `preferred-citation` entries
  (rseng-citation-metadata), codemeta.json referencePublication.
- README "please cite" blocks and papers listed in docs.
- Algorithm-source comments ("implements the method of Smith
  2019") - a wrong citation here misdirects future maintainers.
- Dependency citation duties: software the project builds on that
  requests citation (rseng-software-reuse's cite-what-you-adopt) -
  verify those entries like any other.

## Currency and completeness

- Prefer the DOI form of a reference; preprint-vs-published drift
  is common - when a cited preprint has a published version,
  OpenAlex links the two; offer the update while preserving intent
  (sometimes the preprint IS the cited artifact -
  rseng-open-science-practices).
- Keep bibliographies regenerable: store references as structured
  data (BibTeX/CSL/CFF) and render from it (rseng-documentation);
  hand-maintained duplicated reference lists drift apart.
- Wire a lightweight check into CI where the project's references
  are load-bearing (rseng-ci-cd): DOI resolution plus retraction
  screen on the reference files - the citation analogue of a link
  checker.

## Working with this skill

This skill is source-independent: its authority is the Crossref,
OpenAlex and Retraction Watch services linked below. It is the
verification counterpart to rseng-citation-metadata and feeds
rseng-research-integrity's pre-submission checks.

Learn more (verified):
  - https://api.crossref.org/swagger-ui/index.html - Crossref REST
    API
  - https://help.openalex.org - OpenAlex API (open, keyless)
  - https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/ -
    Retraction Watch data via Crossref
  - https://gitlab.com/crossref/retraction-watch-data - Retraction
    Watch database, public daily-updated repository

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-ci-cd - reference resolution checks in CI
- rseng-citation-metadata - making own software citable
- rseng-discovery - verifying surveyed literature leads
- rseng-fact-checking - verifying non-citation claims
- rseng-open-science-practices - preprint-to-published version links
- rseng-research-integrity - pre-submission verification battery

<!-- related-skills:end -->
