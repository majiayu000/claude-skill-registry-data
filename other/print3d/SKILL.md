---
name: print3d
description: Model a part in Blender from an idea, a photo of an object, or the shop listing of something you would otherwise buy, slice it for the Bambu X2D, and iterate until it prints clean and matches the photo.
argument-hint: "[what to make, a photo of the object, or a shop link]"
disable-model-invocation: true
---

# /print3d — idea to a printable X2D part

`print3d` below is the print3d command line. When the shell cannot find it, the
print3d MCP tools of the same names do the same work. A job's files live in the
report's `job_dir`, written below as `jobs/<slug>`.

```
idea / photo / text  →  model.py (Blender)  →  mesh  →  DFM + printability
        │                    ↑                         + likeness to the photo
    spec.json                └────────  advice: what to fix ───┘
                                              │
                                        slice → .3mf → user prints from Studio
```

Nothing here reaches the printer. The last step is a sentence handing the user a
`.3mf`. Printing is theirs to do in Studio, with the plate in front of them.

## 1. Read the brief

Size, text, colour, what the part has to do. Ask at most one question, and
only when a missing number makes the part unprintable.

**From a photo of an object:** scaffold (step 2) for the slug, then work through
`references/from-photo.md` before writing the model. It turns the photo into a
`spec.json` of measured, given and assumed dimensions, and adds the `likeness`
check that compares the model with the photo.

**To replace something sold in a shop** (a listing URL or a product name): also
work through `references/from-listing.md`. The listing's stated dimensions scale
its product photos, and the hand-off weighs the print against the price.

**More than one part, more than one colour, or parts that fit together** (a box
and lid, a case in halves, a name in a second colour, a pin in a hole): read
`references/parts-and-fits.md` before writing the model.

## 2. Scaffold

```bash
print3d make "<prompt>"
```

With no model yet this writes `jobs/<slug>/model.py` and stops, naming the path.
Take the slug from that path.

## 3. Write the model

Replace the scaffold's body with the real part. The contract:

- Plain bpy. **1 Blender unit == 1 mm.**
- `params` is in scope: `prompt`, `slug`, `text`, `intent`, `size_mm`, `color`,
  `material`, `dims` (name -> mm from `spec.json`) and `fit` (this printer's
  clearance per side for `press`, `snug`, `slide`, `free`). Size every mating
  feature from `params["fit"]`, never from a guessed number.
- Several parts: model each where it sits when assembled and name it with
  `part(objects, name, color=, group=, rotate=, plate=, settings=)`; declare how
  two parts mate with `fit(a, b, kind)`. Without `part()` every mesh is joined
  into one part.
- Leave the geometry as mesh objects. The harness joins them, removes doubles,
  fills holes, recalculates normals, triangulates, centres the part, drops it on
  the bed and exports.
- **Orientation is yours.** Studio's auto-orient is off, so what you model is
  what prints.

`examples/nameplate.py` is the worked reference. `references/modelling.md` has
the bpy recipes, the gotchas that cost an iteration, and the move each check
asks for.

## 4. Run the loop until it goes green

```bash
print3d make "<prompt>"
```

Models, DFM-checks, slices with the pinned X2D presets, and reports. The run is
**red** when `severity` is `error` — exit code 1, `status: needs_work`.

While red: read `advice`, apply the `fix` each note carries to `model.py`, run
again. Each note is phrased as a change to the model, because that is where the
fix lives. `jobs/<slug>/history.jsonl` accumulates what each iteration changed.

Hand over only once it is green.

## 5. Look at the plate

Read the PNG at `plate_png` (each `plates[].png` for several plates), and each
`likeness[].overlay` when there is one.
The numbers go green on parts that are printable and still wrong — mirrored text, a hole in the wrong face, letters too shallow
to read. Look before you hand it over.

`viewer` is `jobs/<slug>/view.html`: the model in 3D, to rotate, zoom, hide parts
and pull them apart. When you have a preview pane (Hermes desktop's
`desktop_preview`, action `open`, with that path as the url), open it there so
the user can turn the part around beside the chat. Otherwise give the path to
open in a browser. `print3d view <slug>` rebuilds it for an older job.

## 6. Hand off

```bash
print3d handoff <slug>
```

writes `jobs/<slug>/handoff/`: a print sheet the user can send on, renders of
the part assembled (and exploded, for several parts), the `.3mf` and an STL per
part. Look at the renders: a colour that does not show, or a part in the wrong
place, is plain there.

Report time, grams and layers, and for several parts the colours and how each
declared fit measured. From a photo, also list which dimensions were
measured, given, listed or assumed, and the unknowns. From a listing, put the
grams and time beside the listing's price. Then give the path:

```
jobs/<slug>/slice/<slug>.3mf
```

That is the project file. The `.gcode.3mf` beside it is a sliced job and
Studio's Prepare tab rejects it as having no geometry. Tell the user to open the
`.3mf`, check the preview, and print from Studio — and offer another iteration
if the preview is not what they wanted.

## Done when

`print3d make` exits 0, no note is at `error`, you have looked at the plate PNGs,
any likeness overlays and the hand-off renders, and the user has the `.3mf` path
and the print sheet.

## The machine

X2D, 0.4 mm nozzle, 256 × 256 × 260 mm bed, 0.20 mm layers, Bambu PLA Basic,
textured PEI plate. **The pinned process has supports off** — that is why an
overhang note is a real defect and not a setting to flip. Two nozzles: two
colours print without a filament change.
