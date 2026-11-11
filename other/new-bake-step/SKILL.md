---
name: new-bake-step
description: "Use when adding or reshaping an offline bake step in pipeline/bake (a new derived per-tile file from DGM, DOM1, DOP, Basis-DLM, LoD2, OSM, Wikidata or a city register), or when a step's output feeds the build in a new way."
---

# Adding a bake step

A step turns raw or committed sources into a small per-tile file under
`data/<site>/dlm/` (or `dop/`), which `scripts/prepare-data.ts` publishes
or bakes into the tileset. Decisions behind this: ADR 0012 (sources),
ADR 0037 (fetch → bake → build). Deep reference: the `city-walker` skill,
"Data pipeline", and `docs/data-pipeline.md`.

## Checklist

1. **Source.** Official data first; OSM only from the local extract
   (`bake/osm.py`, `osm_index.py`), Wikidata only from the fetch's cached
   answer. If the source needs the network, its download belongs in the
   fetch (`bake/fetch.py` or the provider adapter), never in the step.
2. **Write the step** as `pipeline/bake/<name>.py` with a `run(tile)` and
   register it in `STEPS` in `pipeline/bake/__main__.py`, in order: a
   comment says what it must run after and why. A site-wide step goes in
   `SITE_STEPS`.
3. **Every tile, the same files.** A step that finds nothing writes an empty
   file. `lib/city/tile-data.test.ts` fails when one tile lacks a kind of
   file another has: bake the step on every tile of every committed site.
4. **A Land without the source** gets a named stand-in or the layer is off
   with a note; never an invented substitute. Gate the step on
   `Provider.products` where the source is optional, and add the row or
   footnote in `lib/city/source-matrix.ts`, then `bun run docs:matrix`.
5. **A new feature file** gets a contract row in `lib/city/features.ts`
   (checked against every committed file by its test) and an entry in
   `lib/city/tile.ts` (`ARTIFACTS`). A JSON file the build reads gets a
   schema module `lib/city/<name>-file.ts`, a row in `bake-files.test.ts`
   and `parseBakeFile` where it is read (ADR 0059); a key the bake renames
   changes the schema in the same commit.
6. **If the build reads it**, list the module that bakes it in the artifact's
   row of `scripts/bake-entries.ts` (a missing entry leaves a stale cache;
   `bake-entries.test.ts` catches a module `prepare-data.ts` imports that
   no bake's key holds, not one filed under the wrong artifact). The code
   that reads it goes into its step's module in `scripts/prepare/`, never
   into `prepare-data.ts`, which no key carries.
7. **OSM output** carries an `attribution` member; a new source's licence
   and credit go into the guide's licence table (both languages) and, for a
   new provider, `NOTICE`.
8. **Things on the ground** take their feet and edges from
   `lib/city/ground-join.ts` and are listed in `JOIN_PARTS` (ADR 0030).
9. **Tests:** a pytest in `pipeline/tests/`; `bun run test:pipeline`
   (pytest + ruff) and `bun run verify`.
10. **Docs:** follow the `docs-upkeep` skill (ledger row, data-flow,
    data-sources page in both languages).

## Traps

- Fresh OSM: bake from a fresh extract; never dodge a re-bake. BBBike
  works from the cloud container, Geofabrik may not.
- `bun scripts/prepare-sites.ts <one site>` prunes the other sites'
  `public/data/`; rerun without arguments afterwards.
- Unchanged code and inputs skip a step (`step_cache.py`); `--force` runs
  it anyway.
