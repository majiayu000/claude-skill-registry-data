---
name: goodies
category: knowledge
description: >
  Ingest, contextualize, and index curated resources (websites, tools, design references,
  research papers, UI kits) into a public GitHub Pages vault while automatically linking
  them to the local Knowledge Graph via /checkit and P6 bookkeeping. Dynamically resolves
  and expands category ontologies, generates client-side search indices, and publishes
  the updated vault database to a public repository. USE WHEN: /goodies, goodies,
  goodies add, add to goodies, bookmark this site, save to goodies, bookmark good resource,
  curate website. NOT FOR: internal-only notes without public vault indexing; general web
  searches without curating a resource.
---

# goodies — Curate, KG-Index, and Publish to Public Goodies Vault

`/goodies` takes a URL or resource pointer (website, tool, design reference, research paper), metabolizes it into the local Knowledge Graph using `/checkit` and P6 bookkeeping, dynamically classifies it within an evolving category taxonomy, and publishes the rich record to a public GitHub Pages repository (`goodies`).

It is a **bstack composition skill**: it fires `/checkit` research, P6 bookkeeping, dynamic taxonomy resolution, and git sync scripts in sequence.

## The One Rule

> **Curate with depth, index with provenance, publish with dynamic taxonomy.**
>
> A resource saved to goodies must never be a bare link. It must carry deep context, primary-source verification, Knowledge Graph linkage (`kgEntity`), and an evolving category taxonomy so the public vault remains searchable, beautiful, and valuable.

## Pipeline (what `/goodies add <URL>` does)

1. **Ingest & Verify (`/checkit`)**
   - Run the `/checkit` pipeline on the target URL/artifact.
   - Fetch primary source verbatim, extract title, tagline, deep summary, key highlights, stack tags, and favicon/OG image.

2. **Index into Knowledge Graph (P6 Bookkeeping)**
   - Create or update the corresponding entity page in `research/entities/tool/` or `research/entities/concept/`.
   - Score the entity using Nous gate criteria (novelty, specificity, relevance).
   - Capture `kgEntity` reference path for vault linking.

3. **Dynamic Taxonomy Resolution**
   - Execute `scripts/vault_schema.py` to inspect `data/taxonomy.json`.
   - Determine if the resource fits an existing category OR dynamically expands the ontology with a new category node.
   - Assign primary category, subcategory, and tag taxonomy.

4. **Format & Validate Vault Record**
   - Construct Vault Item JSON conforming to schema specification.
   - Execute schema validation tests (`scripts/vault_schema.py`).

5. **Sync & Publish (`scripts/vault_sync.py`)**
   - Write individual record to `data/items/<slug>.json`.
   - Merge into consolidated `data/vault.json` database.
   - Regenerate client-side search index (`data/search-index.json`).
   - Scaffold missing OSS standards (`LICENSE`, `CONTRIBUTING.md`, `.gitignore`, enhanced `README.md` with badges & live links).
   - Enforce CSS `[hidden] { display: none !important; }` rule to guarantee modal backdrops stay hidden on load.
   - Sync GitHub repository metadata (`description`, `homepage`, `topics`) via `gh repo edit`.
   - Commit & push to public repository (e.g. `goodies`), triggering GitHub Pages auto-deploy.

## Deterministic Scripts & Core Tools

- `scripts/vault_schema.py`: Validates item JSON schemas and manages dynamic category taxonomy resolution.
- `scripts/vault_sync.py`: Merges vault items, updates aggregate DB, scaffolds OSS files, syncs GH repo metadata, generates Fuse search indices, and handles Git sync.
- `scripts/vault_ingest.py`: Orchestrates URL ingestion, `/checkit` extraction, metadata scraping, and item construction.

## Anti-Rationalization

| Excuse | Reality |
|---|---|
| "A bare link and title is enough." | Bare links degrade quality. /goodies requires summary, highlights, and KG provenance. |
| "Categories should be hardcoded." | Categories are dynamic ontologies that evolve as new domains are discovered. |
| "I'll sync the public repo later." | The skill commits & pushes automatically to keep GitHub Pages live and fresh. |

## Validation

- Executing `python3 scripts/vault_schema.py` validates schema compliance.
- Executing `pytest tests/` runs unit tests for schema and sync modules.
- Executing `bstack skills audit` verifies skill integrity.

## References

- [`references/vault-architecture.md`](references/vault-architecture.md) — Architectural specification for vault data model and GitHub Pages integration.
