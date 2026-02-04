---
name: bib-managing
description: Curate and validate BibTeX bibliographies against academic databases.
---

# Bibliography Management

Curate BibTeX bibliographies with validation against academic databases.

## When to Use

- Adding a citation for a paper (user knows title/author, needs proper BibTeX)
- Validating an existing references.bib file before submission
- Building a bibliography for a draft (identify what needs citing)
- Cleaning up a messy .bib file (dedup, standardize, fill DOIs)

**Don't use for**: Quick one-off lookups where you don't need validated BibTeX.

## Tool: bibval

bibval validates BibTeX against academic databases:

```bash
bibval references.bib              # Validate all entries
bibval references.bib -k key1,key2 # Validate specific entries
bibval references.bib --strict     # Treat warnings as errors
```

**Databases checked**: CrossRef, DBLP, ArXiv, Semantic Scholar, OpenAlex, OpenReview, Zenodo

**Issues detected**:
- Year mismatches
- Title differences
- Author discrepancies
- Missing DOIs

## Quality Rubric

### Pass (bibliography is healthy)

| Criterion | Requirement |
|-----------|-------------|
| **bibval clean** | Exits 0 with no errors |
| **No duplicates** | No duplicate keys or DOIs |
| **Required fields** | All entries have: author, title, year, venue |
| **DOIs present** | DOIs included where available |

### Warn (needs review)

| Criterion | Requirement |
|-----------|-------------|
| **Low DOI coverage** | >20% entries missing DOIs |
| **Inconsistent keys** | Mix of styles (AuthorYear vs author2024foo) |
| **Venue inconsistency** | Mix of abbreviations (ICML vs Proc. ICML) |
| **Missing seminal works** | Obvious gaps a reviewer would notice |

### Fail (must fix)

| Criterion | Requirement |
|-----------|-------------|
| **bibval errors** | Year/title/author mismatches |
| **Placeholder text** | TODO, TBD, placeholder in fields |
| **Broken cross-refs** | @string or crossref that doesn't resolve |

## Operations

| Operation | Description |
|-----------|-------------|
| **Add** | Find BibTeX for a paper, validate, append to file |
| **Validate** | Run bibval on existing file, fix issues |
| **Curate** | Analyze document for citation needs, build bibliography |
| **Clean** | Deduplicate, standardize formatting, fill missing DOIs |

## Citation Key Format

Use consistent format: `<FirstAuthorLastName><Year><FirstWord>`

Examples:
- `Vaswani2017Attention`
- `Sutskever2014Sequence`
- `Brown2020Language`

## Academic Database Priority

When searching for papers:
1. **DBLP** - CS papers, canonical BibTeX
2. **arXiv** - Preprints, version history
3. **DOI.org** - Direct lookup if DOI known
4. **Semantic Scholar** - Cross-domain, citations

## Output Schema

```json
{
  "operation": "add | validate | curate | clean",
  "status": "CLEAN | NEEDS_INPUT | ERRORS",
  "entries_processed": 0,
  "errors": [],
  "warnings": [],
  "changes": []
}
```

## Artifact Location

Bibliography files co-locate with the writing:

```
project/
├── paper/
│   ├── draft.md
│   ├── references.bib    ← bibliography here
│   └── figures/
```

## Issue Classification

When reviewing bibval output:

| Category | Action | Examples |
|----------|--------|----------|
| **AUTO_FIX** | Fix automatically | Year typos, missing DOIs that exist |
| **VERIFY** | Ask user | Title changes, author spelling |
| **ACCEPT** | Leave as-is | Old paper without DOI, acceptable warning |
