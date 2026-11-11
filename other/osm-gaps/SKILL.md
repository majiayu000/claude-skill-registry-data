---
name: osm-gaps
description: "OSM-Lücken als Aufgaben, run monthly by a scheduled task (or by hand): find what OpenStreetMap lacks that the twin's data shows (nameless landmarks, tall buildings without storeys, listed buildings without name or address), write it as tasks for mappers (GeoJSON for MapRoulette, a Markdown list) and report on the osm-gaps issue. Never edits OpenStreetMap."
---

# OSM-Lücken als Aufgaben

The viewer reads names, addresses, storeys and listing from OSM and
heights and footprints from the official LoD2. Where the two disagree or
OSM is silent, the viewer guesses (storeys and windows from the height,
ADR 0010) or shows a nameless building. Those gaps are tasks for mappers
— people who look on site or on sources OSM may use. **This skill finds
and lists them; it never edits OSM**, not even an obvious one: OSM's
import and automated-edits rules forbid it, and a hint is not a survey.

## Run

The Stadtwissen must be published (`bun dev` or `bun run build` once,
or `bun scripts/prepare-sites.ts` — without arguments: with one site it
prunes the others' `public/data`).

```bash
bun scripts/osm-gaps.ts dresden            # one site: run it for each
bun scripts/osm-gaps.ts dresden --top 30
```

It writes `osm-gaps/<site>/` (gitignored): one GeoJSON per kind —
`wahrzeichen-ohne-name`, `geschosse-fehlen`, `denkmal-ohne-name` — each
feature a point with its instruction and links (the shape MapRoulette
takes for a challenge), and `aufgaben.md`, the counts and the first N of
each kind, highest first.

## Report

1. Run it for every committed site (`data/<site>/` exists).
2. Compare with last month's comment on the open issue labelled
   **`osm-gaps`** in `mdugue/bridge`: how many closed since (mappers did
   them), how many new. A gap that closed is the good news; say it first.
3. Comment once, in German: per site the counts and their change, the
   first ten of „Wahrzeichen ohne Namen“ and „Geschosszahl fehlt“ with
   their links, and how to make a MapRoulette challenge from the GeoJSON
   (the maintainer uploads it; it is his account). Create the issue,
   titled „OSM-Lücken“, only if none is open.
4. Something the twin itself gets wrong (a landmark matched to the wrong
   building, a listed building that is not one) is a finding about the
   bake, not a mapper's task: name the bake step (`landmarks.py`,
   `osm_buildings.py`) in a line of its own.

## Never

- edit, upload to or comment on OpenStreetMap, or create a MapRoulette
  challenge yourself;
- copy anything from Google Maps/Street View into a task (OSM may not use
  it): the tasks' sources are the official LoD2 and Wikidata.
