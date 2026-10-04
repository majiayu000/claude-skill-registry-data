---
name: ieee-search
description: >-
  Search, verify, and organize literature for IEEE communications manuscripts: JSAC, TWC, TCOM,
  WCL, CL, IEEE conference papers, arXiv preprints, DOI/Crossref metadata, BibTeX, related-work
  matrices, novelty checks, and citation-gap audits. Use this when the user asks to "find papers",
  "latest IEEE papers", "related work", "verify DOI", "make BibTeX", "查文献", "找IEEE论文", "补参考文献",
  or compare a manuscript's claims against prior work. Use live search or available connectors for
  current facts; never fabricate bibliographic metadata.
---

# IEEE Literature Search and Verification

Use this skill to gather and verify literature evidence before writing the Introduction, Related
Work, citations, or cover-letter significance claims. It is a search-and-verification skill, not a
license to pad references.

## Core stance

- **Search live for current literature.** For "latest", "recent", venue policy, DOI, metadata, or
  title verification, use available web/connectors rather than memory.
- **Prefer primary sources.** Publisher pages, IEEE Xplore, arXiv records, DOI/Crossref pages, and
  authors' accepted manuscripts beat blog summaries.
- **Verify before formatting.** Title, author order, venue, year, volume/issue/pages, DOI, and arXiv
  ID must come from a source. Missing fields stay missing.
- **Organize by mechanism and gap.** Related work should help the paper argue a technical gap, not
  become a chronological bibliography.
- **Do not overclaim novelty.** Search can support "differs from" and "to the best of our checked
  sources", but not universal first-ever claims without strong evidence.

## When to open extra files

| File | Open when |
|---|---|
| [references/search-strategy.md](references/search-strategy.md) | Planning queries, source selection, venue/time filters, keyword expansion, or novelty checks |
| [references/verification-and-bibtex.md](references/verification-and-bibtex.md) | Verifying metadata, DOI/arXiv records, BibTeX, citation keys, and IEEE reference fields |

Use `ieee-citation` after search to format final references, and `ieee-writing` to turn the
related-work map into manuscript prose.

## Workflow

1. **Extract the search intent:** background survey, related-work paragraph, novelty check, DOI
   verification, BibTeX export, or citation-gap audit.
2. **Build query families:** system/task, method, metric, venue, and synonyms/acronyms.
3. **Search primary sources** and note exact source URLs/DOIs/arXiv IDs. For recent work, include
   the date range searched.
4. **Screen for relevance:** same system model, same metric, same assumption, or same method family.
5. **Verify metadata** before creating BibTeX or numbered references.
6. **Build a related-work matrix:** paper -> problem -> method -> limitation -> how the user's work
   differs.
7. **Return gaps and confidence:** what was searched, what remains uncertain, and which claims need
   softer language.

## Output format

1. `Search strategy:` query families, venues/sources, date range, inclusion criteria.
2. `Verified references:` citation-ready metadata with DOI/arXiv/source links and missing fields.
3. `Related-work matrix:` `Paper -> problem/method -> key result -> limitation -> relevance`.
4. `Citation/BibTeX notes:` fields to pass to `ieee-citation`, including uncertain abbreviations.
5. `Novelty and gap note:` what can be claimed safely and what needs more evidence.
