---
name: author-publication-versions
version: 1.0.0
description: Fetch version lineages of the author's own published works (Zenodo) and record a cross-repository current-DOI ledger. Use when fixing self-citations or related identifiers, after a Zenodo version bump, or when updating own-work rows in the literature matrix
---

# Author Publication Versions

## Purpose
For the author's published works (v1: Zenodo only), fetch **concept DOI** and **per-version DOIs** from the primary API and write a cross-repository ledger. Self-citations, related identifiers in deposit metadata, and own-work rows in the literature matrix must use the **Current** version DOI (avoid citing superseded Zenodo version DOIs).

## Trigger Conditions
- Immediately before citing own work or listing related identifiers (DOI lock)
- Right after publishing a new Zenodo version (refresh the ledger)
- When updating own-work rows (P1 / P2 / …) in the literature matrix
- When the user asks for “own-work versions” or “current Zenodo DOI”

## Prerequisites
- Contact email: `export SCHOLARLY_CONTACT_EMAIL="..."` (polite pool; script refuses HTTP if unset)
- Work list: [`config/author_publications.json`](../../../config/author_publications.json) (`works[].zenodo` = DOI or record id)
- v1 scope: **Zenodo only** (no arXiv version history / ORCID enumeration yet)

## Procedure

### Step 1: Confirm inputs
1. Ensure `config/author_publications.json` lists the author's Zenodo DOIs
2. If missing, append DOIs or pass `--doi` on the CLI
3. Output path is **repo-root relative** `docs/literature/author-publication-versions.md` (not under a paper-id; cross-cutting ledger)

### Step 2: Fetch version lineages
Run from the paper repository root (e.g. `academic-papers`):

```bash
# Submodule install
python3 .scholarly-agent-skills/scripts/fetch_publication_versions.py

# Skills repo root, or via symlink
python3 scripts/fetch_publication_versions.py

# Extra DOI / dry-run
python3 scripts/fetch_publication_versions.py --doi 10.5281/zenodo.22065716 --dry-run
```

> Multiple version DOIs for the same concept are deduplicated by concept id.

### Step 3: Align downstream artifacts
1. Read `docs/literature/author-publication-versions.md`
2. Treat **Cite targets** as the source of truth for the current DOI
3. Align as needed (do not auto-commit):
   - Own-work rows in each paper's `literature/literature-matrix.md`
   - Related identifiers in `design/deposit-metadata.md` (drop superseded version DOIs)
   - Bibliography entries for own works

### Step 4: Superseded version DOIs
- Old versions may appear in the ledger; **default cite / related-id target is Current only**
- Use an older version DOI only with an explicit historical reason
- Concept DOIs may resolve to the latest version; for a pinned version, write the **version DOI**

## Outputs
- `docs/literature/author-publication-versions.md` (cross-repo: Summary / Cite targets / per-work tables)
- (Optional) DOI sync diffs for matrix, deposit-metadata, and bibliography (after author confirmation)

## Related Skills
- [`submission-venue-advisor`](../submission-venue-advisor/SKILL.md) — deposit related-identifier drafts
- [`literature-search`](../literature-search/SKILL.md) — third-party literature search (separate from this ledger)
- [`citation-traceability-audit`](../citation-traceability-audit/SKILL.md) — body citations vs DOIs
- [`pdf-paper-ingestion`](../pdf-paper-ingestion/SKILL.md) — re-fetch PDF for the current version when needed
