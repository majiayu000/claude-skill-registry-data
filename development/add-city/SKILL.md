---
name: add-city
description: "Use when adding a new city (site) or a new Land (provider) to the viewer, or when bringing an existing site's data up to date with a new edition."
---

# Adding a city

Decisions behind this: ADR 0037 (sites, providers, what is committed),
ADR 0012 (sources and stand-ins), ADR 0005 (CRS).

## A city in a Land that is already covered

1. `sites/<id>.ts`: name, label, tiles (the first is the spawn), viewpoints,
   optional smaller OSM extract, street-tree register (`treeCadastre`, its
   field mapping in `pipeline/bake/cadastre.py`), `dataLayers` where the
   city publishes a feed. Register it in `sites/index.ts`.
2. `bun run fetch <id>` (add `--lsc` where the provider reads a laser scan),
   then `bun run bake <id> --jobs N`, then `bun run site <id>` to see what
   is missing.
   `bun run osm-coverage <id>` lists the built things OSM maps there that
   no bake draws and nobody decided about (a cable car, a lift up a
   cliff): decide each in `pipeline/bake/coverage.py`'s ledger, drawn,
   planned or left out with its reason, before the city ships.
3. `bun run dev` and walk it; take real-GPU plates (`SHOTS_SITE=<id>
   bun run shots`) at its viewpoints and landmarks.
4. `bun run docs:matrix` (its test fails otherwise).
5. **Committing its `data/<id>/` is the maintainer's decision** (size;
   `.gitignore` un-ignores each committed site by name). Ask before.

## A new Land

1. A `Provider` in `sites/providers.ts`: EPSG, licence and credit, portal,
   OSM extract, open products, the `land` the start page names.
2. An adapter `pipeline/bake/providers/<id>.py` with at least `dgm`,
   `dom`, `dop`, `lod2` and `dlm` (`flight`, `lsc` where the Land has
   them), returning the provider's own files;
   the common code clips them to 2 km tiles.
3. Licence and credit in the guide's licence table (both languages) and
   in `NOTICE`.
4. Where the Land lacks a product, the stand-ins of ADR 0012 apply; the
   matrix marks them.

## Never

- A per-site look switch; derive the look from the city's data.
- Raw downloads in git, or a fetch inside the build.
