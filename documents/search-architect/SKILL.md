---
name: search-architect
description: >
  Designs a search engine index of an already-scoped use case — Elasticsearch or OpenSearch kept as
  a rebuildable projection of a source of truth: the search document and its strict mapping, the
  versioned index behind an alias, the query and its cursor, the indexer that writes each change
  with the source's version, the rebuild with the alias swap, and the lag the projection consumes
  of the case's freshness — into the `23-search.md` partial. Use when the request involves full-text
  or faceted search, Elasticsearch, OpenSearch, a search index, a mapping, an alias, a reindex, an
  indexer consuming change events, or a read that searches by words, filters and facets. Piece of
  the `/new-feature` pipeline: requires `00-use-case.md` in the given folder with a `Search
  index` row that names an engine, plus `10-domain.md` — and stops without them.
argument-hint: "[path of the UC-NNN-<slug> folder]"
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion, Bash(find:*), Bash(ls:*), Bash(grep:*), Bash(sort:*), Bash(awk:*), Bash(curl:*)
model: opus
---

## Available specs

!`find "${CLAUDE_PROJECT_DIR:-.}/docs/use-cases" -mindepth 1 -maxdepth 1 -type d -name 'UC-*' 2>/dev/null | sort`

Empty above → none yet, run `/use-case-design` first. (`find`, not an `ls` glob: under zsh an unmatched glob
aborts the command before any fallback runs.)

## Target

$ARGUMENTS

---

# Search Architect

Designs **a copy of the project's records that a search engine can answer from, and how the copy
stays a copy**: which fields the engine holds and how each is typed, the index version behind its
alias, the query a reader runs and how it pages, the indexer that keeps the copy in step with the
source, the rebuild that recreates it from the source, and how old an answer can be because of it.

**Entry rule: an engine named by the use case, and a domain to read.** This skill reads
`docs/use-cases/UC-NNN-<slug>/00-use-case.md` and runs only when its `Search index` row names a
projection and its engine (`Order → Elasticsearch projection`). The row reads `none`, or is missing,
or names no engine → stop and say so, and tell the caller to run `/use-case-design`: the engine is a
fact the request or the user states there, never chosen here. `10-domain.md` is required too — the
query side implements a port of kind `search index` it declares, and the indexer consumes an event
it names.

**What this skill never weighs: whether the case should have a search index at all, or which engine.**
Both are recorded in `00-use-case.md` before this skill runs. A projection that this design finds
unworkable — a field the source does not have, a lag larger than the freshness the case states — is
a divergence to report, not a reason to pick another engine.

**Exit rule: it doesn't write code.** It emits `23-search.md`, with the mapping file inside it as a
JSON block headed by its target path. The Java classes and the mapping file come from the executor,
which reads the partial and the `templates/` exemplars.

**Rule rule: the rules don't live here.** The projection invariant, the index lifecycle, mapping,
writes, queries, failure, configuration and tests are `@.claude/rules/search.md`. This skill applies
and cites it; it doesn't reproduce it.

## How it's invoked

Two paths: `/search-architect` by hand, or chained by `/new-feature` as step 3e — after the inbound
and outbound HTTP steps, before messaging and jobs, which read its requirements. That's why it does
**not** carry `disable-model-invocation` (`@.claude/decisions/0007-pipeline-skills-invocation.md`).
The guard against firing out of order is the entry rule above.

## Why this is a skill and not a subagent

Form 1, motivated by axis 1 of the designer's interview: no piece owned a search engine index, and
the maintainer chose to design it ahead of a run that shows the defect, on the pitfalls the official
documentation records (`references/pitfalls-search.md`), so that a planned solution-design step can
write `Search index` for a case and find a designer behind it. The closest rejected form was a
conditional block of `persistence-architect`: the projection is another artifact and another moment —
eventually consistent, fed by events, rebuilt by a job — and its requirements must reach messaging
and jobs, which run before persistence. A subagent fails the counter-test on all three points.

Pinned to `opus`: the partial is what the executor implements verbatim
(`@.claude/decisions/0081-skill-model-required-per-class.md`). Design record:
`@.claude/decisions/0147-document-storage-and-search-architect.md` (this repository only).

## Boundary with neighboring skills

| Piece | Decides | Never decides |
|---|---|---|
| `use-case-design` | Whether the case has a search index and its engine — from the request, or one factual question — and the `Freshness` tolerance | The projection, the mapping |
| `domain-modeling` | The `search index` port, the read projection it returns, the change event with the source version | That the port is served by Elasticsearch |
| **this skill** | The search document and mapping, the index version and alias, the query shape and cursor, the indexer's write rules, the rebuild's adapter, the lag consumed, the search dependency and the search compose row | The engine, the event's transport, when the rebuild runs |
| `messaging-architect` | The indexer's consumer — topic, partition key, retry, dead letter — from § 8's requirement | The document written |
| `jobs-architect` | The rebuild job — trigger, batch, switch — from § 8's requirement | The alias swap's statement |
| `persistence-architect` | The source's version field and its outbox, from § 8's requirement | Anything in the index |
| `cache-architect` | A cache over the search port, bounded by `Freshness` minus § 6's lag | The lag |
| `ai-architect` | A search by meaning (`dense_vector`, `knn_vector`) — a `vector store` port, even on the same engine | Full-text search |

Database indexes and full-text inside the source's own database (`tsvector`, `pg_trgm`, a MongoDB text
index) are `persistence-architect`'s: they are the aggregate's storage, not a projection.

## The three kinds of case

A search projection is never designed by one use case. The boundary test of
`use-case-design/references/scope-boundary.md` separates three, each with its own `23-search.md`:

| Case | `Trigger` | What this skill designs in it |
|---|---|---|
| **Read** — "search orders by customer name" | REST or GraphQL | § 3 query, § 6 lag; § 1 and § 2 only when it is the first case of the projection |
| **Indexer** — "index order on OrderChanged" | `inbound messaging adapter` | § 4 write rules, § 8 consumer requirement; § 1 and § 2 when first; the approved write cases that must publish the event go to `## Impact on approved use cases` |
| **Rebuild** — "rebuild the orders index" | `inbound job adapter` | § 5 sequence, § 8 job requirement; a mapping change's new version in § 2 |

The first case of a projection, whichever kind, fixes § 1 and § 2 (version 1). Every later case
inherits them; a case that changes a field's type writes the next version and requires a rebuild.

## Procedure

1. **Read the specs.** `00-use-case.md` (`Trigger`, `Storage`, `Search index`, `Freshness`, the
   Components table), `10-domain.md` (the `search index` port, the read projection, the change
   event). Apply the entry rule. Name which of the three kinds this case is.

2. **Survey — every answer the project already gave is inherited, never re-asked.**

   ```bash
   # Mapping files and search adapters already in the project
   find src/main/resources/search -name '*.json' 2>/dev/null | sort
   grep -rln "data.elasticsearch.annotations.Document" --include='*.java' src/main 2>/dev/null
   # Earlier search partials
   find docs/use-cases -name '23-search.md' 2>/dev/null
   # The search dependency already in the build
   grep -nE "spring-boot-starter-data-elasticsearch|spring-data-opensearch" pom.xml
   ```

   And the active blueprint's `packages.map` entry ending in `.search` — the package every search
   adapter goes to. No such entry → stop and name the missing blueprint line.

   | Fact | Inherited from | Asked only when |
   |---|---|---|
   | Engine of the project | `00-use-case.md` `Search index`; a search dependency in `pom.xml` | Never asked here. A case naming the other engine than the project's → divergence, stop |
   | Projection document and mapping (§ 1, § 2) | The latest `search/<alias>-v<N>.json` and an earlier `23-search.md` | First case of the projection |
   | The source's version field and change event | `20-persistence.md` and `10-domain.md` of the source's cases | Neither declares one — § 8 requires it |

3. **Interview — only what steps 1 and 2 did not settle.** `AskUserQuestion`, at most 4 questions per
   call and **never fewer than 2 real options** per question (`@CLAUDE.md` § Known pitfalls). Business
   words, never engine vocabulary.

   | Axis | Decides | Skip when |
   |---|---|---|
   | **What a reader types and filters by** — free words over which fields, exact filters, facets | § 1 field types, § 3 query | The request already lists them |
   | **How results are ordered** — relevance, newest first, a field | § 3 sort (always ending in the unique field) | Only one order makes sense — record it |
   | **How deep a reader pages** — a first screen, or every result | § 3 page ceiling; an export is a job, not a page | — |
   | **Read-your-own-write** — must a person see their change in the search the moment they save it? | `WAIT_UNTIL` on that one write path, or the lag | The case states `Freshness`; a reader who tolerates seconds needs nothing |

4. **Design the projection — § 1.** One row per field: source field, search field name, type
   (`text`, `keyword`, `text` + `keyword` sub-field, number, `date` with its format, `nested`), and
   its use (searched, filtered, sorted, displayed). A field no row uses is not projected. Money in
   minor units; ids as `keyword`; a unique `keyword` copy of the id for the sort's tiebreaker; the
   `deleted` tombstone flag. Shape: `templates/SearchDocument.java.example`.

5. **Fix the index — § 2.** Alias, version, the mapping file as a fenced `json` block headed by its
   path (`src/main/resources/search/<alias>-v<N>.json`, shape `templates/search-index.json.example`):
   `dynamic: strict`, every § 1 field, one primary shard, the refresh interval. Replicas per
   environment (`app.search.replicas`). A later version states what changed and why the change needs
   a new index.

6. **Fix the queries — § 3.** Per port method: the match fields and their boosts, the exact filters,
   the tombstone filter, the sort ending in the unique field, the page ceiling, the cursor (the last
   hit's sort values), the fields returned. Shape: `templates/SearchAdapter.java.example`
   (`OrderSearchAdapter`).

7. **Fix the writes — § 4 (indexer case).** The event consumed, the snapshot it carries, the
   upsert with the source's version as the external version, the tombstone on delete, the stale
   result acknowledged, the second alias written during a rebuild, the dead-letter condition. Shape:
   `OrderIndexerAdapter`.

8. **Fix the rebuild — § 5 (rebuild case, or a new version).** The three steps of
   `templates/SearchRebuild.java.example` — begin, write in batches with the source's version,
   publish with one alias action — and the source's port the job pages through.

9. **State the lag — § 6.** Event to index (the outbox's poll and the consumer) plus the refresh
   interval, as one duration, next to the case's `Freshness`. Larger than the tolerance → a
   divergence, reported, never resolved by refreshing on write. What remains is the bound a cache
   over this port may use; `cache-architect` reads it.

10. **Failure — § 7.** The unavailable family for an unreachable engine or a missing alias, and what
    the read does then, from `00-use-case.md`'s errors — fail, or degrade as the case states.

11. **Requirements to other partials — § 8.** By what they are, the final form decided by each owner:
    - `10-domain.md` — the `search index` port and its read projection; the change event carrying the
      snapshot and the source version
    - `20-persistence.md` — the source's version field, and the event written to the outbox with the
      state change
    - `25-messaging.md` — the indexer's consumer: one partition key per aggregate, at-least-once, the
      stale result acknowledged, a bounded retry and a dead letter
    - `35-jobs.md` — the rebuild job: on demand and after a version change, a bounded batch, never two
      at once
    - `22-cache.md` — the remainder of § 6

12. **Declare dependencies — § 9.** Elasticsearch: `spring-boot-starter-data-elasticsearch`, version
    empty — Spring Boot manages it. OpenSearch: `org.opensearch.client:spring-data-opensearch-starter`
    and `org.opensearch.client:opensearch-java`, with
    `org.opensearch.client:spring-data-opensearch-testcontainers` and
    `org.opensearch:opensearch-testcontainers` for tests — Spring Boot manages none of them, so the
    version is resolved now, never from memory (`@CLAUDE.md` invariant 8):

    ```bash
    # 1. The project's Spring Boot version: the parent in pom.xml.
    # 2. The compatibility matrix: the row whose Spring Boot column matches it gives the series.
    curl -s https://raw.githubusercontent.com/opensearch-project/spring-data-opensearch/main/README.md | grep -A12 'Compatibility Matrix'
    # 3. The newest release of that series.
    curl -s https://repo1.maven.org/maven2/org/opensearch/client/spring-data-opensearch-starter/maven-metadata.xml | grep -o '<version>[^<]*'
    curl -s https://repo1.maven.org/maven2/org/opensearch/opensearch-testcontainers/maven-metadata.xml | grep -o '<release>[^<]*'
    ```

    No network, or no row for the project's Spring Boot → ask, and record the answer and its source.
    The executor may write `pom.xml` for exactly these rows.

12b. **Decide the design patterns of this layer.** Run
    `@.claude/skills/gof-design-patterns/SKILL.md` § Design-time use over the adapters this case adds.
    The answer goes into `## Design patterns` — `none` when nothing matches.

13. **Check the engine has a container.** List the keys inside the `services:` block:

    ```bash
    awk '/^services:[[:space:]]*$/{s=1;next} /^[^[:space:]#]/{s=0} s&&/^  [A-Za-z0-9_.-]+:[[:space:]]*(#.*)?$/{sub(/[[:space:]]*#.*$/,"");print}' docker-compose.yml
    ```

    Write the answer as a row of `## Compose services`, shaped and decided by
    `@.claude/skills/docker-architect/references/compose-service-decision.md` — `exists` when
    `elasticsearch` or `opensearch` is listed, otherwise the question that reference owns. An
    `external` answer makes that address the host default of the engine's `uris` in § 10. Do **not**
    invoke `docker-architect` and do not edit `docker-compose.yml`.

14. **Write the partial.** `docs/use-cases/UC-NNN-<slug>/23-search.md`, from
    `templates/search-spec.md.example`. Eleven numbered blocks plus `## Compose services` and
    `## Design patterns`, all mandatory, each `none` when there is nothing — absence is not `none`.

15. **Report and stop.** Path of the file written; the kind of case; the projection's version; the lag
    next to the tolerance; every § 8 requirement with its target partial; the `## Compose services`
    row. Don't invoke anyone else: messaging, jobs and persistence run next and read § 8.

## What the partial contains

| Block | Fixes |
|---|---|
| 1 · Projection | One row per field — step 4 |
| 2 · Index | Alias, version, the mapping file block, shards, replicas per environment, refresh interval |
| 3 · Queries | Per port method — step 6 |
| 4 · Writes | The indexer's rules — step 7. `none` outside an indexer case |
| 5 · Rebuild | The sequence and the source port — step 8. `none` when no rebuild is designed in this case |
| 6 · Lag | The duration consumed, next to `Freshness`, and the remainder |
| 7 · Failure | Per port method: the family and what the read does |
| 8 · Requirements to other partials | One row per requirement, target partial named |
| 9 · Declared dependencies | Coordinates; version empty when Spring Boot manages it, otherwise the resolved version and its source |
| 10 · Configuration | Every property, its value, the reason |
| 11 · Deferred | Same shape as every partial |
| Compose services | The engine's row |
| Design patterns | Step 12b |

Plus `## Impact on approved use cases` and `## Implementation order`, as in every partial.

The exemplars in `templates/` are **reference for form**, not files to copy:

| Exemplar | Shape of |
|---|---|
| `templates/SearchDocument.java.example` | The search document: `createIndex = false`, no type hint, external version, `text` + `keyword`, `nested`, the tombstone |
| `templates/search-index.json.example` | A mapping file: settings and the strict mapping |
| `templates/SearchIndexBootstrap.java.example` | The startup that creates the current version behind its alias, only when the alias is absent |
| `templates/SearchAdapter.java.example` | The query adapter (`CriteriaQuery`, sort, cursor, source filter, failure) and the indexer adapter (external version, stale, tombstone, the second alias during a rebuild) |
| `templates/SearchRebuild.java.example` | The rebuild's begin, batch write and atomic alias swap |
| `templates/application-search.yml.example` | Elasticsearch and OpenSearch connection, timeouts, the TLS bundle outside local runs, replicas |
| `templates/search-spec.md.example` | The partial |

## Contract

**Class:** design — the territory is `skill_classes.design` in `@.claude/schemas/extensions.json`, and
`ArchHook.java guard` enforces it. Writes inside the use case folder and nothing else.

**Reads** `docs/use-cases/UC-NNN-<slug>/00-use-case.md` (mandatory), `10-domain.md` (mandatory),
`20-persistence.md` of the source's cases, earlier `23-search.md`, `src/main/resources/search/`,
`pom.xml`, `docker-compose.yml`, the active blueprint's `packages.map`, `@.claude/rules/search.md`,
`@.claude/rules/architecture-ddd.md`, `@.claude/rules/error-handling.md`, `@.claude/rules/secrets.md`,
`@.claude/skills/docker-architect/references/compose-service-decision.md`, and this skill's
`references/`.

**Writes** `docs/use-cases/UC-NNN-<slug>/23-search.md`. Nothing else — the mapping file lives inside it.

**Owns** the search document and its mapping, the index versions and the alias, the query shape and
its cursor, the indexer's write rules, the rebuild's adapter and alias swap, the lag the projection
consumes, the search dependency and its version, and the search compose row.

**Does not decide** whether the case has a search index or which engine (`00-use-case.md`), the
port or the event (`10-domain.md`), the consumer (`25-messaging.md`), when the rebuild runs
(`35-jobs.md`), the source's schema (`20-persistence.md`), or the tests (`40-tests.md`). Does not
write Java, `pom.xml`, `application.yml` or `docker-compose.yml`. Doesn't touch `.claude/rules/**`.
