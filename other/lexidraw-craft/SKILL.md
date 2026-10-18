---
name: lexidraw-craft
description: Craft guidance for drawing Lexidraw scenes with the lexidraw_* tools — arrow geometry (edges, not centers), layout, dark-mode color behavior, text-width clipping, and a numeric self-review loop. Use whenever drawing or editing a Lexidraw scene.
---

# excalidraw, programmatically

Covers authoring scenes through the `excalidraw` MCP server (`read_me`,
`create_view`, and the `lexidraw_*` tools that read/write scenes as
`app.lexidraw.scene` records in your own atproto repo).

The `lexidraw_*` tools stay out of your tool list until you ask for them.
Call `search_tools(keywords="lexidraw")` to reveal them; they are callable
from your next step.

## the loop

1. `lexidraw_save` — pass `rkey` to update a scene in place, omit it to create a
   new one. Returns the `at://` uri and a `https://lexidraw.app/#atproto=<did>,<rkey>` link.
2. **HARD RULE: never emit more than ~10 elements in a single save call.**
   This applies to revisions as much as creation — one giant save has killed
   entire runs twice by blowing the per-response output cap before anything
   landed. Create with the first ~10 elements, then update by rkey, passing
   the full element list so far plus the next batch, until done.
3. You cannot render the scene, so review it **numerically**: `lexidraw_open`
   the saved scene and check the geometry (see "numeric self-review" below).
4. Name what's wrong concretely, fix via rkey update (in batches, same hard
   rule), repeat. Expect 2–3 passes.

## arrows connect edges, not centers

The single ugliest failure: arrows drawn from box-center to box-center spear
through both shapes and land their arrowheads on top of the label text.

- Compute the **edge intersection**: start the arrow at the source box's border
  nearest the target, end it at the target's border. For a box at (x, y, w, h)
  and a target to the right, the start is (x + w, y + h/2).
- An arrow's `x, y` is its start; `points: [[0,0],[dx,dy]]` is the offset to
  the end. Both endpoints belong OUTSIDE both shapes' interiors.
- Route around, not through: if a straight edge-to-edge line would cross a
  third box, bend it (`points` with a midpoint) or move the boxes.
- Leave breathing room: arrowheads should stop at the border, never overlap a
  label.

## numeric self-review (before posting the link)

After saving, `lexidraw_open` and check, for every arrow (x, y, points):
- neither endpoint lies inside any rectangle/ellipse's bounding box interior;
- the segment does not pass through a third shape's bounding box;
- no text element's bounding box overlaps another element's.
If any check fails, the scene is not done — fix and re-save.

`lexidraw_open` pulls a scene's elements back out, so hand edits made in the app
can be picked up instead of clobbered. `lexidraw_list <handle>` enumerates
anyone's scenes — reading needs no auth; saving uses `LEXIDRAW_HANDLE` /
`LEXIDRAW_APP_PASSWORD` from the server environment.

Never hand over a draft you already know is broken, and always paste the URL —
the reviewer is not watching your screen.

## element format

Required on every element: `type`, `id`, `x`, `y`, `width`, `height`. Defaults
worth knowing: `strokeColor` `#1e1e1e`, `backgroundColor` `transparent`,
`strokeWidth` 2, `roughness` 1, `opacity` 100.

- **Label sugar** — `label: { text, fontSize }` on a rectangle/ellipse/arrow
  auto-centers text inside it. Prefer this over a separate text element
  wherever the text lives inside a shape; it can't clip and it can't drift.
- **Standalone text** needs an explicit `width` ≈ `chars × fontSize × 0.62`.
  Too small and the tail of the line is silently cut off. `x` is the *left*
  edge; to center at `cx`, set `x = cx - width/2`.
- **Triangles / mountains**: a `line` with
  `points: [[0,0],[w/2,-h],[w,0],[0,0]]` plus `backgroundColor` and
  `fillStyle: "solid"`.
- **Arrows**: `points` are offsets from `x,y`; `endArrowhead`/`startArrowhead`
  are `null | "arrow" | "bar" | "dot" | "triangle"`.
- **Roundness is a deliberate style choice, not a rule.** In the app it's the
  "edges: sharp / round" control, and both are ordinary options — curved
  polylines are right for organic shapes, river paths, cartoon tails; sharp is
  right for geometry that should read as geometry. `null` = sharp;
  `{type: 2}` curves a linear element; `{type: 3}` rounds rectangle corners.
  What matters is *choosing*: a multi-point polyline silently given roundness
  turns a triangle into an arc and an envelope flap into a handbag. (A
  two-point line is straight either way.) One published tip-list argues for
  sharp 90° corners as a default for clean technical diagrams — a taste, not a
  law.
- **z-order is array order.** Draw items *before* the container meant to overlap
  them so they read as sitting inside/behind it.
- `cameraUpdate` is a pseudo-element (`create_view` only; stripped on save) that
  pans/zooms the viewport as elements stream in. 4:3 sizes only —
  400×300, 600×450, 800×600, 1200×900, 1600×1200.

## dark mode

Lexidraw renders dark by default. **The theme inverts luminance and keeps hue**,
so specify the *opposite lightness* of what you want on screen:

| you want on screen | specify |
|---|---|
| near-white frame | `#212529` |
| light blue sky | `#1864ab` |
| bright green | `#15803d` |
| bright amber | `#b45309` |
| dark disc / vinyl | `#e9ecef` |

Pastels (`#a5d8ff`, `#ffd8a8`, `#d0bfff`) therefore render as *mid-dark muted*
shapes — fine for furniture like a wooden table, bad for anything meant to pop.
Mid-greys (`#868e96`, `#adb5bd`) survive both themes.

- **Don't use opacity for hierarchy.** Low-opacity fills render as murk; keep
  `opacity: 100` and express hierarchy through color, size and stroke weight.
  For "see through this", use a stroke-only shape with no fill.
- **Prefer `fillStyle: "solid"`** over `hachure`/`cross-hatch` — cleaner, and
  texture reads as noise at small sizes.
- `roughness: 1` is the hand-drawn look; `roughness: 0` reads clean/modern.
- Gray reads as dead/disabled, dashed reads as not-yet-existing. Use hue to mark
  relationships so they're traceable without reading any text.

## viewer quirks

- The Lexidraw viewer overlays a toolbar across the top of the canvas. Add an
  invisible spacer (`opacity: 0`, tiny) ~140px above your topmost content or the
  title sits under it.
- The viewer zoom-to-fits the whole scene, so wide scenes shrink; keep body text
  ≥16, labels ≥20, titles ≥30.
- Public scenes load with no login, so the `#atproto=` link is shareable and
  screenshot-able headlessly.

## composition (from published Excalidraw diagram guidance)

- **A diagram should argue, not display.** Test: strip every word — does the
  structure alone still communicate the idea?
- **Hierarchy through scale**, roughly: hero 300×150, primary 180×90,
  secondary 120×60, small 60×40. The most important element wants ~200px of
  empty space around it; isolation signals importance.
- **Flow direction**: left→right or top→bottom for sequences, radial for
  hub-and-spoke. Pick one and hold it.
- **Containers only when structural.** Free-floating text is the default;
  one guide targets under ~30% of text elements sitting inside a shape.
- **Shapes must carry meaning** — diamonds for decisions, ellipses for
  start/end. Decorative icons are noise.
- Expect **2–4 render-and-look iterations** to clear spacing, overlap and
  clipping problems. That's normal, not a sign of doing it wrong.

## when the drawing has to explain something

Optional opinions, for diagrams aimed at people who don't write software:

- **Comic panels beat system diagrams.** Numbered arrows between boxes are a
  sequence diagram; lay readers don't read those. Frames, a person, and speech
  bubbles carry consent and negotiation far better than labelled edges.
- **Continuity is the argument.** Anything meant to be invariant must be
  *pixel-identical* across panels — same coordinates, same contents. Build from
  a strict template with fixed panel origins and shared furniture at fixed
  panel-relative offsets. If the thing that "never moves" is drawn differently
  each frame, the picture contradicts its own caption.
- **Objects, not symbols.** A music note is a symbol; a record in a sleeve is an
  object. Draw things that could plausibly sit in the scene.
- **No invented metaphor objects.** If a shape needs its own explanation
  ("the sign says where you keep things"), delete it — that's jargon in a costume.
- **Captions advance; pictures describe.** Never caption what's already visible.
- Concrete furniture over abstract nouns ("your table", not "your place").
  Second person, no fictional personas (`@yourname`, never `@grandma.example`).

## before calling it done

- Did you run the numeric self-review, or only trust the save's success?
- Do any arrows cross a box or touch a label?
- Any text clipped, any shape overlapping another by accident?
- Is every word one the intended reader already uses?
