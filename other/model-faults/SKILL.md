---
name: model-faults
description: "Modellfehler aus Straßenfotos, run weekly by a scheduled task (or by hand): put recent Panoramax street photos beside renders of the twin from the same pose, find where the twin is wrong (roof form, height, storeys, colour, a missing or invented object) and turn what recurs into proposals for the general heuristic — never a fix for one building. Reports on the model-faults issue."
---

# Modellfehler aus Straßenfotos

The twin's buildings, roofs, colours and storeys come from heuristics over
open data. A street photo shows where a heuristic goes wrong. This skill
compares a handful of photos a week with the twin and looks for the
**pattern** behind what differs.

**The rule (the maintainer's):** correct the general heuristic, never the
single building. A proposal names the bake step or runtime term, the rule
that misfires, what in the data would tell the case apart, and how many
places it would touch — not "make Hauptstraße 5 red".

## Make the pairs

```bash
bun scripts/prepare-sites.ts dresden            # a fresh session has no public/data (≈ 9 min)
bun scripts/street-photos.ts dresden --n 8      # the week's photos + snapshots
NEXT_PUBLIC_POC_DEBUG=1 bunx next build && (bunx next start -p 3000 &)
until curl -sf -o /dev/null localhost:3000/dresden; do sleep 2; done
# a real GPU (headed):
SHOTS=1 SHOTS_AT=1 bunx playwright test e2e/snapshot-shot.spec.ts --headed -g "foto-dresden"
# the cloud container (SwiftShader, small, lite booted at each photo):
PW_CHROMIUM=/opt/pw-browsers/chromium SHOTS=1 SHOTS_SMALL=1 SHOTS_AT=1 \
  SHOTS_QUERY="scene=lite&block=1" \
  bunx playwright test e2e/snapshot-shot.spec.ts --workers=1 -g "foto-dresden"
```

The first walks the site's 400 m cells in an order the ISO week draws
(`--seed` to repeat one) and takes the newest usable Panoramax photo of
each until it has N: a street (not MapComplete's point-of-interest
close-ups), flat, aimed, placed within 6 m. It writes a
snapshot at each photo's pose to `shots/foto-<site>-<n>.json` and the
photo to `street-photos/<site>/` with `pairs.json` (author, licence,
link). The second renders the snapshots to `shots/foto-<site>-<n>.png`.

Wait for the server to answer before Playwright starts: a port that is
still closed makes Playwright run its own build and server, which rebuilds
`.next` under the running one and starves the render. In the container:
`prepare-sites` with one site prunes the others'
`public/data` (fine here). `PW_CHROMIUM` points Playwright at the
container's own Chromium, which the repository's Playwright pin does not
find by itself. `SHOTS_AT=1` boots each page at its photo (`?at=lat,lng`):
`lite` streams only around where it booted, so a pose a kilometre from the
spawn would show the wrong part of town. A shot takes 7–11 minutes
there (`SHOTS_SMALL` waits up to 15 for the scene); eight are over an hour.
So look at the photos first and keep only the pairs that show a building
or a street — move the other snapshots out of `shots/` before the render
starts (Playwright lists them when it begins); a close-up or a photo of a
hedge is skipped, not rendered. Then start the render in the background
and read the kept photos closely meanwhile.
SwiftShader is good for geometry and colour, wrong for light and shadow
— never judge shading from it; a lite render is coarse (half the pixel
ratio), enough for roofs, heights and storeys.

## Compare

Read each photo and its render side by side. The pose is approximate:
the photo's GPS can be 5 m off, its heading a few degrees, its pitch is
unknown (the render looks level), its lens assumed where the photo does
not say (`lensAssumed`). So first find the same building in both; a
pair where you cannot is skipped, not a finding.

For each building both show, note what differs, by category:

- **Dachform** (gable vs hip vs flat, the ridge direction), **Dachfarbe**;
- **Höhe / Geschosse** (count the storeys in the photo);
- **Fassade**: colour (plaster vs brick, ADR: OSM `building:colour`,
  the neighbourhood's `context`), material, the window rhythm (the
  windows' columns — only from photos, ADR 0010);
- **Fehlt / zu viel**: a building, a tree, a wall, a kiosk the twin lacks
  or invents; **Lage** (an object metres off).

Ignore what the twin draws on purpose (stylised clay, windows without panes or mullions, no
signage, no people or cars, the pastel light) and what the photo's season
or time explains.

## Turn it into proposals

1. Group the week's notes by category and find the rule behind each
   group: which step makes that value (`roofs.py`, `roof_colour.py`,
   `osm_buildings.py`, `windows.ts`, `building-tint.ts`,
   `small-buildings.py`, the canopy …; the knowledge base's
   `docs/transformations.md` names them) and why it misfires there.
2. Check the rule across the site before proposing: how many buildings
   share the trait (the Stadtwissen, `bun scripts/stadtwissen.ts`, or the
   bake's own outputs)? A proposal states that count.
3. A proposal that is clear, small and testable may become a **draft PR**
   on its own branch: the rule's change and a unit test that pins it,
   no baked data. Its body says the re-bake is the maintainer's (the
   maintainer's rule: never dodge a re-bake), names the sites and steps
   it touches and the count from step 2. Do not bake here: a fresh
   container lacks the raw inputs (`data/_raw/`, the OSM extract, the
   Mapillary caches), and a bake on less rewrites committed outputs with
   less. Anything larger is an issue comment for the maintainer.

## Report

One comment in German on the open issue labelled **`model-faults`** in
`mdugue/bridge` (create it, „Modellfehler aus Straßenfotos“, only if none
is open): the week's pairs (Panoramax link, the snapshot JSON inline so
the maintainer can paste it into the preview, the photographer and
„CC BY-SA 4.0“), the differences by category, and the proposals with
their counts. The photos and renders stay out of the repository and the
issue (the licence asks for attribution and share-alike; a link is
enough).

## Never

- fix a single building (a patch, an override list, a special case by
  id);
- use Google Street View or Maps; Mapillary only where the maintainer
  lifts the pause on its poses (2026-10);
- commit photos or renders.
