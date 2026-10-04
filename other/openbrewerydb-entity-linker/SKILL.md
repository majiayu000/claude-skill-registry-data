---
name: openbrewerydb-entity-linker
description: Match existing OpenBreweryDB records to Wikidata and OpenStreetMap entities for interoperability, external identifier analysis, and linkage audits. Trigger when users ask to reconcile OBDB breweries with Wikidata QIDs, OSM objects, Nominatim, Overpass, knowledge graphs, or external IDs; produce read-only, issue-ready findings only.
---

# OpenBreweryDB Entity Linker

Research links between existing OpenBreweryDB (OBDB) records and Wikidata or OpenStreetMap (OSM). This is a read-only analysis skill that returns an issue-ready report. Do not edit datasets, schemas, generated files, application code, or GitHub issues. The current OBDB schema has no Wikidata/OSM identifier fields, so never write external IDs into records or propose a data PR as the output.

## Non-negotiable limits

- Never run `npm install`, any npm script, an equivalent package-manager command, an upstream script implementation, or an ad hoc reproduction of an upstream implementation.
- Do not clone, branch, edit, commit, push, or open a data/schema PR.
- Do not modify Wikidata or OSM. Do not submit changes through APIs, bots, QuickStatements, editors, or imports.
- Do not infer an identity from name similarity alone. Preserve unresolved and conflicting cases.
- Query only the records needed for the selected scope. Respect published API limits and terms; stop on throttling rather than rotating endpoints or evading controls.

## Workflow

### 1. Select a bounded scope

Require an explicit OBDB record, ID list, city/region, or small auditable batch. Clarify the intended targets (Wikidata, OSM, or both). For a broad request, propose a representative pilot rather than scanning either upstream dataset.

Record the retrieval time, source URLs/endpoints, query text or parameters, and scope. Use the current OBDB API/read-only files only to identify existing records; do not alter them.

### 2. Check existing work first

Before external queries, search open issues and pull requests in `openbrewerydb/openbrewerydb` for the OBDB ID, brewery name, candidate QID, and OSM object (`node|way|relation` plus ID). Include both issue and PR results in the report. If the finding is already tracked, link it and place any new evidence in the draft report rather than commenting or opening a duplicate.

### 3. Discover candidates responsibly

- Wikidata: follow `references/wikidata-matching.md`. Prefer direct entity lookup/search before a narrowly bounded SPARQL query.
- OSM: follow `references/openstreetmap-matching.md`. Prefer direct object lookup or a bounded geographic query; use public Nominatim only for occasional interactive searches.
- Use descriptive identification headers where supported, cache results during the task, serialize requests, and apply exponential backoff to `429`/`5xx` responses.
- Preserve required attribution and links in the report. Do not bulk scrape, bypass quotas, or use public services for systematic coverage.

### 4. Compare evidence

For every candidate compare normalized name and aliases, full address, locality/postcode/country, canonical website/domain, and coordinates. Treat coordinates as supporting evidence with source accuracy in mind, not as proof. Note operating status and source recency where relevant.

Use exact source values in the evidence table. Normalize only for comparison: case-fold names, remove superficial punctuation/legal suffixes, normalize URL hosts, and compare addresses component-by-component. Do not silently replace source values.

### 5. Resolve cardinality

- **One OBDB to one entity:** accept only when the combined evidence identifies the same physical brewery/location.
- **One OBDB to many entities:** distinguish duplicate external entities from legitimate brewery, brand, headquarters, production site, and taproom entities. Report each candidate and relationship; do not choose without evidence.
- **Many OBDB to one entity:** determine whether OBDB records are duplicate locations or distinct venues represented too broadly externally. Report all OBDB IDs and do not collapse them.
- **Many to many:** split into location-level propositions. Mark unresolved propositions `conflict` or `low`, never force a global mapping.

Apply `references/confidence-model.md` independently to each proposed pair. A conflict overrides an otherwise high numeric or textual match.

### 6. Produce issue-ready reporting only

Use `references/issue-report-template.md`. Include confirmed links, rejected candidates, unresolved conflicts, query provenance, attribution, policy notes, existing issue/PR search results, and a clear maintainer decision request. Recommendations may describe a future schema discussion, but must not include dataset/schema edits or external-ID writes.

Return the completed issue title/body as Markdown. Never open or modify an issue or pull request in this workflow.

## Stop conditions

Stop and report the limitation when the scope is unbounded, a service forbids the intended query pattern, rate limiting persists, evidence cannot distinguish same-name locations, coordinates materially disagree, official sources indicate different businesses, or existing work already tracks the same linkage. Keep uncertain findings in the report instead of resolving them by assumption.
