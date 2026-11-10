---
name: use-canvas
description: Create or edit an Endless Design Studio canvas, an .excalidraw page of views, documents, notes and arrows. Use only when the Canvases module is enabled.
---

Read this module's [README](../../README.md) first; it describes the file, the tools and how a canvas shows.

## Before you change anything

1. Run `yarn studio context src/prototypes/<key>/<id> --json` and respect `canEdit`. Only the prototype's owner or an Admin may change its canvases, and only while the prototype is active.
2. A canvas is one `<name>.excalidraw` file inside a prototype. Create it through the file menu (+ → New canvas), or write the empty scene from `types/canvas/check.ts` (`template`). For files written by hand, run `yarn studio identify <prototype folder>` and apply with `--yes`; never change or copy an existing `studioId`.
3. Read the current tool help instead of assuming arguments: `yarn canvas help`, then `yarn canvas help create` for the element types.

## Changing a canvas

Prefer the tools over editing the JSON: they keep arrows attached, labels inside their shapes, element versions raised and links in their stored form.

- **On the file:** `yarn canvas <file.excalidraw> <tool> '<json>'`. When the shell can change quotes (PowerShell, cmd), pass `--json-file <path>` or pipe the JSON with `-`; all three give the same result. The result is JSON on stdout; an open canvas takes the change in live.
- **In the open canvas** (a browser on the local studio): `window.__studioCanvas` has the same tools, plus `context`, `point`, `screenshot` and `persist`. Read its `help()` first. Each call is one undo step for the person.
- If the command says files have no identity yet, run the command it names, or repeat the call with `--identify`.

Work in small, reviewable steps:

1. `describe` before changing anything (`context` first in the browser when the person says "this" or "here").
2. Keep items in the canvas's own prototype: `artifacts` lists what can go on it. To show another prototype's view, copy it into this prototype first.
3. Prefer native elements: `text` for annotations, with shapes, arrows, lines and `section`s. Sticky `note`s are optional, not the default.
4. To show a view's named states, use `states` with the view's file, such as `{ "artifact": "flows/Home.vue" }`: one call places every state side by side, titled and linked to each state's permanent address. For a view without states, use `create` with `type: "artifact"`.
5. Preserve the person's arrangement; move existing content only when the request needs it.
6. Never write images yourself: a person pastes or drops them in the studio, which stores each picture in the prototype's `_canvas-images/` folder. Prefer the working view to a screenshot of it.
7. `describe` again afterwards, and in the browser `point` at what you placed so the person sees it.

If you must edit the JSON directly, keep each element's `id`, raise its `version` with a new `versionNonce` when you change it, keep `"files"` and `"studioVersion"` as they are, and write the file in one go. An item is an `"embeddable"` whose `link` is `/prototypes/<prototype-id>/artifacts/<artifact-id>`.

## Check the result

Open the canvas in the studio and look at the rendered result: items show live previews or cards, nothing overlaps by accident (`create` warns about overlaps), arrows join what they should. `yarn build` refuses a canvas with invalid JSON, a picture's bytes inside the file, images whose picture `files` doesn't list, links to another prototype or an unknown `studioVersion`. Report which canvas changed, what you placed, and the canvas's link.
