---
name: rseng-discovery
description: >-
  Covers discovering the research landscape around a topic or project: finding
  relevant publications (OpenAlex, arXiv, Zenodo, JOSS, Semantic Scholar,
  Google Scholar) and finding related software - libraries, packages, tools,
  platforms and competitor or alternative projects - across software
  registries, archives, package indexes, public forges and curated awesome
  lists. Use when the user asks what exists on a topic, wants related work,
  prior art, alternatives or competitors surveyed, needs a state-of-the-field
  picture for a paper or proposal, or is about to build something whose
  neighbors are unknown. (RSD-based reuse suggestions with bundled snapshots
  are rseng-software-reuse; adoption vetting is rseng-dependency-management;
  verifying found references is rseng-citation-hygiene.)
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Discovery: publications and software around a topic

Most research work begins in a landscape someone else has already
mapped in part. Discovery is the deliberate survey of that
landscape before building, writing or claiming novelty: the
publications that define the state of the field, and the software
that already solves pieces of the problem. Doing it early is
cheaper than discovering a competitor in review, and the survey
itself becomes reusable material for the paper's related-work
section and the proposal's state of the art.

## Finding publications

Work from open, keyless APIs first; they make searches
reproducible and scriptable:

- OpenAlex covers most of the scholarly record with abstracts,
  citation links and topic filters; Crossref serves DOI metadata;
  Semantic Scholar adds influence signals and TLDRs; arXiv covers
  preprints in its fields. Zenodo and JOSS matter specifically for
  research software: JOSS papers ARE software descriptions, and
  Zenodo records often carry the software itself.
- Google Scholar casts the widest net (theses, reports, gray
  literature) but has no API and rate-limits scraping; use it
  interactively for coverage checks, not in pipelines.
- Snowball in both directions from the two or three most relevant
  hits: who do they cite (backward), who cites them (forward -
  OpenAlex and Semantic Scholar both serve citing works). One good
  seed paper beats twenty keyword guesses.
- Search by concept variants, not one phrasing: field synonyms,
  British/American spellings, method names old and new - and
  record the queries used, so the search is repeatable and its
  gaps are visible (rseng-reproducibility's spirit applied to
  searching).

## Finding software

Cast several nets; each finds things the others miss:

- Research software registries: Research Software Directory
  instances (rseng-software-reuse ships offline snapshots and the
  search discipline), domain registries (bio.tools for life
  sciences, ASCL for astronomy, and their field equivalents).
- Package indexes for the stack (PyPI, CRAN, conda-forge, npm):
  search by task words and by the names publications mention;
  libraries.io searches across ecosystems at once.
- Public forges: code search on GitHub/GitLab finds the
  unregistered majority - search READMEs by domain terms, filter
  by language and activity, and check the topics/tags of anything
  close.
- Curated awesome lists collect a community's known tools; find
  the list for the domain, then treat it as a lead generator -
  lists rot, so verify each candidate is alive.
- Software archives: Software Heritage preserves code whose forge
  home vanished; JOSS and Zenodo double as software discovery for
  peer-reviewed and archived tools.
- Papers with Code links publications to implementations in
  ML-adjacent fields.

## From findings to decisions

Discovery feeds the pack's decision skills rather than replacing
them:

- Candidate software worth adopting goes through the six-axis
  intake vetting (rseng-dependency-management); fit judgment and
  citation duty live with rseng-software-reuse.
- Competitor and alternative surveys become an honest comparison
  table: what each neighbor does, its stack, license, activity and
  how the user's project differs - the state-of-the-field material
  that software papers (rseng-software-peer-review), communication
  (rseng-science-communication) and documentation's related-projects
  section (rseng-documentation) all need. Differences stated
  honestly build more trust than silence about competitors.
- Everything found gets verified before it is repeated: resolve
  the DOI, open the repository, confirm the claim matches the
  source (rseng-fact-checking, rseng-citation-hygiene) - discovery
  collects leads, verification makes them citable.
- Record the survey: queries, sources searched, date, and the
  shortlist with reasons, in the project record
  (rseng-project-tracking) - a documented search can be updated;
  an undocumented one gets redone from scratch.

## Working with this skill

This skill is source-independent: its authority is the discovery
services linked below. It is the front end of a chain: discovery
finds, rseng-software-reuse and rseng-dependency-management judge,
rseng-fact-checking and rseng-citation-hygiene verify.

Learn more (verified):
  - https://help.openalex.org - OpenAlex API
  - https://arxiv.org - arXiv
  - https://www.semanticscholar.org - Semantic Scholar
  - https://scholar.google.com - Google Scholar (interactive)
  - https://zenodo.org - Zenodo
  - https://joss.theoj.org - JOSS
  - https://bio.tools - bio.tools registry
  - https://libraries.io - cross-ecosystem package search
  - https://github.com/sindresorhus/awesome - the awesome-list
    index
  - https://huggingface.co/papers - Hugging Face Papers

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-citation-hygiene - verifying surveyed references
- rseng-dependency-management - vetting discovered software
- rseng-fact-checking - verifying claims before repeating them
- rseng-science-communication - related-work narrative for audiences
- rseng-software-peer-review - state-of-field for JOSS paper
- rseng-software-reuse - candidate fit and citation duty

<!-- related-skills:end -->
