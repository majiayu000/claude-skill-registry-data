---
name: pr-snapshots
description: "Invoke whenever a pull request changes what the viewer shows (a look, a layer, a bake that alters the picture, a palette, a post pass). Every such PR carries JSON snapshots the reviewer pastes into the preview to judge the change; screenshots are optional."
---

# PR snapshots

The maintainer reviews visual changes by **looking at them in the PR's
Vercel preview**, at the places the author picked. So a PR that changes
what the viewer shows is not ready for review until its description has a
**Snapshots** section. Screenshots are optional: a SwiftShader render is
slow and lies about light and shadow, so add them only when they are cheap
and say that they are SwiftShader. The JSON is the deliverable.

## What counts as visual

Anything a reviewer would judge by eye: a scene material or shader term, a
layer or its dressing, a bake whose output changes the picture (land
cover, trees, facades, rails, …), the palette, a post pass or picture
style, the sky and the sun, the HUD's look. A pure refactor, a test, a doc
or a pipeline change that writes the same files needs none.

## The section

Put it in the PR description (not a comment, so it stays at the top as
the PR evolves), under `## Snapshots`:

1. One line on how to use them: open the preview at the site's route
   (`/dresden`, …), sidebar **Erweitert → Snapshot**, paste one JSON,
   **Anwenden**. Link the preview deployment when it exists.
2. Two to five views, each named after the place in a few words
   (*Königsbrücker Straße, schräg von oben*), with one sentence on what to
   look for there.
3. Per view a `<details>` block holding the snapshot JSON in a ```json
   fence, so the description stays short.
4. **Before and after in one place where the change has a control**:
   give the pair as two snapshots that differ only in that look key
   (e.g. `"look": {"fogPct": 0}` vs `100`, `"style": "pastel"` vs
   `"comic"`), so the reviewer flips between them in the same preview. Only
   *Nebel*, the picture style and the data layers are
   controls; the rest of the look is fixed — named constants in the code
   (ADR 0018, plan 073) — so a change to it has no look key: say that
   *before* is the same snapshot on the production site or the base PR's
   preview.
5. On a stacked PR, say which preview shows the base.

Keep `look` to the keys the comparison needs: a snapshot's look keys are
all optional, and every key left out keeps the reviewer's current value
(set `fogPct` and `style` when the view depends on them). Never write a
retired key (`RETIRED_SNAPSHOT_KEYS` in `lib/city/look-controls.ts`):
it is ignored, and suggests a slider that is not there.
Set `date` to an instant whose light shows the change (afternoon sun for
relief and shadow, night for lamps).

## Getting the JSON

A snapshot is `{ v: 1, camera, date, look? }` (`lib/city/snapshot.ts`,
checked by `parseSnapshot`; `camera` needs `pos` in the Y-up scene frame
*and* `epsg`, so capture it rather than writing it by hand):

- In a running viewer: sidebar **Erweitert → Snapshot → Kopieren**, or
  `__poc.handle.getCameraState()` (the page needs a build with
  `NEXT_PUBLIC_POC_DEBUG=1` or the dev server). *Link kopieren* gives the
  same view as a link (`?snap=…`): put it next to the JSON, with the
  preview's origin, and the reviewer opens it in one click.
- A committed QA view (`qa/views/`, its index has the links) may already
  show the place: reuse it.
- Headless, at a place given in EPSG: place the camera with
  `__poc.handle.flyToViewpoint` or `applyCameraState`, wait for
  `__poc.firstFrame`, then read `getCameraState()`. The camera needs the
  spawn tile only, so `?scene=lite` is enough to capture a pose (never to
  judge pixels).
- Check a hand-trimmed JSON with `parseSnapshot` before posting it.

Pick views from oblique angles, at the height a reviewer would stand or
fly, where the change is on screen and not hidden behind a tree crown or
inside a building (AGENTS.md, *Verify renders from oblique angles*).

## Screenshots, when cheap

`bun run shots` (`e2e/snapshot-shot.spec.ts`, headed, a real GPU) turns
the same snapshots into plates when a GPU is at hand. In the cloud
container there is none: a SwiftShader render of the full profile takes
minutes per view and leaves out night lamps and late trees, so post such
images in the conversation if at all, marked as SwiftShader, and never
hold the PR for them.
