---
name: open-data-watch
description: "The weekly Open-Data-Wächter of city walk, run by a scheduled task (or by hand): check the Länder's download services, new editions of DGM1, DOM1, LoD2, DOP and the Basis-DLM, and the age of the OSM data the bakes used; report on the open-data issue, with what a re-bake of a new edition would touch, for the maintainer."
---

# Open-Data-Wächter

The twin is built from open data that changes under it: Saxony replaces
tiles as it flies them again, the statewide Basis-DLM every quarter, OSM
every minute; services go down for days (GeoSN's in 2026-10). This skill
says what changed since the committed data was fetched and reports it for
the maintainer.

## Run the check

```bash
bun scripts/open-data-watch.ts            # every committed site
bun scripts/open-data-watch.ts dresden    # one
bun scripts/open-data-watch.ts --json     # for a script
```

It downloads no data. Its report has two parts: **Zu tun** (a service
that does not answer, a newer `Stand` than `provenance.json` records, a
newer Basis-DLM, OSM data older than 60 days) and **Stand** (what answered,
and editions no record holds yet). Only a recorded edition can be
outdone: `bun scripts/open-data-watch.ts <site> --record` writes the
current ones into the tiles that record none, right after a fetch.

## Act on it

1. **Nothing under „Zu tun“:** stop. Write nothing.
2. **A service down:** say which, since when (look at the last comment on
   the issue: was it down last week too?), and whether a re-bake is
   blocked by it. Three weeks in a row is worth a line to the maintainer.
3. **A new edition of a committed tile** (DGM1, LoD2, DOM1, DOP): report
   it for the maintainer, with the tiles, the old and new `Stand` and
   what a re-bake touches; do not re-bake here. A re-bake needs the whole
   site's raw inputs, which a fresh container lacks: the OSM extract
   (Geofabrik does not answer from it), the Mapillary caches (no
   `MAPILLARY_TOKEN`; without them the facade, window and lamp steps
   write empty files over the committed ones), gigabytes of scan and
   orthophoto. A bake on less rewrites committed outputs with less, and
   no check in the run reliably tells. Record nothing in
   `provenance.json` either: the record names what was baked.
4. **A newer Basis-DLM, OSM older than 60 days:** these re-bake every
   tile of every site of that Land (hours, gigabytes). Do not start it:
   report it with what it would touch, for the maintainer to schedule.
   The maintainer's rule: bake from fresh OSM extracts (BBBike works from
   the container, Geofabrik does not), never dodge a re-bake — so say
   plainly when one is due.
5. **Editions no record holds:** list them once (they stay until someone
   records them); recording them (`--record`) is the maintainer's, after
   a fetch.
6. **Report** in German as one comment on the open issue labelled
   **`open-data`** in `mdugue/bridge` (create it, titled
   „Open-Data-Wächter“, only if none is open): the „Zu tun“ lines with
   what each needs from the maintainer, and the report's
   „Stand“ folded under `<details>`.

## Never

- commit raw downloads (`data/_raw/` is gitignored for a reason) or
  another site's data folder that is not committed yet (ADR 0037);
- merge, push, or open a PR (the report is the whole output);
- re-bake a whole Land on your own initiative.
