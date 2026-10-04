---
name: dota-data
description: >
  Data engineering guidance for Dota AI Coach — sourcing match data from
  OpenDota/STRATZ, identifiers (Steam IDs, match IDs, patch IDs, rank
  tiers), hero/item reference data, match timelines and replays, API
  caching, and the RAW→BRONZE→NORMALIZED→FEATURES→DATASET pipeline using
  DuckDB/Parquet. Use whenever fetching, caching, normalizing, storing, or
  building a training dataset from historical Dota 2 match data, or when
  deciding how a new data source or dataset should be structured. Existing
  dataset-quality bugs (Turbo mixed into ranked training data, leakage,
  duplicate matches, missing patch/timestamp) are expensive to discover
  after a model is trained — consult this skill before data flows into a
  pipeline, not after.
---

# Dota AI Coach Data Engineering

This skill governs how historical Dota 2 match data gets from external
APIs into a trustworthy training dataset. The core risk this guards
against isn't "the code doesn't run" — it's silently wrong data that
still produces a plausible-looking, trained model: Turbo games diluting a
ranked-meta model, a leaked test match inflating an eval score, duplicate
matches skewing item/hero frequencies. These bugs don't crash anything;
they just make the model wrong in ways that are hard to notice later.

## Ground truth warning

Neither OpenDota nor STRATZ publish a fully stable, exhaustively-documented
contract, and their exact field semantics (rate limits, rank_tier
encoding, STRATZ-specific fields) shift and are inconsistently documented.
Treat field names and numeric codes in `references/apis-and-identifiers.md`
the same way `dota-gsi` treats GSI fields: verify against a live API
response or `odota/dotaconstants` before depending on an exact value in
code, especially rate limits and anything STRATZ-specific.

## Identifiers

Getting identifiers wrong silently corrupts joins across data sources.
See `references/apis-and-identifiers.md` for full detail; short version:

- **Steam IDs** — OpenDota's `account_id` is Steam32, not Steam64. Convert
  consistently (`steam64 = steam32 + 76561197960265728`) and pick one
  canonical form to store; don't let both forms coexist unlabeled in the
  same column.
- **Match IDs** — globally unique per match across OpenDota/STRATZ/Steam;
  the natural join key across all data sources for a given match.
- **Patch IDs** — a match's patch is either present as a direct field or
  must be derived from `start_time` against a patch-date lookup table.
  Every stored match-level record must carry patch, not just start_time,
  even when patch could theoretically be re-derived later — see the
  provenance rule below.
- **Rank tiers** — encode medal + star (and a separate leaderboard rank
  for top Immortals); confirm exact digit encoding against current
  `dotaconstants` before hardcoding a mapping.

## Data sources covered

- **OpenDota** — primary match/player data source; free tier with
  optional API key, higher limits with a key. Parsed vs. unparsed matches
  expose different data (see `references/apis-and-identifiers.md`) —
  timelines/positions require an explicit parse request.
- **STRATZ** — GraphQL API, generally used for richer parsed/historical
  data where OpenDota is insufficient. Treat STRATZ-specific claims as
  lower-confidence until verified against current STRATZ docs.
- **Replays** — raw `.dem` files are the ultimate source of truth but
  expensive to fetch/parse at scale; most pipeline work should run off
  already-parsed API data, falling back to replay parsing only when a
  needed field genuinely isn't available otherwise.
- **Heroes/items reference data** — static, patch-versioned reference
  data (hero/item mechanics) — this is what `dota-domain`'s data model
  calls "static reference data"; keep it patch-tagged and don't silently
  reuse a stale copy across patches that changed hero/item balance.

## API caching

Never call OpenDota/STRATZ live from a training run or from
`dota-architecture`'s Data Platform being invoked repeatedly for the same
match. Cache raw API responses (see the RAW stage below) keyed by match
ID/account ID/endpoint, and treat the cache — not the live API — as the
input to everything downstream. This protects rate limits, makes pipeline
runs reproducible (the API's live state can change; a cached RAW snapshot
doesn't), and keeps `dota-architecture`'s "UI must not call OpenDota
directly" rule easy to honor, since only the caching layer talks to the
network at all.

## The pipeline: RAW → BRONZE → NORMALIZED → FEATURES → DATASET

Full detail in `references/pipeline-stages.md`. Summary:

- **RAW** — unmodified API responses / replay data, exactly as received,
  cached with source/timestamp metadata. Never mutated after capture.
- **BRONZE** — RAW parsed into typed records (still close to source
  shape), with obvious garbage rejected (malformed responses, private-
  profile placeholders) but no business rules applied yet.
- **NORMALIZED** — BRONZE reshaped into this project's canonical schema:
  consistent IDs, consistent units, patch/timestamp attached to every
  record, duplicates resolved. This is the layer `dota-domain`'s data
  model concepts (Hero, Item, Position, DamageType) should align with.
  Deduplication and the "attach patch and timestamp" rule apply here —
  see `references/data-quality-rules.md`.
- **FEATURES** — NORMALIZED data transformed into model-ready features
  (equivalent in spirit to `dota-architecture`'s Feature Engine, but for
  offline/training data rather than live `MatchState`).
  Turbo/Ranked separation and abandoned-game exclusion are applied here
  or earlier — never later, since a downstream consumer shouldn't have to
  re-derive "was this game valid to use."
- **DATASET** — the final train/validation/test split, with the temporal
  split and leakage rules from `references/data-quality-rules.md`
  enforced and the split itself version-tracked as part of provenance.

## Storage: DuckDB and Parquet

- **Parquet** for BRONZE/NORMALIZED/FEATURES at-rest storage — columnar,
  compressed, easy to version by writing new files rather than mutating
  existing ones (append-only partitions, e.g. by date or patch, rather
  than in-place updates).
- **DuckDB** as the query/transform engine across pipeline stages —
  reads Parquet directly, good for the kind of analytical joins/
  aggregations this pipeline needs (joining match/player/hero data,
  computing per-patch aggregates) without standing up a server database,
  consistent with this being a local-first project (see
  `dota-architecture`).
- Keep RAW as whatever format the source naturally provides (JSON from
  APIs, `.dem` for replays) rather than forcing it into Parquet — RAW's
  job is fidelity to the source, not query performance.

## Data quality rules

The eight rules from the requesting brief, with reasoning, live in
`references/data-quality-rules.md` — read it before building or modifying
any FEATURES/DATASET-stage logic. Summary list:

1. Never mix Turbo with normal Ranked training data by default.
2. Exclude abandoned/incomplete games when inappropriate for the task.
3. Always attach patch and timestamp to every stored record.
4. Avoid duplicate matches across sources/re-fetches.
5. Track data provenance (source, fetch time, pipeline stage/version).
6. Handle private/missing profiles explicitly, not silently.
7. Prefer temporal dataset splits over random splits.
8. Never cause train/test leakage.

## Data quality checklists

`references/data-quality-checklists.md` has pre-ingestion, pre-training,
and pre-release checklists — run the relevant one before trusting a new
data source, before kicking off a training run, or before shipping a
dataset/model built from this pipeline.
